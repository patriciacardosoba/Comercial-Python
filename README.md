# Projeto de Análise Comercial e ETL 
Pipeline automatizado em Python para tratamento de dados, auditoria de inconsistências, cruzamento de bases relacionais e geração de indicadores de desempenho comercial (KPIs).

## Ferramentas e Tecnologias
* **Python** (Pandas, NumPy, Matplotlib)
* **VS Code** e ambiente Windows
* **Git** para controlo de versão
* **SQL** para tratamento, manipulação, limpeza, inclusão dos dados

## Visualizações de Dados
![Tendência Mensal](PYTHON/tendencia_vendas_mensal.png)
![Distribuição por Estabelecimento](PYTHON/percentagem_estabelecimentos.png)
## 🔄 Pipeline de ETL (Extração, Transformação e Carga)
O projeto automatiza todo o tratamento dos dados comerciais através de um script em Python utilizando a biblioteca `pandas`:

1. **Extração (Extract):**
   - Leitura automatizada dos ficheiros de dados base (`calendario.xlsx`, `Filiais.xlsx`, `Vendas.xlsx`, `Vendedores.xlsx` e `Visitas.xlsx`).

2. **Transformação (Transform):**
   - **Padronização:** Conversão de colunas de texto para datas reais (`pd.to_datetime`) para permitir agrupamentos temporais corretos.
   - **Cruzamento de Dados:** Relacionamento automatizado das informações das filiais com base na tabela de vendedores através de mapeamento.

3. **Carga e Visualização (Load & Output):**
   - Cálculo e agregação de indicadores de desempenho comercial (KPIs).
   - Exportação automática dos gráficos finais em formato `.png` para exibição direta.
   ## 🗄️ Módulo SQL e Gestão de Dados
O projeto também inclui scripts em SQL estruturados para:
- **DDL & DCL:** Criação de tabelas relacionais (`Vendas`, `Visitas`, `Vendedores`, `Filiais`, `Calendário`) e controle de acessos/permissões.
- **DML & Integração:** Inserção de dados e enriquecimento demográfico automatizado via **API do IBGE**.
- **DQL (Business Intelligence Queries):** Consultas avançadas para responder a indicadores comerciais como conversão por filial, ranking YTD e projeções comerciais.
   
