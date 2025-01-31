import json
import subprocess

class LaTeXGenerator:
    def __init__(self, filename="methodology.tex"):
        self.filename = filename

    def save_to_latex(self, methodology_text):
        """Save methodology text to a LaTeX file."""
        latex_template = f"""\\documentclass{{article}}
\\usepackage{{geometry}}
\\geometry{{a4paper, margin=1in}}

\\title{{Research Methodology}}
\\author{{Copilot}}
\\date{{\\today}}

\\begin{{document}}
\\maketitle

{methodology_text}

\\end{{document}}
"""

        with open(self.filename, "w", encoding="utf-8") as f:
            f.write(latex_template)
    
    # compile automatically into pdf
    def compile_to_pdf(self):
        """Compile the LaTeX file to a PDF using pdflatex."""
        try:
            subprocess.run(["pdflatex", self.filename], check=True)
            print("PDF successfully generated!")
        except Exception as e:
            print(f"Error during PDF generation: {e}")