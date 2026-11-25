# Cookbook de Consultas Analíticas (DuckDB e Python)

Receitas canônicas de SQL e Python para consultar o `gold_warehouse.duckdb` gerado pelo `bacen-ifdata-scraper`. Todas as consultas abaixo respeitam as [Regras de Domínio](DOMAIN_RULES.md) e foram executadas contra o warehouse Gold publicado em modo somente leitura.

---

## 1. Conexão Segura em Python (`duckdb` + `polars`)

Resolva o caminho da release ativa automaticamente via `warehouse_path('gold')` e abra o banco em modo `read_only=True`:

```python
import duckdb
from bacen_ifdata.utilities.releases import warehouse_path

gold_db = warehouse_path('gold')

with duckdb.connect(str(gold_db), read_only=True) as con:
    df = con.execute(
        """
        SELECT nome_instituicao, segmento, ativo_total / 1e6 AS ativo_bi_brl
        FROM view_resumo_financeiro_relatorios
        WHERE id_data = 20241201
          AND tipo_instituicao = 'Conglomerado Prudencial'
        ORDER BY ativo_total DESC NULLS LAST
        LIMIT 10
        """
    ).pl()

print(df)
```

---

## 2. Ranking de Instituições em uma Data-Base

Usa `view_resumo_financeiro_relatorios` filtrando apenas `Conglomerado Prudencial` para evitar dupla contagem. Valores monetários são convertidos de `R$ mil` para bilhões de reais (`1e6`).

```sql
SELECT
    nome_instituicao,
    segmento,
    tipo_de_controle,
    ROUND(ativo_total / 1e6, 2) AS ativo_total_bi,
    ROUND(patrimonio_liquido / 1e6, 2) AS pl_bi,
    ROUND(captacoes / 1e6, 2) AS captacoes_bi,
    ROUND(lucro_liquido / 1e6, 2) AS lucro_semestral_bi
FROM view_resumo_financeiro_relatorios
WHERE id_data = 20241201
  AND tipo_instituicao = 'Conglomerado Prudencial'
ORDER BY ativo_total DESC NULLS LAST
LIMIT 15;
```

---

## 3. Evolução de Ativos e Patrimônio Líquido por Segmento Prudencial (S1–S5)

Mostra a concentração de ativos por segmento prudencial (`S1` a `S5`) ao final de cada ano entre 2020 e 2024:

```sql
SELECT
    EXTRACT(YEAR FROM data_base)::INT AS ano,
    segmento,
    COUNT(DISTINCT id_instituicao) AS qtd_instituicoes,
    ROUND(SUM(ativo_total) / 1e6, 2) AS ativo_total_bi,
    ROUND(SUM(patrimonio_liquido) / 1e6, 2) AS pl_total_bi
FROM view_resumo_financeiro_relatorios
WHERE tipo_instituicao = 'Conglomerado Prudencial'
  AND id_data IN (20201201, 20211201, 20221201, 20231201, 20241201)
  AND segmento IS NOT NULL
GROUP BY 1, 2
ORDER BY 1, 2;
```

---

## 4. Solvência e Capital Prudencial (Basileia, Capital Principal e Imobilização)

Consulta `fato_capital_prudencial` a partir de 2015 sob `Conglomerado Prudencial`. Multiplica os índices por `100` apenas na apresentação:

```sql
SELECT
    i.nome AS instituicao,
    s.codigo AS segmento,
    ROUND(c.pr_total / 1e6, 2) AS pr_total_bi,
    ROUND(c.rwa_total / 1e6, 2) AS rwa_total_bi,
    ROUND(c.indice_capital_principal * 100, 2) AS cet1_pct,
    ROUND(c.indice_basileia * 100, 2) AS basileia_pct,
    ROUND(c.indice_imobilizacao * 100, 2) AS imobilizacao_pct
FROM fato_capital_prudencial c
JOIN dim_instituicao i ON c.id_instituicao = i.id_instituicao
LEFT JOIN dim_segmento s ON i.id_segmento = s.id_segmento
WHERE c.id_data = 20241201
  AND i.tipo_instituicao = 'Conglomerado Prudencial'
ORDER BY c.pr_total DESC NULLS LAST
LIMIT 15;
```

---

## 5. Lucro Líquido Anual e ROE Anualizado Correto (Regra Semestral da DRE)

Na DRE do IF.data, junho (`06`) acumula o 1º semestre e dezembro (`12`) acumula o 2º semestre. O lucro anual correto soma apenas `06` + `12`, e o ROE anual divide o lucro anual pelo patrimônio líquido médio do ano:

```sql
WITH dre_semestres AS (
    SELECT
        id_instituicao,
        nome_instituicao,
        EXTRACT(YEAR FROM data_base)::INT AS ano,
        SUM(lucro_liquido) AS lucro_anual_mil
    FROM view_dre_relatorios
    WHERE tipo_instituicao = 'Conglomerado Prudencial'
      AND id_data IN (20240601, 20241201)
    GROUP BY 1, 2, 3
),
pl_medio AS (
    SELECT
        id_instituicao,
        AVG(patrimonio_liquido) AS pl_medio_mil
    FROM view_resumo_financeiro_relatorios
    WHERE tipo_instituicao = 'Conglomerado Prudencial'
      AND id_data IN (20240301, 20240601, 20240901, 20241201)
    GROUP BY 1
)
SELECT
    d.nome_instituicao,
    d.ano,
    ROUND(d.lucro_anual_mil / 1e6, 2) AS lucro_anual_bi,
    ROUND(p.pl_medio_mil / 1e6, 2) AS pl_medio_bi,
    ROUND((d.lucro_anual_mil / NULLIF(p.pl_medio_mil, 0)) * 100, 2) AS roe_anual_pct
FROM dre_semestres d
JOIN pl_medio p ON d.id_instituicao = p.id_instituicao
WHERE p.pl_medio_mil > 0
ORDER BY d.lucro_anual_mil DESC NULLS LAST
LIMIT 15;
```

---

## 6. Resultado Trimestral Isolado (1T, 2T, 3T e 4T)

Isola o resultado de cada trimestre subtraindo `03` de `06` (para o 2T) e `09` de `12` (para o 4T):

```sql
WITH base AS (
    SELECT
        nome_instituicao,
        id_data,
        EXTRACT(MONTH FROM data_base)::INT AS mes,
        lucro_liquido,
        LAG(lucro_liquido) OVER (
            PARTITION BY id_instituicao
            ORDER BY id_data
        ) AS lucro_trimestre_anterior
    FROM view_dre_relatorios
    WHERE tipo_instituicao = 'Conglomerado Prudencial'
      AND id_data BETWEEN 20240301 AND 20241201
      AND nome_instituicao = 'ITAU - PRUDENCIAL'
)
SELECT
    id_data,
    ROUND(lucro_liquido / 1e6, 2) AS lucro_acumulado_semestre_bi,
    ROUND(
        CASE
            WHEN mes IN (3, 9) THEN lucro_liquido
            ELSE lucro_liquido - lucro_trimestre_anterior
        END / 1e6,
        2
    ) AS lucro_trimestral_isolado_bi
FROM base
ORDER BY id_data;
```

---

## 7. Carteira de Crédito por Modalidade (PF/PJ) e Prazo de Vencimento

Lembre-se: fatos de carteira de crédito existem sob `Conglomerado Financeiro` (`2014-06`..`2024-12`) e `Conglomerado Financeiro (SCR)` (`2012-06`..`2014-03`). Note o join `c.id_faixa_vencimento = f.id_faixa`:

```sql
SELECT
    p.tipo_pessoa,
    p.nome_produto,
    f.nome_faixa,
    ROUND(SUM(c.valor) / 1e6, 2) AS carteira_bi
FROM fato_carteira_credito_produto c
JOIN dim_instituicao i ON c.id_instituicao = i.id_instituicao
JOIN dim_produto_credito p ON c.id_produto = p.id_produto
JOIN dim_faixa_vencimento f ON c.id_faixa_vencimento = f.id_faixa
WHERE c.id_data = 20241201
  AND i.tipo_instituicao = 'Conglomerado Financeiro'
GROUP BY 1, 2, 3, f.ordem
ORDER BY carteira_bi DESC NULLS LAST
LIMIT 15;
```

---

## 8. Distribuição da Carteira de Crédito por Nível de Risco (AA–H) e por Região

### Por nível de risco (`fato_risco_credito`)

Note o join `r.id_nivel_risco = dr.id_risco`:

```sql
SELECT
    dr.nome_risco,
    ROUND(SUM(r.valor) / 1e6, 2) AS carteira_bi,
    ROUND(
        SUM(r.valor) * 100.0 / SUM(SUM(r.valor)) OVER (),
        2
    ) AS participacao_pct
FROM fato_risco_credito r
JOIN dim_instituicao i ON r.id_instituicao = i.id_instituicao
JOIN dim_risco dr ON r.id_nivel_risco = dr.id_risco
WHERE r.id_data = 20241201
  AND i.tipo_instituicao = 'Conglomerado Financeiro'
GROUP BY dr.nome_risco
ORDER BY dr.nome_risco;
```

### Por região geográfica (`fato_regiao_credito`)

```sql
SELECT
    reg.nome_regiao,
    ROUND(SUM(rc.valor) / 1e6, 2) AS carteira_bi
FROM fato_regiao_credito rc
JOIN dim_instituicao i ON rc.id_instituicao = i.id_instituicao
JOIN dim_regiao reg ON rc.id_regiao = reg.id_regiao
WHERE rc.id_data = 20241201
  AND i.tipo_instituicao = 'Conglomerado Financeiro'
GROUP BY reg.nome_regiao
ORDER BY carteira_bi DESC NULLS LAST;
```

---

## 9. Rastreamento de Mudanças de Nome de Instituições

Identifica alterações de razão social ou marcas ao longo da série histórica usando `view_instituicoes_historico_nomes`:

```sql
SELECT
    data_base,
    codigo_origem,
    tipo_instituicao,
    nome_instituicao_anterior,
    nome_instituicao_historico AS novo_nome
FROM view_instituicoes_historico_nomes
WHERE houve_mudanca_nome = true
  AND tipo_instituicao = 'Conglomerado Prudencial'
ORDER BY data_base DESC
LIMIT 20;
```

---

## 10. Série Contínua 2014–2026 Cruzando o Novo COSIF (`view_resumo_prudencial_serie`)

Concilia `Ativo Total` e `Patrimônio Líquido` de `Conglomerado Prudencial` entre o regime histórico (`cosif_ate_2024`) e o regime atual da Resolução CMN nº 4.966 (`cosif_desde_2025`), preservando o marcador `regime_contabil`:

```sql
SELECT
    data_base,
    regime_contabil,
    COUNT(DISTINCT codigo) AS qtd_conglomerados,
    ROUND(SUM(ativo_total) / 1e6, 2) AS ativo_total_bi,
    ROUND(SUM(patrimonio_liquido) / 1e6, 2) AS pl_total_bi
FROM view_resumo_prudencial_serie
WHERE data_base BETWEEN DATE '2024-06-01' AND DATE '2026-06-01'
GROUP BY 1, 2
ORDER BY 1;
```

---

## 11. Consulta Direta ao Leiaute Atual 2025+ (`fato_ifdata_2025_campos`)

Explora campos publicados a partir de `2025-03` em formato longo. Sempre filtre `escopo`, `relatorio`, `id_data` e `campo_original`, e observe `formato_valor` (percentuais já estão em pontos percentuais):

```sql
SELECT
    data_base,
    codigo,
    instituicao,
    MAX(valor_numerico) FILTER (WHERE campo_original = 'Ativo Total') / 1e6 AS ativo_total_bi,
    MAX(valor_numerico) FILTER (WHERE campo_original = 'Patrimônio Líquido') / 1e6 AS pl_bi,
    MAX(valor_numerico) FILTER (WHERE campo_original = 'Índice de Basileia') AS basileia_pct
FROM fato_ifdata_2025_campos
WHERE id_data = 20260601
  AND escopo = 'prudential_conglomerates'
  AND relatorio = 'summary'
  AND campo_original IN ('Ativo Total', 'Patrimônio Líquido', 'Índice de Basileia')
GROUP BY 1, 2, 3
ORDER BY ativo_total_bi DESC NULLS LAST
LIMIT 15;
```

---

## Anti-Patterns de SQL (Erros Comuns a Evitar)

| Anti-Pattern | Por que está errado | Correção |
| :--- | :--- | :--- |
| `SELECT SUM(ativo_total) FROM fato_resumo_financeiro WHERE id_data = 20241201` | Soma o mesmo banco 3 vezes (Prudencial + Financeiro + Individual). | Sempre filtre `tipo_instituicao` (ex.: `'Conglomerado Prudencial'`). |
| `WHERE tipo_instituicao = 'Instituição Individual'` | Retorna 0 linhas — o valor armazenado não tem cedilha nem acento. | Use `WHERE tipo_instituicao = 'Instituicao Individual'`. |
| `SELECT SUM(lucro_liquido) FROM view_dre_relatorios WHERE id_data BETWEEN 20240301 AND 20241201` | Conta 1T e 3T duas vezes porque 2T e 4T são acumulados semestrais. | Para lucro anual, filtre `id_data IN (20240601, 20241201)`. |
| Buscar `id_data >= 20250301` nas 13 tabelas fato históricas ou nas 4 views antigas | Retorna 0 linhas — os dados de 2025+ ficam em `fato_ifdata_2025_campos` e `view_resumo_prudencial_serie`. | Consulte `fato_ifdata_2025_campos` ou `view_resumo_prudencial_serie` para trimestres a partir de `2025-03`. |
| Multiplicar por `100` colunas com `formato_valor = 'percentual'` em `fato_ifdata_2025_campos` | Em `fato_ifdata_2025_campos`, percentuais já vêm em pontos percentuais (ex.: `16.51` = `16,51%`). | Use `valor_numerico` diretamente quando `formato_valor = 'percentual'`. |
| Somar `fato_ifdata_2025_campos` sem filtrar `escopo`, `relatorio` e `campo_original` | Mistura diferentes relatórios, escopos e métricas incompatíveis na mesma coluna `valor_numerico`. | Filtre sempre `escopo`, `relatorio` e `campo_original` (e `eh_dimensao = false` para agregações). |
| `WHERE tipo_instituicao = 'Conglomerado Prudencial'` em `fato_carteira_credito_*` (histórico) | Retorna 0 linhas — relatórios de carteira históricos estão em `Conglomerado Financeiro` / `(SCR)`. | Para `2012–2024`, filtre `Conglomerado Financeiro` (ou `tipo_relatorio_bcb`); para `2025+`, use `fato_ifdata_2025_campos` com `escopo = 'prudential_conglomerates'`. |
| `JOIN dim_faixa_vencimento f ON c.id_faixa_vencimento = f.id_faixa_vencimento` | A PK em `dim_faixa_vencimento` chama-se `id_faixa`. | Use `ON c.id_faixa_vencimento = f.id_faixa`. |
| `JOIN dim_risco dr ON r.id_nivel_risco = dr.id_nivel_risco` | A PK em `dim_risco` chama-se `id_risco`. | Use `ON r.id_nivel_risco = dr.id_risco`. |
| Tratar `ativo_total` como reais (`R$`) ou `indice_basileia` histórico como percentual (`0–100`) | `ativo_total` está em `R$ mil` e `indice_basileia` histórico em fração decimal (`0.1651`). | Divida valores monetários por `1e6` para bilhões de reais e multiplique índices históricos por `100` para `%`. |
