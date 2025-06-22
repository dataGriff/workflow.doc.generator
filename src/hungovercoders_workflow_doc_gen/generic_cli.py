"""
Generic CLI for validating and converting OKR JSON data to Markdown.
"""
import argparse
import json
import os
import logging
import sys
from hungovercoders_workflow_doc_gen.markdown_formatter import MarkdownOKRFormatter
import jsonschema

logger = logging.getLogger(__name__)

def main() -> None:
    parser = argparse.ArgumentParser(description="Validate OKR JSON and output Markdown.")
    parser.add_argument("--input", required=True, help="Input JSON file (must match okr_summary schema)")
    parser.add_argument("--output", default="okr_report.md", help="Output Markdown file")
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
        with open(schema_path, encoding='utf-8') as f:
            schema = json.load(f)
        try:
            jsonschema.validate(instance=data, schema=schema)
            print("OKR data validated successfully against schema.")
        except jsonschema.ValidationError as e:
            logger.error(f"OKR data validation failed: {e.message}")
            sys.exit(1)

    # Format to Markdown
    formatter = MarkdownOKRFormatter()
    objectives = data["objectives"]
    markdown = formatter.format_markdown(objectives)
    print(markdown)
    with open(args.output, "w") as f:
        f.write(markdown)
    print(f"OKR Markdown report written to {args.output}")

if __name__ == "__main__":
    main()
