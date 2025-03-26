import os
import pdfplumber
import pandas as pd
import zipfile

def extrair_tabela_PDF(pdf_path):
    data = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            tables = page.extract_table()
            if tables:
                data.extend(tables)
    df = pd.DataFrame(data)
    # Substituir abreviações OD e AMB
    df.replace({"OD": "Odontológico", "AMB": "Ambulatorial"}, inplace=True)
    csv_path = "Rol_de_Procedimentos.csv"
    df.to_csv(csv_path, index=False, encoding="utf-8")
    return csv_path

def zip_csv(csv_file, zip_name="Teste_seu_nome.zip"):
    with zipfile.ZipFile(zip_name, "w", zipfile.ZIP_DEFLATED) as zipf:
        zipf.write(csv_file, os.path.basename(csv_file))
    print(f"Arquivo CSV compactado em {zip_name}")

if __name__ == "__main__":
    pdf_path = "downloads/Anexo_I.pdf"  # Ajuste para o caminho correto
    csv_file = extrair_tabela_PDF(pdf_path)
    zip_csv(csv_file)