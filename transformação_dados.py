import pdfplumber
import pandas as pd
import zipfile

def extrair_tabela_pdf(pdf_path):
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

