import json
from  ollama import chat, ChatResponse, ResponseError, RequestError

# My librarys and modules imports.
from utils.logger import logger

def build_prompt(candidate_data: dict, job_description: str) -> dict:
    """This function return the list of two dictionary."""
    
    # This is dictionary comprehension to get name and surname and joined into to full name.
    full_name = " ".join([candidate_data['personal_information'].get(key) for key in ['name', 'surname']])
    
    logger.info('Converting candidate_data dictionary to JSON formate.')
    candidate_data_json = json.dumps(candidate_data, indent=4)
    
    logger.info('Generating the prompt for the ollama client.')
    role_system_dict = dict(
        role = "system",
        content = f"""Act like a professional resume writer.
                    You are creating a job-specific resume for a candidate name {full_name}.
                    Generate a tailored resume in structured, professional English and ATS friendly. Focus on aligning experience, skills, and achievements to the job.
                    Use clear sections and bullet points. Do not fabricate any details.
                    Format the output in well designed HTML format."""
    )
    
    role_user_dict = dict(
        role = "user",
        content = f"""Here is candidate profile in json format:
                    {candidate_data_json}
                    
                    Here is the job description:
                    {job_description}
        """
    )
    
    return [role_system_dict,role_user_dict]
    
    
def generate_resume_with_ollama(candidate_data: dict, job_description: str, model='mistral') -> str:
    
    prompt = build_prompt(candidate_data, job_description)
    
    try:
        response: ChatResponse = chat(
            model= model,
            messages=[prompt]
        )

        return (response['message']['content'])
    
    except ollama.ResponseError as res_e:
        logger.error(f'Error generating resume with Ollama: {res_e}')
    except ollama.RequestError as req_e:
        logger.error(f'Error generating resume with Ollama: {req_e}')
    except Exception as e:
        logger.error(f'Error generating resume with Ollama: {e}')

if __name__ == "__main__":
    pass