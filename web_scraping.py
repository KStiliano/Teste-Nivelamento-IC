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
    if not pdf_links:
        print("Nenhum PDF encontrado!")
        return
    os.makedirs("downloads", exist_ok=True)
    pdf_files = []
    for pdf_url in pdf_links:
        pdf_name = pdf_url.split("/")[-1]
        pdf_path = os.path.join("downloads", pdf_name)
        pdf_files.append(pdf_path)
        print(f"Baixando {pdf_name}...")
        pdf_response = requests.get(pdf_url)
        pdf_response.raise_for_status()
        with open(pdf_path, "wb") as f:
            f.write(pdf_response.content)
    return pdf_files

def zip_PDFs(pdf_files, zip_name="anexos.zip"):
    with zipfile.ZipFile(zip_name, "w", zipfile.ZIP_DEFLATED) as zipf:
        for pdf in pdf_files:
            zipf.write(pdf, os.path.basename(pdf))
    print(f"Arquivos compactados em {zip_name}")

if __name__ == "__main__":
    pdf_files = download_PDFs()
    if pdf_files:
        zip_PDFs(pdf_files)