from generate_data import gerar_dados
from transform import executar_transformacoes


def imprimir_relatorio(resultados):

    df_cadastro = resultados["cadastro_fundos"]
    df_mercado = resultados["mercado"]
    df_pipeline = resultados["pipeline"]
    velas_15m = resultados["velas_15m"]

    alertas = resultados["alertas_institucionais"]

    fraudes = resultados["fraudes_rede"]
    limite_anomalia = resultados["limite_anomalia"]

    portfolios = resultados["relatorio_portfolios"]
    matriz_corr = resultados["matriz_corr"]

    print("=" * 90)
    print(
        "INICIALIZANDO FRAMEWORK AVANÇADO "
        "DE DATA ENGINEERING"
    )
    print("=" * 90)

    print(
        "\n"
        + "📊 " * 3
        + "1. FORMATO RELACIONAL DE CADASTROS "
        + "(PD.MELT + CATEGORICAL)"
        + " 📊" * 3
    )

    print(
        df_cadastro
        .head(5)
        .to_string(index=False)
    )

    print(
        "\n"
        + "📈 " * 3
        + "2. HISTÓRICO DE MERCADO "
        + "COM MÉTRICAS MÓVEIS"
        + " 📈" * 3
    )

    print(
        df_mercado
        .dropna()
        .query("ticker == 'BTC'")
        .head(4)
        .to_string(index=False)
    )

    print(
        "\n"
        + "⚡ " * 3
        + "3. SESSÕES COMBINADAS "
        + "POR TIME-MATCHING"
        + " ⚡" * 3
    )

    print(
        df_pipeline[
            [
                "timestamp",
                "ticker",
                "direcao",
                "preco_spot",
                "volume_financeiro_usd"
            ]
        ]
        .head(5)
        .to_string(index=False)
    )

    print(
        "\n"
        + "🕯️ " * 3
        + "4. VELAS DE MERCADO "
        + "(.RESAMPLE + OHLC)"
        + " 🕯️" * 3
    )

    print(
        velas_15m
        .query("ticker == 'BTC'")
        .head(4)
        .to_string(index=False)
    )

    print(
        "\n"
        + "🐳 " * 3
        + "5. OPERAÇÕES INSTITUCIONAIS"
        + " 🐳" * 3
    )

    if not alertas.empty:

        print(
            alertas[
                [
                    "id_ordem",
                    "id_usuario",
                    "ticker",
                    "volume_financeiro_usd"
                ]
            ]
            .head(4)
            .to_string(index=False)
        )

    else:

        print(
            "Nenhuma transação institucional "
            "mapeada no intervalo atual."
        )

    print(
        "\n"
        + "💎 " * 3
        + "6. CONSOLIDADO DE PORTFÓLIO"
        + " 🛡️" * 3
    )

    print(
        portfolios
        .head(6)
        .to_string(index=False)
    )

    print(
        "\n"
        + "🚨 " * 3
        + "7. FORENSICS: EXECUÇÕES ANÔMALAS"
        + " 🚨" * 3
    )

    print(
        f"Linha de corte para volumes fora "
        f"da normalidade: ${limite_anomalia:,.2f}"
    )

    print(
        "Volume total de ordens classificadas "
        f"como anomalias severas: {len(fraudes)}"
    )

    print(
        "\n"
        + "🔢 " * 3
        + "8. MATRIZ DE CORRELAÇÃO"
        + " 🔢" * 3
    )

    print(
        matriz_corr
        .round(4)
    )

    print("\n" + "=" * 90)

    print(
        f"Pipeline concluído. "
        f"{len(df_pipeline)} ordens processadas "
        "e cruzadas com telemetria."
    )

    print("=" * 90)


def executar_relatorio():

    (
        df_fundos,
        df_mercado,
        df_ordens
    ) = gerar_dados()

    resultados = executar_transformacoes(
        df_fundos,
        df_mercado,
        df_ordens
    )

    imprimir_relatorio(resultados)


if __name__ == "__main__":
    executar_relatorio()