# Catálogo de Dados da Camada Gold

Referência completa do modelo dimensional (Star Schema) publicado em `gold_warehouse.duckdb`. Todos os nomes de tabelas, colunas e tipos abaixo refletem a introspecção direta do banco Gold e do projeto dbt (`src/bacen_ifdata/data_analytics/models/gold/schema.yml`).

Antes de escrever consultas analíticas, leia [Regras de Domínio](DOMAIN_RULES.md) para evitar dupla contagem entre escopos institucionais e erros na acumulação semestral da DRE.

## Resumo da Cobertura

- **Horizonte temporal:** `20000301` (`2000-03`) até `20260601` (`2026-12`) — **106 trimestres**.
- **Objetos analíticos no schema `main`:** 5 views prontas, 14 tabelas fato, 13 dimensões, 1 tabela intermediária enriquecida (`int_instituicao_enriquecida`) e 10 seeds de domínio.
- **Unidades padrão:** valores monetários em **R$ mil**; índices/percentuais em **fração decimal** no histórico (`2000–2024`, ex.: `0.165` = `16,5%`) e em **pontos percentuais** em `fato_ifdata_2025_campos` (`2025+`, marcados com `formato_valor = 'percentual'`, ex.: `16.5` = `16,5%`).

## Inventário Rápido

### Views Analíticas Prontas (Ponto de Partida Recomendado)

| View | Colunas | Grão | Uso principal |
| :--- | :---: | :--- | :--- |
| `view_balanco_patrimonial_relatorios` | 55 | 1 linha por instituição e data-base (visão desnormalizada de fato_balanco_patrimonial, 2000–2024) | Análise detalhada de composição do Ativo (crédito, TVM, disponibilidades) e Passivo (depósitos, LCI, LCA, LF) |
| `view_dre_relatorios` | 50 | 1 linha por instituição e data-base (visão desnormalizada de fato_demonstracao_resultado, 2000–2024) | Análise de receitas de intermediação, despesas de captação, PDD, eficiência administrativa e lucro líquido |
| `view_instituicoes_historico_nomes` | 19 | 1 linha por instituição e data-base com comparação de nome anterior via LAG (2000–2024) | Rastreamento de mudanças de razão social, fusões e incorporações ao longo da série histórica |
| `view_resumo_financeiro_relatorios` | 27 | 1 linha por instituição e data-base (visão desnormalizada de fato_resumo_financeiro, 2000–2024) | Rankings de instituições por ativo total, patrimônio líquido, captações ou lucro líquido; Evolução temporal de indicadores principais sem necessidade de joins manuais |
| `view_resumo_prudencial_serie` | 8 | 1 linha por instituição prudencial e data-base conciliando Ativo Total e PL de 2014-03 a 2026-06 | Série contínua de Ativo Total e Patrimônio Líquido de Conglomerados Prudenciais cruzando 2014–2024 (cosif_ate_2024) e 2025+ (cosif_desde_2025) |

### Tabelas Fato

| Tabela Fato | Colunas | Grão | Escopos disponíveis |
| :--- | :---: | :--- | :--- |
| `fato_balanco_patrimonial` | 41 | 1 linha por instituição (id_instituicao) e data-base (id_data) | `Instituicao Individual` (20000301..20241201), `Conglomerado Financeiro` (20000301..20241201), `Conglomerado Prudencial` (20140301..20241201) |
| `fato_capital_prudencial` | 25 | 1 linha por instituição (id_instituicao) e data-base (id_data) | `Conglomerado Financeiro` (20001201..20141201), `Conglomerado Prudencial` (20150301..20241201) |
| `fato_carteira_credito_atividade` | 5 | 1 linha por instituição, data-base, atividade econômica (CNAE) e faixa de vencimento | `Conglomerado Financeiro (SCR)` (20120601..20140301), `Conglomerado Financeiro` (20140601..20241201) |
| `fato_carteira_credito_indexador` | 19 | 1 linha por instituição (id_instituicao) e data-base (id_data) | `Conglomerado Financeiro (SCR)` (20120601..20140301), `Conglomerado Financeiro` (20140601..20241201) |
| `fato_carteira_credito_porte` | 4 | 1 linha por instituição, data-base e porte do tomador PJ | `Conglomerado Financeiro (SCR)` (20120601..20140301), `Conglomerado Financeiro` (20140601..20241201) |
| `fato_carteira_credito_produto` | 6 | 1 linha por instituição, data-base, produto de crédito e faixa de vencimento | `Conglomerado Financeiro (SCR)` (20120601..20140301), `Conglomerado Financeiro` (20140601..20241201) |
| `fato_carteira_credito_totais` | 8 | 1 linha por instituição (id_instituicao) e data-base (id_data) | `Conglomerado Financeiro (SCR)` (20120601..20140301), `Conglomerado Financeiro` (20140601..20241201) |
| `fato_demonstracao_resultado` | 35 | 1 linha por instituição (id_instituicao) e data-base (id_data) | `Instituicao Individual` (20000301..20241201), `Conglomerado Financeiro` (20000301..20241201), `Conglomerado Prudencial` (20140301..20241201) |
| `fato_ifdata_2025_campos` | 14 | 1 linha por escopo, relatório, data-base, linha da instituição e coluna publicada (formato longo 2025+) | `prudential_conglomerates (14 relatórios)` (20250301..20260601), `financial_conglomerates (4 relatórios)` (20250301..20260601), `individual_institutions (4 relatórios)` (20250301..20260601) |
| `fato_movimentacao_cambio` | 24 | 1 linha por instituição de câmbio (id_instituicao) e data-base (id_data) | `Instituição de Câmbio` (20141201..20230601) |
| `fato_operacoes_clientes` | 4 | 1 linha por instituição (id_instituicao) e data-base (id_data) | `Conglomerado Financeiro (SCR)` (20120601..20140301), `Conglomerado Financeiro` (20140601..20241201) |
| `fato_regiao_credito` | 4 | 1 linha por instituição, data-base e região geográfica | `Conglomerado Financeiro (SCR)` (20120601..20140301), `Conglomerado Financeiro` (20140901..20241201) |
| `fato_resumo_financeiro` | 13 | 1 linha por instituição (id_instituicao) e data-base (id_data) | `Instituicao Individual` (20000301..20241201), `Conglomerado Financeiro` (20000301..20241201), `Conglomerado Prudencial` (20140301..20241201) |
| `fato_risco_credito` | 4 | 1 linha por instituição, data-base e nível de risco (AA–H) | `Conglomerado Financeiro (SCR)` (20120601..20140301), `Conglomerado Financeiro` (20140601..20241201) |

### Dimensões e Intermediária

| Tabela | Colunas | Descrição |
| :--- | :---: | :--- |
| `dim_atividade` | 3 | 1 linha por setor de atividade econômica (CNAE) |
| `dim_classe_instituicao` | 3 | Dimensão de Classe/Tipo Detalhado da Instituição. |
| `dim_consolidado` | 3 | Dimensão de Tipo de Consolidado Bancário. |
| `dim_controle` | 3 | Dimensão de Tipo de Controle de Capital. |
| `dim_faixa_vencimento` | 4 | 1 linha por faixa de prazo de vencimento |
| `dim_instituicao` | 11 | Dimensão de Instituições. Unifica dados de Conglomerados Prudenciais, Financeiros e Instituições Independentes. |
| `dim_localizacao` | 4 | Dimensão de Localidade (Cidade, UF, Região). |
| `dim_porte` | 3 | 1 linha por porte do tomador PJ |
| `dim_produto_credito` | 4 | 1 linha por modalidade de produto de crédito (PF/PJ) |
| `dim_regiao` | 3 | 1 linha por macrorregião geográfica |
| `dim_risco` | 3 | 1 linha por nível de risco (AA a H) |
| `dim_segmento` | 3 | Dimensão de Segmento Prudencial (S1, S2, etc). |
| `dim_tempo` | 5 | Dimensão de Tempo baseada nas datas base dos relatórios. |
| `int_instituicao_enriquecida` | 15 | Modelo intermediário reutilizável com enriquecimento dimensional da instituição para consumo dos data marts de relatório. |

---

## Detalhamento das Views Analíticas

### `view_balanco_patrimonial_relatorios`

Data Mart View unificando o Fato Balanço Patrimonial (Ativos e Passivos) com as Dimensões, para o relatório completo do IF.data.

- **Grão:** 1 linha por instituição e data-base (visão desnormalizada de fato_balanco_patrimonial, 2000–2024)
- **Chave:** `id_instituicao, id_data`

| Coluna | Tipo DuckDB | Descrição |
| :--- | :--- | :--- |
| `id_instituicao` | `VARCHAR` | Chave da instituição (FK para dim_instituicao). |
| `id_data` | `INTEGER` | Chave da data (FK para dim_tempo). |
| `codigo_origem` | `BIGINT` |  |
| `nome_instituicao` | `VARCHAR` | Nome da instituição. |
| `nome_instituicao_historico` | `VARCHAR` |  |
| `tipo_instituicao` | `VARCHAR` | Classificação Original. |
| `nome_conglomerado` | `VARCHAR` | Nome do conglomerado pertencente. |
| `tipo_relatorio_bcb` | `VARCHAR` | Qual dos 4 tipos de relatório oficiais do BCB esta linha pertence. |
| `segmento` | `VARCHAR` | Segmento de atuação. |
| `segmento_descricao` | `VARCHAR` |  |
| `cidade` | `VARCHAR` | Cidade da sede. |
| `uf` | `VARCHAR` | UF da sede. |
| `regiao` | `VARCHAR` | Região da sede. |
| `tipo_de_controle` | `VARCHAR` | Qual a natureza do controle acionário (Público, Privado Nacional, etc). |
| `tcb` | `VARCHAR` | Sigla do Tipo de Consolidado Bancário (ex: b1, b2, b3C, n4). |
| `consolidado_bancario` | `VARCHAR` | Descrição completa do Tipo de Consolidado Bancário. |
| `classe_instituicao` | `VARCHAR` | Classe da instituição. |
| `data_base` | `DATE` | Ativo: (a) Disponibilidades |
| `disponibilidades` | `DOUBLE` |  |
| `aplicacoes_interfinanceiras_liquidez` | `DOUBLE` | Ativo: (b) Aplicações Interfinanceiras de Liquidez |
| `tvm_derivativos` | `DOUBLE` | Ativo: (c) TVM e Instrumentos Financeiros Derivativos |
| `operacoes_de_credito` | `DOUBLE` | Ativo: (d1) Operações de Crédito |
| `provisao_operacoes_de_credito` | `DOUBLE` | Ativo: (d2) Provisão sobre Operações de Crédito |
| `operacoes_de_credito_liquidas_provisao` | `DOUBLE` | Ativo: (d) Operações de Crédito Líquidas de Provisão |
| `arrendamento_mercantil_a_receber` | `DOUBLE` | Ativo: (e1) Arrendamento Mercantil a Receber |
| `imobilizado_de_arrendamento` | `DOUBLE` | Ativo: (e2) Imobilizado de Arrendamento |
| `credores_antecipacao_valor_residual` | `DOUBLE` | Ativo: (e3) / (j) Credores por Antecipação de Valor Residual |
| `provisao_arrendamento_mercantil` | `DOUBLE` | Ativo: (e4) Provisão sobre Arrendamento Mercantil |
| `arrendamento_mercantil_liquido_de_provisao` | `DOUBLE` | Ativo: (e) Arrendamento Mercantil Líquido de Provisão |
| `outros_creditos_liquido_de_provisao` | `DOUBLE` | Ativo: (f) Outros Créditos - Líquido de Provisão |
| `outros_ativos_realizaveis` | `DOUBLE` | Ativo: (g) Outros Ativos Realizáveis |
| `permanente_ajustado` | `DOUBLE` | Ativo: (h) Permanente Ajustado |
| `ativo_total_ajustado` | `DOUBLE` | Ativo: (i) Ativo Total Ajustado |
| `ativo_total` | `DOUBLE` | Ativo: (k) Ativo Total |
| `depositos_vista` | `DOUBLE` | Passivo: (a1) Depósitos à Vista |
| `depositos_poupanca` | `DOUBLE` | Passivo: (a2) Depósitos de Poupança |
| `depositos_interfinanceiros` | `DOUBLE` | Passivo: (a3) Depósitos Interfinanceiros |
| `depositos_a_prazo` | `DOUBLE` | Passivo: (a4) Depósitos a Prazo |
| `conta_de_pagamento_pre_paga` | `DOUBLE` | Passivo: (a5) Conta de Pagamento Pré-Paga |
| `depositos_outros` | `DOUBLE` | Passivo: (a6) Depósitos Outros |
| `depositos` | `DOUBLE` | Passivo: (a) Depósito Total |
| `captacoes_mercado_aberto` | `DOUBLE` | Passivo: (b) Obrigações por Operações Compromissadas |
| `letras_de_credito_imobiliario` | `DOUBLE` | Passivo: (c1) Letras de Crédito Imobiliário |
| `letras_de_credito_agronegocio` | `DOUBLE` | Passivo: (c2) Letras de Crédito do Agronegócio |
| `letras_financeiras` | `DOUBLE` | Passivo: (c3) Letras Financeiras |
| `obrigacoes_titulos_e_valores_mobiliarios_exterior` | `DOUBLE` | Passivo: (c4) Obrigações por Títulos e Valores Mobiliários no Exterior |
| `outros_recursos_de_aceites_e_emissao_de_titulos` | `DOUBLE` | Passivo: (c5) Outros Recursos de Aceites e Emissão de Títulos |
| `recursos_aceites_cambiais` | `DOUBLE` | Passivo: (c) Recursos de Aceites e Emissão de Títulos |
| `obrigacoes_emprestimos_repasses` | `DOUBLE` | Passivo: (d) Obrigações por Empréstimos e Repasses |
| `captacoes` | `DOUBLE` | Passivo: (e) Captações Totais |
| `obrigacoes_por_instr_financeiros_derivativos` | `DOUBLE` | Passivo: (f) Instrumentos Derivativos |
| `outras_obrigacoes` | `DOUBLE` | Passivo: (g) Outras Obrigações |
| `passivo_circulante_exigivel_longo_prazo` | `DOUBLE` | Passivo: (h) Passivo Circulante e Exigível a Longo Prazo |
| `patrimonio_liquido` | `DOUBLE` | Passivo: (i) Patrimônio Líquido |
| `passivo_total` | `DOUBLE` | Passivo: (j) Passivo Total |

### `view_dre_relatorios`

Data Mart View unificando o Fato Demonstração de Resultados com as Dimensões.

- **Grão:** 1 linha por instituição e data-base (visão desnormalizada de fato_demonstracao_resultado, 2000–2024)
- **Chave:** `id_instituicao, id_data`

| Coluna | Tipo DuckDB | Descrição |
| :--- | :--- | :--- |
| `id_instituicao` | `VARCHAR` | Chave da instituição (FK para dim_instituicao). |
| `id_data` | `INTEGER` | Chave da data (FK para dim_tempo). |
| `codigo_origem` | `BIGINT` |  |
| `nome_instituicao` | `VARCHAR` | Nome da instituição. |
| `nome_instituicao_historico` | `VARCHAR` |  |
| `tipo_instituicao` | `VARCHAR` | Classificação Original. |
| `nome_conglomerado` | `VARCHAR` | Nome do conglomerado pertencente. |
| `tipo_relatorio_bcb` | `VARCHAR` | Qual dos 4 tipos de relatório oficiais do BCB esta linha pertence. |
| `segmento` | `VARCHAR` | Segmento de atuação. |
| `segmento_descricao` | `VARCHAR` |  |
| `cidade` | `VARCHAR` | Cidade da sede. |
| `uf` | `VARCHAR` | UF da sede. |
| `regiao` | `VARCHAR` | Região da sede. |
| `tipo_de_controle` | `VARCHAR` | Qual a natureza do controle acionário (Público, Privado Nacional, etc). |
| `tcb` | `VARCHAR` | Sigla do Tipo de Consolidado Bancário (ex: b1, b2, b3C, n4). |
| `consolidado_bancario` | `VARCHAR` | Descrição completa do Tipo de Consolidado Bancário. |
| `classe_instituicao` | `VARCHAR` | Classe da instituição. |
| `data_base` | `DATE` | Data-base de referência. |
| `rendas_operacoes_de_credito` | `DOUBLE` | (a1) Rendas de Operações de Crédito |
| `rendas_operacoes_de_arrendamento_mercantil` | `DOUBLE` | (a2) Rendas de Operações de Arrendamento Mercantil |
| `rendas_operacoes_tvm` | `DOUBLE` | (a3) Rendas de Operações com TVM |
| `rendas_operacoes_instrumentos_financeiros_derivativos` | `DOUBLE` | (a4) Rendas de Operações com Instrumentos Financeiros Derivativos |
| `resultado_operacoes_cambio` | `DOUBLE` | (a5/b4) Resultado de Operações de Câmbio |
| `rendas_aplicacoes_compulsorias` | `DOUBLE` | (a6) Rendas de Aplicações Compulsórias |
| `receitas_intermediacao_financeira` | `DOUBLE` | (a) Receitas de Intermediação Financeira |
| `despesas_captacao` | `DOUBLE` | (b1) Despesas de Captação |
| `despesas_obrigacoes_emprestimos_repasses` | `DOUBLE` | (b2) Despesas de Obrigações por Empréstimos e Repasses |
| `despesas_operacoes_arrendamento_mercantil` | `DOUBLE` | (b3) Despesas de Operações de Arrendamento Mercantil |
| `despesas_operacoes_cambio` | `DOUBLE` |  |
| `resultado_provisao_creditos_dificil_liquidacao` | `DOUBLE` | (b5) Resultado de Provisão para Créditos de Difícil Liquidação |
| `despesas_intermediacao_financeira` | `DOUBLE` | (b) Despesas de Intermediação Financeira |
| `resultado_intermediacao_financeira` | `DOUBLE` | (c) Resultado de Intermediação Financeira |
| `rendas_prestacao_servicos` | `DOUBLE` | (d1) Rendas de Prestação de Serviços |
| `rendas_tarifas_bancarias` | `DOUBLE` | (d2) Rendas de Tarifas Bancárias |
| `despesas_pessoal` | `DOUBLE` | (d3) Despesas de Pessoal |
| `despesas_administrativas` | `DOUBLE` | (d4) Despesas Administrativas |
| `despesas_tributarias` | `DOUBLE` | (d5) Despesas Tributárias |
| `resultado_participacoes` | `DOUBLE` | (d6) Resultado de Participações |
| `outras_receitas_operacionais` | `DOUBLE` | (d7) Outras Receitas Operacionais |
| `outras_despesas_operacionais` | `DOUBLE` | (d8) Outras Despesas Operacionais |
| `outras_receitas_despesas_operacionais` | `DOUBLE` | (d) Outras Receitas/Despesas Operacionais |
| `resultado_operacional` | `DOUBLE` | (e) Resultado Operacional |
| `resultado_nao_operacional` | `DOUBLE` | (f) Resultado Não Operacional |
| `resultado_antes_tributacao` | `DOUBLE` | (g) Resultado antes da Tributação, Lucro e Participação |
| `imposto_renda_contribuicao_social` | `DOUBLE` | (h) Imposto de Renda e Contribuição Social |
| `participacao_lucros` | `DOUBLE` | (i) Participação nos Lucros |
| `lucro_liquido` | `DOUBLE` | (j) Lucro Líquido |
| `juros_sobre_capital` | `DOUBLE` | (k) Juros Sobre Capital Social/Próprio |
| `roe` | `DOUBLE` |  |
| `roa` | `DOUBLE` |  |

### `view_instituicoes_historico_nomes`

Data Mart View focada exclusivamente no acompanhamento histórico (De-Para) de mudanças de nome das instituições nos relatórios do Bacen.

- **Grão:** 1 linha por instituição e data-base com comparação de nome anterior via LAG (2000–2024)
- **Chave:** `id_instituicao, id_data`

| Coluna | Tipo DuckDB | Descrição |
| :--- | :--- | :--- |
| `id_instituicao` | `VARCHAR` | Chave da instituição (FK para dim_instituicao). |
| `id_data` | `INTEGER` | Chave da data (FK para dim_tempo). |
| `codigo_origem` | `BIGINT` | Código original no Bacen. |
| `nome_instituicao` | `VARCHAR` | Nome oficial e mais atualizado da instituição (Dimensional). |
| `nome_instituicao_anterior` | `VARCHAR` | Nome que constava no relatório imediatamente anterior a este. |
| `nome_instituicao_historico` | `VARCHAR` | Nome exato que a instituição declarou no Bacen nesta data-base. |
| `houve_mudanca_nome` | `BOOLEAN` | Flag (true/false) sinalizando se houve troca no nome em relação ao período anterior (uso para analistas filtrarem os momentos de mudança). |
| `tipo_instituicao` | `VARCHAR` | Classificação Original. |
| `nome_conglomerado` | `VARCHAR` | Nome do conglomerado pertencente. |
| `tipo_relatorio_bcb` | `VARCHAR` | Qual dos 4 tipos de relatório oficiais do BCB esta linha pertence. |
| `segmento` | `VARCHAR` | Segmento de atuação. |
| `cidade` | `VARCHAR` | Cidade da sede. |
| `uf` | `VARCHAR` | UF da sede. |
| `regiao` | `VARCHAR` | Região da sede. |
| `tipo_de_controle` | `VARCHAR` | Qual a natureza do controle acionário (Público, Privado Nacional, etc). |
| `tcb` | `VARCHAR` | Sigla do Tipo de Consolidado Bancário (ex: b1, b2, b3C, n4). |
| `consolidado_bancario` | `VARCHAR` | Descrição completa do Tipo de Consolidado Bancário. |
| `classe_instituicao` | `VARCHAR` | Classe da instituição. |
| `data_base` | `DATE` | Data-base de referência (Temporal). |

### `view_resumo_financeiro_relatorios`

Data Mart View unificando o Fato Resumo Financeiro com as Dimensões, facilitando o filtro por Tipo de Relatório BCB.

- **Grão:** 1 linha por instituição e data-base (visão desnormalizada de fato_resumo_financeiro, 2000–2024)
- **Chave:** `id_instituicao, id_data`

| Coluna | Tipo DuckDB | Descrição |
| :--- | :--- | :--- |
| `id_instituicao` | `VARCHAR` | Chave da instituição (FK para dim_instituicao). |
| `id_data` | `INTEGER` | Chave da data (FK para dim_tempo). |
| `codigo_origem` | `BIGINT` |  |
| `nome_instituicao` | `VARCHAR` | Nome da instituição. |
| `nome_instituicao_historico` | `VARCHAR` |  |
| `tipo_instituicao` | `VARCHAR` |  |
| `nome_conglomerado` | `VARCHAR` |  |
| `tipo_relatorio_bcb` | `VARCHAR` | Qual dos 4 tipos de relatório oficiais do BCB esta linha pertence. |
| `segmento` | `VARCHAR` |  |
| `segmento_descricao` | `VARCHAR` |  |
| `cidade` | `VARCHAR` |  |
| `uf` | `VARCHAR` |  |
| `regiao` | `VARCHAR` |  |
| `tipo_de_controle` | `VARCHAR` |  |
| `tcb` | `VARCHAR` |  |
| `consolidado_bancario` | `VARCHAR` |  |
| `data_base` | `DATE` |  |
| `ativo_total` | `DOUBLE` |  |
| `carteira_credito` | `DOUBLE` |  |
| `passivo_exigivel` | `DOUBLE` |  |
| `captacoes` | `DOUBLE` |  |
| `patrimonio_liquido` | `DOUBLE` |  |
| `lucro_liquido` | `DOUBLE` |  |
| `quantidade_agencias` | `BIGINT` |  |
| `quantidade_postos_atendimento` | `BIGINT` |  |
| `roe` | `DOUBLE` |  |
| `roa` | `DOUBLE` |  |

### `view_resumo_prudencial_serie`

- **Grão:** 1 linha por instituição prudencial e data-base conciliando Ativo Total e PL de 2014-03 a 2026-06

| Coluna | Tipo DuckDB | Descrição |
| :--- | :--- | :--- |
| `data_base` | `DATE` | Data de referência do trimestre (DATE, 2014-03-01 a 2026-06-01). |
| `codigo` | `VARCHAR` | Código identificador da instituição no Bacen (VARCHAR). |
| `instituicao` | `VARCHAR` | Nome histórico da instituição na data-base. |
| `ativo_total` | `DECIMAL(38,8)` | Ativo Total em R$ mil (DECIMAL(38,8)). |
| `patrimonio_liquido` | `DECIMAL(38,8)` | Patrimônio Líquido em R$ mil (DECIMAL(38,8)). |
| `regime_contabil` | `VARCHAR` | Regime COSIF da observação ('cosif_ate_2024' ou 'cosif_desde_2025'). |
| `escopo` | `VARCHAR` | Escopo fixo 'prudential_conglomerates'. |
| `unidade` | `VARCHAR` | Unidade monetária fixa 'BRL mil'. |

---

## Detalhamento das Dimensões

### `dim_atividade`

- **Grão:** 1 linha por setor de atividade econômica (CNAE)

| Coluna | Tipo DuckDB | Descrição |
| :--- | :--- | :--- |
| `id_atividade` | `INTEGER` |  |
| `nome_atividade` | `VARCHAR` |  |
| `prefixo_coluna` | `VARCHAR` |  |

### `dim_classe_instituicao`

Dimensão de Classe/Tipo Detalhado da Instituição.

- **Grão:** 1 linha por classe detalhada de instituição
- **Chave:** `id_classe`

| Coluna | Tipo DuckDB | Descrição |
| :--- | :--- | :--- |
| `id_classe` | `VARCHAR` |  |
| `codigo` | `INTEGER` |  |
| `descricao` | `VARCHAR` |  |

### `dim_consolidado`

Dimensão de Tipo de Consolidado Bancário.

- **Grão:** 1 linha por código de consolidado bancário (TCB)
- **Chave:** `id_consolidado`

| Coluna | Tipo DuckDB | Descrição |
| :--- | :--- | :--- |
| `id_consolidado` | `VARCHAR` |  |
| `codigo` | `VARCHAR` |  |
| `descricao` | `VARCHAR` |  |

### `dim_controle`

Dimensão de Tipo de Controle de Capital.

- **Grão:** 1 linha por tipo de controle societário
- **Chave:** `id_controle`

| Coluna | Tipo DuckDB | Descrição |
| :--- | :--- | :--- |
| `id_controle` | `VARCHAR` |  |
| `codigo` | `INTEGER` |  |
| `descricao` | `VARCHAR` |  |

### `dim_faixa_vencimento`

- **Grão:** 1 linha por faixa de prazo de vencimento

| Coluna | Tipo DuckDB | Descrição |
| :--- | :--- | :--- |
| `id_faixa` | `INTEGER` |  |
| `nome_faixa` | `VARCHAR` |  |
| `ordem` | `INTEGER` |  |
| `sufixo_coluna` | `VARCHAR` |  |

### `dim_instituicao`

Dimensão de Instituições. Unifica dados de Conglomerados Prudenciais, Financeiros e Instituições Independentes.

- **Grão:** 1 linha por instituição por escopo institucional (codigo_origem + tipo_instituicao)
- **Chave:** `id_instituicao`
- **Chaves estrangeiras:** `id_segmento` -> `dim_segmento.id_segmento`, `id_localizacao` -> `dim_localizacao.id_localizacao`, `id_controle` -> `dim_controle.id_controle`, `id_consolidado` -> `dim_consolidado.id_consolidado`, `id_classe` -> `dim_classe_instituicao.id_classe`

| Coluna | Tipo DuckDB | Descrição |
| :--- | :--- | :--- |
| `id_instituicao` | `VARCHAR` | Chave primária substituta (Surrogate Key) gerada via MD5 do código da instituição. |
| `codigo_origem` | `BIGINT` | Código original da instituição no Bacen. |
| `nome` | `VARCHAR` | Nome da instituição. |
| `tipo_instituicao` | `VARCHAR` | Tipo da fonte de dados (Conglomerado Prudencial, Financeiro, etc). |
| `tipo_relatorio_bcb` | `VARCHAR` | Classificação padronizada para os 4 tipos oficiais de relatório do BCB IF.data. |
| `id_segmento` | `VARCHAR` | Chave estrangeira para dim_segmento (Segmento Prudencial). |
| `id_localizacao` | `VARCHAR` | Chave estrangeira para dim_localizacao (região, UF, cidade). |
| `id_controle` | `VARCHAR` | Chave estrangeira para dim_controle (Tipo de Controle). |
| `id_consolidado` | `VARCHAR` | Chave estrangeira para dim_consolidado (Consolidado Bancário). |
| `id_classe` | `VARCHAR` | Chave estrangeira para dim_classe_instituicao (Tipo detalhado). |
| `nome_conglomerado` | `VARCHAR` | Nome do conglomerado ao qual a instituição pertence. Específico para Instituições Individuais. |

### `dim_localizacao`

Dimensão de Localidade (Cidade, UF, Região).

- **Grão:** 1 linha por combinação única de cidade, UF e região
- **Chave:** `id_localizacao`

| Coluna | Tipo DuckDB | Descrição |
| :--- | :--- | :--- |
| `id_localizacao` | `VARCHAR` | Chave primária (MD5 de Cidade + UF + Região). |
| `cidade` | `VARCHAR` | Cidade da instituição. |
| `uf` | `VARCHAR` | Unidade Federativa. |
| `regiao` | `VARCHAR` | Região Geográfica. |

### `dim_porte`

- **Grão:** 1 linha por porte do tomador PJ

| Coluna | Tipo DuckDB | Descrição |
| :--- | :--- | :--- |
| `id_porte` | `INTEGER` |  |
| `nome_porte` | `VARCHAR` |  |
| `coluna` | `VARCHAR` |  |

### `dim_produto_credito`

- **Grão:** 1 linha por modalidade de produto de crédito (PF/PJ)

| Coluna | Tipo DuckDB | Descrição |
| :--- | :--- | :--- |
| `id_produto` | `INTEGER` |  |
| `nome_produto` | `VARCHAR` |  |
| `tipo_pessoa` | `VARCHAR` |  |
| `prefixo_coluna` | `VARCHAR` |  |

### `dim_regiao`

- **Grão:** 1 linha por macrorregião geográfica

| Coluna | Tipo DuckDB | Descrição |
| :--- | :--- | :--- |
| `id_regiao` | `INTEGER` |  |
| `nome_regiao` | `VARCHAR` |  |
| `coluna` | `VARCHAR` |  |

### `dim_risco`

- **Grão:** 1 linha por nível de risco (AA a H)

| Coluna | Tipo DuckDB | Descrição |
| :--- | :--- | :--- |
| `id_risco` | `INTEGER` |  |
| `nome_risco` | `VARCHAR` |  |
| `coluna` | `VARCHAR` |  |

### `dim_segmento`

Dimensão de Segmento Prudencial (S1, S2, etc).

- **Grão:** 1 linha por segmento prudencial (S1 a S5)
- **Chave:** `id_segmento`

| Coluna | Tipo DuckDB | Descrição |
| :--- | :--- | :--- |
| `id_segmento` | `VARCHAR` |  |
| `codigo` | `VARCHAR` |  |
| `descricao` | `VARCHAR` |  |

### `dim_tempo`

Dimensão de Tempo baseada nas datas base dos relatórios.

- **Grão:** 1 linha por data-base trimestral (id_data YYYYMMDD)
- **Chave:** `id_data`

| Coluna | Tipo DuckDB | Descrição |
| :--- | :--- | :--- |
| `id_data` | `INTEGER` | Chave primária (YYYYMMDD) inteira. |
| `data` | `DATE` | Data completa. |
| `ano` | `INTEGER` |  |
| `trimestre` | `INTEGER` |  |
| `mes` | `INTEGER` |  |

### `int_instituicao_enriquecida`

Modelo intermediário reutilizável com enriquecimento dimensional da instituição para consumo dos data marts de relatório.

- **Grão:** 1 linha por instituição já enriquecida com atributos das dimensões cadastrais
- **Chave:** `id_instituicao`

| Coluna | Tipo DuckDB | Descrição |
| :--- | :--- | :--- |
| `id_instituicao` | `VARCHAR` | Chave única da instituição enriquecida. |
| `codigo_origem` | `BIGINT` | Código original da instituição no Bacen. |
| `nome_instituicao` | `VARCHAR` | Nome oficial da instituição na dimensão. |
| `tipo_instituicao` | `VARCHAR` |  |
| `nome_conglomerado` | `VARCHAR` |  |
| `tipo_relatorio_bcb` | `VARCHAR` | Tipo de relatório oficial do BCB associado à instituição. |
| `segmento` | `VARCHAR` | Código de segmento prudencial em formato padronizado. |
| `segmento_descricao` | `VARCHAR` | Descrição textual do segmento prudencial. |
| `cidade` | `VARCHAR` | Cidade da sede. |
| `uf` | `VARCHAR` | Unidade federativa da sede. |
| `regiao` | `VARCHAR` | Região geográfica da sede. |
| `tipo_de_controle` | `VARCHAR` | Descrição do tipo de controle acionário. |
| `tcb` | `VARCHAR` | Código do tipo de consolidado bancário. |
| `consolidado_bancario` | `VARCHAR` | Descrição do tipo de consolidado bancário. |
| `classe_instituicao` | `VARCHAR` | Classe detalhada da instituição. |

---

## Detalhamento das Tabelas Fato

### `fato_balanco_patrimonial`

Fato consolidada de Ativos e Passivos para todas as instituições.

- **Grão:** 1 linha por instituição (id_instituicao) e data-base (id_data)
- **Chave:** `id_instituicao, id_data`
- **Chaves estrangeiras:** `id_instituicao` -> `dim_instituicao.id_instituicao`, `id_data` -> `dim_tempo.id_data`
- **Cobertura temporal por escopo:** `Instituicao Individual` (`20000301..20241201`); `Conglomerado Financeiro` (`20000301..20241201`); `Conglomerado Prudencial` (`20140301..20241201`)

| Coluna | Tipo DuckDB | Descrição |
| :--- | :--- | :--- |
| `id_instituicao` | `VARCHAR` |  |
| `id_data` | `INTEGER` |  |
| `tipo_consolidado` | `VARCHAR` |  |
| `nome_instituicao_historico` | `VARCHAR` |  |
| `disponibilidades` | `DOUBLE` | Caixa e Equivalentes de Caixa. |
| `aplicacoes_interfinanceiras_liquidez` | `DOUBLE` |  |
| `tvm_derivativos` | `DOUBLE` |  |
| `operacoes_de_credito` | `DOUBLE` | Carteira de Crédito Total. |
| `provisao_operacoes_de_credito` | `DOUBLE` |  |
| `operacoes_de_credito_liquidas_provisao` | `DOUBLE` |  |
| `arrendamento_mercantil_a_receber` | `DOUBLE` |  |
| `imobilizado_de_arrendamento` | `DOUBLE` |  |
| `credores_antecipacao_valor_residual` | `DOUBLE` |  |
| `provisao_arrendamento_mercantil` | `DOUBLE` |  |
| `arrendamento_mercantil_liquido_de_provisao` | `DOUBLE` |  |
| `outros_creditos_liquido_de_provisao` | `DOUBLE` |  |
| `outros_ativos_realizaveis` | `DOUBLE` |  |
| `permanente_ajustado` | `DOUBLE` |  |
| `ativo_total_ajustado` | `DOUBLE` |  |
| `ativo_total` | `DOUBLE` | Ativo Total. |
| `depositos_vista` | `DOUBLE` |  |
| `depositos_poupanca` | `DOUBLE` |  |
| `depositos_interfinanceiros` | `DOUBLE` |  |
| `depositos_a_prazo` | `DOUBLE` |  |
| `conta_de_pagamento_pre_paga` | `DOUBLE` |  |
| `depositos_outros` | `DOUBLE` |  |
| `depositos` | `DOUBLE` | Depósitos Totais. |
| `captacoes_mercado_aberto` | `DOUBLE` |  |
| `letras_de_credito_imobiliario` | `DOUBLE` |  |
| `letras_de_credito_agronegocio` | `DOUBLE` |  |
| `letras_financeiras` | `DOUBLE` |  |
| `obrigacoes_titulos_e_valores_mobiliarios_exterior` | `DOUBLE` |  |
| `outros_recursos_de_aceites_e_emissao_de_titulos` | `DOUBLE` |  |
| `recursos_aceites_cambiais` | `DOUBLE` |  |
| `obrigacoes_emprestimos_repasses` | `DOUBLE` |  |
| `captacoes` | `DOUBLE` | Total de Captações (Depósitos + Outras Obrigações). |
| `obrigacoes_por_instr_financeiros_derivativos` | `DOUBLE` |  |
| `outras_obrigacoes` | `DOUBLE` |  |
| `passivo_circulante_exigivel_longo_prazo` | `DOUBLE` |  |
| `patrimonio_liquido` | `DOUBLE` | Patrimônio Líquido. |
| `passivo_total` | `DOUBLE` | Passivo Total (Exigível + PL). |

### `fato_capital_prudencial`

Fato com informações de Capital Regulatório (Basileia III).

- **Grão:** 1 linha por instituição (id_instituicao) e data-base (id_data)
- **Chave:** `id_instituicao, id_data`
- **Chaves estrangeiras:** `id_instituicao` -> `dim_instituicao.id_instituicao`, `id_data` -> `dim_tempo.id_data`
- **Cobertura temporal por escopo:** `Conglomerado Financeiro` (`20001201..20141201`); `Conglomerado Prudencial` (`20150301..20241201`)

| Coluna | Tipo DuckDB | Descrição |
| :--- | :--- | :--- |
| `id_instituicao` | `VARCHAR` |  |
| `id_data` | `INTEGER` |  |
| `capital_principal` | `DOUBLE` |  |
| `capital_complementar` | `DOUBLE` |  |
| `pr_nivel_1` | `DOUBLE` |  |
| `capital_nivel_2` | `DOUBLE` |  |
| `pr_total` | `DOUBLE` |  |
| `rwa_total` | `DOUBLE` | Ativos Ponderados pelo Risco Total. |
| `rwa_risco_credito` | `DOUBLE` |  |
| `rwa_risco_mercado` | `DOUBLE` |  |
| `rwa_risco_operacional` | `DOUBLE` |  |
| `rwa_servicos_pagamento` | `DOUBLE` |  |
| `rwa_cambio` | `DOUBLE` |  |
| `rwa_commodities` | `DOUBLE` |  |
| `rwa_juros` | `DOUBLE` |  |
| `rwa_acoes` | `DOUBLE` |  |
| `rwa_cva` | `DOUBLE` |  |
| `rwa_drc` | `DOUBLE` |  |
| `exposicao_total` | `DOUBLE` |  |
| `indice_capital_principal` | `DOUBLE` |  |
| `indice_capital_nivel_i` | `DOUBLE` |  |
| `indice_basileia` | `DOUBLE` | Índice de Basileia (PR / RWA). |
| `razao_alavancagem` | `DOUBLE` |  |
| `indice_imobilizacao` | `DOUBLE` |  |
| `adicional_capital_principal` | `DOUBLE` |  |

### `fato_carteira_credito_atividade`

Fato detalhando a carteira de crédito por atividade econômica (CNAE/Setor).

- **Grão:** 1 linha por instituição, data-base, atividade econômica (CNAE) e faixa de vencimento
- **Chave:** `id_instituicao, id_data, id_atividade_economica, id_faixa_vencimento`
- **Chaves estrangeiras:** `id_instituicao` -> `dim_instituicao.id_instituicao`
- **Cobertura temporal por escopo:** `Conglomerado Financeiro (SCR)` (`20120601..20140301`); `Conglomerado Financeiro` (`20140601..20241201`)

| Coluna | Tipo DuckDB | Descrição |
| :--- | :--- | :--- |
| `id_instituicao` | `VARCHAR` |  |
| `id_data` | `INTEGER` |  |
| `id_atividade_economica` | `INTEGER` |  |
| `id_faixa_vencimento` | `INTEGER` |  |
| `valor` | `DOUBLE` |  |

### `fato_carteira_credito_indexador`

Fato detalhando a carteira de crédito por indexador (Selic, IPCA, etc).

- **Grão:** 1 linha por instituição (id_instituicao) e data-base (id_data)
- **Chave:** `id_instituicao, id_data`
- **Chaves estrangeiras:** `id_instituicao` -> `dim_instituicao.id_instituicao`, `id_data` -> `dim_tempo.id_data`
- **Cobertura temporal por escopo:** `Conglomerado Financeiro (SCR)` (`20120601..20140301`); `Conglomerado Financeiro` (`20140601..20241201`)

| Coluna | Tipo DuckDB | Descrição |
| :--- | :--- | :--- |
| `id_instituicao` | `VARCHAR` |  |
| `id_data` | `INTEGER` |  |
| `total_carteira` | `DOUBLE` |  |
| `prefixado` | `DOUBLE` |  |
| `selic` | `DOUBLE` | Carteira indexada à SELIC. |
| `cdi` | `DOUBLE` | Carteira indexada ao CDI. |
| `tr` | `DOUBLE` |  |
| `tjlp` | `DOUBLE` |  |
| `tlp` | `DOUBLE` |  |
| `libor` | `DOUBLE` |  |
| `ipca` | `DOUBLE` |  |
| `igpm` | `DOUBLE` |  |
| `ipcc` | `DOUBLE` |  |
| `outros_indices_de_preco` | `DOUBLE` |  |
| `outras_taxas_pos_fixadas` | `DOUBLE` |  |
| `outras_taxas_flutuantes` | `DOUBLE` |  |
| `outros_indexadores` | `DOUBLE` |  |
| `total_exterior` | `DOUBLE` |  |
| `total_nao_individualizado` | `DOUBLE` |  |

### `fato_carteira_credito_porte`

Fato detalhando a carteira de crédito por porte do tomador (PJ).

- **Grão:** 1 linha por instituição, data-base e porte do tomador PJ
- **Chave:** `id_instituicao, id_data, id_porte`
- **Chaves estrangeiras:** `id_instituicao` -> `dim_instituicao.id_instituicao`
- **Cobertura temporal por escopo:** `Conglomerado Financeiro (SCR)` (`20120601..20140301`); `Conglomerado Financeiro` (`20140601..20241201`)

| Coluna | Tipo DuckDB | Descrição |
| :--- | :--- | :--- |
| `id_instituicao` | `VARCHAR` |  |
| `id_data` | `INTEGER` |  |
| `id_porte` | `INTEGER` |  |
| `valor` | `DOUBLE` |  |

### `fato_carteira_credito_produto`

Carteira de crédito por instituição, data-base, produto, faixa de vencimento e tipo de pessoa.

- **Grão:** 1 linha por instituição, data-base, produto de crédito e faixa de vencimento
- **Chave:** `id_instituicao, id_data, id_produto, id_faixa_vencimento`
- **Chaves estrangeiras:** `id_instituicao` -> `dim_instituicao.id_instituicao`, `id_data` -> `dim_tempo.id_data`
- **Cobertura temporal por escopo:** `Conglomerado Financeiro (SCR)` (`20120601..20140301`); `Conglomerado Financeiro` (`20140601..20241201`)

| Coluna | Tipo DuckDB | Descrição |
| :--- | :--- | :--- |
| `id_instituicao` | `VARCHAR` |  |
| `id_data` | `INTEGER` |  |
| `id_produto` | `INTEGER` |  |
| `id_faixa_vencimento` | `INTEGER` |  |
| `valor` | `DOUBLE` |  |
| `tipo_pessoa` | `VARCHAR` | Tipo de pessoa identificado pelo relatório de origem na Silver. |

### `fato_carteira_credito_totais`

Fato auxiliar com totais de carteira e valores não individualizados que não entram nos breakdowns dimensionais.

- **Grão:** 1 linha por instituição (id_instituicao) e data-base (id_data)
- **Chave:** `id_instituicao, id_data`
- **Chaves estrangeiras:** `id_instituicao` -> `dim_instituicao.id_instituicao`, `id_data` -> `dim_tempo.id_data`
- **Cobertura temporal por escopo:** `Conglomerado Financeiro (SCR)` (`20120601..20140301`); `Conglomerado Financeiro` (`20140601..20241201`)

| Coluna | Tipo DuckDB | Descrição |
| :--- | :--- | :--- |
| `id_instituicao` | `VARCHAR` |  |
| `id_data` | `INTEGER` |  |
| `total_carteira_pj` | `DOUBLE` | Valor Total da Carteira PJ informado nos relatórios. |
| `total_nao_individualizado_pj` | `DOUBLE` | Parcela da carteira PJ não classificada por atividade (valor baixo ou sem info). |
| `total_exterior_pj` | `DOUBLE` |  |
| `total_geral_risco` | `DOUBLE` | Valor Total da Carteira sujeita a Risco (conferência). |
| `total_carteira_pf` | `DOUBLE` | Valor Total da Carteira PF informado nos relatórios. |
| `total_exterior_pf` | `DOUBLE` | Valor Total da Carteira PF no Exterior. |

### `fato_demonstracao_resultado`

Fato consolidada de Demonstração de Resultados (DRE).

- **Grão:** 1 linha por instituição (id_instituicao) e data-base (id_data)
- **Chave:** `id_instituicao, id_data`
- **Chaves estrangeiras:** `id_instituicao` -> `dim_instituicao.id_instituicao`, `id_data` -> `dim_tempo.id_data`
- **Cobertura temporal por escopo:** `Instituicao Individual` (`20000301..20241201`); `Conglomerado Financeiro` (`20000301..20241201`); `Conglomerado Prudencial` (`20140301..20241201`)

| Coluna | Tipo DuckDB | Descrição |
| :--- | :--- | :--- |
| `id_instituicao` | `VARCHAR` |  |
| `id_data` | `INTEGER` |  |
| `nome_instituicao_historico` | `VARCHAR` |  |
| `receitas_intermediacao_financeira` | `DOUBLE` | Receitas Totais de Intermediação. |
| `rendas_operacoes_de_credito` | `DOUBLE` | Rendas de operações de crédito. |
| `rendas_operacoes_de_arrendamento_mercantil` | `DOUBLE` |  |
| `rendas_operacoes_tvm` | `DOUBLE` |  |
| `rendas_operacoes_instrumentos_financeiros_derivativos` | `DOUBLE` |  |
| `resultado_operacoes_cambio` | `DOUBLE` |  |
| `rendas_aplicacoes_compulsorias` | `DOUBLE` |  |
| `despesas_intermediacao_financeira` | `DOUBLE` | Despesas Totais de Intermediação. |
| `despesas_captacao` | `DOUBLE` | Custos de captação de recursos. |
| `despesas_obrigacoes_emprestimos_repasses` | `DOUBLE` |  |
| `despesas_operacoes_arrendamento_mercantil` | `DOUBLE` |  |
| `despesas_operacoes_cambio` | `DOUBLE` |  |
| `resultado_provisao_creditos_dificil_liquidacao` | `DOUBLE` | Impacto das provisões para devedores duvidosos (PDD). |
| `resultado_intermediacao_financeira` | `DOUBLE` | Resultado Bruto da Intermediação. |
| `rendas_prestacao_servicos` | `DOUBLE` |  |
| `rendas_tarifas_bancarias` | `DOUBLE` |  |
| `despesas_pessoal` | `DOUBLE` | Despesas de Pessoal. |
| `despesas_administrativas` | `DOUBLE` | Total de Despesas Administrativas. |
| `despesas_tributarias` | `DOUBLE` | Despesas de Impostos e Taxas. |
| `resultado_participacoes` | `DOUBLE` |  |
| `outras_receitas_operacionais` | `DOUBLE` |  |
| `outras_despesas_operacionais` | `DOUBLE` |  |
| `outras_receitas_despesas_operacionais` | `DOUBLE` |  |
| `resultado_operacional` | `DOUBLE` |  |
| `resultado_nao_operacional` | `DOUBLE` |  |
| `resultado_antes_tributacao` | `DOUBLE` |  |
| `imposto_renda_contribuicao_social` | `DOUBLE` |  |
| `participacao_lucros` | `DOUBLE` |  |
| `lucro_liquido` | `DOUBLE` | Lucro Líquido final. |
| `juros_sobre_capital` | `DOUBLE` |  |
| `roe` | `DOUBLE` |  |
| `roa` | `DOUBLE` |  |

### `fato_ifdata_2025_campos`

- **Grão:** 1 linha por escopo, relatório, data-base, linha da instituição e coluna publicada (formato longo 2025+)
- **Chave:** `id_data`
- **Cobertura temporal por escopo:** `prudential_conglomerates (14 relatórios)` (`20250301..20260601`); `financial_conglomerates (4 relatórios)` (`20250301..20260601`); `individual_institutions (4 relatórios)` (`20250301..20260601`)

| Coluna | Tipo DuckDB | Descrição |
| :--- | :--- | :--- |
| `id_data` | `INTEGER` | Chave temporal YYYYMMDD (FK lógica para dim_tempo.id_data). |
| `escopo` | `VARCHAR` | Escopo institucional em snake_case (prudential_conglomerates, financial_conglomerates, individual_institutions). |
| `relatorio` | `VARCHAR` | Identificador do relatório em snake_case (ex.: summary, assets, liabilities, income_statement, capital_information). |
| `data_base` | `DATE` | Data de referência do trimestre (DATE). |
| `linha` | `BIGINT` | Posição da linha da instituição no CSV publicado. |
| `ordem_coluna` | `INTEGER` | Posição ordinal da coluna no CSV publicado. |
| `codigo` | `VARCHAR` | Código identificador da instituição no IF.data. |
| `instituicao` | `VARCHAR` | Nome da instituição publicado na data-base. |
| `campo_original` | `VARCHAR` | Nome exato da coluna/rubrica conforme publicado pelo Bacen. |
| `eh_dimensao` | `BOOLEAN` | Indica se a coluna é atributo cadastral/dimensional (true) ou medida numérica/indicador (false). |
| `valor_original` | `VARCHAR` | Texto original publicado no CSV (preserva marcadores como NI; células vazias ficam NULL). |
| `valor_numerico` | `DECIMAL(38,8)` | Valor numérico convertido para DECIMAL(38,8) na escala publicada (percentuais em pontos percentuais). |
| `formato_valor` | `VARCHAR` | Marcador de formato ('percentual' quando em pontos percentuais; NULL nos demais casos). |
| `arquivo_origem` | `VARCHAR` | Caminho relativo do CSV bruto versionado de origem. |

### `fato_movimentacao_cambio`

Fato de Movimentação no Mercado de Câmbio (Fluxo de Moedas).

- **Grão:** 1 linha por instituição de câmbio (id_instituicao) e data-base (id_data)
- **Chave:** `id_instituicao, id_data`
- **Chaves estrangeiras:** `id_instituicao` -> `dim_instituicao.id_instituicao`, `id_data` -> `dim_tempo.id_data`
- **Cobertura temporal por escopo:** `Instituição de Câmbio` (`20141201..20230601`)

| Coluna | Tipo DuckDB | Descrição |
| :--- | :--- | :--- |
| `id_instituicao` | `VARCHAR` |  |
| `id_data` | `INTEGER` |  |
| `operacoes_comerciais_compra_numero_operacoes` | `BIGINT` |  |
| `operacoes_comerciais_compra_valor` | `DOUBLE` |  |
| `operacoes_comerciais_venda_numero_operacoes` | `BIGINT` |  |
| `operacoes_comerciais_venda_valor` | `DOUBLE` |  |
| `operacoes_comerciais_total_numero_operacoes` | `BIGINT` |  |
| `operacoes_comerciais_total_valor` | `DOUBLE` |  |
| `operacoes_financeiras_compra_numero_operacoes` | `BIGINT` |  |
| `operacoes_financeiras_compra_valor` | `DOUBLE` |  |
| `operacoes_financeiras_venda_numero_operacoes` | `BIGINT` |  |
| `operacoes_financeiras_venda_valor` | `DOUBLE` |  |
| `operacoes_financeiras_total_numero_operacoes` | `BIGINT` |  |
| `operacoes_financeiras_total_valor` | `DOUBLE` |  |
| `mercado_primario_total_numero_operacoes` | `BIGINT` |  |
| `mercado_primario_total_valor` | `DOUBLE` |  |
| `mercado_interbancario_compra_numero_operacoes` | `BIGINT` |  |
| `mercado_interbancario_compra_valor` | `DOUBLE` |  |
| `mercado_interbancario_venda_numero_operacoes` | `BIGINT` |  |
| `mercado_interbancario_venda_valor` | `DOUBLE` |  |
| `mercado_interbancario_total_numero_operacoes` | `BIGINT` |  |
| `mercado_interbancario_total_valor` | `DOUBLE` |  |
| `total_geral_numero_operacoes` | `BIGINT` |  |
| `total_geral_valor` | `DOUBLE` | Valor total das operações (Primário + Interbancário) em milhares de USD. |

### `fato_operacoes_clientes`

Fato com contagem de clientes e operações ativas.

- **Grão:** 1 linha por instituição (id_instituicao) e data-base (id_data)
- **Chave:** `id_instituicao, id_data`
- **Chaves estrangeiras:** `id_instituicao` -> `dim_instituicao.id_instituicao`, `id_data` -> `dim_tempo.id_data`
- **Cobertura temporal por escopo:** `Conglomerado Financeiro (SCR)` (`20120601..20140301`); `Conglomerado Financeiro` (`20140601..20241201`)

| Coluna | Tipo DuckDB | Descrição |
| :--- | :--- | :--- |
| `id_instituicao` | `VARCHAR` |  |
| `id_data` | `INTEGER` |  |
| `quantidade_clientes` | `BIGINT` | Número de clientes com operações ativas. |
| `quantidade_operacoes` | `BIGINT` |  |

### `fato_regiao_credito`

Fato detalhando a carteira de crédito por região geográfica.

- **Grão:** 1 linha por instituição, data-base e região geográfica
- **Chave:** `id_instituicao, id_data, id_regiao`
- **Chaves estrangeiras:** `id_regiao` -> `dim_regiao.id_regiao`
- **Cobertura temporal por escopo:** `Conglomerado Financeiro (SCR)` (`20120601..20140301`); `Conglomerado Financeiro` (`20140901..20241201`)

| Coluna | Tipo DuckDB | Descrição |
| :--- | :--- | :--- |
| `id_instituicao` | `VARCHAR` |  |
| `id_data` | `INTEGER` |  |
| `id_regiao` | `INTEGER` |  |
| `valor` | `DOUBLE` |  |

### `fato_resumo_financeiro`

Fato com métricas financeiras resumidas (Ativo Total, Lucro, Patrimônio) para visualização rápida.

- **Grão:** 1 linha por instituição (id_instituicao) e data-base (id_data)
- **Chave:** `id_instituicao, id_data`
- **Chaves estrangeiras:** `id_instituicao` -> `dim_instituicao.id_instituicao`, `id_data` -> `dim_tempo.id_data`
- **Cobertura temporal por escopo:** `Instituicao Individual` (`20000301..20241201`); `Conglomerado Financeiro` (`20000301..20241201`); `Conglomerado Prudencial` (`20140301..20241201`)

| Coluna | Tipo DuckDB | Descrição |
| :--- | :--- | :--- |
| `id_instituicao` | `VARCHAR` |  |
| `id_data` | `INTEGER` |  |
| `nome_instituicao_historico` | `VARCHAR` |  |
| `ativo_total` | `DOUBLE` | Ativo Total em milhares de R$. |
| `carteira_credito` | `DOUBLE` | Carteira de Crédito Classificada em milhares de R$. |
| `passivo_exigivel` | `DOUBLE` | Passivo Circulante e Exigível a Longo Prazo. |
| `captacoes` | `DOUBLE` | Captações Totais. |
| `patrimonio_liquido` | `DOUBLE` | Patrimônio Líquido. |
| `lucro_liquido` | `DOUBLE` | Lucro Líquido do período. |
| `quantidade_agencias` | `BIGINT` | Número de agências físicas. |
| `quantidade_postos_atendimento` | `BIGINT` | Número de postos de atendimento. |
| `roe` | `DOUBLE` | Return on Equity (Lucro / PL). |
| `roa` | `DOUBLE` | Return on Assets (Lucro / Ativo Total). |

### `fato_risco_credito`

Fato detalhando a carteira de crédito por nível de risco.

- **Grão:** 1 linha por instituição, data-base e nível de risco (AA–H)
- **Chave:** `id_instituicao, id_data, id_nivel_risco`
- **Chaves estrangeiras:** `id_instituicao` -> `dim_instituicao.id_instituicao`
- **Cobertura temporal por escopo:** `Conglomerado Financeiro (SCR)` (`20120601..20140301`); `Conglomerado Financeiro` (`20140601..20241201`)

| Coluna | Tipo DuckDB | Descrição |
| :--- | :--- | :--- |
| `id_instituicao` | `VARCHAR` |  |
| `id_data` | `INTEGER` |  |
| `id_nivel_risco` | `INTEGER` |  |
| `valor` | `DOUBLE` |  |

---

## Tabelas de Domínio (Seeds)

Valores categóricos oficiais carregados nas dimensões via `src/bacen_ifdata/data_analytics/seeds/`. Use estes valores exatos em filtros `WHERE`.

### `seed_dim_atividade`

| `id_atividade` | `nome_atividade` | `prefixo_coluna` |
| :--- | :--- | :--- |
| 1 | Agricultura | agricultura |
| 2 | Industrias de Transformacao | industrias_transformacao |
| 3 | Construcao | construcao |
| 4 | Servicos Industriais | servicos_industriais |
| 5 | Industrias Extrativas | industrias_extrativas |
| 6 | Comercio | comercio |
| 7 | Administracao Publica | administracao_publica |
| 8 | Transporte | transporte |
| 9 | Outros | outros |
| 10 | Exterior | total_exterior |

### `seed_dim_classe_instituicao`

| `codigo` | `descricao` |
| :--- | :--- |
| 1 | Banco do Brasil - Banco Múltiplo |
| 2 | Banco Comercial |
| 3 | Banco Comercial Cooperativo |
| 4 | BNDES |
| 5 | Banco de Desenvolvimento |
| 6 | Caixa Econômica Federal |
| 7 | Caixa Econômica Estadual |
| 8 | Banco Múltiplo |
| 9 | Cooperativa de Crédito |
| 10 | Sociedade de Crédito ao Microempreendedor |
| 11 | Banco Múltiplo Cooperativo |
| 13 | Banco de Investimento |
| 14 | Sociedade de Crédito, Financiamento e Investimento |
| 15 | Sociedade Corretora de TVM |
| 16 | Sociedade Distribuidora de TVM |
| 19 | Sociedade de Arrendamento Mercantil |
| 20 | Sociedade de Crédito Imobiliário |
| 21 | Sociedade Corretora de Câmbio |
| 25 | Associação de Poupança e Empréstimo |
| 28 | Banco Comercial Estrangeiro - Filial no país |
| 29 | Companhia Hipotecária |
| 30 | Agência de Fomento |
| 31 | Sociedade de Crédito Imobiliário - Repassadora |
| 39 | Banco de Câmbio |
| 41 | Instituições de Pagamento |
| 43 | Sociedades de Crédito Direto |
| 44 | Sociedades de Empréstimo entre Pessoas |
| 196 | Conglomerado de Mercado de Capitais |
| 197 | Conglomerado Não-Bancário de Crédito |
| 198 | Conglomerado - Bancário II |
| 199 | Conglomerado - Bancário I |
| 38 | Cooperativa Central de Crédito |

### `seed_dim_consolidado`

| `codigo` | `descricao` |
| :--- | :--- |
| b1 | Banco Comercial, Banco Múltiplo com Carteira Comercial ou Caixas Econômicas. |
| b2 | Banco Múltiplo sem Carteira Comercial ou Banco de Câmbio ou Banco de Investimento. |
| b3s | Cooperativa de Crédito Singular. |
| b3c | Central e Confederação de Cooperativas de Crédito. |
| b4 | Banco de Desenvolvimento. |
| n1 | Instituição não bancária atuante no mercado de crédito. |
| n2 | Instituição não bancária atuante no mercado de capitais. |
| n4 | Instituições de pagamento. |
| z2 |  |

### `seed_dim_controle`

| `codigo` | `descricao` |
| :--- | :--- |
| 1 | Público |
| 2 | Privado Nacional |
| 3 | Controle Estrangeiro |

### `seed_dim_faixa_vencimento`

| `id_faixa` | `nome_faixa` | `ordem` | `sufixo_coluna` |
| :--- | :--- | :--- | :--- |
| 1 | Vencido acima de 15 dias | 1 | _vencido_a_partir_15_dias |
| 2 | A vencer ate 90 dias | 2 | _a_vencer_ate_90_dias |
| 3 | A vencer 91 a 360 dias | 3 | _a_vencer_91_a_360_dias |
| 4 | A vencer 361 a 1080 dias | 4 | _a_vencer_361_a_1080_dias |
| 5 | A vencer 1081 a 1800 dias | 5 | _a_vencer_1081_a_1800_dias |
| 6 | A vencer 1801 a 5400 dias | 6 | _a_vencer_1801_a_5400_dias |
| 7 | A vencer acima de 5400 dias | 7 | _a_vencer_acima_5400_dias |

### `seed_dim_porte`

| `id_porte` | `nome_porte` | `coluna` |
| :--- | :--- | :--- |
| 1 | Micro | micro |
| 2 | Pequena | pequena |
| 3 | Media | media |
| 4 | Grande | grande |
| 5 | Indisponivel | indisponivel |
| 6 | Exterior | total_exterior_pessoa_juridica |

### `seed_dim_produto_credito`

| `id_produto` | `nome_produto` | `tipo_pessoa` | `prefixo_coluna` |
| :--- | :--- | :--- | :--- |
| 1 | Consignado | PF | consignacao |
| 2 | Sem Consignacao | PF | sem_consignacao |
| 3 | Veiculos | PF | veiculos |
| 4 | Habitacao | PF | habitacao |
| 5 | Cartao de Credito | PF | cartao_credito |
| 6 | Rural e Agroindustrial | Ambos | rural_agroindustrial |
| 7 | Outros Creditos | Ambos | outros_creditos |
| 8 | Capital de Giro | PJ | capital_giro |
| 9 | Investimento | PJ | investimento |
| 10 | Cheque Especial e Conta Garantida | PJ | cheque_especial_conta_garantida |
| 11 | Operacoes com Recebiveis | PJ | operacoes_recebiveis |
| 12 | Comercio Exterior | PJ | comercio_exterior |
| 13 | Financiamento Infraestrutura | PJ | financiamento_infraestrutura |
| 14 | Habitacao PJ | PJ | habitacional |

### `seed_dim_regiao`

| `id_regiao` | `nome_regiao` | `coluna` |
| :--- | :--- | :--- |
| 1 | Sudeste | sudeste |
| 2 | Centro-Oeste | centro_oeste |
| 3 | Nordeste | nordeste |
| 4 | Norte | norte |
| 5 | Sul | sul |
| 6 | Nao Informado | regiao_nao_informada |
| 7 | Exterior | total_exterior |

### `seed_dim_risco`

| `id_risco` | `nome_risco` | `coluna` |
| :--- | :--- | :--- |
| 1 | AA | aa |
| 2 | A | a |
| 3 | B | b |
| 4 | C | c |
| 5 | D | d |
| 6 | E | e |
| 7 | F | f |
| 8 | G | g |
| 9 | H | h |
| 10 | Exterior | total_exterior |

### `seed_dim_segmento`

| `codigo` | `descricao` |
| :--- | :--- |
| s1 | Bancos múltiplos, bancos comerciais, bancos de investimento, bancos de câmbio e caixas econômicas de grande porte. |
| s2 | Bancos e demais instituições de médio porte. |
| s3 | Instituições de porte inferior a 1% e igual ou superior a 0.1% do PIB. |
| s4 | Instituições de porte inferior a 0.1%. |
| s5 | Instituições de pequeno porte com metodologia simplificada. |
