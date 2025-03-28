import pandas as pd
import os

# Caminhos dos diretórios
caminho_contabeis = "/content/dados_contabeis"
caminho_operadoras = "/content/dados_operadoras"

# 1. Carregar e consolidar os dados contabeis
def carregar_dados_contabeis():
    df_list = []
    for arquivo in os.listdir(caminho_contabeis):
        if arquivo.endswith(".csv"):
            print(f"\n📂 Carregando: {arquivo}")
            try:
                df = pd.read_csv(
                    os.path.join(caminho_contabeis, arquivo),
                    delimiter=";",
                    encoding="latin1",
                    on_bad_lines="skip",
                    dtype=str
                )
                df_list.append(df)
            except Exception as e:
                print(f"❌ Erro ao carregar {arquivo}: {e}")
    return pd.concat(df_list, ignore_index=True) if df_list else pd.DataFrame()

# 2. Carregar os dados das operadoras
def carregar_dados_operadoras():
    for arquivo in os.listdir(caminho_operadoras):
        if arquivo.endswith(".csv"):
            try:
                df = pd.read_csv(
                    os.path.join(caminho_operadoras, arquivo),
                    delimiter=";",
                    encoding="latin1",
                    on_bad_lines="skip",
                    dtype=str
                )
                return df
            except Exception as e:
                print(f"❌ Erro ao carregar {arquivo}: {e}")
    return pd.DataFrame()

# 3. Filtrar despesas médicas relevantes
def filtrar_despesas(df):
    filtro = "EVENTOS/SINISTROS CONHECIDOS"
    return df[df["DESCRICAO"].str.contains(filtro, case=False, na=False)]

# 4. Corrigir a conversão de DATA e extrair Ano e Trimestre corretamente
def preparar_dados(df):
    if "DATA" not in df.columns or df["DATA"].isnull().all():
        print("Erro: Coluna 'DATA' está ausente ou vazia.")
        return df
    df["DATA"] = pd.to_datetime(df["DATA"], errors="coerce", dayfirst=True, infer_datetime_format=True)
    if df["DATA"].isnull().all():
        print("❌ Erro: Nenhuma data válida encontrada após conversão.")
    else:
        print("✅ Datas convertidas corretamente!")
    df["Ano"] = df["DATA"].dt.year
    df["Trimestre"] = df["DATA"].dt.quarter
    if "VL_SALDO_FINAL" in df.columns:
        df["VL_SALDO_FINAL"] = (
            df["VL_SALDO_FINAL"]
            .astype(str)
            .str.replace(",", ".")
            .str.replace(r"[^\d.]", "", regex=True)
        )
        df["VL_SALDO_FINAL"] = pd.to_numeric(df["VL_SALDO_FINAL"], errors="coerce")
    else:
        print("❌ Erro: Coluna 'VL_SALDO_FINAL' não encontrada.")
    return df

# 5. Encontrar as 10 operadoras com maiores despesas no último trimestre
def top10_operadoras_trimestre(df, df_operadoras):
    ano_max = df["Ano"].max()
    trimestre_max = df[df["Ano"] == ano_max]["Trimestre"].max()
    df_filtrado = df[(df["Ano"] == ano_max) & (df["Trimestre"] == trimestre_max)]
    df_agrupado = df_filtrado.groupby("REG_ANS")["VL_SALDO_FINAL"].sum().nlargest(10)
    df_agrupado = df_agrupado.reset_index()
    df_agrupado = df_agrupado.merge(df_operadoras, left_on="REG_ANS", right_on="Registro_ANS", how="left")
    df_agrupado["Nome_Fantasia"].fillna("Desconhecida", inplace=True)
    print(f"\n🔹 Top 10 Operadoras - 4º Trimestre de {ano_max} 🔹")
    df_agrupado["VL_SALDO_FINAL"] = df_agrupado["VL_SALDO_FINAL"].apply(lambda x: f"{x:,.2f}")
    print(df_agrupado[["REG_ANS", "Nome_Fantasia", "VL_SALDO_FINAL"]])

# 6. Encontrar as 10 operadoras com maiores despesas no ano
def top10_operadoras_ano(df, df_operadoras):
    ano_max = df["Ano"].max()
    df_filtrado = df[df["Ano"] == ano_max]
    df_agrupado = df_filtrado.groupby("REG_ANS")["VL_SALDO_FINAL"].sum().nlargest(10)
    df_agrupado = df_agrupado.reset_index()
    df_agrupado = df_agrupado.merge(df_operadoras, left_on="REG_ANS", right_on="Registro_ANS", how="left")
    df_agrupado["Nome_Fantasia"].fillna("Desconhecida", inplace=True)
    print(f"\n🔹 Top 10 Operadoras - Ano {ano_max} 🔹")
    df_agrupado["VL_SALDO_FINAL"] = df_agrupado["VL_SALDO_FINAL"].apply(lambda x: f"{x:,.2f}")
    print(df_agrupado[["REG_ANS", "Nome_Fantasia", "VL_SALDO_FINAL"]])

# 7. Executar pipeline
df_contabeis = carregar_dados_contabeis()
df_operadoras = carregar_dados_operadoras()
df_despesas = filtrar_despesas(df_contabeis)

# Carregar o trimestre específico (4T2024)
df_trimestre = pd.read_csv("/content/dados_contabeis/4T2024.csv", delimiter=";", encoding="latin1", dtype=str)

# Garantir que a coluna 'DATA' está presente e processar
df_despesas = preparar_dados(df_trimestre)

top10_operadoras_trimestre(df_despesas, df_operadoras)
top10_operadoras_ano(df_despesas, df_operadoras)
