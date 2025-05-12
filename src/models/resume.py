import yaml
from datetime import date
from dataclasses import dataclass
from typing import Optional, List, Dict, Union
from pydantic import BaseModel, Field, EmailStr, HttpUrl


class PersonalInformation(BaseModel):
    name: str = Field(..., description="First name of the candidate")
    surname: str = Field(..., description="Second name of the candidate")
    date_of_birth: str = Field(..., description="Date of birth of the candidate")
    address: str = Field(..., description="Address of the candidate")
    city: str = Field(..., description="City of residence of the candidate")
    pin_code: str = Field(..., description="Postal code of the candidate's address")
    country: str = Field(..., description="Country of residence of the candidate")
    phone_prefix: str = Field(..., description="Phone number prefix of the candidate")
    phone: str = Field(..., description="Phone number of the candidate")
    email: EmailStr = Field(..., description="Email address of the candidate")
    linkedin: HttpUrl = Field(..., description="LinkedIn profile URL of the candidate")
    github: HttpUrl = Field(None, description="GitHub profile URL of the candidate")


class EducationDetails(BaseModel):
    education_level: str = Field(..., description="Level of education")
    insitution: str = Field(..., description="Name of the educational institution")
    field_of_study: str = Field(..., description="Field of study")
    final_evaluation_grade: Optional[str] = Field(..., description="Final evaluation grade")
    start_date: str = Field(..., description="Start date of education")
    finish_date: str = Field(..., description="Finish date of education")
    exam: Optional[List[Dict[str, str]]] = Field(None, description="Exams taken during education")

class ExperienceDetails(BaseModel):
    position: str = Field(..., description="Job title of the candidate")
    company: str = Field(..., description="Name of the company")
    start_date: date = Field(..., description="Start date of employment")
    finish_date: Union[date, str] = Field(..., description="Finish date of employment")
    location: str = Field(..., description="Location of the job")
    industry: str = Field(..., description="Industry of the job")
    key_responsibilities: List[str] = Field(None, description="Key responsibilities in the job")
    skills: List[str] = Field(None, description="Skills used in the job")


class Project(BaseModel):
    name: str = Field(..., description="Name of the project")
    description: str = Field(..., description="Description of the project")
    start_date: Optional[date] = Field(None, description="Start date of the project")
    finish_date: Optional[Union[date, str]] = Field(None, description="Finish date of the project")
    technologies: Optional[List[str]] = Field(None, description="Technologies used in the project")
    link: Optional[HttpUrl] = Field(None, description="Link to the project")


class Achievement(BaseModel):
    title: Optional[str] = Field(None, description="Title of the achievement")
    description: Optional[str] = Field(None, description="Description of the achievement")
    date: Optional[date] = Field(None, description="Date of the achievement")
    link: Optional[HttpUrl] = Field(None, description="Link to the achievement")


class Certification(BaseModel):
    title: str = Field(..., description="Title of the certification")
    description: str = Field(..., description="Description of the certification")
    institution: Optional[str] = Field(None, description="Name of the institution that issued the certification")
    date: Optional[date] = Field(None, description="Date of the certification")
    link: Optional[HttpUrl] = Field(None, description="Link to the certification")


class Language(BaseModel):
    name: str = Field(..., description="Name of the language")
    level: str = Field(..., description="Proficiency level in the language")


class Skill(BaseModel):
    __root__: Dict[str, List[str]] = Field(..., description="Dynamic skill groups with lists of skills")
    

class Resume(BaseModel):
    personal_information: PersonalInformation = Field(..., description="Personal information of the candidate")
    education: List[EducationDetails] = Field(..., description="List of education details")
    experience: List[ExperienceDetails] = Field(..., description="List of experience details")
    projects: Optional[List[Project]] = Field(None, description="List of projects")
    achievements: Optional[List[Achievement]] = Field(None, description="List of achievements")
    certifications: Optional[List[Certification]] = Field(None, description="List of certifications")
    languages: Optional[List[Language]] = Field(None, description="List of languages spoken")
    skill: Optional[Skill] = Field(None, description="Skills of the candidate")
    
    def __init__(self, yaml_str: str):
        try:
            # Load YAML data
            data = yaml.safe_load(yaml_str)
        
            super().__init__(**data)
        
        except yaml.YAMLError as e:
            raise ValueError(f"Error parsing YAML data: {e}")
        except Exception as e:
            raise ValueError(f"Error initializing resume object: {e}")
        
    def _process_personal_information(self, data: dict) -> PersonalInformation:
        try:
            return PersonalInformation(**data)
        except TypeError as te:
            raise TypeError(f"Invalid data for personal information: {te}") from te
        except AttributeError as ae:
            raise AttributeError(f"Missing required field in personal information: {ae}") from ae
        except Exception as e:
            raise Exception(f"Error processing personal information: {e}") from e
    
    def _process_education(self, data: list) -> List[EducationDetails]:
        try:
            return [EducationDetails(**edu) for edu in data]
        except TypeError as te:
            raise TypeError(f"Invalid data for education details: {te}") from te
        except AttributeError as ae:
            raise AttributeError(f"Missing required field in education details: {ae}") from ae
        except Exception as e:
            raise Exception(f"Error processing education details: {e}") from e
    
    def _process_experience(self, data: list) -> List[ExperienceDetails]:
        try:
            return [ExperienceDetails(**exp) for exp in data]
        except TypeError as te:
            raise TypeError(f"Invalid data for experience details: {te}") from te
        except AttributeError as ae:
            raise AttributeError(f"Missing required field in experience details: {ae}") from ae
        except Exception as e:
            raise Exception(f"Error processing experience details: {e}") from e
    
    def _process_projects(self, data: list) -> List[Project]:
        try:
            return [Project(**proj) for proj in data]
        except TypeError as te:
            raise TypeError(f"Invalid data for projects: {te}") from te
        except AttributeError as ae:
            raise AttributeError(f"Missing required field in projects: {ae}") from ae
        except Exception as e:
            raise Exception(f"Error processing projects: {e}") from e
    
    def _process_achievements(self, data: list) -> List[Achievement]:
        try:
            return [Achievement(**ach) for ach in data]
        except TypeError as te:
            raise TypeError(f"Invalid data for achievements: {te}") from te
        except AttributeError as ae:
            raise AttributeError(f"Missing required field in achievements: {ae}") from ae
        except Exception as e:
            raise Exception(f"Error processing achievements: {e}") from e
    
    def _process_certifications(self, data: list) -> List[Certification]:
        try:
            return [Certification(**cert) for cert in data]
        except TypeError as te:
            raise TypeError(f"Invalid data for certifications: {te}") from te
        except AttributeError as ae:
            raise AttributeError(f"Missing required field in certifications: {ae}") from ae
        except Exception as e:
            raise Exception(f"Error processing certifications: {e}") from e
    
    def _process_languages(self, data: list) -> List[Language]:
        try:
            return [Language(**lang) for lang in data]
        except TypeError as te:
            raise TypeError(f"Invalid data for languages: {te}") from te
        except AttributeError as ae:
            raise AttributeError(f"Missing required field in languages: {ae}") from ae
        except Exception as e:
            raise Exception(f"Error processing languages: {e}") from e
    
    def _process_skills(self, data: dict) -> Skill:
        try:
            return Skill(__root__=data)
        except TypeError as te:
            raise TypeError(f"Invalid data for skills: {te}") from te
        except AttributeError as ae:
            raise AttributeError(f"Missing required field in skills: {ae}") from ae
        except Exception as e:
            raise Exception(f"Error processing skills: {e}") from e