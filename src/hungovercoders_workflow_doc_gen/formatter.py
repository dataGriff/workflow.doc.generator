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
        self.env = Environment(
            loader=FileSystemLoader(template_dir + '/templates'),
            extensions=["jinja2.ext.do", "jinja2.ext.loopcontrols"]
        )
        # Add 'now' function to Jinja2 environment
        from jinja2 import pass_context
        import datetime
        @pass_context
        def now(context, tz=None, fmt=None):
            dt = datetime.datetime.now()
            if fmt:
                return dt.strftime(fmt)
            return dt.isoformat()
        self.env.globals['now'] = now

    def _extract_objectives(self, okr_data: Any) -> List[Dict[str, Any]]:
        """
        Helper to extract objectives list from either a dict with 'objectives' or a list.
        Always returns a list.
        """
        if isinstance(okr_data, dict) and "objectives" in okr_data and isinstance(okr_data["objectives"], list):
            return okr_data["objectives"]
        if isinstance(okr_data, list):
            return okr_data
        return []

    def format_markdown(self, okr_data: Any) -> str:
        """
        Generate a Markdown document from OKR data (dict or list) using a Jinja2 template.

        Args:
            okr_data: Dict with 'objectives' key or list of objective dicts.
        Returns:
            Markdown string representing the OKR structure.
        """
        objectives = self._extract_objectives(okr_data)
        try:
            template = self.env.get_template('okr_markdown_template.j2')
            return template.render(objectives=objectives)
        except TemplateNotFound:
            logger.error("Markdown template 'okr_markdown_template.j2' not found.")
            return ""
        except Exception as e:
            logger.error(f"Failed to format markdown: {e}")
            return ""

    def format_doc(self, okr_data: Any) -> str:
        """
        Generate a Word-compatible HTML document from OKR data (dict or list) using a Jinja2 template.

        Args:
            okr_data: Dict with 'objectives' key or list of objective dicts.
        Returns:
            HTML string representing the OKR structure, compatible with Word.
        """
        objectives = self._extract_objectives(okr_data)
        try:
            template = self.env.get_template('okr_doc_template.j2')
            return template.render(objectives=objectives)
        except TemplateNotFound:
            logger.error("Word template 'okr_doc_template.j2' not found.")
            return ""
        except Exception as e:
            logger.error(f"Failed to format word-compatible HTML: {e}")
            return ""

    def format_pdf(self, okr_data: Any, output_path: str) -> None:
        """
        Generate a PDF document from OKR data (dict or list) using the Word-compatible HTML Jinja2 template and WeasyPrint.

        Args:
            okr_data: Dict with 'objectives' key or list of objective dicts.
            output_path: Path to write the PDF file.
        """
        objectives = self._extract_objectives(okr_data)
        try:
            template = self.env.get_template('okr_doc_template.j2')
            html_str = template.render(objectives=objectives)
            HTML(string=html_str).write_pdf(output_path)
        except TemplateNotFound:
            logger.error("Word template 'okr_doc_template.j2' not found for PDF export.")
        except Exception as e:
            logger.error(f"Failed to generate PDF: {e}")