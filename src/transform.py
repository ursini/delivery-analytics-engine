import pandas as pd


def transformar_cadastro_fundos(df_fundos):

    df_cadastro_fundos = pd.melt(
        df_fundos,
        id_vars=[
            "id_usuario",
            "perfil_risco"
        ],
        value_vars=[
            "faturamento_2023",
            "faturamento_2024",
            "faturamento_2025"
        ],
        var_name="ano_fiscal",
        value_name="capital_inicial"
    )

    df_cadastro_fundos["ano_fiscal"] = (
        df_cadastro_fundos["ano_fiscal"]
        .str.extract(r"(\d+)")
        .astype(int)
    )

    df_cadastro_fundos["perfil_risco"] = pd.Categorical(
        df_cadastro_fundos["perfil_risco"]
    )

    return df_cadastro_fundos


def calcular_metricas_mercado(df_mercado):

    df_mercado = df_mercado.copy()

    # Retorno percentual por ativo
    df_mercado["retorno_imediato"] = (
        df_mercado
        .groupby("ticker")["preco_spot"]
        .pct_change()
    )

    # Médias móveis
    df_mercado["media_movel_rapida"] = (
        df_mercado
        .groupby("ticker")["preco_spot"]
        .transform(
            lambda x: x.rolling(window=10).mean()
        )
    )

    df_mercado["media_movel_lenta"] = (
        df_mercado
        .groupby("ticker")["preco_spot"]
        .transform(
            lambda x: x.rolling(window=50).mean()
        )
    )

    # Volatilidade
    df_mercado["volatilidade_movel"] = (
        df_mercado
        .groupby("ticker")["preco_spot"]
        .transform(
            lambda x: x.rolling(window=20).std()
        )
    )

    # Máxima histórica por ativo
    df_mercado["max_historico_ativo"] = (
        df_mercado
        .groupby("ticker")["preco_spot"]
        .transform("max")
    )

    return df_mercado


def cruzar_ordens_com_mercado(
    df_ordens,
    df_mercado
):

    df_ordens = df_ordens.sort_values(
        ["timestamp", "ticker"]
    )

    df_mercado = df_mercado.sort_values(
        ["timestamp", "ticker"]
    )

    df_pipeline = pd.merge_asof(
        df_ordens,
        df_mercado,
        on="timestamp",
        by="ticker",
        direction="backward"
    )

    df_pipeline["volume_financeiro_usd"] = (
        df_pipeline["quantidade_tokens"]
        * df_pipeline["preco_spot"]
    ).round(2)

    return df_pipeline


def gerar_velas_15m(df_mercado):

    df_temp = df_mercado.copy()

    df_temp = df_temp.set_index("timestamp")

    velas_15m = (
        df_temp
        .groupby("ticker")["preco_spot"]
        .resample("15min")
        .ohlc()
        .reset_index()
    )

    return velas_15m


def detectar_alertas_institucionais(df_pipeline):

    alertas = df_pipeline.query(
        "volume_financeiro_usd >= 100000 "
        "and status == 'FILLED' "
        "and direcao == 'BUY'"
    )

    return alertas


def detectar_anomalias(df_pipeline):

    q1 = df_pipeline[
        "volume_financeiro_usd"
    ].quantile(0.25)

    q3 = df_pipeline[
        "volume_financeiro_usd"
    ].quantile(0.75)

    iqr = q3 - q1

    limite_anomalia = q3 + (3.0 * iqr)

    df_fraudes_rede = df_pipeline.query(
        "volume_financeiro_usd > @limite_anomalia"
    )

    return (
        df_fraudes_rede,
        limite_anomalia
    )


def gerar_relatorio_portfolios(df_pipeline):

    relatorio = (
        df_pipeline
        .query("status == 'FILLED'")
        .groupby([
            "id_usuario",
            "ticker"
        ])
        .agg(
            total_ordens=(
                "id_ordem",
                "count"
            ),

            tokens_acumulados=(
                "quantidade_tokens",
                "sum"
            ),

            capital_movimentado_usd=(
                "volume_financeiro_usd",
                "sum"
            ),

            preco_medio_execucao=(
                "preco_spot",
                "mean"
            ),

            compras_realizadas=(
                "direcao",
                lambda x: (x == "BUY").sum()
            ),

            retorno_maximo_pego=(
                "retorno_imediato",
                "max"
            )
        )
        .round(4)
        .reset_index()
        .sort_values(
            by="capital_movimentado_usd",
            ascending=False
        )
    )

    return relatorio


def gerar_matriz_correlacao(df_pipeline):

    colunas = [
        "quantidade_tokens",
        "preco_spot",
        "volume_financeiro_usd",
        "volatilidade_movel"
    ]

    return df_pipeline[colunas].corr()


def executar_transformacoes(
    df_fundos,
    df_mercado,
    df_ordens
):

    df_cadastro_fundos = transformar_cadastro_fundos(
        df_fundos
    )

    df_mercado = calcular_metricas_mercado(
        df_mercado
    )

    df_pipeline = cruzar_ordens_com_mercado(
        df_ordens,
        df_mercado
    )

    velas_15m = gerar_velas_15m(
        df_mercado
    )

    alertas_institucionais = (
        detectar_alertas_institucionais(
            df_pipeline
        )
    )

    df_fraudes_rede, limite_anomalia = (
        detectar_anomalias(df_pipeline)
    )

    relatorio_portfolios = (
        gerar_relatorio_portfolios(
            df_pipeline
        )
    )

    matriz_corr = gerar_matriz_correlacao(
        df_pipeline
    )

    return {
        "cadastro_fundos": df_cadastro_fundos,
        "mercado": df_mercado,
        "pipeline": df_pipeline,
        "velas_15m": velas_15m,
        "alertas_institucionais": alertas_institucionais,
        "fraudes_rede": df_fraudes_rede,
        "limite_anomalia": limite_anomalia,
        "relatorio_portfolios": relatorio_portfolios,
        "matriz_corr": matriz_corr
    }