import streamlit as st
import pandas as pd
import os

# ==========================================
# 1. CONFIGURAÇÃO DA PÁGINA
# ==========================================
st.set_page_config(page_title="Dashboard E-commerce", layout="wide")

st.title("📊 Dashboard de Vendas - E-commerce Brasileiro")
st.write("Análise de faturamento, comportamento e desempenho de produtos (Base Olist).")

st.divider()

# ==========================================
# 2. CARREGAMENTO DOS DADOS (ETL CONCLUÍDO)
# ==========================================
# O @st.cache_data guarda os dados na memória para o dashboard não ficar lento

@st.cache_data
def carregar_dados():
    diretorio_atual = os.path.dirname(os.path.abspath(__file__))
    caminho_arquivo = os.path.join(diretorio_atual, "..", "data", "ecommerce_consolidado.csv")
    return pd.read_csv(caminho_arquivo)

df = carregar_dados()

# ==========================================
# 3. CÁLCULO DOS INDICADORES (KPIs)
# ==========================================
faturamento_total = df['price'].sum()
qtd_pedidos = df['order_id'].nunique()
ticket_medio = faturamento_total / qtd_pedidos

st.subheader("Indicadores Principais")
col1, col2, col3 = st.columns(3)

col1.metric("Faturamento Total", f"R$ {faturamento_total:,.2f}")
col2.metric("Pedidos Realizados", f"{qtd_pedidos:,}")
col3.metric("Ticket Médio", f"R$ {ticket_medio:,.2f}")

st.divider()

# ==========================================
# 4. GRÁFICOS (Visualizações)
# ==========================================

# Criamos duas colunas na tela para colocar um gráfico ao lado do outro
col_esq, col_dir = st.columns(2)

with col_esq:
    st.subheader("Top 10 Categorias Mais Vendidas")
    # Conta a quantidade de vezes que cada categoria aparece e pega as 10 maiores
    top_categorias = df['product_category_name'].value_counts().head(10)
    st.bar_chart(top_categorias)

with col_dir:
    st.subheader("Evolução do Faturamento no Tempo")
    # Agrupa os dados pela coluna 'ano_mes' (que criamos no ETL) e soma os preços
    evolucao_vendas = df.groupby('ano_mes')['price'].sum().reset_index()
    # Define a coluna 'ano_mes' como índice para o Streamlit entender que é o eixo X do gráfico
    evolucao_vendas.set_index('ano_mes', inplace=True)
    st.line_chart(evolucao_vendas)