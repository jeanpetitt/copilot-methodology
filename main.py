from symbolic.helpers import SymbolicModel
from llm.openai_recipe.utils import generate_methodology_section
from store.utils import LaTeXGenerator

data = {
    "research_question": "How Levrage GPT Model for semantic table annotation",
    "domain": "",  # Domain is missing; it will be inferred
    "annotations": {
        "research_type": "quantitative",
        "method": [{"prompting_techniques": ["few-shot", "zero-shot"]}, "finetuning GPT-3"],
        "participant": "experimentions",
        "tools": ["Experimention", {
            "metrics": "precision, Recall and F1-score", 
            "datasets": "superSemtab2024", 
            "task": ["CEA", "CTA", "CPA", "RA(Raw Annotation)", "TD(Table Topic Detection)"]
        }
        ]
    }
}

model = SymbolicModel(data["research_question"], data["domain"], data["annotations"])
structure_data = model.generate_structure()
print(structure_data)
latex_gen = LaTeXGenerator('store/latex/methodology.tex')

methodology_generate_text = generate_methodology_section(structure_data, 'gpt4')
latex_gen.save_to_latex(methodology_generate_text.response)
print("===Latex successful build=============")
latex_gen.compile_to_pdf()

# print(methodology_generate_text.response)