"""
MarkdownOKRFormatter: Outputs OKR data as Markdown.
"""
import logging
from typing import List, Dict, Any
import os
from jinja2 import Environment, FileSystemLoader, TemplateNotFound

logger = logging.getLogger(__name__)

class MarkdownOKRFormatter:
    """
    Formats Objectives, Key Results, Hypotheses, and Issues into Markdown and JSON.
    """
    def __init__(self) -> None:
        # Set up Jinja2 environment for templates
        template_dir = os.path.dirname(os.path.abspath(__file__))
        self.env = Environment(loader=FileSystemLoader(template_dir))

    def format_markdown(self, objectives: List[Dict[str, Any]]) -> str:
        """
        Generate a Markdown document from a list of objectives with required fields and their hypotheses using a Jinja2 template.

        Args:
            objectives: List of objective dicts with id, title, state, key_results, objective, method_of_measure, objective_outcome, hypotheses.
        Returns:
            Markdown string representing the OKR structure.
        """
        try:
            template = self.env.get_template('templates/okr_markdown_template.j2')
            return template.render(objectives=objectives)
        except TemplateNotFound:
            logger.error("Markdown template 'okr_markdown_template.j2' not found.")
            return ""
        except Exception as e:
            logger.error(f"Failed to format markdown: {e}")
            return ""