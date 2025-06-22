import os
import json
import jsonschema
import logging

logger = logging.getLogger(__name__)

def validate_against_schema(data, schema_path):
    """
    Validate data against a JSON schema. Raises SystemExit(1) on failure.
    """
    with open(schema_path, encoding='utf-8') as f:
        schema = json.load(f)
    try:
        jsonschema.validate(instance=data, schema=schema)
        print("OKR data validated successfully against schema.")
    except jsonschema.ValidationError as e:
        logger.error(f"OKR data validation failed: {e.message}")
        raise SystemExit(1)

def get_output_path(output_dir, format):
    """
    Ensure output_dir exists and return the full output file path for the given format.
    """
    ext_map = {
        "markdown": ".md",
        "doc": ".html",
        "pdf": ".pdf",
        "raw-json": ".json",
        "json": ".json"
    }
    ext = ext_map.get(format, ".md")
    if not os.path.isdir(output_dir):
        os.makedirs(output_dir, exist_ok=True)
    return os.path.join(output_dir, f"okr_summary{ext}")
