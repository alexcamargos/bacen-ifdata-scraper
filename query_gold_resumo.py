import duckdb
import pandas as pd

def main():
    """
    Exporta dados de Resumo Financeiro no schema Gold para Parquet.
    Normaliza o nome da instituição para a versão mais recente e
    adiciona uma flag de descontinuidade (is_descontinuada).
    """
    con = duckdb.connect("data/gold_warehouse.duckdb")

    query = """
    WITH base AS (
        SELECT 
            codigo_origem AS codigo,
            nome_instituicao AS instituicao,
            nome_conglomerado AS conglomerado,
            nome_conglomerado AS conglomerado_financeiro, -- Cópia baseada no schema atual
            nome_conglomerado AS conglomerado_prudencial, -- Cópia baseada no schema atual
            consolidado_bancario,
            tipo_de_controle,
            tipo_instituicao AS tipo_de_instituicao,
            cidade,
            uf,
            regiao,
            data_base,
            ativo_total,
            carteira_credito AS carteira_de_credito_classificada,
            passivo_exigivel AS passivo_circulante_e_exigivel_a_longo_prazo,
            captacoes,
            patrimonio_liquido,
            lucro_liquido,
            quantidade_agencias AS numero_de_agencias,
            quantidade_postos_atendimento AS numero_de_postos_de_atendimento
        FROM main.view_resumo_financeiro_relatorios
        WHERE 
            tipo_instituicao = 'Instituicao Individual'
            -- NOTA: O usuário quer a maior cobertura possível para ver os nomes antigos
            -- e o histórico (2000 a 2024). Algumas cooperativas nos anos 2000 não 
            -- possuíam o TCB assinalado ou o tipo exato 'Cooperativa de Crédito Singular.'.
            -- Se necessário restringir perfeitamente o ESCOPO a "somente cooperativas", 
            -- mantemos os filtros, lembrando que cortará parte do histórico antigo.
            AND tcb = 'b3s'
            AND consolidado_bancario = 'Cooperativa de Crédito Singular.'
    ),
    instituicoes_mais_recentes AS (
        -- Descobre qual é o nome, cidade, UF e região mais recentes para CADA código (PK)
        SELECT 
            codigo,
            instituicao AS instituicao_atualizada,
            cidade AS cidade_atualizada,
            uf AS uf_atualizada,
            regiao AS regiao_atualizada,
            MAX(data_base) OVER(PARTITION BY codigo) AS max_data_base_instituicao,
            MAX(data_base) OVER() AS max_data_base_geral,
            ROW_NUMBER() OVER(PARTITION BY codigo ORDER BY data_base DESC) AS rn
        FROM base
    ),
    nomes_consolidados AS (
        -- Mantém apenas a 1ª linha mais recente de cada código 
        -- e calcula se ela deixou de existir/parou de enviar dados (is_descontinuada)
        SELECT 
            codigo,
            instituicao_atualizada,
            cidade_atualizada,
            uf_atualizada,
            regiao_atualizada,
            CASE 
                -- Se a última data base da cooperativa for menor que a última data do Bacen
                -- ignora pequenos gaps (buracos de meses) pois pega o MAX absoluto.
                WHEN max_data_base_instituicao < max_data_base_geral THEN True 
                ELSE False 
            END AS is_descontinuada
        FROM instituicoes_mais_recentes
        WHERE rn = 1
    )
    SELECT 
        nc.instituicao_atualizada AS instituicao,
        b.codigo,
        b.conglomerado,
        b.conglomerado_financeiro,
        b.conglomerado_prudencial,
        b.consolidado_bancario,
        b.tipo_de_controle,
        b.tipo_de_instituicao,
        nc.cidade_atualizada AS cidade,
        nc.uf_atualizada AS uf,
        nc.regiao_atualizada AS regiao,
        b.data_base,
        b.ativo_total,
        b.carteira_de_credito_classificada,
        b.passivo_circulante_e_exigivel_a_longo_prazo,
        b.captacoes,
        b.patrimonio_liquido,
        b.lucro_liquido,
        b.numero_de_agencias,
        b.numero_de_postos_de_atendimento,
        nc.is_descontinuada
    FROM base b
    INNER JOIN nomes_consolidados nc ON b.codigo = nc.codigo
    ORDER BY
        b.codigo ASC,
        b.data_base ASC;
    """

    print("Executando query consolidada e extraindo os dados...\n")
    df_resultado = con.execute(query).df()
    
    print(f"Total de registros encontrados: {len(df_resultado)}\n")
    
    if not df_resultado.empty:
        # Mostra as primeiras 5 linhas
        pd.set_option('display.max_columns', None)
        print(df_resultado.head())
        
        # Validando o código específico
        print("\n\nExemplo para cooperativa 71243034:")
        print(df_resultado[df_resultado['codigo'] == 71243034][['instituicao', 'data_base', 'is_descontinuada']].head(5))
        
        # Salva o resultado otimizado no formato Parquet
        output_file = "cooperativas_b3s_resumo.parquet"
        print(f"\nSalvando dados finais consolidados em {output_file}...")
        df_resultado.to_parquet(output_file, engine='pyarrow', compression='snappy')
        print("Arquivo salvo com sucesso!")

if __name__ == "__main__":
    main()
