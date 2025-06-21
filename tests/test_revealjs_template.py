import os
from jinja2 import Environment, FileSystemLoader

def test_render_revealjs_template():
    """
    Test rendering the Reveal.js OKR Jinja2 template with sample data.
    Prints the output for manual inspection and asserts key content.
    """
    # Always resolve relative to this test file's location
    this_dir = os.path.dirname(os.path.abspath(__file__))
    template_dir = os.path.abspath(os.path.join(this_dir, '../src/hungovercoders_workflow_doc_gen'))
    print("Template directory:", template_dir)
    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template('revealjs_okr_template.j2')

    # Example objectives data
    objectives = [
        {
            "title": "Increase User Engagement",
            "key_results": "<li>Grow DAU by 20%</li><li>Increase session length by 10%</li>",
            "hypotheses": [
                {"title": "Gamification increases retention", "hypothesis": "Adding badges will boost DAU"},
                {"title": "Push notifications drive sessions", "hypothesis": "Timely reminders increase session count"}
            ]
        },
        {
            "title": "Improve Platform Stability",
            "key_results": "<li>99.9% uptime</li><li>Reduce error rate by 50%</li>",
            "hypotheses": [
                {"title": "Error monitoring reduces downtime", "hypothesis": "Faster alerts = faster fixes"}
            ]
        }
    ]

    # Render the template
    output = template.render(objectives=objectives)
    print(output)  # Or write to a file for manual inspection

    # Optionally, assert some expected content
    assert "Increase User Engagement" in output
    assert "99.9% uptime" in output

if __name__ == "__main__":
    test_render_revealjs_template()
