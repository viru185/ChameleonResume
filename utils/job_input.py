import os
import requests
from bs4 import BeautifulSoup
from utils.logger import logger

def get_job_description():
    source = input("Choose job description source (text / file / url): ").strip().lower()

    if source == "text":
        logger.info("Job description input via text.")
        return input("Paste the job description here:\n")

    elif source == "file":
        path = input("Enter the path to the job description file: ").strip()
        try:
            with open(path, "r", encoding="utf-8") as f:
                logger.info(f"Loaded job description from file: {path}")
                return f.read()
        except Exception as e:
            logger.error(f"Failed to load job description from file: {e}")
            return ""

    elif source == "url":
        url = input("Enter the URL of the job posting: ").strip()
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            # Very basic logic - user may need to tweak for specific sites
            job_text = soup.get_text(separator='\n')
            logger.info(f"Scraped job description from URL: {url}")
            return job_text
        except Exception as e:
            logger.error(f"Failed to scrape job description from URL: {e}")
            return ""

    else:
        logger.warning("Invalid input method selected.")
        return ""
