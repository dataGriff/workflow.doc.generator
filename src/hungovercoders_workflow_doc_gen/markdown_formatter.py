"""
MarkdownOKRFormatter: Outputs OKR data as Markdown and JSON.
"""
import logging
from typing import List, Dict, Any
import json

logger = logging.getLogger(__name__)

class MarkdownOKRFormatter:
    """
    Formats Objectives, Key Results, Hypotheses, and Issues into Markdown and JSON.
    """
    def __init__(self) -> None:
        pass

    def format_markdown(self, objectives: List[Dict[str, Any]]) -> str:
        """
        Generate a Markdown document from a list of objectives.

        Args:
            objectives: List of objective dicts, each with key_results, hypotheses, and issues.
        Returns:
            Markdown string representing the OKR structure.
        """
        try:
            md = "# Objectives and Key Results\n\n"
            for obj in objectives:
                md += f"## Objective: {obj.get('title', 'Untitled')}\n"
                md += f"{obj.get('description', '')}\n\n"
                for kr in obj.get('key_results', []):
                    md += f"### Key Result: {kr.get('title', 'Untitled')}\n"
                    md += f"{kr.get('description', '')}\n\n"
                    for hyp in kr.get('hypotheses', []):
                        md += f"#### Hypothesis: {hyp.get('title', 'Untitled')}\n"
                        md += f"{hyp.get('description', '')}\n\n"
                        for issue in hyp.get('issues', []):
                            md += f"- **Issue:** {issue.get('title', 'Untitled')}\n"
                            if issue.get('description'):
                                md += f"    - {issue['description']}\n"
                        md += "\n"
            return md
        except Exception as e:
            logger.error(f"Failed to format markdown: {e}")
            return ""

    def format_json(self, objectives: List[Dict[str, Any]]) -> str:
        """
        Output the OKR structure as a JSON string.

        Args:
            objectives: List of objective dicts.
        Returns:
            JSON string.
        """
        try:
            return json.dumps(objectives, indent=2)
        except Exception as e:
            logger.error(f"Failed to format JSON: {e}")
            return "{}"
