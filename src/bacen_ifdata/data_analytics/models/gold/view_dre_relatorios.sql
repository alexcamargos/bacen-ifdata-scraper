{{ config(materialized='view') }}

WITH fatos AS (
    SELECT
        id_instituicao,
        id_data,
        nome_instituicao_historico,
        rendas_operacoes_de_credito,
        rendas_operacoes_de_arrendamento_mercantil,
        rendas_operacoes_tvm,
        rendas_operacoes_instrumentos_financeiros_derivativos,
        resultado_operacoes_cambio,
        rendas_aplicacoes_compulsorias,
        receitas_intermediacao_financeira,
        despesas_captacao,
        despesas_obrigacoes_emprestimos_repasses,
        despesas_operacoes_arrendamento_mercantil,
        despesas_operacoes_cambio,
        resultado_provisao_creditos_dificil_liquidacao,
        despesas_intermediacao_financeira,
        resultado_intermediacao_financeira,
        rendas_prestacao_servicos,
        rendas_tarifas_bancarias,
        despesas_pessoal,
        despesas_administrativas,
        despesas_tributarias,
        resultado_participacoes,
        outras_receitas_operacionais,
        outras_despesas_operacionais,
        outras_receitas_despesas_operacionais,
        resultado_operacional,
        resultado_nao_operacional,
        resultado_antes_tributacao,
        imposto_renda_contribuicao_social,
        participacao_lucros,
        lucro_liquido,
        juros_sobre_capital,
        roe,
        roa
    FROM {{ ref('fato_demonstracao_resultado') }}
),
dim_inst AS (
    SELECT
        id_instituicao,
        codigo_origem,
        nome_instituicao,
        tipo_instituicao,
        nome_conglomerado,
        tipo_relatorio_bcb,
        segmento,
        segmento_descricao,
        cidade,
        uf,
        regiao,
        tipo_de_controle,
        tcb,
        consolidado_bancario,
        classe_instituicao
    FROM {{ ref('int_instituicao_enriquecida') }}
),
dim_tempo AS (
    SELECT
        id_data,
        data
    FROM {{ ref('dim_tempo') }}
)

SELECT
    f.id_instituicao,
    f.id_data,
    
    -- Instituição
    i.codigo_origem,
    i.nome_instituicao,
    f.nome_instituicao_historico,
    i.tipo_instituicao,
    i.nome_conglomerado,
    
    -- Tipo do Relatório Filtrado
    i.tipo_relatorio_bcb,
    
    -- Atributos Dimensionais
    i.segmento,
    i.segmento_descricao,
    i.cidade,
    i.uf,
    i.regiao,
    i.tipo_de_controle,
    i.tcb,
    i.consolidado_bancario,
    i.classe_instituicao,
    
    -- Data
    t.data as data_base,
    
    -- DRE - Receitas Intermediação
    f.rendas_operacoes_de_credito,
    f.rendas_operacoes_de_arrendamento_mercantil,
    f.rendas_operacoes_tvm,
    f.rendas_operacoes_instrumentos_financeiros_derivativos,
    f.resultado_operacoes_cambio,
    f.rendas_aplicacoes_compulsorias,
    f.receitas_intermediacao_financeira,
    
    -- DRE - Despesas Intermediação
    f.despesas_captacao,
    f.despesas_obrigacoes_emprestimos_repasses,
    f.despesas_operacoes_arrendamento_mercantil,
    f.despesas_operacoes_cambio,
    f.resultado_provisao_creditos_dificil_liquidacao,
    f.despesas_intermediacao_financeira,
    
    -- DRE - Resultado Intermediação
    f.resultado_intermediacao_financeira,
    
    -- DRE - Outras Receitas/Despesas Operacionais
    f.rendas_prestacao_servicos,
    f.rendas_tarifas_bancarias,
    f.despesas_pessoal,
    f.despesas_administrativas,
    f.despesas_tributarias,
    f.resultado_participacoes,
    f.outras_receitas_operacionais,
    f.outras_despesas_operacionais,
    f.outras_receitas_despesas_operacionais,
    
    -- DRE - Resultados
    f.resultado_operacional,
    f.resultado_nao_operacional,
    f.resultado_antes_tributacao,
    f.imposto_renda_contribuicao_social,
    f.participacao_lucros,
    f.lucro_liquido,
    f.juros_sobre_capital,
    
    -- KPIs
    f.roe,
    f.roa

FROM fatos f
LEFT JOIN dim_inst i ON f.id_instituicao = i.id_instituicao
LEFT JOIN dim_tempo t ON f.id_data = t.id_data
