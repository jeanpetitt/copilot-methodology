import json
from typing import Set
from llm.openai_recipe.utils import determine_research_domain

RESEARCH_TYPES: Set[str] = {"qualitative", "quantitative", "mixed"}

class SymbolicModel:
    def __init__(self, research_question: str, domain: list[str], annotations: dict):
        if not research_question:
            raise ValueError("The research question is required.")
        
        if not annotations:
            raise ValueError("Annotations are required and must contain research_type, method, participant, and tools.")
        
        self.research_question = research_question
        if domain:
            self.domain = domain 
        else:
            self.domain = determine_research_domain(research_question, 'gpt4')
            self.domain = json.loads(self.domain.response)['research_domains']
        self.annotations = annotations
        self.structure = {}

        # Vérification que tous les éléments sont bien fournis check that all elements are well provided
        required_keys = {"research_type", "method", "participant", "tools"}
        missing_keys = required_keys - self.annotations.keys()
        if missing_keys:
            raise ValueError(f"Missing required annotation fields: {', '.join(missing_keys)}")

    def generate_structure(self):
        """Generate the structure of methodology based on annotations."""
        self.structure["research_question"] = self.research_question
        self.structure["domain"] = self.domain

        # Define type of research
        research_type = self.annotations["research_type"]
        if research_type in RESEARCH_TYPES:
            self.structure["research_type"] = research_type
        else:
            raise ValueError("Invalid research type. Must be one of: qualitative, quantitative, or mixed.")

        # Add method used
        self.structure["Methods"] = self._define_methods(research_type)

        # Add participants
        self.structure["Participants"] = self.annotations["participant"]

        # Add tools
        self.structure["Tools"] = self.annotations["tools"]

        # Define protocol and procedures
        self.structure["Procedures"] = self._define_procedures()

        return self.structure

    def _define_methods(self, research_type):
        """Description of used methods."""
        method_descriptions = {
            "qualitative": "This study employs qualitative methods such as interviews and thematic analysis.",
            "quantitative": "A quantitative approach is used, involving statistical analysis and hypothesis testing.",
            "mixed": "A mixed-methods approach is adopted, combining qualitative and quantitative techniques."
        }
        return method_descriptions.get(research_type, "Method not defined.")

    def _define_procedures(self):
        """Description of procedures based on tools and methods."""
        procedures = []
        tools = self.annotations["tools"]

        if "survey" in tools:
            procedures.append("A survey was conducted among participants.")
        if "experiment" in tools:
            procedures.append("An experiment was carried out in a controlled environment.")
        if "interview" in tools:
            procedures.append("Interviews were conducted to gather qualitative insights.")

        return procedures if procedures else "No specific procedure defined."

    def determine_research_domain(self, research_question: str) -> str:
        """Infer the research domain from the research question."""
        if "AI" in research_question or "artificial intelligence" in research_question.lower():
            return "Artificial Intelligence"
        elif "HCI" in research_question or "human-computer interaction" in research_question.lower():
            return "Human-Computer Interaction"
        else:
            return "General Research"

# Example of use case
data = {
    "research_question": "How do AI models assist in research methodology generation?",
    "domain": "",  # Domain is missing; it will be inferred
    "annotations": {
        "research_type": "mixed",
        "method": "qualitative",
        "participant": "Researchers and AI experts",
        "tools": ["survey", "interview"]
    }
}

model = SymbolicModel(data["research_question"], data["domain"], data["annotations"])
structure = model.generate_structure()
print(structure)
