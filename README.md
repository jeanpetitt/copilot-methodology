# Copilot: Research Methodology
This project aims to assist researchers in scientific writing by helping them draft the methodology section of their articles. The methodology is generated based on inputs provided by the researcher, such as the research question, research domain, and annotations (e.g., tools, methods, research type, etc.).

By leveraging the power of advanced LLMs like GPT-4 and Mistral, our goal is to develop an intelligent assistant to support researchers in this process.

## Process
This image present How our process is done.
<img src="assets/process.png">


## Run Project locally on your computer device

### Dependancies
to install all dependacies for the project run this command:
```sh
pip install -r requirements.txt

```

### Arguments
The project required the following arguments: <br>
* research_domain: if domain is not provided, it will be automatically generate based on research question
* reseach_question
* annotations: additional: information that help to generate the structure of methodology

annotions  is look like this:
```
"annotations": {
    "research_type": "quantitative",
    "method": "few-shot, zero-shot prompting and finetuning",
    "participant": "experimentions",
    "tools": ["Experimention", {"metrics": "precision, Recall and F1-score", "datasets": "superSemtab2024"}]
}
```

### Run Project
If you want to run the project locally and to see the output pdf file generate, please assure you that you have pdflatex install in you computer, if this is not the case please follow these instruction: <br>

On MacOs device:
```sh
brew install mactex
```
On Ubuntu/Debian device:
```sh
sudo apt update
sudo apt install texlive-latex-base texlive-latex-extra texlive-fonts-recommended

```

If you are using Windows as OS, please search on how to install MilTex in your device.<br>

Once this is done, run this command in the root of your project

```sh
python main.py
```

### Output
At the end of, you will see a pdf file generated a the root of the project and the latex code is locate in [store/latext](store/latex/)

