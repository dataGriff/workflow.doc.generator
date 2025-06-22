import json
import os
from hungovercoders_workflow_doc_gen.formatter import MarkdownOKRFormatter

def test_markdown_output_matches_expected():
    """
    Test that formatting the example OKR JSON produces the expected Markdown output.
    """
    # Paths
    example_json = os.path.join(os.path.dirname(__file__), '../example_input/okr_summary.example.json')
    expected_md = os.path.join(os.path.dirname(__file__), '../example_output/okr_report.md')

    # Load input and expected output
    with open(example_json, encoding='utf-8') as f:
        data = json.load(f)
    with open(expected_md, encoding='utf-8') as f:
        expected = f.read().strip()

    # Format using the formatter
    formatter = MarkdownOKRFormatter()
    actual = formatter.format_markdown(data['objectives']).strip()

    # Normalize whitespace for comparison
    def normalize(text):
        return '\n'.join(line.rstrip() for line in text.strip().splitlines() if line.strip())

    assert normalize(actual) == normalize(expected), "Markdown output does not match expected!"
