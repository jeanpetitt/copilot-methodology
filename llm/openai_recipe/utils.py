from openai import OpenAI
from dotenv import load_dotenv
from llm.models.utils import Model, MODEL_MAP, ResponseResearchQuestion, ResponseResearchDomain, ResponseMethodologySection
import openai
import os
import json


environments = os.environ

def get_client_openai(api_key: str = None): 
    if not api_key:
        load_dotenv()
        api_key = environments["OPENAI_API_KEY"] if "OPENAI_API_KEY" in environments else  ValueError("OPENAI_API_KEY is not set. please provide it, you can use an .env file.")
    client = OpenAI(api_key=api_key)
    
    return client


client = get_client_openai()


def determine_research_question(user_prompt: str, model: Model):
    completion = client.beta.chat.completions.parse(
        model=MODEL_MAP[model],
        messages=[
            {
            "role": "system",
            "content": "You are an expert in classifying research questions. "
                       "Respond with a JSON object containing the key 'research_question'."
            },
            {
                "role": "user",
                "content": f"Determine the research question for this query: {user_prompt}"
            }
        ],
        response_format=ResponseResearchQuestion
    )
    return completion.choices[0].message.parsed


def determine_research_domain(user_prompt: str, model: Model):
    completion = client.beta.chat.completions.parse(
        model=MODEL_MAP[model],
        messages=[
            {
            "role": "system",
            "content": "You are an expert in classifying research domains. "
                       "Respond with a JSON object containing the key 'research_domains'."
            },
            {
                "role": "user",
                "content": f"Determine the research domain for this query: {user_prompt}"
            }
        ],
        response_format=ResponseResearchDomain
    )
    return completion.choices[0].message.parsed

def generate_methodology_section(structure_data: str, model: Model):
    completion = client.beta.chat.completions.parse(
        model=MODEL_MAP[model],
        messages=[
            {
            "role": "system",
            "content": "You are a research assistant expert in scientific writting "
                       "Respond with a JSON object containing the key 'methodology_section'. The response  should be write in Latex."
                       "Based on the structured methodology below, generate a detailed methodology section."
            },
            {
                "role": "user",
                "content": "Structured Methodology:"
                            f"{json.dumps(structure_data, indent=2)}"
                            "Write a well-structured methodology section suitable for a good research paper."
            }
        ],
        response_format=ResponseMethodologySection
    )
    return completion.choices[0].message.parsed

# structured_data = {
#     "research_question": "How do AI models assist in research methodology generation?",
#     "domain": "Artificial Intelligence & HCI",
#     "research_type": "mixed",
#     "methods": "qualitative",
#     "participants": "Researchers and AI experts",
#     "tools": ["survey", "interview"],
#     "procedures": ["A survey was conducted among participants.", "Interviews were conducted to gather qualitative insights."]
# }

