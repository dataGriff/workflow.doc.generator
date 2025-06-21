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

    def fetch_objectives(self) -> List[Dict[str, Any]]:
        """
        Fetch Objective (Objectives) from Azure DevOps.
        Returns a list of work item dicts.
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
        # Fetch details for each Objective
        return self._fetch_work_items(ids)

    def _fetch_work_items(self, ids: List[int], expand_relations: bool = False) -> List[Dict[str, Any]]:
        """
        Fetch work item details for a list of IDs, including custom OKR fields and optionally relations.
        """
        url = self.base_url + "wit/workitemsbatch?api-version=7.0"
        payload = {
            "ids": ids,
            "fields": [
                "System.Id",
                "System.Title",
                "System.Description",
                "System.State",
                "Custom.Objective",
                "Custom.KeyResults",
                "Custom.MethodOfMeasure",
                "Custom.ObjectiveOutcome",
                "System.WorkItemType",
                "System.RelatedLinks",
                "System.Tags",
                "System.AssignedTo",
                "System.CreatedDate",
                "System.ChangedDate"
            ]
        }
        if expand_relations:
            payload["expand"] = "relations"
        resp = self.session.post(f'{url}', json=payload)
        if resp.status_code != 200:
            logger.error(f"Azure DevOps workitemsbatch failed: {resp.status_code} {resp.text}")
            raise RuntimeError(f"Azure DevOps workitemsbatch failed: {resp.status_code} {resp.text}")
        try:
            return resp.json().get('value', [])
        except Exception as e:
            logger.error(f"Failed to decode workitemsbatch response as JSON: {e}\nResponse text: {resp.text}")
            raise

    def fetch_and_normalize_okrs(self) -> List[Dict[str, Any]]:
        """
        Fetch and normalize OKR data for the Markdown formatter, including direct children (hypotheses).
        Returns a list of objectives with required fields and their direct children.
        """
        objectives = []
        items = self._fetch_work_items([item['id'] for item in self.fetch_objectives()], expand_relations=True)
        for item in items:
            fields = item.get("fields", {})
            obj = {
                "id": fields.get("System.Id", item.get("id")),
                "title": fields.get("System.Title", "Untitled"),
                "state": fields.get("System.State", ""),
                "key_results": fields.get("Custom.KeyResults", ""),
                "objective": fields.get("Custom.Objective", ""),
                "method_of_measure": fields.get("Custom.MethodOfMeasure", ""),
                "objective_outcome": fields.get("Custom.ObjectiveOutcome", ""),
                "hypotheses": []
            }
            # Debug: log relations
            logger.debug(f"Objective {obj['id']} relations: {item.get('relations', [])}")
            child_ids = []
            for rel in item.get("relations", []):
                logger.debug(f"Relation: {rel}")
                if rel.get("rel") == "System.LinkTypes.Hierarchy-Forward":
                    url = rel.get("url", "")
                    if url.endswith("/workItems/"):
                        continue
                    child_id = url.split("/workItems/")[-1]
                    if child_id.isdigit():
                        child_ids.append(int(child_id))
            logger.debug(f"Objective {obj['id']} child_ids: {child_ids}")
            if child_ids:
                children = self._fetch_work_items(child_ids)
                for child in children:
                    cfields = child.get("fields", {})
                    obj["hypotheses"].append({
                        "id": cfields.get("System.Id", child.get("id")),
                        "title": cfields.get("System.Title", "Untitled"),
                        "state": cfields.get("System.State", ""),
                        "hypothesis": cfields.get("Custom.Hypothesis", ""),
                        "method_of_measuring_hypothesis": cfields.get("Custom.MethodOfMeasuringHypothesis", ""),
                        "hypothesis_outcome": cfields.get("Custom.HypothesisOutcome", "")
                    })
            objectives.append(obj)
        return objectives

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

    def fetch_and_normalize_okrs_with_relations(self) -> List[Dict[str, Any]]:
        """
        Fetch and normalize OKR data using per-objective relations.
        Returns a list of objectives with required fields and their direct children (hypotheses).
        """
        objectives = []
        items = self.fetch_objectives_with_relations()
        for item in items:
            fields = item.get("fields", {})
            obj = {
                "id": fields.get("System.Id", item.get("id")),
                "title": fields.get("System.Title", "Untitled"),
                "state": fields.get("System.State", ""),
                "key_results": fields.get("Custom.KeyResults", ""),
                "objective": fields.get("Custom.Objective", ""),
                "method_of_measure": fields.get("Custom.MethodOfMeasure", ""),
                "objective_outcome": fields.get("Custom.ObjectiveOutcome", ""),
                "hypotheses": []
            }
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
            # Fetch and attach child work items
            if child_ids:
                for cid in child_ids:
                    workitem_url = self.base_url + f"wit/workitems/{cid}?api-version=7.0"
                    wresp = self.session.get(workitem_url)
                    if wresp.status_code != 200:
                        logger.error(f"Failed to fetch child {cid}: {wresp.status_code} {wresp.text}")
                        continue
                    cfields = wresp.json().get("fields", {})
                    obj["hypotheses"].append({
                        "id": cfields.get("System.Id", cid),
                        "title": cfields.get("System.Title", "Untitled"),
                        "state": cfields.get("System.State", ""),
                        "hypothesis": cfields.get("Custom.Hypothesis", ""),
                        "method_of_measuring_hypothesis": cfields.get("Custom.MethodOfMeasuringHypothesis", ""),
                        "hypothesis_outcome": cfields.get("Custom.HypothesisOutcome", "")
                    })
            objectives.append(obj)
        return objectives
