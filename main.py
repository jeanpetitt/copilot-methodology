from symbolic.helpers import SymbolicModel
from llm.openai_recipe.utils import generate_methodology_section

data = {
    "research_question": "How Levrage GPT Model for semantic table annotation",
    "domain": "",  # Domain is missing; it will be inferred
    "annotations": {
        "research_type": "mixed",
        "method": "qualitative",
        "participant": "Researchers and AI experts",
        "tools": ["survey", "interview"]
    }
}

model = SymbolicModel(data["research_question"], data["domain"], data["annotations"])
structure_data = model.generate_structure()

response = generate_methodology_section(structure_data, 'gpt4')

print(response)