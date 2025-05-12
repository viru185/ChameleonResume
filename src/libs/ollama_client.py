import json
from  ollama import chat, ChatResponse, ResponseError, RequestError

# App librarys, modules and utils imports.
from src.utils.logger import logger

def prompt_builder(candidate_data: dict, job_description: str) -> list:
    """
    Generates a prompt for the Ollama client to create a tailored resume in HTML format.
    Args:
        candidate_data (dict): A dictionary containing the candidate's personal and professional information.
            Expected to include a 'personal_information' key with 'name' and 'surname' fields.
        job_description (str): A string containing the job description to tailor the resume for.
    Returns:
        list: A list of two dictionaries:
            - The first dictionary defines the system's role and provides instructions for generating the resume.
            - The second dictionary defines the user's role, including the candidate's data and job description,
              along with detailed requirements for the resume.
    Notes:
        - The generated resume should be a single HTML file with embedded CSS.
        - The design should be modern, mobile-friendly, and ATS-compliant.
        - The function logs the conversion of candidate data to JSON and the generation of the prompt.
    """
    
    # This is dictionary comprehension to get name and surname and join them into a full name.
    full_name = " ".join([candidate_data['personal_information'].get(key) for key in ['name', 'surname']])
    
    logger.info('Converting candidate_data dictionary to JSON format.')
    candidate_data_json = json.dumps(candidate_data, indent=4)
    
    logger.info('Generating the prompt for the ollama client.')
    
    # Define the system role dictionary
    role_system_dict = {
        "role": "system",
        "content": (
            "You are an expert resume writer and frontend developer. Your job is to create visually appealing, "
            "modern, job-tailored resumes. The resume should be generated in a single HTML file with embedded CSS. "
            "The layout should include proper sections, a clean structure, and mobile responsiveness. Make sure it "
            "is well-suited for ATS (Applicant Tracking Systems) while still being human-readable."
        )
    }
    
    # Define the user role dictionary
    role_user_dict = {
        "role": "user",
        "content": (
            f"Here is the user's information in JSON format:\n{candidate_data_json}\n\n"
            f"Here is the job description:\n{job_description}\n\n"
            "Using the information above, generate a resume that:\n"
            "- Is tailored to the job description.\n"
            "- Includes a polished Profile Summary.\n"
            "- Highlights relevant Skills, Experience, Education, Projects, and Certifications (if available).\n"
            "- Presents content using professional and concise language.\n"
            "- Is output as a single, valid HTML file.\n"
            "- Includes a <style> block in the <head> for all CSS (no external CSS).\n"
            "- Uses clean, modern design (nice typography, spacing, light shadows, subtle colors).\n"
            "- Is mobile-friendly and looks good when opened in a browser.\n\n"
            "Return only the HTML file. Do not explain anything."
        )
    }
    
    return [role_system_dict, role_user_dict]
    
    
def generate_resume_with_ollama(candidate_data: dict, job_description: str, model='mistral') -> str:
    """
    Generates a resume tailored to a specific job description using the Ollama client.
    Args:
        candidate_data (dict): A dictionary containing the candidate's information, such as skills, experience, and education.
        job_description (str): A string containing the job description to tailor the resume to.
        model (str, optional): The name of the model to use for generating the resume. Defaults to 'mistral'.
    Returns:
        str: The generated resume as a string.
    Raises:
        ResponseError: If there is an error in the response from the Ollama client.
        RequestError: If there is an error in the request to the Ollama client.
        Exception: For any other unexpected errors during the resume generation process.
    """
    
    prompt = prompt_builder(candidate_data, job_description)
    
    try:
        response: ChatResponse = chat(
            model = model,
            messages = prompt
        )
        
        logger.info('Received response from Ollama client successfully.')
        if response and 'message' in response and 'content' in response['message']:
            logger.debug(f"Ollama response content: {response['message']['content'][:500]}...")  # Log first 500 chars
        else:
            logger.warning('Unexpected response format from Ollama client.')
        return (response['message']['content'])
    
    except ResponseError as res_e:
        logger.error(f'Error generating resume with Ollama: {res_e}')
    except RequestError as req_e:
        logger.error(f'Error generating resume with Ollama: {req_e}')
    except Exception as e:
        logger.error(f'Error generating resume with Ollama: {e}')

if __name__ == "__main__":
    # * Testing the ollama_client.py
    
    import yaml
    import json
    from rich import print
    import os
    
    def data_loader():
        with open("private/candidate.yaml", "r") as candidate_yaml_file:
            candidate_data: dict = yaml.load(candidate_yaml_file, Loader=yaml.FullLoader)
 
        return candidate_data

    def job_description_loader():
        with open("private/job_des.txt", "r") as job_desc_file:
            job_description = job_desc_file.read()
        
        return job_description
    
    candidate_data = data_loader()
    job_des = job_description_loader()
    
    response = generate_resume_with_ollama(candidate_data, job_des, model='deepseek-r1:14b')
    
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)

    base_filename = "resume_beta"
    file_extension = ".html"
    counter = 1

    while True:
        filename = f"{base_filename}_{counter}{file_extension}"
        file_path = os.path.join(output_dir, filename)
        if not os.path.exists(file_path):
            break
        counter += 1

    with open(file_path, "w", encoding="utf-8") as html_file:
        html_file.write(response)

    print(f"Resume written to {file_path}")