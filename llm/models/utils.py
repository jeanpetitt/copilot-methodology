from pydantic import BaseModel
from typing import Literal

Model = Literal['gpt4', 'gpt_finetuned', 'mistral', "gemini", "deepseek"]

MODEL_MAP = {
    'gpt4': "gpt-4o",
    "mistral": "",
    "gpt_finetuned": "ft:gpt-4o-2024-08-06:tib:tableqa:AuR8BGDB",
    "gemini": "",
}

ANNOTATION = Literal['method', 'tools', "type_research", "participant"]

class ResponseResearchDomain(BaseModel):
    response: str 
    
class ResponseResearchQuestion(BaseModel):
    response: str
    
class AnnotationResponse(BaseModel):
    annotation: ANNOTATION
    
class ResponseMethodologySection(BaseModel):
    response: str