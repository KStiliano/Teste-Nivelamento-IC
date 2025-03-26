import os
import requests
import zipfile
from bs4 import BeautifulSoup

def download_PDFs():
    url = "https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos"
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    pdf_links = []
    # Encontrar links para os anexos I e II
    for link in soup.find_all("a", href=True):
        href = link["href"]
        if "anexo-i" in href.lower() or "anexo-ii" in href.lower():
            if href.startswith("/"):
                href = "https://www.gov.br" + href
            pdf_links.append(href)
