import pandas as pd
import numpy as np

np.random.seed(42)


pedidos = pd.DataFrame({
    "id_pedido": range(1, 501),
    "restaurante": np.random.choice(["Burgeria", "Pizzaria", "Sushi", "Tailandês", "Brasileiro"], 500),
    "preco_pedido": np.random.uniform(15, 150, 500).round(2),
    "tempo_entrega_min": np.random.randint(15, 90, 500),
    "rating": np.random.choice([1, 2, 3, 4, 5], 500),
    "data_pedido": pd.date_range("2024-01-01", periods=500, freq="h"),
    "entregador": np.random.choice(["João", "Maria", "Pedro", "Ana", "Carlos", "Sofia"], 500),
    "status": np.random.choice(["Entregue", "Cancelado", "Em trânsito", "Preparando"], 500)
})

reviews = pd.DataFrame({
    "id_pedido": np.random.choice(pedidos["id_pedido"], 350),
    "comentario": [f"Comentário_{i}" for i in range(350)],
    "palavras_chave": np.random.choice(["Delicioso", "Lindo", "Rápido", "Frio", "Pequeno", "Caro"], 350)
})

pedidos = pedidos.drop_duplicates(subset=["id_pedido"])
reviews["comentario"] = reviews["comentario"].fillna("Sem comentário")

df = pedidos.merge(reviews, on="id_pedido", how="left")

df["hora_pedido"] = df["data_pedido"].dt.hour
df["margem_tempo"] = df["tempo_entrega_min"] / 60

df["pedido_ok"] = df["status"].apply(
    lambda x: "Sim" if x == "Entregue" else "Não"
)

df["restaurante_lower"] = df["restaurante"].str.lower()
df["tamanho_comentario"] = df["comentario"].str.len()