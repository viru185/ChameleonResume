import os
from markdown import markdown
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML
from utils.logger import logger


def render_resume(markdown_resume):
    try:
        os.makedirs("output", exist_ok=True)

        # Convert Markdown to HTML body
        resume_body = markdown(markdown_resume)

        # Load Jinja2 template
        env = Environment(loader=FileSystemLoader("templates"))
        template = env.get_template("resume_template.html")

        # Render full HTML
        rendered_html = template.render(resume_content=resume_body)

        # Save HTML
        html_path = "output/resume.html"
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(rendered_html)

        # Convert to PDF
        pdf_path = "output/resume.pdf"
        HTML(string=rendered_html).write_pdf(pdf_path)

        logger.info("Resume rendered and exported to HTML and PDF.")

    except Exception as e:
        logger.error(f"Error rendering resume: {e}")
