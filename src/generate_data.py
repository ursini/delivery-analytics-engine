import numpy as np
import pandas as pd


def gerar_dados_fundos():
    np.random.seed(42)

    dados_fundos_pivotados = pd.DataFrame({
        "id_usuario": range(1001, 1051),
        "faturamento_2023": np.random.uniform(50000, 200000, 50).round(2),
        "faturamento_2024": np.random.uniform(70000, 350000, 50).round(2),
        "faturamento_2025": np.random.uniform(100000, 500000, 50).round(2),
        "perfil_risco": np.random.choice(
            ["CONSERVADOR", "MODERADO", "AGRESSIVO"],
            50
        )
    })

    return dados_fundos_pivotados


def gerar_dados_mercado():
    np.random.seed(42)

    timestamps_mercado = pd.date_range(
        "2026-01-01 09:00:00",
        periods=2000,
        freq="30s"
    )

    ativos = [
        ("BTC", 65000),
        ("ETH", 3500),
        ("SOL", 150)
    ]

    lista_mercado = []

    for ticker, preco_base in ativos:

        retornos_aleatorios = np.random.normal(
            0.00002,
            0.0015,
            2000
        )

        precos_calculados = (
            preco_base *
            (1 + retornos_aleatorios).cumprod()
        )

        df_ativo = pd.DataFrame({
            "timestamp": timestamps_mercado,
            "ticker": ticker,
            "preco_spot": precos_calculados.round(2)
        })

        lista_mercado.append(df_ativo)

    df_mercado_master = (
        pd.concat(lista_mercado)
        .sort_values(["timestamp", "ticker"])
        .reset_index(drop=True)
    )

    return df_mercado_master


def gerar_dados_ordens(timestamps_mercado):
    np.random.seed(42)

    timestamps_ordens = (
        np.random.choice(timestamps_mercado, 8000)
        + pd.to_timedelta(
            np.random.randint(1, 29, 8000),
            unit="s"
        )
    )

    df_ordens_brutas = pd.DataFrame({
        "id_ordem": range(1, 8001),
        "id_usuario": np.random.randint(1001, 1051, 8000),
        "timestamp": pd.to_datetime(timestamps_ordens),
        "ticker": np.random.choice(
            ["BTC", "ETH", "SOL"],
            8000
        ),
        "quantidade_tokens": np.random.uniform(
            0.05,
            3.0,
            8000
        ).round(4),
        "direcao": np.random.choice(
            ["BUY", "SELL"],
            8000
        ),
        "status": np.random.choice(
            ["FILLED", "REJECTED", "PARTIAL"],
            8000,
            p=[0.90, 0.06, 0.04]
        )
    })

    df_ordens_brutas = (
        df_ordens_brutas
        .sort_values("timestamp")
        .drop_duplicates(subset=["id_ordem"])
        .reset_index(drop=True)
    )

    return df_ordens_brutas


def gerar_dados():
    df_fundos = gerar_dados_fundos()

    timestamps_mercado = pd.date_range(
        "2026-01-01 09:00:00",
        periods=2000,
        freq="30s"
    )

    df_mercado = gerar_dados_mercado()

    df_ordens = gerar_dados_ordens(
        timestamps_mercado
    )

    return (
        df_fundos,
        df_mercado,
        df_ordens
    )