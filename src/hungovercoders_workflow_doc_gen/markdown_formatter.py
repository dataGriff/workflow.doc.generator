"""
MarkdownOKRFormatter: Outputs OKR data as Markdown and JSON.
"""
import logging
from typing import List, Dict, Any
import json
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
            template = self.env.get_template('okr_markdown_template.j2')
            return template.render(objectives=objectives)
        except TemplateNotFound:
            logger.error("Markdown template 'okr_markdown_template.j2' not found.")
            return ""
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

    def format_revealjs(self, objectives: List[Dict[str, Any]]) -> str:
        """
        Generate a single compact Reveal.js slide: objectives as columns, only name in top row, key results and hypotheses below.
        """
        try:
            n = len(objectives)
            headline = "<h2 style='text-align:center;color:#2d7ff9;margin-bottom:0.5em;font-size:2em;'>🎯 OKRs Overview</h2>"
            grid_template = f"display: grid; grid-template-columns: repeat({n}, 1fr); gap: 0.7em; justify-items: center; align-items: start;"
            box_css = "background: #f4f4f4; border-radius: 8px; box-shadow: 0 1px 4px #0001; padding: 0.5em; min-width: 120px; max-width: 200px; margin-bottom: 0.5em; font-size:0.95em;"
            html = [headline, f"<div style='{grid_template}'>"]
            # Row 1: Objective names only
            for obj in objectives:
                html.append(
                    f"<div style='{box_css};font-size:1.1em;font-weight:bold;text-align:center;background:#e6f7ff;'>"
                    f"{obj.get('title', 'Untitled')}"
                    f"</div>"
                )
            # Row 2: Key Results (short, bullet list)
            for obj in objectives:
                key_results = obj.get('key_results', '')
                kr_box = ""
                if key_results:
                    import re
                    kr_list = re.findall(r'<li>(.*?)</li>', key_results) or [key_results]
                    kr_box = "<ul style='padding-left:1.1em;margin:0;font-size:0.95em;'>" + ''.join(f"<li>{kr}</li>" for kr in kr_list) + "</ul>"
                html.append(
                    f"<div style='{box_css};background:#f0faff;'>"
                    f"{kr_box}"
                    f"</div>"
                )
            # Row 3: Hypotheses (short, bullet list)
            for obj in objectives:
                hyp_box = ""
                if obj.get('hypotheses'):
                    hyp_box = "<ul style='padding-left:1.1em;margin:0;font-size:0.95em;'>"
                    for hyp in obj['hypotheses']:
                        hyp_box += (
                            f"<li>{hyp.get('title', '')}" +
                            (f"<br><span style='font-size:0.9em;color:#888;'>{hyp.get('hypothesis', '')}</span>" if hyp.get('hypothesis', '') else "") +
                            "</li>"
                        )
                    hyp_box += "</ul>"
                html.append(
                    f"<div style='{box_css};background:#fffbe6;'>"
                    f"{hyp_box}"
                    f"</div>"
                )
            html.append("</div>")
            return "\n".join(html)
        except Exception as e:
            logger.error(f"Failed to format reveal.js markdown: {e}")
            return ""
