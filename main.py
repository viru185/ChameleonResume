import os
import yaml
from utils.job_input import get_job_description
from utils.ollama_client import generate_resume_with_ollama
from utils.resume_renderer import render_resume
from utils.logger import logger
import sys

# clear the log is the arg pass.
if "--clear-log" in sys.argv:
    open("logs/chameleon_resume.log", "w").close()


# Load candidate data
def load_candidate_data():
    try:
        with open("private/candidate.yaml", "r", encoding="utf-8") as f:
            logger.info("Loaded candidate data from YAML.")
            return yaml.safe_load(f)
    except Exception as e:
        logger.error(f"Failed to load candidate data: {e}")
        raise

def main():
    candidate = load_candidate_data()
    job_desc = get_job_description()

    logger.info("Generating tailored resume using Mistral via Ollama...")
    resume_text = generate_resume_with_ollama(candidate, job_desc)

    logger.info("Rendering resume to HTML and PDF...")
    render_resume(resume_text)

    logger.info("Resume generation complete. Output saved to 'output/' folder.")
    print("Done. Check the 'output' folder.")

if __name__ == "__main__":
    main()