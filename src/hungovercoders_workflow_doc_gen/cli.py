"""
CLI for generating OKR documentation from Azure DevOps.
"""
import argparse
import logging
import json
from typing import Any
from hungovercoders_workflow_doc_gen.markdown_formatter import MarkdownOKRFormatter
from hungovercoders_workflow_doc_gen.azure_devops_client import AzureDevOpsClient

logger = logging.getLogger(__name__)

def main() -> None:
    parser = argparse.ArgumentParser(description="Generate OKR documentation from Azure DevOps.")
    parser.add_argument("--org", required=True, help="Azure DevOps organization name")
    parser.add_argument("--project", required=True, help="Azure DevOps project name")
    parser.add_argument("--pat", required=True, help="Azure DevOps Personal Access Token")
    parser.add_argument("--output", default="okr_report.md", help="Output file (Markdown or JSON)")
    parser.add_argument("--format", choices=["markdown", "raw-json"], default="markdown", help="Output format: markdown or raw-json")
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
        formatter = MarkdownOKRFormatter()
        markdown = formatter.format_markdown(objectives)
        print(markdown)
        with open(args.output, "w") as f:
            f.write(markdown)
        print(f"OKR Markdown report written to {args.output}")

if __name__ == "__main__":
    main()
