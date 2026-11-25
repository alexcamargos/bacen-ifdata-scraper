# Guia de Uso do Pacote

Este guia cobre a instalação, a configuração de ambiente, a execução do pipeline via CLI e o consumo programático dos bancos DuckDB produzidos pelo `bacen-ifdata-scraper` (versão `0.1.0`).

## Requisitos

- **Python:** 3.11 ou superior.
- **Gerenciador de dependências:** Astral [uv](https://docs.astral.sh/uv/).
- **Apenas para coleta (`--scraper`):** Firefox e [GeckoDriver](https://github.com/mozilla/geckodriver/releases) disponíveis no `PATH` do sistema. As etapas de limpeza, transformação, carga, modelagem dbt e leitura analítica não abrem navegador.

## Instalação

### Como dependência em um projeto de análise

Para consumir os módulos Python e ler os bancos DuckDB gerados pelo pacote:

```bash
uv add bacen-ifdata-scraper
```

Na versão `0.1.0`, o pacote publicado no PyPI expõe o módulo Python `bacen_ifdata`, mas não registra um script de console em `[project.scripts]`. Para executar a interface de linha de comando (`ifdata.py`) e os modelos dbt localmente, clone o repositório.

### Instalação local completa (CLI + dbt)

```bash
git clone https://github.com/alexcamargos/bacen-ifdata-scraper.git
cd bacen-ifdata-scraper
uv sync
```

## Configuração de Ambiente

Crie o arquivo `.env` a partir do modelo versionado:

```bash
cp .env.example .env
```

No Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

### Variáveis reconhecidas

| Variável | Onde é usada | Descrição |
| :--- | :--- | :--- |
| `IFDATA_DATA_DIRECTORY` | `Config` (`configurations.py`) | Raiz alternativa para todas as camadas de dados (`raw`, `interim`, `processed`). Quando omitida, usa `<raiz-do-projeto>/data`. |
| `SILVER_DB_PATH` | `dbt` (`profiles.yml` / `.env`) | Caminho do banco DuckDB Silver consumido pelo dbt em execuções standalone. |
| `GOLD_DB_PATH` | `dbt` (`profiles.yml` / `.env`) | Caminho do banco DuckDB Gold gerado pelo dbt em execuções standalone. |
| `PYTHONUTF8` | Runtime Python | Definir como `1` no Windows para evitar erros de codificação em logs e CSVs. |
| `PYTHONIOENCODING` | Runtime Python | Definir como `utf-8` para saída padronizada. |

## Interface de Linha de Comando (`ifdata.py`)

O ponto de entrada principal na raiz do repositório é [ifdata.py](../ifdata.py), executado via `uv run ifdata.py [opções]`.

### Etapas individuais do pipeline

| Flag | Etapa | O que faz |
| :--- | :--- | :--- |
| `-s`, `--scraper` | Extração | Baixa os relatórios CSV do portal histórico IF.data (até `2024-12`) para a camada `raw/`. |
| `-c`, `--cleaner` | Limpeza | Normaliza CSVs brutos do Bacen (cabeçalhos múltiplos, linhas de resumo e separadores). |
| `-t`, `--transformer` | Transformação | Aplica schemas Pydantic/Pandera e grava arquivos tipados prontos para carga. |
| `-l`, `--loader` | Carga (Silver) | Recria e carrega as tabelas normalizadas no `silver_warehouse.duckdb`. |
| `-a`, `--analytics` | Modelagem (Gold) | Executa o projeto dbt (`src/bacen_ifdata/data_analytics`) para construir o Star Schema em `gold_warehouse.duckdb`. |

Sem nenhuma flag de ação, `uv run ifdata.py` executa o fluxo padrão de limpeza e transformação (`-c -t`).

### Operações incrementais, reparo e auditoria

| Flag | Comportamento |
| :--- | :--- |
| `--data-base YYYY-MM` | Limita a coleta a um mês de referência específico até `2024-12`. Exige `--scraper` ou `--repair-raw`. |
| `--repair-raw` | Ativa o scraper e recoleta apenas CSVs em `raw/` com datas de referência ou cabeçalhos inválidos. |
| `--refresh` | Ativa o scraper e recoleta o mês informado em `--data-base` para verificar revisões do Bacen. Exige `--data-base` e não pode ser combinado com `--repair-raw`. |
| `--update` | Processa apenas os relatórios alterados, atualiza a camada Silver com controle de ledger, gera e testa uma nova release Gold e atualiza `processed/current.json`. Substitui `-c`, `-t`, `-l` e `-a`. |
| `--audit-coverage` | Ação somente leitura que compara as medidas originais com a camada Silver publicada. Não pode ser combinada com nenhuma flag de execução. |
| `--no-cleanup` | Mantém a sessão do navegador aberta ao final (útil para depuração do scraper). |
| `-v`, `--version` | Exibe a versão instalada do pacote. |

### Filtros de escopo (`-i` e `-r`)

As flags `-i/--institution` e `-r/--report` restringem o scraper, cleaner, transformer, loader ou a coleta antes de `--update` (a etapa `-a/--analytics` sempre constrói o modelo Gold inteiro).

Valores aceitos em `-i / --institution`:

| Valor CLI (`InstitutionType`) | Escopo no portal IF.data | Qtd. relatórios |
| :--- | :--- | :---: |
| `PRUDENTIAL_CONGLOMERATES` | Conglomerados Prudenciais e Instituições Independentes | 14 |
| `FINANCIAL_CONGLOMERATES` | Conglomerados Financeiros e Instituições Independentes | 13 |
| `FINANCIAL_CONGLOMERATES_SCR` | Conglomerados Financeiros e Instituições Independentes (SCR) | 8 |
| `INDIVIDUAL_INSTITUTIONS` | Instituições Individuais | 4 |
| `FOREIGN_EXCHANGE` | Instituições com Operações de Câmbio | 1 |

Principais valores de `-r / --report`: `SUMMARY`, `ASSETS`, `LIABILITIES`, `INCOME_STATEMENT`, `CAPITAL_INFORMATION`, `SEGMENTATION`, `QUARTERLY_FOREIGN_CURRENCY_FLOW`, `PORTFOLIO_INDIVIDUALS_TYPE_MATURITY`, `PORTFOLIO_LEGAL_PERSON_TYPE_MATURITY`, `PORTFOLIO_LEGAL_PERSON_ECONOMIC_ACTIVITY`, `PORTFOLIO_LEGAL_PERSON_BUSINESS_SIZE`, `PORTFOLIO_NUMBER_CLIENTS_OPERATIONS`, `PORTFOLIO_RISK_LEVEL`, `PORTFOLIO_INDEXER`, `PORTFOLIO_GEOGRAPHIC_REGION` e `PORTFOLIO_FINANCIAL_INSTRUMENTS`.

### Exemplos práticos de CLI

```bash
# Coletar um único trimestre de Conglomerados Prudenciais (Resumo)
uv run ifdata.py -s -i PRUDENTIAL_CONGLOMERATES -r SUMMARY --data-base 2024-12

# Verificar revisão de um trimestre e publicar nova release Gold testada
uv run ifdata.py --refresh --data-base 2024-12 --update

# Reparar arquivos raw corrompidos de um escopo específico
uv run ifdata.py --repair-raw -i INDIVIDUAL_INSTITUTIONS

# Processar alterações pendentes e publicar release Silver + Gold
uv run ifdata.py --update

# Auditar cobertura de medidas (somente leitura)
uv run ifdata.py --audit-coverage
```

### Execução standalone do dbt

```bash
cd src/bacen_ifdata/data_analytics
uv run --env-file ../../../.env dbt build
uv run --env-file ../../../.env dbt run -s view_resumo_financeiro_relatorios
uv run --env-file ../../../.env dbt test -s view_resumo_financeiro_relatorios
```

## Uso Programático em Python

### Leitura analítica do warehouse Gold (recomendado para ferramentas de análise)

Use `warehouse_path('gold')` ou `current_release(...)` para resolver automaticamente a release publicada em `data/processed/current.json` (com fallback para caminhos legados quando ainda não existe ponteiro de release). Sempre abra o banco com `read_only=True` em scripts e agentes de análise para evitar conflitos de lock.

```python
import duckdb
from bacen_ifdata.utilities.releases import current_release, warehouse_path

gold_db = warehouse_path('gold')
release = current_release(gold_db.parents[3])  # opcional: inspecionar model_revision

with duckdb.connect(str(gold_db), read_only=True) as con:
    df = con.execute(
        """
        SELECT nome_instituicao, segmento, ativo_total, patrimonio_liquido
        FROM view_resumo_financeiro_relatorios
        WHERE id_data = 20241201
          AND tipo_instituicao = 'Conglomerado Prudencial'
        ORDER BY ativo_total DESC NULLS LAST
        LIMIT 10
        """
    ).pl()

print(df)
```

Se o seu projeto analítico lê os dados a partir de outro diretório, informe `directory` ou defina `IFDATA_DATA_DIRECTORY`:

```python
from pathlib import Path
from bacen_ifdata.utilities.releases import warehouse_path

gold_db = warehouse_path('gold', directory=Path('/caminho/para/data'))
```

### Execução do pipeline via `Application`

A classe `Application` gerencia todas as dependências do pipeline e inicia o navegador apenas quando `run_scraper()` é chamado (inicialização preguiçosa):

```python
from bacen_ifdata.application import Application

with Application(enable_cleanup=True) as app:
    app.pipeline_manager.run_cleaner(institution='PRUDENTIAL_CONGLOMERATES', report='SUMMARY')
    app.pipeline_manager.run_transformer(institution='PRUDENTIAL_CONGLOMERATES', report='SUMMARY')
    app.pipeline_manager.run_update()
```

Para composição customizada sem a fábrica padrão, `Pipeline` está exportado diretamente na raiz do pacote (`from bacen_ifdata import Pipeline`).

## Estrutura Física dos Artefatos Gerados

O fluxo de dados é unidirecional (`raw -> interim -> processed`). A localização dos arquivos depende de `IFDATA_DATA_DIRECTORY`:

| Artefato | Layout padrão (`<repo>/data`) | Layout isolado (`IFDATA_DATA_DIRECTORY` externo) |
| :--- | :--- | :--- |
| CSVs brutos (Bronze) | `data/raw/<escopo>/<relatorio>/` | `<DIR>/raw/<escopo>/<relatorio>/` |
| CSVs limpos | `data/processed/<escopo>/` | `<DIR>/interim/cleaned/<escopo>/` |
| CSVs tipados | `data/transformed/<escopo>/` | `<DIR>/interim/typed/<escopo>/` |
| Releases Silver publicados | `data/interim/releases/<release-id>/silver_warehouse.duckdb` | `<DIR>/interim/releases/<release-id>/silver_warehouse.duckdb` |
| Releases Gold publicados | `data/processed/releases/<release-id>/gold_warehouse.duckdb` | `<DIR>/processed/releases/<release-id>/gold_warehouse.duckdb` |
| Ponteiro da release ativa | `data/processed/current.json` | `<DIR>/processed/current.json` |

O ponteiro `data/processed/current.json` tem a estrutura:

```json
{
  "silver": "interim/releases/<timestamp>-<hash>/silver_warehouse.duckdb",
  "gold": "processed/releases/<timestamp>-<hash>/gold_warehouse.duckdb",
  "model_revision": "<sha256-do-projeto-dbt>"
}
```

## Próximos Documentos

- [Catálogo de Dados da Camada Gold](DATA_CATALOG.md) — todas as dimensões, fatos, views e domínios.
- [Regras de Domínio do IF.data](DOMAIN_RULES.md) — prevenções contra dupla contagem, convenções de DRE e escalas.
- [Cookbook de Consultas](COOKBOOK.md) — receitas SQL DuckDB e Python/Polars prontas e validadas.
- [Índice para Agentes de IA](../llms.txt) e [Manifesto Semântico Gold](ai/gold_semantic_model.yaml).
