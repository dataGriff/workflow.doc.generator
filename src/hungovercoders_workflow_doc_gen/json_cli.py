"""
Generic CLI for validating and converting OKR JSON data to Markdown or Word-compatible HTML.
"""
import argparse
import json
import os
import logging
import sys
from hungovercoders_workflow_doc_gen.formatter import Formatter
from hungovercoders_workflow_doc_gen.cli_utils import validate_against_schema, get_output_path

logger = logging.getLogger(__name__)

def main() -> None:
    parser = argparse.ArgumentParser(description="Validate OKR JSON and output Markdown or Word-compatible HTML.")
    parser.add_argument("--input", required=True, help="Input JSON file (must match okr_summary schema)")
    parser.add_argument("--output-dir", default="outputs/", help="Output directory (default: current directory)")
    parser.add_argument("--format", choices=["markdown", "doc", "pdf"], default="markdown", help="Output format: markdown, word, or pdf")
    parser.add_argument("--schema", default=None, help="Path to JSON schema (default: okr_summary.json in schemas dir)")
    parser.add_argument("--no-validate", action="store_true", help="Skip validation against JSON schema")
    args = parser.parse_args()

    # Load input data
    with open(args.input, encoding='utf-8') as f:
        data = json.load(f)

    # Determine schema path
    schema_path = args.schema
    if not schema_path:
        here = os.path.dirname(os.path.abspath(__file__))
        schema_path = os.path.join(here, 'schemas/okr_summary.json')
        if not os.path.exists(schema_path):
            schema_path = os.path.join(here, '../schemas/okr_summary.json')

    # Validate
    if not args.no_validate:
        validate_against_schema(data, schema_path)

    objectives = data["objectives"]
    formatter = Formatter()
    output_path = get_output_path(args.output_dir, args.format)
    if args.format == "markdown":
        markdown = formatter.format_markdown(objectives)
        with open(output_path, "w") as f:
            f.write(markdown)
        print(f"OKR Markdown report written to {output_path}")
    elif args.format == "doc":
        html = formatter.format_doc(objectives)
        with open(output_path, "w") as f:
            f.write(html)
        print(f"OKR Word-compatible HTML report written to {output_path}")
    elif args.format == "pdf":
        formatter.format_pdf(objectives, output_path)
        print(f"OKR PDF report written to {output_path}")

if __name__ == "__main__":
    main()
