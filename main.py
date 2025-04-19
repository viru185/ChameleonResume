import os
import sys
import yaml
import json

# My librarys and modules imports.
from utils.job_input import GetJobDescription
from utils.ollama_client import generate_resume_with_ollama
from utils.resume_renderer import render_resume
from utils.logger import logger

# clear the log is the arg pass.
if "--clear-log" in sys.argv:
    open("logs/chameleon_resume.log", "w").close()

# Load candidate data
def load_candidate_data() -> dict:
    try:
        with open("private/candidate.yaml", "r", encoding="utf-8") as candidate_yaml_file:
            
            candidate_data: dict = yaml.load(candidate_yaml_file, Loader=yaml.FullLoader)
            logger.info("Candidate data has been loaded from YAML.")
            
            return candidate_data
        
    except Exception as e:
        logger.error(f"Failed to load candidate data: {e}")
        raise

# Entry point to the programm
def main():
    logger.info("Loading candidate data.")
    candidate_data: dict = load_candidate_data()
    
    logger.info("Getting the job description from user.")
    job_desc = GetJobDescription.run()

    logger.info("Generating tailored resume using Mistral via Ollama...")
    resume_text = generate_resume_with_ollama(candidate_data, job_desc)
    
    print(resume_text)
    exit()

    logger.info("Rendering resume to HTML and PDF...")
    render_resume(resume_text)

    logger.info("Resume generation complete. Output saved to 'output/' folder.")
    print("Done. Check the 'output' folder.")

if __name__ == "__main__":
    main()