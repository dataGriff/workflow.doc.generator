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
        Generate a Markdown document from a list of objectives with required fields and their hypotheses.

        Args:
            objectives: List of objective dicts with id, title, state, key_results, objective, method_of_measure, objective_outcome, hypotheses.
        Returns:
            Markdown string representing the OKR structure.
        """
        try:
            md = "# Objectives and Key Results\n\n"
            for obj in objectives:
                md += f"## Objective: {obj.get('title', 'Untitled')} (ID: {obj.get('id', '')})\n"
                md += f"**State:** {obj.get('state', '')}\n\n"
                md += f"**Objective:** {obj.get('objective', '')}\n\n"
                md += f"**Key Results:** {obj.get('key_results', '')}\n\n"
                md += f"**Method of Measure:** {obj.get('method_of_measure', '')}\n\n"
                md += f"**Objective Outcome:** {obj.get('objective_outcome', '')}\n\n"
                if obj.get('hypotheses'):
                    md += f"### Hypotheses\n"
                    for hyp in obj['hypotheses']:
                        md += f"- **Hypothesis:** {hyp.get('hypothesis', '')} (ID: {hyp.get('id', '')})\n"
                        md += f"  - **Title:** {hyp.get('title', '')}\n"
                        md += f"  - **State:** {hyp.get('state', '')}\n"
                        md += f"  - **Method of Measuring Hypothesis:** {hyp.get('method_of_measuring_hypothesis', '')}\n"
                        md += f"  - **Hypothesis Outcome:** {hyp.get('hypothesis_outcome', '')}\n\n"
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
