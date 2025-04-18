import json
from  ollama import chat, ChatResponse, ResponseError, RequestError

# My librarys and modules imports.
from utils.logger import logger

def build_prompt(candidate: json, job_description: str) -> dict:
    name = candidate['personal_informaion'].get('name', 'surname')
    
    role_system_dict = dict(
        role = "system",
        content = f"""Act like a professional resume writer.
                    You are creating a job-specific resume for a candidate name {name}.
                    Generate a tailored resume in structured, professional English and ATS friendly. Focus on aligning experience, skills, and achievements to the job.
                    Use clear sections and bullet points. Do not fabricate any details.
                    Format the output in well designed HTML format."""
    )
    
    role_user_dict = dict(
        role = "user",
        content = f"""Here is candidate profile in json format:
                    {candidate}
                    
                    Here is the job description:
                    {job_description}
        """
    )
    
    return [role_system_dict,role_user_dict]
    
    
def generate_resume_with_ollama(candidate: json, job_description: str, model='mistral') -> str:
    
    prompt = build_prompt(candidate, job_description)
    
    try:
        response: ChatResponse = chat(
            model= model,
            messages=[prompt]
        )
    
    except ollama.ResponseError as res_e:
        logger.error(f'Error generating resume with Ollama: {res_e}')
    except ollama.RequestError as req_e:
        logger.error(f'Error generating resume with Ollama: {req_e}')
    except Exception as e:
        logger.error(f'Error generating resume with Ollama: {e}')

if __name__ == "__main__":
    response: ChatResponse = chat(
        model='mistral',
        messages=[
            {
                'role': 'system',
                'content': 'Act like a professional resume writer. You are creating a job-specific resume for a candidate named Viren Hirpara.',
            },
            {
                'role': 'user',
                'content':
            }
                
        ]
    )
    print('type of the response')
    pprint(type(response))
    
    print('THIS IS THE MAIN RESPONSE.')
    pprint(response)
    
    print('THIS RESPONSE IS FROM CHUNK.')
    for chunk in response:
        print(chunk['message']['content'], end='', flush=True)