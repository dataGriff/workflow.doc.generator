"""
CLI for generating OKR documentation from Azure DevOps.
"""
import argparse
import logging
import json
import os
from hungovercoders_workflow_doc_gen.formatter import Formatter
from hungovercoders_workflow_doc_gen.azure_devops_client import AzureDevOpsClient
from hungovercoders_workflow_doc_gen.cli_utils import validate_against_schema, get_output_path

logger = logging.getLogger(__name__)

def main() -> None:
    parser = argparse.ArgumentParser(description="Generate OKR documentation from Azure DevOps.")
    parser.add_argument("--org", required=True, help="Azure DevOps organization name")
    parser.add_argument("--project", required=True, help="Azure DevOps project name")
    parser.add_argument("--pat", required=True, help="Azure DevOps Personal Access Token")
    parser.add_argument("--output-dir", default="outputs/", help="Output directory (default: current directory)")
    parser.add_argument("--format", choices=["markdown", "doc", "pdf", "raw-json"], default="markdown", help="Output format: markdown, doc (Word-compatible HTML), pdf, or raw-json")
    parser.add_argument("--schema", default=None, help="Path to JSON schema (default: okr_summary.json in schemas dir)")
    parser.add_argument("--no-validate", action="store_true", help="Skip validation against JSON schema")
    args = parser.parse_args()

    client = AzureDevOpsClient(args.org, args.project, args.pat)
    okr_data = client.fetch_and_normalize_okrs_with_relations()

    # Determine schema path
    schema_path = args.schema
    if not schema_path:
        here = os.path.dirname(os.path.abspath(__file__))
        schema_path = os.path.join(here, 'schemas/okr_summary.json')
        if not os.path.exists(schema_path):
            schema_path = os.path.join(here, '../schemas/okr_summary.json')

    # Validate
    if not args.no_validate:
        validate_against_schema(okr_data, schema_path)

    formatter = Formatter()
    output_path = get_output_path(args.output_dir, args.format)

    if args.format == "markdown":
        output_str = formatter.format_markdown(okr_data)
        with open(output_path, "w") as f:
            f.write(output_str)
        print(f"OKR Markdown report written to {output_path}")
    elif args.format == "doc":
        output_str = formatter.format_doc(okr_data)
        with open(output_path, "w") as f:
            f.write(output_str)
        print(f"OKR Word-compatible HTML report written to {output_path}")
    elif args.format == "pdf":
        formatter.format_pdf(okr_data, output_path)
        print(f"OKR PDF report written to {output_path}")
    elif args.format == "raw-json":
        with open(output_path, "w") as f:
            json.dump(okr_data, f, indent=2)
        print(f"OKR JSON report written to {output_path}")

if __name__ == "__main__":
    main()
