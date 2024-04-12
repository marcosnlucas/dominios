import streamlit as st
import pandas as pd
import whois
from datetime import datetime

def check_domain(domain):
    try:
        domain_info = whois.whois(domain)
        # Imprimir a resposta inteira para depuração
        st.write(f"WHOIS para {domain}: {domain_info}")

        # Converter a resposta inteira em uma string e para minúsculas para facilitar a busca
        response_text = str(domain_info).lower()

        # Verifica se há mensagens específicas que indicam que o domínio está disponível
        if "no match for" in response_text or "not found" in response_text or "no data found" in response_text:
            return True  # Domínio disponível se essas strings forem encontradas

        # Verificar também campos comuns de status e data de expiração
        if domain_info.status is None and domain_info.expiration_date is None:
            return True  # Domínio possivelmente disponível se não houver status ou data de expiração

        return False
    except Exception as e:
        st.error(f"Erro ao verificar o domínio {domain}: {e}")
        return False


def check_domains(df):
    available_domains = []
    for index, row in df.iterrows():
        domain_com = f"{row['Domain']}.com"
        domain_com_br = f"{row['Domain']}.com.br"
        if check_domain(domain_com):
            available_domains.append(domain_com)
        if check_domain(domain_com_br):
            available_domains.append(domain_com_br)
    return available_domains

st.title("Verificador de Disponibilidade de Domínios")

uploaded_file = st.file_uploader("Escolha um arquivo CSV com os domínios para verificar", type="csv")
if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)
    if "Domain" not in data.columns:
        st.error("O arquivo CSV deve ter uma coluna chamada 'Domain'")
    else:
        available_domains = check_domains(data)
        st.write("Domínios disponíveis:")
        st.write(available_domains)
