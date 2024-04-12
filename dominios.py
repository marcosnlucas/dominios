import streamlit as st
import pandas as pd
import whois
from datetime import datetime

def check_domain(domain):
    try:
        domain_info = whois.whois(domain)
        # Usamos st.write para depuração visível na interface do usuário
        st.write(f"WHOIS para {domain}: {domain_info}")

        # Verifica se a resposta WHOIS indica que o domínio não está registrado
        if domain_info.status is None and domain_info.expiration_date is None:
            return True
        if isinstance(domain_info.status, list):
            if any("no match" in s.lower() or "available" in s.lower() for s in domain_info.status):
                return True
        elif domain_info.status:
            if "no match" in domain_info.status.lower() or "available" in domain_info.status.lower():
                return True
        if "no match for" in str(domain_info).lower():
            return True
        return False
    except Exception as e:
        st.write(f"Erro ao verificar o domínio {domain}: {e}")
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
