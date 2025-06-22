"""
CLI for generating OKR documentation from Azure DevOps.
"""
import argparse
import logging
import json
import os
from typing import Any
from hungovercoders_workflow_doc_gen.markdown_formatter import MarkdownOKRFormatter
from hungovercoders_workflow_doc_gen.azure_devops_client import AzureDevOpsClient
import jsonschema

logger = logging.getLogger(__name__)

def main() -> None:
    parser = argparse.ArgumentParser(description="Generate OKR documentation from Azure DevOps.")
    parser.add_argument("--org", required=True, help="Azure DevOps organization name")
    parser.add_argument("--project", required=True, help="Azure DevOps project name")
    parser.add_argument("--pat", required=True, help="Azure DevOps Personal Access Token")
    parser.add_argument("--output", default="okr_report.md", help="Output file (Markdown or JSON)")
    parser.add_argument("--format", choices=["markdown", "raw-json", "revealjs"], default="markdown", help="Output format: markdown, raw-json, or revealjs")
    parser.add_argument("--validate", action="store_true", help="Validate OKR data against JSON schema before output")
    args = parser.parse_args()

    client = AzureDevOpsClient(args.org, args.project, args.pat)

    if args.format == "raw-json":
        # Fetch objectives with relations (one by one)
        objectives = client.fetch_objectives_with_relations()
        print(json.dumps(objectives, indent=2))
        with open(args.output, "w") as f:
            json.dump(objectives, f, indent=2)
        print(f"Raw Azure DevOps objectives JSON (with relations) written to {args.output}")
    else:
        # Use new normalization logic that uses per-objective relations
        objectives = client.fetch_and_normalize_okrs_with_relations()
        if args.validate:
            schema_path = os.path.join(os.path.dirname(__file__), 'schemas/okr_summary.json')
            if not os.path.exists(schema_path):
                schema_path = os.path.join(os.path.dirname(__file__), '../schemas/okr_summary.json')
            with open(schema_path, encoding='utf-8') as f:
                schema = json.load(f)
            try:
                jsonschema.validate(instance={"objectives": objectives}, schema=schema)
                print("OKR data validated successfully against schema.")
            except jsonschema.ValidationError as e:
                logger.error(f"OKR data validation failed: {e.message}")
                raise SystemExit(1)
        formatter = MarkdownOKRFormatter()
        if args.format == "markdown":
            markdown = formatter.format_markdown(objectives)
            print(markdown)
            with open(args.output, "w") as f:
                f.write(markdown)
            print(f"OKR Markdown report written to {args.output}")

if __name__ == "__main__":
    main()
