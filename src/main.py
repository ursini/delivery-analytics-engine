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

performance_entregador = (
    df[df["status"] == "Entregue"]
    .groupby("entregador")
    .agg(
        entregas_completadas=("id_pedido", "count"),
        tempo_medio=("tempo_entrega_min", "mean"),
        rating_medio=("rating", "mean"),
        faturamento=("preco_pedido", "sum")
    )
    .round(2)
    .sort_values("rating_medio", ascending=False)
)

qualidade_restaurante = (
    df.groupby("restaurante")
    .agg(
        pedidos_total=("id_pedido", "count"),
        rating_medio=("rating", "mean"),
        pedidos_5_estrelas=("rating", lambda x: (x == 5).sum()),
        pedidos_1_estrela=("rating", lambda x: (x == 1).sum()),
        preco_medio=("preco_pedido", "mean")
    )
    .round(2)
    .sort_values("rating_medio", ascending=False)
)

pedidos_por_hora = (
    df.groupby("hora_pedido")
    .agg(
        quantidade=("id_pedido", "count"),
        faturamento=("preco_pedido", "sum"),
        tempo_medio=("tempo_entrega_min", "mean")
    )
    .reset_index()
)

status_resumo = (
    df["status"]
    .value_counts()
    .to_frame(name="quantidade")
    .reset_index()
    .rename(columns={"index": "status"})
)

pedidos_ruim = (
    df[df["rating"] <= 2]
    .groupby(["restaurante", "status"])
    .agg(
        quantidade=("id_pedido", "count"),
        preco_medio=("preco_pedido", "mean")
    )
    .reset_index()
)

df_numericos = df[["preco_pedido", "tempo_entrega_min", "rating", "tamanho_comentario"]].corr()

df["velocidade"] = pd.cut(
    df["tempo_entrega_min"],
    bins=[0, 30, 60, 90],
    labels=["Rápido", "Normal", "Lento"]
)

velocidade_rating = (
    df.groupby("velocidade")
    .agg(
        pedidos=("id_pedido", "count"),
        rating_medio=("rating", "mean"),
        preco_medio=("preco_pedido", "mean")
    )
    .round(2)
)