# Regras de Domínio do IF.data (Camada Gold)

Este documento reúne as regras contábeis, regulatórias e estruturais necessárias para produzir análises corretas sobre o `gold_warehouse.duckdb`. Ele é leitura obrigatória para analistas humanos e para agentes de IA antes de gerar consultas SQL.

---

## 1. Regra Anti-Dupla Contagem (Escopos Institucionais)

O portal IF.data publica os mesmos bancos sob diferentes visões de consolidação. Na camada Gold, essas visões convivem na tabela `dim_instituicao` e nas tabelas fato contábeis. **Nunca agregue valores financeiros sem filtrar `tipo_instituicao` ou `tipo_relatorio_bcb`.**

### Valores exatos presentes em `dim_instituicao`

| `tipo_instituicao` (use para filtro exato) | `tipo_relatorio_bcb` | Significado |
| :--- | :--- | :--- |
| `Conglomerado Prudencial` | `Conglomerados Prudenciais e Instituições Independentes` | Visão prudencial consolidada (Resolução CMN 4.280/2013, Basileia III). Padrão de mercado a partir de 2014/2015. |
| `Conglomerado Financeiro` | `Conglomerados Financeiros e Instituições Independentes` | Consolidação societária/financeira (COSIF). Cobre séries desde 2000 e os relatórios de carteira de crédito a partir de 2014-06. |
| `Conglomerado Financeiro (SCR)` | `Conglomerados Financeiros e Instituições Independentes` | Série legada dos relatórios de carteira de crédito (SCR) entre 2012-06 e 2014-03. |
| `Instituicao Individual` | `Instituições Individuais` | Cada CNPJ/entidade individualmente (sem eliminação intragrupo). Note a grafia **sem cedilha e sem acento** em `tipo_instituicao`. |
| `Instituição de Câmbio` | `Instituições com Operações de Câmbio` | Instituições autorizadas a operar câmbio (exclusivo de `fato_movimentacao_cambio`). |

> **Atenção:** filtrar por `tipo_relatorio_bcb = 'Conglomerados Financeiros e Instituições Independentes'` retorna tanto `Conglomerado Financeiro` quanto `Conglomerado Financeiro (SCR)`. Para séries contínuas de carteira de crédito desde 2012-06, isso é desejado (pois os períodos não se sobrepõem: SCR vai até `2014-03` e Financeiro começa em `2014-06`). Para tabelas contábeis, prefira filtrar por `tipo_instituicao`.

---

## 2. Dois Regimes Contábeis e Cobertura Temporal Real

O calendário `dim_tempo` cobre **106 trimestres**, de `20000301` (`2000-03-01`) a `20260601` (`2026-06-01`), divididos em dois regimes regulatórios publicados em portais e leiautes distintos pelo Banco Central:

1. **Regime histórico (`cosif_ate_2024`, `2000-03` a `2024-12`):** servido pelas 13 tabelas fato dimensionais (`fato_resumo_financeiro`, `fato_balanco_patrimonial`, `fato_demonstracao_resultado`, `fato_capital_prudencial`, `fato_carteira_credito_*`, `fato_risco_credito`, `fato_regiao_credito`, `fato_operacoes_clientes`, `fato_movimentacao_cambio`) e pelas 4 views de relatórios históricos.
2. **Regime atual (`cosif_desde_2025`, `2025-03` em diante — Resolução CMN nº 4.966/2021):** servido por `fato_ifdata_2025_campos` (formato longo preservando 100% dos campos e rubricas publicados no novo leiaute).
3. **Série conciliada (`2014-03` a `2026-06`):** a view `view_resumo_prudencial_serie` unifica `Ativo Total` e `Patrimônio Líquido` de `Conglomerado Prudencial` nos dois regimes, identificando cada observação na coluna `regime_contabil` (`'cosif_ate_2024'` ou `'cosif_desde_2025'`). Definições de provisão e classificações de risco não são misturadas automaticamente porque mudaram de metodologia com a Resolução CMN 4.966.

### Cobertura por tabela fato

| Tabela Fato | Escopo / `tipo_instituicao` disponível | Intervalo (`id_data`) |
| :--- | :--- | :--- |
| `fato_resumo_financeiro` | `Instituicao Individual`, `Conglomerado Financeiro` | `20000301` a `20241201` |
| `fato_resumo_financeiro` | `Conglomerado Prudencial` | `20140301` a `20241201` |
| `fato_balanco_patrimonial` | `Instituicao Individual`, `Conglomerado Financeiro` | `20000301` a `20241201` |
| `fato_balanco_patrimonial` | `Conglomerado Prudencial` | `20140301` a `20241201` |
| `fato_demonstracao_resultado` | `Instituicao Individual`, `Conglomerado Financeiro` | `20000301` a `20241201` |
| `fato_demonstracao_resultado` | `Conglomerado Prudencial` | `20140301` a `20241201` |
| `fato_capital_prudencial` | `Conglomerado Financeiro` | `20001201` a `20141201` |
| `fato_capital_prudencial` | `Conglomerado Prudencial` | `20150301` a `20241201` |
| `fato_carteira_credito_produto` | `Conglomerado Financeiro (SCR)` / `Conglomerado Financeiro` | `20120601`..`20140301` / `20140601`..`20241201` |
| `fato_carteira_credito_atividade` | `Conglomerado Financeiro (SCR)` / `Conglomerado Financeiro` | `20120601`..`20140301` / `20140601`..`20241201` |
| `fato_carteira_credito_porte` | `Conglomerado Financeiro (SCR)` / `Conglomerado Financeiro` | `20120601`..`20140301` / `20140601`..`20241201` |
| `fato_carteira_credito_indexador` | `Conglomerado Financeiro (SCR)` / `Conglomerado Financeiro` | `20120601`..`20140301` / `20140601`..`20241201` |
| `fato_carteira_credito_totais` | `Conglomerado Financeiro (SCR)` / `Conglomerado Financeiro` | `20120601`..`20140301` / `20140601`..`20241201` |
| `fato_risco_credito` | `Conglomerado Financeiro (SCR)` / `Conglomerado Financeiro` | `20120601`..`20140301` / `20140601`..`20241201` |
| `fato_operacoes_clientes` | `Conglomerado Financeiro (SCR)` / `Conglomerado Financeiro` | `20120601`..`20140301` / `20140601`..`20241201` |
| `fato_regiao_credito` | `Conglomerado Financeiro (SCR)` / `Conglomerado Financeiro` | `20120601`..`20140301` / `20140901`..`20241201` |
| `fato_movimentacao_cambio` | `Instituição de Câmbio` | `20141201` a `20230601` |
| `fato_ifdata_2025_campos` | `escopo` em `prudential_conglomerates` (14 rel.), `financial_conglomerates` (4 rel.), `individual_institutions` (4 rel.) | `20250301` a `20260601` |

Consequências práticas:

- **Séries de capital prudencial antes e depois de 2015:** até `20141201`, os dados estão em `Conglomerado Financeiro`; de `20150301` a `20241201`, em `Conglomerado Prudencial` (`fato_capital_prudencial`); a partir de `20250301`, em `fato_ifdata_2025_campos` com `escopo = 'prudential_conglomerates'` e `relatorio = 'capital_information'`.
- **Relatórios de carteira de crédito até 2024:** não existem sob `Conglomerado Prudencial` nem `Instituicao Individual` nos fatos históricos — consulte sob `Conglomerado Financeiro` (e `Conglomerado Financeiro (SCR)` para `2012-06` a `2014-03`). A partir de `2025-03`, os relatórios de carteira de crédito passaram a ser publicados no escopo `prudential_conglomerates` em `fato_ifdata_2025_campos`.

---

## 3. Unidades, Escalas e Formatos

- **Valores monetários (Balanço, DRE, Resumo, Capital, Carteira de Crédito — histórico e 2025+):** expressos em **milhares de reais (`R$ mil`)**, preservando a unidade original do IF.data. Para converter em bilhões de reais, divida por `1e6` (`1_000_000`).
- **Índices e percentuais — diferença entre histórico e 2025+:**
  - **Tabelas históricas (`2000-03`..`2024-12`):** `roe`, `roa`, `indice_basileia`, `indice_capital_principal`, `indice_capital_nivel_i`, `razao_alavancagem` e `indice_imobilizacao` estão em **fração decimal** (`0.1651` = `16,51%`). Multiplique por `100` apenas na apresentação.
  - **Tabela atual (`fato_ifdata_2025_campos`, `2025-03` em diante):** percentuais vêm em **pontos percentuais** (ex.: `16.51` representa `16,51%`) e são marcados com `formato_valor = 'percentual'`. **Não multiplique por `100` novamente.**
- **Campos textuais e marcadores em `fato_ifdata_2025_campos`:** `valor_original` preserva o texto exato do CSV (incluindo `'NI'` para não informado); células vazias ficam `NULL`; `valor_numerico` (`DECIMAL(38,8)`) só é preenchido quando o campo contém número reconhecível.
- **Quantidades (`quantidade_agencias`, `quantidade_postos_atendimento`, `quantidade_clientes`, `quantidade_operacoes`):** números inteiros/contagens absolutas.
- **Chave temporal (`id_data`):** inteiro no formato `YYYYMMDD` sempre apontando para o dia `01` do mês de encerramento do trimestre (`03`, `06`, `09` ou `12`), por exemplo `20260601` para junho de 2026. Use `dim_tempo.data` ou `data_base` quando precisar de tipo `DATE`.

---

## 4. Convenção Contábil: Estoque vs Fluxo Semestral na DRE

Esta é a armadilha mais comum em análises do sistema financeiro brasileiro (padrão COSIF do Bacen):

- **Balanço Patrimonial e Carteira de Crédito são estoques:** representam o saldo na data-base. Nunca some estoques entre trimestres para obter "ativo anual"; use o saldo de fechamento ou a média dos saldos.
- **DRE (`fato_demonstracao_resultado`, `view_dre_relatorios` e `lucro_liquido` no resumo) é fluxo acumulado por semestre civil:**
  - **Março (`YYYY0301`):** acumulado de 3 meses (Jan–Mar = 1T).
  - **Junho (`YYYY0601`):** acumulado de 6 meses (Jan–Jun = 1T + 2T).
  - **Setembro (`YYYY0901`):** reinicia a acumulação; 3 meses (Jul–Set = 3T).
  - **Dezembro (`YYYY1201`):** acumulado de 6 meses (Jul–Dez = 3T + 4T).

### Fórmulas obrigatórias para DRE

| Medida desejada | Fórmula correta | Erro comum a evitar |
| :--- | :--- | :--- |
| **Lucro / Receita anual (`YYYY`)** | `valor(YYYY0601) + valor(YYYY1201)` | Somar os 4 trimestres (conta 1T e 3T duas vezes). |
| **Resultado isolado do 1T** | `valor(YYYY0301)` | — |
| **Resultado isolado do 2T** | `valor(YYYY0601) - valor(YYYY0301)` | Usar `YYYY0601` direto como se fosse trimestral. |
| **Resultado isolado do 3T** | `valor(YYYY0901)` | — |
| **Resultado isolado do 4T** | `valor(YYYY1201) - valor(YYYY0901)` | Usar `YYYY1201` direto como se fosse trimestral. |

### Cálculo de `roe` e `roa` no modelo Gold

Nas tabelas `fato_resumo_financeiro` e `fato_demonstracao_resultado`, `roe` (`lucro_liquido / NULLIF(patrimonio_liquido, 0)`) e `roa` (`lucro_liquido / NULLIF(ativo_total, 0)`) são calculados diretamente sobre o `lucro_liquido` daquela data-base, **sem anualização**. Portanto:

- Em `03` e `09`, `roe` e `roa` refletem retorno de **3 meses**.
- Em `06` e `12`, `roe` e `roa` refletem retorno de **6 meses**.
- Para **ROE anual**, calcule `(lucro_1S + lucro_2S) / patrimonio_liquido_medio` (usando a média do PL nas datas-base do ano).

---

## 5. Identidade de Instituições e Histórico de Nomes

- **Chave primária (`id_instituicao`):** hash MD5 determinístico composto por `codigo_origem` (código da instituição no Bacen) + `tipo_instituicao`. A mesma instituição física terá `id_instituicao` diferentes conforme o escopo (`Conglomerado Prudencial` vs `Conglomerado Financeiro` vs `Instituicao Individual`).
- **Mudanças de razão social:** `dim_instituicao.nome` guarda o nome mais recente da instituição, enquanto `nome_instituicao_historico` nos fatos preserva o nome exatamente como reportado em cada data-base.
- **Rastreamento de renomeações:** consulte `view_instituicoes_historico_nomes` com `WHERE houve_mudanca_nome = true` para listar transições de nome ao longo do tempo.
- **Instituições exclusivas de crédito (SCR fallback):** instituições que aparecem apenas nas tabelas de carteira de crédito entram em `dim_instituicao` via fallback para preservar a integridade referencial, podendo ter atributos de resumo nulos.

---

## 6. Segmentação Prudencial e Consolidado Bancário

- **Segmento prudencial (`dim_segmento`):** classificação da Resolução CMN 4.553/2017 de `S1` (maiores bancos, exposição > 10% do PIB ou atividade internacional relevante) até `S5` (perfil de risco simplificado, majoritariamente cooperativas e pequenas instituições). Aplica-se principalmente a `Conglomerado Prudencial` e `Conglomerado Financeiro`; instituições individuais frequentemente têm `segmento` nulo.
- **Consolidado bancário (`dim_consolidado`):** códigos `b1` (bancos comerciais/múltiplos com carteira comercial e caixas), `b2` (bancos múltiplos sem carteira comercial/investimento), `b3C` (cooperativas centrais), `b3S` (cooperativas singulares), `b4` (bancos de desenvolvimento), `n1` a `n4` (instituições não bancárias e de pagamento).

---

## 7. Referências Oficiais Locais

Os dicionários originais publicados pelo Banco Central estão arquivados em `docs/dicionario_dados/`:

- **Período histórico (`2000`–`2024`):** organizados por escopo em `docs/dicionario_dados/<escopo>/*.pdf`.
- **Período atual (`2025` em diante):** organizados por data-base, escopo e relatório em [docs/dicionario_dados/2025_em_diante/](dicionario_dados/2025_em_diante/README.md) (`AAAA-MM/<escopo>/<relatorio>.pdf`), com URLs e hashes SHA-256 registrados em `docs/dicionario_dados/2025_em_diante/manifesto.json` e atualizáveis via `uv run ifdata.py --download-dictionaries`.
