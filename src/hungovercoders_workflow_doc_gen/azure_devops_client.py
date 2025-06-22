"""
Azure DevOps client for fetching and normalizing OKR data.
"""
import requests
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)

class AzureDevOpsClient:
    """
    Client for interacting with Azure DevOps REST API to fetch OKR data.
    """
    def __init__(self, organization: str, project: str, pat_token: str) -> None:
        self.organization = organization
        self.project = project
        self.pat_token = pat_token
        self.base_url = f"https://dev.azure.com/{organization}/{project}/_apis/"
        self.session = requests.Session()
        self.session.auth = ('', pat_token)
        self.session.headers.update({"Content-Type": "application/json"})

    def fetch_objectives_with_relations(self) -> List[Dict[str, Any]]:
        """
        Fetch each Objective individually with relations expanded.
        Returns a list of work item dicts with relations.
        """
        wiql = {
            "query": "SELECT [System.Id] FROM WorkItems WHERE [System.WorkItemType] = 'Objective' ORDER BY [System.Id]"
        }
        url = self.base_url + "wit/wiql?api-version=7.0"
        resp = self.session.post(url, json=wiql)
        if resp.status_code != 200:
            logger.error(f"Azure DevOps WIQL query failed: {resp.status_code} {resp.text}")
            raise RuntimeError(f"Azure DevOps WIQL query failed: {resp.status_code} {resp.text}")
        try:
            ids = [item['id'] for item in resp.json().get('workItems', [])]
        except Exception as e:
            logger.error(f"Failed to decode WIQL response as JSON: {e}\nResponse text: {resp.text}")
            raise
        if not ids:
            return []
        # Fetch each Objective individually with relations
        objectives = []
        for oid in ids:
            workitem_url = self.base_url + f"wit/workitems/{oid}?api-version=7.0&$expand=relations"
            wresp = self.session.get(workitem_url)
            if wresp.status_code != 200:
                logger.error(f"Failed to fetch Objective {oid} with relations: {wresp.status_code} {wresp.text}")
                continue
            objectives.append(wresp.json())
        return objectives

    def fetch_and_normalize_okrs_with_relations(self) -> dict:
        """
        Fetch and normalize OKR data using per-objective relations.
        Returns a dict with a top-level 'objectives' key, matching the schema.
        """
        objectives = []
        items = self.fetch_objectives_with_relations()
        for item in items:
            fields = item.get("fields", {})
            obj_id = fields.get("System.Id", item.get("id"))
            obj = {
                "id": obj_id,
                "title": fields.get("System.Title", "Untitled"),
                "state": fields.get("System.State", ""),
                "objective": fields.get("Custom.Objective", ""),
                "key_results": fields.get("Custom.KeyResults", []),
                "method_of_measure": fields.get("Custom.MethodOfMeasure", ""),
                "objective_outcome": fields.get("Custom.ObjectiveOutcome", ""),
                "link": f"https://dev.azure.com/{self.organization}/{self.project}/_workitems/edit/{obj_id}",
                "hypotheses": []
            }
            # Ensure key_results is a list of strings
            if isinstance(obj["key_results"], str):
                obj["key_results"] = [kr.strip() for kr in obj["key_results"].split("\n") if kr.strip()]
            elif not isinstance(obj["key_results"], list):
                obj["key_results"] = []
            # Find direct children via relations
            child_ids = []
            for rel in item.get("relations", []):
                if rel.get("rel") == "System.LinkTypes.Hierarchy-Forward":
                    url = rel.get("url", "")
                    if url.endswith("/workItems/"):
                        continue
                    child_id = url.split("/workItems/")[-1]
                    if child_id.isdigit():
                        child_ids.append(int(child_id))
            # Fetch and attach child work items as hypotheses
            if child_ids:
                for cid in child_ids:
                    workitem_url = self.base_url + f"wit/workitems/{cid}?api-version=7.0"
                    wresp = self.session.get(workitem_url)
                    if wresp.status_code != 200:
                        logger.error(f"Failed to fetch child {cid}: {wresp.status_code} {wresp.text}")
                        continue
                    cfields = wresp.json().get("fields", {})
                    hyp_id = cfields.get("System.Id", cid)
                    hypothesis = {
                        "id": hyp_id,
                        "title": cfields.get("System.Title", "Untitled"),
                        "state": cfields.get("System.State", ""),
                        "hypothesis": cfields.get("Custom.Hypothesis", ""),
                        "hypothesis_context": cfields.get("Custom.HypothesisContext", ""),
                        "link": f"https://dev.azure.com/{self.organization}/{self.project}/_workitems/edit/{hyp_id}",
                        "method_of_measuring_hypothesis": cfields.get("Custom.MethodOfMeasuringHypothesis", ""),
                        "hypothesis_outcome": cfields.get("Custom.HypothesisOutcome", "")
                    }
                    # Ensure required fields for hypothesis
                    for field in ["hypothesis", "title", "state"]:
                        if not hypothesis.get(field):
                            hypothesis[field] = ""
                    obj["hypotheses"].append(hypothesis)
            objectives.append(obj)
        return {"objectives": objectives}
