import os
import pandas as pd

# Diretórios dos dados
dados_contabeis_dir = "dados_contabeis"
dados_operadoras_dir = "dados_operadoras"

# Função para carregar e consolidar os dados contábeis
def carregar_dados_contabeis():
    df_list = []
    for arquivo in os.listdir(dados_contabeis_dir):
        if arquivo.endswith(".csv"):
            print(f"📂 Carregando: {arquivo}")
            try:
                df = pd.read_csv(
                    os.path.join(dados_contabeis_dir, arquivo),
                    delimiter=";",
                    encoding="latin1",
                    on_bad_lines="skip",
                    dtype=str
                )
                df_list.append(df)
            except Exception as e:
                print(f"❌ Erro ao carregar {arquivo}: {e}")
    return pd.concat(df_list, ignore_index=True) if df_list else pd.DataFrame()

# Função para carregar os dados das operadoras
def carregar_dados_operadoras():
    for arquivo in os.listdir(dados_operadoras_dir):
        if arquivo.endswith(".csv"):
            try:
                df = pd.read_csv(
                    os.path.join(dados_operadoras_dir, arquivo),
                    delimiter=";",
                    encoding="latin1",
                    on_bad_lines="skip",
                    dtype=str
                )
                return df
            except Exception as e:
                print(f"❌ Erro ao carregar {arquivo}: {e}")
    return pd.DataFrame()

# Filtrar apenas as despesas médicas relevantes
def filtrar_despesas(df):
    filtro = "EVENTOS/SINISTROS CONHECIDOS"
    df_filtrado = df[df["DESCRICAO"].str.contains(filtro, case=False, na=False)].copy()  # Adicionando .copy() aqui!
    return df_filtrado

# Processar dados e salvar CSV
def preparar_e_salvar_dados():
    df_contabeis = carregar_dados_contabeis()
    df_operadoras = carregar_dados_operadoras()
    print("🔍 Visualizando amostra de descrições disponíveis:")
    print(df_contabeis["DESCRICAO"].dropna().unique()[:10])  # Exibir as 10 primeiras descrições únicas
    df_despesas = filtrar_despesas(df_contabeis)
    if df_despesas.empty:
        print("❌ Nenhum dado relevante encontrado após o filtro.")
        return
    # Verificar e converter DATA
    if "DATA" in df_despesas.columns:
        df_despesas["DATA"] = pd.to_datetime(df_despesas["DATA"], errors="coerce", dayfirst=True)
        df_despesas = df_despesas.dropna(subset=["DATA"])
        df_despesas["Ano"] = df_despesas["DATA"].dt.year
        df_despesas["Trimestre"] = df_despesas["DATA"].dt.quarter
    # Converter valores financeiros
    if "VL_SALDO_FINAL" in df_despesas.columns:
        df_despesas["VL_SALDO_FINAL"] = (
            df_despesas["VL_SALDO_FINAL"].astype(str)
            .str.replace(",", ".")
            .str.replace(r"[^\d.]", "", regex=True)
        )
        df_despesas["VL_SALDO_FINAL"] = pd.to_numeric(df_despesas["VL_SALDO_FINAL"], errors="coerce")
    # Salvar CSV processado
    caminho_saida = "dados_tratados.csv"
    df_despesas.to_csv(caminho_saida, index=False, encoding="utf-8", sep=";")
    print(f"✅ Dados processados e salvos em {caminho_saida}")
    # Verificar conteúdo salvo
    df_lido = pd.read_csv(caminho_saida, delimiter=";", encoding="utf-8")
    print(df_lido.head())

# Executar processamento
if __name__ == "__main__":
    preparar_e_salvar_dados()
