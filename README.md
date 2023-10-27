
# API Python para Análise de Ações

Este é um projeto de API Python desenvolvido com o objetivo de fornecer informações detalhadas sobre ações e dados de mercado financeiro. A API foi construída com as seguintes tecnologias e bibliotecas:

- **Python:** A linguagem de programação utilizada para desenvolver a API.
- **Flask:** Um framework Python que facilita a criação de rotas e solicitações HTTP.
- **Pandas:** Uma biblioteca Python amplamente utilizada para manipulação e análise de dados.
- **yfinance:** Uma biblioteca Python que permite acessar e extrair dados de ações e finanças.
- **Fundamentus:** Uma biblioteca Python que  acessar e extrair informações financeiras fundamentais.

**Nota:** Este projeto encontra-se em fase de desenvolvimento e ainda não foi concluído. Estou trabalhando para adicionar mais recursos e aprimorar a funcionalidade da API

## Iniciando o Servidor

Para iniciar o servidor da API, execute o seguinte comando:

```bash
python src/app.py
```

# Rotas

## /api/stock-ranking (Método: GET)

Esta rota fornece informações sobre o ranking de ações com base na fórmula de Greenblatt Magic Formula.

**Exemplo de resposta:**
```bash
[ {
    "price": 35.7,
    "score": 40.0,
    "ticker": "PETR4",
    "type": "energyStocks"
    "percentageVariation": -1.03,
    "stockClose": "{\"2023-04-26 00:00:00-03:00\": 21.52, \"2023-04-27 00:00:00-03:00\": 21.0, ...}
  },...]
```

## /api/stock-candlestick-data (Método: GET)

Esta rota fornece dados de gráficos de candlestick para várias ações.

**Descrição:** Retorna dados de gráficos de candlestick para várias ações, incluindo preços de fechamento e valores de ações.

**Exemplo de resposta:**
```bash
 [{
    "price": 32.56,
    "ticker": "RRRP3",
    "type": "energyStocks"
    "percentageVariation": 0.68,
    "chartClose": [ {
        "x": "2023-04-26 00:00:00-03:00",
        "y": 27.2
      },...],
    "chartValues":[ {
        "x": "2023-04-26 00:00:00-03:00",
        "y": 30.4
      },...]
  },...]
```

## /api/stock-chart-line-data (Método: GET)

Esta rota fornece dados de gráfico de linha para o fechamento das ações das cinco melhores classificadas.

**Descrição:** Retorna dados de gráfico de linha para o fechamento de ações das cinco melhores classificadas.

**Exemplo de resposta:**
```bash
[{
    "name": "PETR4",
    "data": [{
        "x": "2023-04-26 00:00:00-03:00",
        "y": 0.06
},...]
```

## /api/stock-table-values (Método: GET)

Esta rota fornece valores de tabela para as ações em uma data específica.

**Descrição:** Retorna valores de tabela para as ações em uma data específica, incluindo abertura, máxima, mínima, fechamento, preço, variação percentual, etc.

**Exemplo de resposta:**
```bash
[
  {
    "ticker": "AAPL",
    "date": "2023-10-26T00:00:00-03:00",
    "open": 148.0,
    "high": 150.0,
    "low": 145.0,
    "close": 149.5,
    "price": 150.0,
    "percentageVariation": 0.5
  },...]
```



