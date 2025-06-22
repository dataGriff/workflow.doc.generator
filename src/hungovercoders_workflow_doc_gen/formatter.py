"""
MarkdownOKRFormatter: Outputs OKR data as Markdown.
"""
import logging
from typing import List, Dict, Any
import os
from jinja2 import Environment, FileSystemLoader, TemplateNotFound
from weasyprint import HTML

logger = logging.getLogger(__name__)

class Formatter:
    """
    Formats Objectives, Key Results, Hypotheses, and Issues into Markdown, Word-compatible HTML, and JSON.
    """
    def __init__(self) -> None:
        # Set up Jinja2 environment for templates
        template_dir = os.path.dirname(os.path.abspath(__file__))
        self.env = Environment(loader=FileSystemLoader(template_dir + '/templates'))

    def format_markdown(self, objectives: List[Dict[str, Any]]) -> str:
        """
        Generate a Markdown document from a list of objectives with required fields and their hypotheses using a Jinja2 template.

        Args:
            objectives: List of objective dicts with id, title, state, key_results, objective, method_of_measure, objective_outcome, hypotheses.
        Returns:
            Markdown string representing the OKR structure.
        """
        try:
            template = self.env.get_template('okr_markdown_template.j2')
            return template.render(objectives=objectives)
        except TemplateNotFound:
            logger.error("Markdown template 'okr_markdown_template.j2' not found.")
            return ""
        except Exception as e:
            logger.error(f"Failed to format markdown: {e}")
            return ""

    def format_doc(self, objectives: List[Dict[str, Any]]) -> str:
        """
        Generate a Word-compatible HTML document from a list of objectives using a Jinja2 template.

        Args:
            objectives: List of objective dicts with id, title, state, key_results, objective, method_of_measure, objective_outcome, hypotheses.
        Returns:
            HTML string representing the OKR structure, compatible with Word.
        """
        try:
            template = self.env.get_template('okr_doc_template.j2')
            return template.render(objectives=objectives)
        except TemplateNotFound:
            logger.error("Word template 'okr_doc_template.j2' not found.")
            return ""
        except Exception as e:
            logger.error(f"Failed to format word-compatible HTML: {e}")
            return ""

    def format_pdf(self, objectives: List[Dict[str, Any]], output_path: str) -> None:
        """
        Generate a PDF document from a list of objectives using the Word-compatible HTML Jinja2 template and WeasyPrint.

        Args:
            objectives: List of objective dicts.
            output_path: Path to write the PDF file.
        """
        try:
            template = self.env.get_template('okr_doc_template.j2')
            html_str = template.render(objectives=objectives)
            HTML(string=html_str).write_pdf(output_path)
        except TemplateNotFound:
            logger.error("Word template 'okr_doc_template.j2' not found for PDF export.")
        except Exception as e:
            logger.error(f"Failed to generate PDF: {e}")