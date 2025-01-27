# import arxiv
import json
from arxiv import Client
import re
import arxiv
import spacy
import os
import requests
from PyPDF2 import PdfReader

def search_arxiv_articles(query, max_results=5):
    """
    Search articles on arxiv for a given query
    """
    search = arxiv.Search(
        query=query,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.SubmittedDate
    )
    client = Client()
    results = client.results(search=search)
    articles = []
    for result in results:
        articles.append({
            "title": result.title,
            "summary": result.summary,
            "pdf_url": result.pdf_url,
            "categories": result.categories
        })
    return articles

def download_pdf(url, save_dir="downloads"):
    """
    Download PDF file from a URL
    """
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    
    response = requests.get(url)
    if response.status_code == 200:
        filename = url.split("/")[-1] + ".pdf"
        filepath = os.path.join(save_dir, filename)
        with open(filepath, "wb") as f:
            f.write(response.content)
        return filepath
    else:
        raise Exception(f"Échec du téléchargement : {response.status_code}")

def extract_text_from_pdf(pdf_path):
    """
    Extract the row text of a PDF file
    """
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

def extract_methodology_section(text):
    """
    Identifie and extrac methodology section of article
    """
    patterns = [
        r"(methodology|methods|materials and methods)([\s\S]*?)(results|discussion|conclusion|references)",
        r"(méthodologie|méthodes)([\s\S]*?)(résultats|discussion|conclusion|références)"
    ]
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(0)
    return "Section 'Methodology' not found."

def save_to_jsonl(data, file_path):
    """
    Save data in JSONL format.
    """
    with open(file_path, "w", encoding="utf-8") as f:
        for entry in data:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
def get_research_domain(categories):
    """
    tranform arxiv categories into lisble research domain.
    """
    domain_mapping = {
        "cs": "Computer Science",
        "math": "Mathematics",
        "stat": "Statistics",
        "physics": "Physics",
        "bio": "Biology",
        "econ": "Economics",
        "q-fin": "Quantitative Finance"
    }
    primary_category = categories[0] if categories else "unknown"
    main_domain = primary_category.split(".")[0]
    return domain_mapping.get(main_domain, "Other")

def annotate_methodology_section(section_text):
    """
    Analyse and annote methodology section with spacy
    """
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(section_text)

    # Example of annotation
    annotations = {
        "mentions_quantitative": bool(re.search(r"(survey|experiment|quantitative)", section_text, re.IGNORECASE)),
        "mentions_qualitative": bool(re.search(r"(interviews|focus group|qualitative)", section_text, re.IGNORECASE)),
        "mentions_participants": [ent.text for ent in doc.ents if ent.label_ in ["CARDINAL", "PERSON"]],
        "methods_used": [ent.text for ent in doc.ents if ent.label_ == "WORK_OF_ART"]
    }

    return annotations


# Main step
query = "methodology in computer science"
max_results = 5
output_file = "downloads/json/methodology_dataset.jsonl" 
if not os.path.exists(output_file): os.makedirs(output_file)

articles = search_arxiv_articles(query, max_results=max_results)
dataset = []

for i, article in enumerate(articles):
    # print(f"Download of the article : {article['title']}")
    pdf_path = download_pdf(article["pdf_url"])
    full_text = extract_text_from_pdf(pdf_path)
    methodology_section = extract_methodology_section(full_text)
    annotations = annotate_methodology_section(methodology_section)
    research_domain = get_research_domain(article["categories"])
    
    dataset.append({
        "title": article["title"],
        "summary": article["summary"],
        "research_question": query,
        "research_domain": research_domain,
        "methodology_section": methodology_section if methodology_section else "Section 'Methodology' not found.",
        "annotation": annotations
    })
    
    print(f"Article {i}: {article["title"]}")
    
save_to_jsonl(dataset, output_file)
print(f"\n Data store in thee file : {output_file}")

