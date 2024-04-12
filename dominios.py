import streamlit as st
import pandas as pd
import whois
from datetime import datetime
import time

import time
import whois
import streamlit as st

def check_domain(domain):
    max_attempts = 3
    for attempt in range(max_attempts):
        try:
            domain_info = whois.whois(domain)
            response_text = str(domain_info).lower()
            if "no match for" in response_text or "not found" in response_text or "no data found" in response_text:
                return True
            if domain_info.status is None and domain_info.expiration_date is None:
                return True
            return False
        except ConnectionResetError as e:
            st.error(f"Conexão reiniciada ao verificar {domain}: {e}")
            time.sleep(5)  # Esperar 5 segundos antes de tentar novamente
        except Exception as e:
            st.error(f"Erro ao verificar o domínio {domain}: {e}")
            return False
        finally:
            time.sleep(1)  # Pausa entre tentativas ou antes da próxima verificação
    return False  # Retorna falso se todas as tentativas falharem


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
