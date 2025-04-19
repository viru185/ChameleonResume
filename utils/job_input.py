import os
import requests
import inquirer
from bs4 import BeautifulSoup

# My librarys and modules imports.
from utils.logger import logger

class GetJobDescription:
    """User will be prompted to choose and load job description from a choice of the user."""
    
    @classmethod
    def run(cls):
        # Prompt user to select the source
        questions = [
            inquirer.List(
                "source",
                message="Choose job description source",
                choices=["Text", "File", "URL"],
                carousel=True # loop through choises
            )
        ]

        answer = inquirer.prompt(questions)
        source = answer.get("source") # Get the user's selection
    
        # Call the appropriate method
        try:
            if source == "Text":
                return cls._from_text()
            elif source == "File":
                return cls._from_file()
            elif source == "URL":
                return cls._from_url()
        except Exception as e:
            logger.warning(f"Something has gone wrong. -> {e}")
            return ""

    @staticmethod
    def _from_text() -> str:
        # Prompt user tho input job description as text
        logger.info("Job description input via text")
        questions = [
            inquirer.Editor("job_des_text", message="Provide long text")
        ]

        answers = inquirer.prompt(questions)
        return answers.get("job_des_text")
    
    @staticmethod
    def _from_file() -> str:
        # Prompt user to provide a file path
        questions = [
            inquirer.Path(
                'job_des_file_path',
                message="Enter path to the job description file",
                path_type=inquirer.Path.FILE
            )
        ]
        answer = inquirer.prompt(questions)
        path = answer.get('job_des_file_path')
        
        try:
            with open(path, "r", encoding="utf-8") as f:
                logger.info(f"Loaded job description from file: {path}")
                return f.read()
        except Exception as e:
            logger.error(f"Failed to load job description from file: {e}")
            return ""
    
    @staticmethod
    def _from_url() -> str:
        # Prompt user to provide a URL
        questions = [
            inquirer.Text(
                'job_des_URL',
                message="Enter the URL of the job posting: "
            ) 
        ]
        answer = inquirer.prompt(questions)
        url = answer.get('job_des_URL')
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

if __name__ == "__main__":
    
    # get_job_description()
    job_description = GetJobDescription.run()
    print(job_description)