import pandas as pd

print("Iniciando o processo de ETL...")

# ==========================================
# 1. EXTRAÇÃO (Carregar os dados brutos)
# ==========================================
df_pedidos = pd.read_csv("data/olist_orders_dataset.csv")
df_itens = pd.read_csv("data/olist_order_items_dataset.csv")
df_produtos = pd.read_csv("data/olist_products_dataset.csv")

# ==========================================
# 2. TRANSFORMAÇÃO (Limpar e Juntar)
# ==========================================

# Passo A: Filtrar apenas pedidos que foram efetivamente entregues
# (Evita que pedidos cancelados distorçam o faturamento real)
df_pedidos_entregues = df_pedidos[df_pedidos['order_status'] == 'delivered'].copy()

# Passo B: Juntar Pedidos com os Itens (Preço e Frete)
df_consolidado = pd.merge(df_pedidos_entregues, df_itens, on="order_id", how="inner")

# Passo C: Juntar com as informações dos Produtos (Categorias)
df_final = pd.merge(df_consolidado, df_produtos, on="product_id", how="left")

# Passo D: Tratar as datas (Transformar texto em formato de data real)
df_final['order_purchase_timestamp'] = pd.to_datetime(df_final['order_purchase_timestamp'])

# Passo E: Criar uma coluna de Ano-Mês (Facilita o gráfico de evolução temporal no Streamlit)
df_final['ano_mes'] = df_final['order_purchase_timestamp'].dt.strftime('%Y-%m')

# ==========================================
# 3. CARGA (Salvar o resultado final)
# ==========================================
# Salva a base perfeitamente tratada em um novo arquivo dentro da pasta data
df_final.to_csv("data/ecommerce_consolidado.csv", index=False)

print("\n=== PROCESSO CONCLUÍDO COM SUCESSO! ===")
print(f"Total de linhas processadas: {df_final.shape[0]}")
print("O arquivo 'data/ecommerce_consolidado.csv' foi gerado e está pronto para o Dashboard.")