import os
import pdfplumber
import pandas as pd
import zipfile

def encontrar_PDF_anexo():
    """Busca pelo arquivo Anexo I na pasta downloads."""
    pasta_downloads = "downloads"
    for arquivo in os.listdir(pasta_downloads):
        if "anexo_i" in arquivo.lower():
            return os.path.join(pasta_downloads, arquivo)
    print("Arquivo do Anexo I não encontrado!")
    return None

def extrair_tabela_PDF(pdf_path):
    data = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            tables = page.extract_tables()
            for table in tables:
                for row in table:
                    if any(row):
                        data.append(row)
    if not data:
        print("Nenhuma tabela foi extraída!")
        return None
    df = pd.DataFrame(data)
    df.columns = df.iloc[0]
    df = df[1:].reset_index(drop=True)
    if "OD" in df.columns:
        df["OD"] = df["OD"].replace({"OD": "Odontológico"})
    if "AMB" in df.columns:
        df["AMB"] = df["AMB"].replace({"AMB": "Ambulatorial"})
    csv_path = "Rol_de_Procedimentos.csv"
    df.to_csv(csv_path, index=False, encoding="utf-8")
    print("Extraindo dados das tabelas...")
    return csv_path

def zip_csv(csv_file, zip_name="Teste_Kayky.zip"):
    with zipfile.ZipFile(zip_name, "w", zipfile.ZIP_DEFLATED) as zipf:
        zipf.write(csv_file, os.path.basename(csv_file))
    print(f"Arquivo CSV compactado em {zip_name}")

if __name__ == "__main__":
    pdf_path = encontrar_PDF_anexo()
    if pdf_path:
        csv_file = extrair_tabela_PDF(pdf_path)
        if csv_file:
            zip_csv(csv_file)
