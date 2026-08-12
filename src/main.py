from generate_data import gerar_dados
from transform import executar_transformacoes
from report import imprimir_relatorio


def main():
    # 1. Geração dos dados
    df_fundos, df_mercado, df_ordens = gerar_dados()

    # 2. Processamento e transformação
    resultados = executar_transformacoes(
        df_fundos,
        df_mercado,
        df_ordens
    )

    # 3. Geração do relatório
    imprimir_relatorio(resultados)


if __name__ == "__main__":
    main()