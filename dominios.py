import streamlit as st
import pandas as pd
import whois
from datetime import datetime

def check_domain(domain):
    try:
        domain_info = whois.whois(domain)
        # Se a data de expiração é None, o domínio pode estar disponível
        # ou um erro ocorreu. Verificamos também se a data de expiração é passada.
        if domain_info.expiration_date is None:
            return True
        if isinstance(domain_info.expiration_date, list):
            # Se for uma lista, pegamos a primeira data
            return datetime.now() > domain_info.expiration_date[0]
        else:
            return datetime.now() > domain_info.expiration_date
    except Exception as e:
        # Erro ao buscar o domínio, pode ser considerado como disponível para registro
        return True

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
