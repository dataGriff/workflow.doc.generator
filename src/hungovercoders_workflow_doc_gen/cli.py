"""
CLI for generating OKR documentation from Azure DevOps.
"""
import argparse
import logging
import json
import os
from hungovercoders_workflow_doc_gen.formatter import Formatter
from hungovercoders_workflow_doc_gen.azure_devops_client import AzureDevOpsClient
import jsonschema

logger = logging.getLogger(__name__)

def main() -> None:
    parser = argparse.ArgumentParser(description="Generate OKR documentation from Azure DevOps.")
    parser.add_argument("--org", required=True, help="Azure DevOps organization name")
    parser.add_argument("--project", required=True, help="Azure DevOps project name")
    parser.add_argument("--pat", required=True, help="Azure DevOps Personal Access Token")
    parser.add_argument("--output", default="okr_report.md", help="Output file (Markdown, HTML, PDF, or JSON)")
    parser.add_argument("--format", choices=["markdown", "doc", "pdf", "raw-json"], default="markdown", help="Output format: markdown, doc (Word-compatible HTML), pdf, or raw-json")
    parser.add_argument("--validate", action="store_true", help="Validate OKR data against JSON schema before output")
    args = parser.parse_args()

    client = AzureDevOpsClient(args.org, args.project, args.pat)
    okr_data = client.fetch_and_normalize_okrs_with_relations()

    if args.validate:
        schema_path = os.path.join(os.path.dirname(__file__), 'schemas/okr_summary.json')
        if not os.path.exists(schema_path):
            schema_path = os.path.join(os.path.dirname(__file__), '../schemas/okr_summary.json')
        with open(schema_path, encoding='utf-8') as f:
            schema = json.load(f)
        try:
            jsonschema.validate(instance=okr_data, schema=schema)
            print("OKR data validated successfully against schema.")
        except jsonschema.ValidationError as e:
            logger.error(f"OKR data validation failed: {e.message}")
            raise SystemExit(1)

    formatter = Formatter()
    if args.format == "markdown":
        output_str = formatter.format_markdown(okr_data)
        with open(args.output, "w") as f:
            f.write(output_str)
        print(f"OKR Markdown report written to {args.output}")
    elif args.format == "doc":
        output_str = formatter.format_doc(okr_data)
        with open(args.output, "w") as f:
            f.write(output_str)
        print(f"OKR Word-compatible HTML report written to {args.output}")
    elif args.format == "pdf":
        formatter.format_pdf(okr_data, args.output)
        print(f"OKR PDF report written to {args.output}")
    elif args.format == "raw-json":
        with open(args.output, "w") as f:
            json.dump(okr_data, f, indent=2)
        print(f"OKR JSON report written to {args.output}")

if __name__ == "__main__":
    main()
