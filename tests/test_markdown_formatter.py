"""
Unit tests for MarkdownOKRFormatter.
"""
import pytest
from hungovercoders_workflow_doc_gen.markdown_formatter import MarkdownOKRFormatter

@pytest.fixture
def sample_okrs():
    return [
        {
            "title": "Increase Customer Satisfaction",
            "description": "Objective to improve NPS score.",
            "key_results": [
                {
                    "title": "Raise NPS by 10 points",
                    "description": "Key result to measure NPS improvement.",
                    "hypotheses": [
                        {
                            "title": "Faster support response improves NPS",
                            "description": "Test if reducing response time increases NPS.",
                            "issues": [
                                {"title": "Support team understaffed", "description": "Need to hire 2 more agents."},
                                {"title": "Ticket system slow", "description": "Optimize backend queries."}
                            ]
                        }
                    ]
                }
            ]
        }
    ]

def test_format_markdown(sample_okrs):
    formatter = MarkdownOKRFormatter()
    md = formatter.format_markdown(sample_okrs)
    assert "# Objectives and Key Results" in md
    assert "## Objective: Increase Customer Satisfaction" in md
    assert "### Key Result: Raise NPS by 10 points" in md
    assert "#### Hypothesis: Faster support response improves NPS" in md
    assert "- **Issue:** Support team understaffed" in md
    assert "Need to hire 2 more agents." in md

def test_format_json(sample_okrs):
    formatter = MarkdownOKRFormatter()
    json_str = formatter.format_json(sample_okrs)
    assert '"title": "Increase Customer Satisfaction"' in json_str
    assert '"issues":' in json_str

def test_format_markdown_empty():
    formatter = MarkdownOKRFormatter()
    md = formatter.format_markdown([])
    assert md.strip().startswith("# Objectives and Key Results")
    assert "Objective:" not in md

def test_format_json_empty():
    formatter = MarkdownOKRFormatter()
    json_str = formatter.format_json([])
    assert json_str == "[]"
