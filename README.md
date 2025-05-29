# 🌊 HidroScan - Simulador de Impacto Econômico de Enchentes

Este projeto em Python tem como objetivo **analisar dados de enchentes no Brasil**, utilizando como base dados reais extraídos de fontes oficiais Sistema Integrado de Informações sobre Desastres. A aplicação permite gerar análises rápidas, gráficos, relatórios e simulações, com foco em impactos humanos, ambientais e habitacionais.

## 📁 Estrutura do Projeto

- `app.py` — Script principal com menu interativo e todas as funções de análise.
- `mdr_sedec_dados_informados_2022.csv` — Arquivo CSV com os dados de entrada.
- `poluicoes_municipios.xlsx` — Gerado automaticamente com os municípios afetados por poluição ambiental.

## ⚙️ Requisitos

- Python 3.7+
- Bibliotecas:
  - `pandas`
  - `matplotlib`
  - `openpyxl` (para exportação `.xlsx`)

Para instalar as dependências:
```bash
pip install pandas matplotlib openpyxl
```

## Funcionalidades

### 1. Análise Rápida por UF
Filtra um estado (UF) e apresenta a quantidade de:

 - Mortos

- Feridos

- Desabrigados

- Desaparecidos

### 2. Municípios com Mais Unidades Habitacionais Destruídas

Mostra os 10 municípios mais impactados em termos de destruição de moradias.

### 3. Exportar Planilha de Poluição Ambiental

Gera um arquivo .xlsx com os municípios afetados por:

- Poluição da água, ar e solo

- Diminuição hídrica

- Incêndios em áreas de proteção

#### 4. Gráfico de Pessoas Desabrigadas/Desalojadas por UF
Gera um gráfico de barras com o total de pessoas afetadas por estado.

### 5. Índice de Risco por UF
Classifica os estados em baixo, médio ou alto risco com base na soma dos seguintes indicadores:

- Mortos

- Feridos

- Desabrigados

- Desalojados

- Moradias destruídas

### 6. Simulação de Cenários com Aumento de Chuvas
Permite simular o impacto de um aumento percentual das chuvas (ex: +30%) nos indicadores de desastres.

### 0. Sair
Encerra o programa.

## Autor
RM559023 - WITALON ANTONIO RODRIGUES
