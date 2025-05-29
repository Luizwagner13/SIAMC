import pdfplumber
import re
import pandas as pd
import os
import logging
import sys

logging.basicConfig(level=logging.ERROR)

def extrair_texto_pdf(caminho_pdf):
    with pdfplumber.open(caminho_pdf) as pdf:
        return ''.join(pagina.extract_text() for pagina in pdf.pages)

def extrair_informacoes(texto):
    numeros_os = re.findall(r'N[º°]? Ordem Serviço:\s*([A-Z0-9]+)', texto)
    codigos_servico = re.findall(r'Serviço SICOM:\s*([A-Z0-9]+)\s*-\s*(.+)', texto)
    enderecos = re.findall(r'Endereço Ordem Serviço:\s*(.+?)(?=Situação Ordem Serviço:|Cod\. Equipe:)', texto, re.DOTALL)
    datas_baixa = re.findall(r'Data de Baixa:\s*(\d{2}/\d{2}/\d{4})', texto)
    valores_os = re.findall(r'Valor Total:\s*R\$\s*([\d\.,]+)', texto)

    max_length = max(len(numeros_os), len(codigos_servico), len(enderecos), len(datas_baixa), len(valores_os))
    for lst in [numeros_os, codigos_servico, enderecos, datas_baixa, valores_os]:
        lst += [None] * (max_length - len(lst))

    codigos_completo, codigos_numericos = [], []
    for c in codigos_servico:
        if c and len(c) >= 2:
            codigos_completo.append(f"{c[0]} - {c[1]}")
            try:
                codigos_numericos.append(int(c[0]) if c[0].isdigit() else None)
            except ValueError:
                codigos_numericos.append(None)
        else:
            codigos_completo.append(None)
            codigos_numericos.append(None)

    ruas, numeros, bairros = [], [], []
    for endereco in enderecos:
        if endereco:
            partes = [p.strip() for p in endereco.split(",")]
        else:
            partes = []
        ruas.append(partes[0] if len(partes) > 0 else "")
        numeros.append(partes[1] if len(partes) > 1 else "")
        bairros.append(partes[2] if len(partes) > 2 else "")

    return pd.DataFrame({
        "Número da O.S.": numeros_os,
        "Código do Serviço": codigos_completo,
        "Código Numérico": codigos_numericos,
        "Rua": ruas,
        "Número": numeros,
        "Bairro": bairros,
        "Data de Baixa": datas_baixa,
        "Valor da O.S.": valores_os
    })

def processar_pdfs_da_pasta(pasta_pdf):
    arquivos_pdf = [f for f in os.listdir(pasta_pdf) if f.lower().endswith('.pdf')]
    todos_dados = []

    for nome_arquivo in arquivos_pdf:
        caminho_pdf = os.path.join(pasta_pdf, nome_arquivo)
        print(f"Processando: {nome_arquivo}")
        try:
            texto = extrair_texto_pdf(caminho_pdf)
            df = extrair_informacoes(texto)
            df["Arquivo"] = os.path.splitext(nome_arquivo)[0].upper()
            todos_dados.append(df)
        except Exception as e:
            print(f"❌ Erro ao processar {nome_arquivo}: {e}")

    if not todos_dados:
        print("Nenhum dado foi extraído.")
        return

    df_final = pd.concat(todos_dados, ignore_index=True)

    def corrigir_valor(valor):
        if valor:
            return float(valor.replace(".", "").replace(",", "."))
        return None

    def formatar_os(valor):
        if valor and valor.isdigit():
            try:
                return float(valor)
            except:
                return valor
        return valor

    df_final["Número da O.S."] = df_final["Número da O.S."].apply(formatar_os)
    df_final["Valor da O.S."] = df_final["Valor da O.S."].apply(corrigir_valor)

    df_final["Código Numérico"] = pd.to_numeric(df_final["Código Numérico"], errors='coerce')
    df_final = df_final[(df_final["Código Numérico"].isna()) | (df_final["Código Numérico"] >= 3000000)]
    df_final = df_final[~df_final["Código Numérico"].between(3020000, 3029999, inclusive='both')]
    df_final = df_final[~df_final["Código Numérico"].between(5050000, 5050300, inclusive='both')]
    df_final = df_final[~df_final["Código Numérico"].between(5050400, 5050499, inclusive='both')]
    df_final = df_final[~df_final["Código Numérico"].between(5050401, 5050409, inclusive='both')]
    df_final = df_final[df_final["Código Numérico"] != 5210100]

    df_final = df_final[~df_final["Código Numérico"].isin([5120200, 5040700])]

    codigos_alfanumericos_excluir = ["IRTVA", "MA001", "IRTRAA", "RDA001"]
    for codigo in codigos_alfanumericos_excluir:
        df_final = df_final[~df_final["Código do Serviço"].str.startswith(codigo, na=False)]

    filtro_5080400 = df_final["Código Numérico"] == 5080400
    texto_geral = (df_final["Rua"].fillna("") + " " + df_final["Bairro"].fillna("")).str.upper()
    manter = texto_geral.str.contains("INDUSTRIAL|BANDEIRANTES", na=False)
    remover = texto_geral.str.contains("GENERAL|FREDERICO", na=False)
    condicao_excluir = filtro_5080400 & (~manter | remover)
    df_final = df_final[~condicao_excluir]

    df_final.sort_values(by=["Número da O.S.", "Arquivo"], ascending=[True, True], inplace=True)
    df_final = df_final[~df_final.duplicated(subset="Número da O.S.", keep=False) | (df_final["Arquivo"] == "OSNP")]

    df_final.drop(columns=["Código Numérico"], inplace=True)
    colunas = ["Número da O.S.", "Código do Serviço", "Rua", "Número", "Bairro", "Data de Baixa", "Valor da O.S.", "Arquivo"]
    df_final = df_final[colunas]

    caminho_excel = os.path.join(pasta_pdf, "informacoes_extraidas.xlsx")
    df_final.to_excel(caminho_excel, index=False, sheet_name='Dados')

    print(f"\n✅ Planilha salva com sucesso em:\n{caminho_excel}")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("⚠️ Por favor, forneça o caminho da pasta como argumento.")
        sys.exit(1)
    pasta_pdf = sys.argv[1]
    processar_pdfs_da_pasta(pasta_pdf)
