# 📊 Análise de Pedidos e Entregas - Projeto Pandas

Projeto de análise de dados com **Python e Pandas** focado em compreender padrões de vendas, desempenho de entregadores e qualidade de restaurantes.

## 🎯 Objetivo

Analisar 500 pedidos de delivery para identificar:
- Performance de entregadores
- Qualidade dos restaurantes
- Padrões de horários
- Correlações entre variáveis
- Outliers e anomalias

## 🛠️ Tecnologias Utilizadas

- **Python 3.x**
- **Pandas** - Manipulação e análise de dados
- **NumPy** - Geração de dados aleatórios

## 📥 Como Usar

### 1. Instalar dependências
```bash
pip install pandas numpy
```

### 2. Executar o projeto
```bash
python analise_pedidos.py
```

### 3. Resultado
O script gera 10 análises diferentes e imprime os resultados no console.

## 📊 Datasets Criados

### `pedidos`
- id_pedido
- restaurante
- preco_pedido
- tempo_entrega_min
- rating (1-5 estrelas)
- data_pedido
- entregador
- status (Entregue, Cancelado, Em trânsito, Preparando)

### `reviews`
- id_pedido
- comentario
- palavras_chave

## 🔍 Análises Realizadas

### 1. Performance dos Entregadores
Métrica: entregas completadas, tempo médio, rating médio, faturamento

### 2. Qualidade por Restaurante
Métrica: total de pedidos, rating médio, pedidos 5-estrelas, pedidos 1-estrela, preço médio

### 3. Pedidos por Hora do Dia
Identifica horários de pico e sazonalidade

### 4. Status dos Pedidos
Proporção de entregues, cancelados, em trânsito, preparando

### 5. Pedidos com Baixa Avaliação
Filtra ratings ≤ 2 por restaurante e status

### 6. Correlação entre Variáveis
Analisa relação entre preço, tempo de entrega, rating e tamanho do comentário

### 7. Análise: Velocidade vs Qualidade
Categoriza entregas (Rápido, Normal, Lento) e correlaciona com rating

### 8. Top 3 Restaurantes
Ranking por volume de pedidos

### 9. 5 Piores Avaliações
Identifica pedidos problemáticos

### 10. Outliers de Preço
Detecta pedidos com preço anormalmente alto usando IQR

## 💡 Principais Insights

- Entregas mais rápidas = ratings melhores
- Correlação negativa entre tempo de entrega e satisfação (-0.67)
- Sushi é o restaurante com melhor avaliação média
- Alguns pedidos apresentam preços outliers (suspeitos)

## 📈 Técnicas Utilizadas

- **Merge**: Junção de DataFrames
- **Groupby + Agg**: Agrupamento e agregação de dados
- **Lambda functions**: Aplicação de lógica customizada
- **pd.cut()**: Categorização de dados contínuos
- **Correlação**: Análise de relações entre variáveis
- **IQR**: Detecção de outliers
- **String operations**: Manipulação de texto
- **Date operations**: Extração de componentes de data/hora

## 📁 Estrutura do Código

1. **Criação de dados** - Simulação com NumPy
2. **Limpeza** - Remoção de duplicatas e preenchimento de vazios
3. **Transformação** - Merge, derivações, categorizações
4. **Análise** - Agregações e cálculos
5. **Visualização** - Prints estruturados dos resultados

## 🚀 Próximos Passos

- [ ] Exportar resultados para Excel
- [ ] Criar visualizações com Matplotlib/Seaborn
- [ ] Adicionar análise de série temporal
- [ ] Machine Learning para previsão de ratings

## ✍️ Autor

Leonardo - Estudante de Analytics Engineer

