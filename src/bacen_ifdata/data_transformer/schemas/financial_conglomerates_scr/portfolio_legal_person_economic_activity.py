#!/usr/bin/env python
# encoding: utf-8
#
#  ------------------------------------------------------------------------------
#  Name: portfolio_legal_person_economic_activity.py
#  Version: 0.0.1
#  Summary: Bacen IF.data AutoScraper & Data Manager
#           Este sistema foi projetado para automatizar o download dos
#           relatórios da ferramenta IF.data do Banco Central do Brasil.
#           Criado para facilitar a integração com ferramentas automatizadas de
#           análise e visualização de dados, garantido acesso fácil e oportuno
#           aos dados.
#
#  Author: Alexsander Lopes Camargos
#  Author-email: alcamargos@vivaldi.net
#
#  License: MIT
#  ------------------------------------------------------------------------------

"""
Bacen IF.data AutoScraper & Data Manager

This script is designed to automate the download of reports from the Banco Central do Brasil's
IF.data tool. It facilitates the integration with automated data analysis and visualization tools,
ensuring easy and timely access to data.

Author: Alexsander Lopes Camargos
License: MIT
"""

from typing import Any, Final

from bacen_ifdata.data_transformer.schemas.base_schema import BaseSchema


class FinancialConglomerateSCRPortfolioLegalPersonEconomicActivitySchema(BaseSchema):
    """
    Define e categoriza os nomes das colunas para os relatórios de
    Carteira de Pessoa Jurídica por Atividade Econômica de
    instituições financeiras independentes (SCR), enriquecido com metadados do dicionário de dados.
    """

    SCHEMA_DEFINITION: Final[dict[str, dict[str, Any]]] = {
        'instituicao': {
            'description': 'Nome da instituição.',
            'type': 'text',
            'raw_csv_header': 'Instituição',
        },
        'codigo': {
            'description': 'Conglomerado ou CNPJ.',
            'type': 'numeric',
            'raw_csv_header': 'Código',
        },
        'consolidado_bancario': {
            'description': 'Tipo de Consolidado Bancário (B1, B2, B3S, B3C, B4, N1, N2, N4).',
            'type': 'categorical',
            'raw_csv_header': 'TCB',
            'mapping': {
                'b1': (
                    'Instituição individual do tipo Banco Comercial, Banco Múltiplo com Carteira Comercial '
                    'ou caixas econômicas e Conglomerado composto de pelo menos uma instituição do tipo Banco '
                    'Comercial, Banco Múltiplo com Carteira Comercial ou caixas econômicas.'
                ),
                'b2': (
                    'Instituição individual do tipo Banco Múltiplo sem Carteira Comercial ou Banco de Câmbio '
                    'ou Banco de Investimento e Conglomerado composto de pelo menos uma instituição do tipo '
                    'Banco Múltiplo sem Carteira Comercial ou Banco de Investimento, mas sem conter instituições '
                    'do tipo Banco Comercial e Banco Múltiplo com Carteira Comercial.'
                ),
                'b3s': 'Cooperativa de Crédito Singular.',
                'b3c': 'Central e Confederação de Cooperativas de Crédito.',
                'b4': 'Banco de Desenvolvimento',
                'n1': 'Instituição não bancária atuante no mercado de crédito.',
                'n2': 'Instituição não bancária atuante no mercado de capitais.',
                'n4': 'Instituições de pagamento.',
            },
        },
        'tipo_de_consolidacao': {
            'description': 'Tipo de Consolidação (I) identifica uma Instituição Independente e (C) identifica um Conglomerado.',
            'type': 'categorical',
            'raw_csv_header': 'TD',
            'mapping': {
                'i': 'Instituição Independente',
                'c': 'Conglomerado',
            },
        },
        'tipo_de_controle': {
            'description': 'Tipo de Controle.',
            'type': 'categorical',
            'raw_csv_header': 'TC',
            'mapping': {'1': 'Público', '2': 'Privado Nacional', '3': 'Controle Estrangeiro'},
        },
        'segmento_resolucao': {
            'description': 'Segmento conforme Resolução n.º 4.553/2017 (S1, S2, S3, S4, S5).',
            'type': 'categorical',
            'raw_csv_header': 'SR',
            'mapping': {
                's1': (
                    'Bancos múltiplos, bancos comerciais, bancos de investimento, bancos de câmbio e caixas '
                    'econômicas que (i) tenham porte (Exposição/Produto Interno Bruto) superior a 10%; ou (ii) '
                    'exerçam atividade internacional relevante (ativos no exterior superiores a US$ 10 bilhões).'
                ),
                's2': (
                    'Composto por: (i) bancos múltiplos, bancos comerciais, bancos de investimento, '
                    'bancos de câmbio e caixas econômicas de porte inferior a 10% e igual ou superior '
                    'a 1%; e (ii) demais instituições autorizadas a funcionar pelo Banco Central do '
                    'Brasil de porte igual ou superior a 1% do PIB.'
                ),
                's3': 'Instituições de porte inferior a 1% e igual ou superior a 0,1%.',
                's4': 'Instituições de porte inferior a 0,1%.',
                's5': (
                    'Composto por: (i) instituições de porte inferior a 0,1% que utilizem metodologia '
                    'facultativa simplificada para apuração dos requerimentos mínimos de Patrimônio '
                    'de Referência (PR), de Nível I e de Capital Principal, exceto bancos múltiplos, '
                    'bancos comerciais, bancos de investimento, bancos de câmbio e caixas econômicas; '
                    'e (ii) não sujeitas a apuração de PR.'
                ),
            },
        },
        'segmento': {
            'description': 'Segmentos de instituições financeiras.',
            'type': 'categorical',
            'raw_csv_header': 'Segmento',
            'mapping': {
                '2': 'Banco Comercial',
                '4': 'BNDES',
                '5': 'Banco de Desenvolvimento',
                '6': 'Caixa Econômica Federal',
                '7': 'Caixa Econômica Estadual',
                '8': 'Banco Múltiplo',
                '9': 'Cooperativa de Crédito',
                '10': 'Sociedade de Crédito ao Microempreendedor',
                '11': 'Banco Múltiplo Cooperativo',
                '13': 'Banco de Investimento',
                '14': 'Sociedade de Crédito, Financiamento e Investimento',
                '15': 'Sociedade Corretora de TVM',
                '16': 'Sociedade Distribuidora de TVM',
                '19': 'Sociedade de Arrendamento Mercantil',
                '21': 'Sociedade Corretora de Câmbio',
                '25': 'Associação de Poupança e Empréstimo',
                '28': 'Banco Comercial Estrangeiro - Filial no país',
                '29': 'Companhia Hipotecária',
                '30': 'Agência de Fomento',
                '31': 'Sociedade de Crédito Imobiliário - Repassadora',
                '39': 'Banco de Câmbio',
                '41': 'Instituições de Pagamento',
                '43': 'Sociedades de Crédito Direto',
                '44': 'Sociedades de Empréstimo entre Pessoas',
                '196': 'Conglomerado de Mercado de Capitais',
                '197': 'Conglomerado Não-Bancário de Crédito',
                '198': 'Conglomerado - Bancário II',
                '199': 'Conglomerado - Bancário I',
            },
        },
        'cidade': {
            'description': 'Cidade da sede da instituição.',
            'type': 'text',
            'raw_csv_header': 'Cidade',
        },
        'uf': {
            'description': 'Unidade da Federação onde fica a sede da instituição.',
            'type': 'categorical',
            'raw_csv_header': 'UF',
        },
        'regiao': {
            'description': 'Região geográfica onde fica a sede da instituição.',
            'type': 'categorical',
            'raw_csv_header': 'Região',
        },
        'data_base': {
            'description': 'Data-base do relatório.',
            'type': 'date',
            'raw_csv_header': 'Data',
        },
        'total_da_carteira_de_pessoa_juridica': {
            'description': (
                'Volume de crédito disponibilizado a pessoas jurídicas por instituições financeiras, '
                'excluindo carteiras adquiridas em cessão de crédito com retenção de risco por outra '
                'instituição financeira.'
            ),
            'type': 'numeric',
            'raw_csv_header': 'Total da Carteira de Pessoa Jurídica',
        },
        # Administração Pública
        'administracao_publica_vencido_a_partir_15_dias': {
            'description': 'Administração Pública - Operações vencidas há, no mínimo, 15 dias.',
            'type': 'numeric',
            'raw_csv_header': 'Administração Pública, Defesa e Seguridade Social',
        },
        'administracao_publica_a_vencer_ate_90_dias': {
            'description': 'Administração Pública - Operações a vencer em até 90 dias ou vencidas há, no máximo, 14 dias.',
            'type': 'numeric',
            'raw_csv_header': 'Administração Pública, Defesa e Seguridade Social - A Vencer em 90 Dias',
        },
        'administracao_publica_a_vencer_de_91_ate_360_dias': {
            'description': 'Administração Pública - Operações a vencer entre 91 a 360 dias.',
            'type': 'numeric',
            'raw_csv_header': 'Administração Pública, Defesa e Seguridade Social - A Vencer Entre 91 a 360 Dias',
        },
        'administracao_publica_a_vencer_de_361_ate_1080_dias': {
            'description': 'Administração Pública - Operações a vencer entre 361 a 1080 dias.',
            'type': 'numeric',
            'raw_csv_header': 'Administração Pública, Defesa e Seguridade Social - A Vencer Entre 361 a 1080 Dias',
        },
        'administracao_publica_a_vencer_de_1081_ate_1800_dias': {
            'description': 'Administração Pública - Operações a vencer entre 1081 a 1800 dias.',
            'type': 'numeric',
            'raw_csv_header': 'Administração Pública, Defesa e Seguridade Social - A Vencer Entre 1081 a 1800 Dias',
        },
        'administracao_publica_a_vencer_de_1801_ate_5400_dias': {
            'description': 'Administração Pública - Operações a vencer entre 1801 a 5400 dias.',
            'type': 'numeric',
            'raw_csv_header': 'Administração Pública, Defesa e Seguridade Social - A Vencer Entre 1801 a 5400 Dias',
        },
        'administracao_publica_a_vencer_acima_5400_dias': {
            'description': 'Administração Pública - Operações a vencer acima de 5400 dias.',
            'type': 'numeric',
            'raw_csv_header': 'Administração Pública, Defesa e Seguridade Social - A vencer Acima de 5400 Dias',
        },
        'administracao_publica_total': {
            'description': 'Administração Pública - Total do grupo.',
            'type': 'numeric',
            'raw_csv_header': 'Administração Pública, Defesa e Seguridade Social - Total',
        },
        # Agricultura, Pecuária, Produção Florestal, Pesca e Aquicultura
        'agricultura_vencido_a_partir_15_dias': {
            'description': 'Agricultura - Operações vencidas há, no mínimo, 15 dias.',
            'type': 'numeric',
            'raw_csv_header': 'Agricultura, Pecuária, Produção Florestal, Pesca e Aquicultura',
        },
        'agricultura_a_vencer_ate_90_dias': {
            'description': 'Agricultura - Operações a vencer em até 90 dias ou vencidas há, no máximo, 14 dias.',
            'type': 'numeric',
            'raw_csv_header': 'Agricultura, Pecuária, Produção Florestal, Pesca e Aquicultura - A Vencer em 90 Dias',
        },
        'agricultura_a_vencer_de_91_ate_360_dias': {
            'description': 'Agricultura - Operações a vencer entre 91 a 360 dias.',
            'type': 'numeric',
            'raw_csv_header': 'Agricultura, Pecuária, Produção Florestal, Pesca e Aquicultura - A Vencer Entre 91 a 360 Dias',
        },
        'agricultura_a_vencer_de_361_ate_1080_dias': {
            'description': 'Agricultura - Operações a vencer entre 361 a 1080 dias.',
            'type': 'numeric',
            'raw_csv_header': 'Agricultura, Pecuária, Produção Florestal, Pesca e Aquicultura - A Vencer Entre 361 a 1080 Dias',
        },
        'agricultura_a_vencer_de_1081_ate_1800_dias': {
            'description': 'Agricultura - Operações a vencer entre 1081 a 1800 dias.',
            'type': 'numeric',
            'raw_csv_header': 'Agricultura, Pecuária, Produção Florestal, Pesca e Aquicultura - A Vencer Entre 1081 a 1800 Dias',
        },
        'agricultura_a_vencer_de_1801_ate_5400_dias': {
            'description': 'Agricultura - Operações a vencer entre 1801 a 5400 dias.',
            'type': 'numeric',
            'raw_csv_header': 'Agricultura, Pecuária, Produção Florestal, Pesca e Aquicultura - A Vencer Entre 1801 a 5400 Dias',
        },
        'agricultura_a_vencer_acima_5400_dias': {
            'description': 'Agricultura - Operações a vencer acima de 5400 dias.',
            'type': 'numeric',
            'raw_csv_header': 'Agricultura, Pecuária, Produção Florestal, Pesca e Aquicultura - A vencer Acima de 5400 Dias',
        },
        'agricultura_total': {
            'description': 'Agricultura - Total do grupo.',
            'type': 'numeric',
            'raw_csv_header': 'Agricultura, Pecuária, Produção Florestal, Pesca e Aquicultura - Total',
        },
        # Atividades Imobiliárias
        'atividade_imobiliaria_vencido_a_partir_15_dias': {
            'description': 'Atividades Imobiliárias - Operações vencidas há, no mínimo, 15 dias.',
            'type': 'numeric',
            'raw_csv_header': 'Atividades Imobiliárias',
        },
        'atividade_imobiliaria_a_vencer_ate_90_dias': {
            'description': 'Atividades Imobiliárias - Operações a vencer em até 90 dias ou vencidas há, no máximo, 14 dias.',
            'type': 'numeric',
            'raw_csv_header': 'Atividades Imobiliárias - A Vencer em 90 Dias',
        },
        'atividade_imobiliaria_a_vencer_de_91_ate_360_dias': {
            'description': 'Atividades Imobiliárias - Operações a vencer entre 91 a 360 dias.',
            'type': 'numeric',
            'raw_csv_header': 'Atividades Imobiliárias - A Vencer Entre 91 a 360 Dias',
        },
        'atividade_imobiliaria_a_vencer_de_361_ate_1080_dias': {
            'description': 'Atividades Imobiliárias - Operações a vencer entre 361 a 1080 dias.',
            'type': 'numeric',
            'raw_csv_header': 'Atividades Imobiliárias - A Vencer Entre 361 a 1080 Dias',
        },
        'atividade_imobiliaria_a_vencer_de_1081_ate_1800_dias': {
            'description': 'Atividades Imobiliárias - Operações a vencer entre 1081 a 1800 dias.',
            'type': 'numeric',
            'raw_csv_header': 'Atividades Imobiliárias - A Vencer Entre 1081 a 1800 Dias',
        },
        'atividade_imobiliaria_a_vencer_de_1801_ate_5400_dias': {
            'description': 'Atividades Imobiliárias - Operações a vencer entre 1801 a 5400 dias.',
            'type': 'numeric',
            'raw_csv_header': 'Atividades Imobiliárias - A Vencer Entre 1801 a 5400 Dias',
        },
        'atividade_imobiliaria_a_vencer_acima_5400_dias': {
            'description': 'Atividades Imobiliárias - Operações a vencer acima de 5400 dias.',
            'type': 'numeric',
            'raw_csv_header': 'Atividades Imobiliárias - A vencer Acima de 5400 Dias',
        },
        'atividade_imobiliaria_total': {
            'description': 'Atividades Imobiliárias - Total do grupo.',
            'type': 'numeric',
            'raw_csv_header': 'Atividades Imobiliárias - Total',
        },
        # Comércio, Reparação de Veículos Automotores e Motocicletas
        'comercio_vencido_a_partir_15_dias': {
            'description': 'Comércio - Operações vencidas há, no mínimo, 15 dias.',
            'type': 'numeric',
            'raw_csv_header': 'Comércio, Reparação de Veículos Automotores e Motocicletas',
        },
        'comercio_a_vencer_ate_90_dias': {
            'description': 'Comércio - Operações a vencer em até 90 dias ou vencidas há, no máximo, 14 dias.',
            'type': 'numeric',
            'raw_csv_header': 'Comércio, Reparação de Veículos Automotores e Motocicletas - A Vencer em 90 Dias',
        },
        'comercio_a_vencer_de_91_ate_360_dias': {
            'description': 'Comércio - Operações a vencer entre 91 a 360 dias.',
            'type': 'numeric',
            'raw_csv_header': 'Comércio, Reparação de Veículos Automotores e Motocicletas - A Vencer Entre 91 a 360 Dias',
        },
        'comercio_a_vencer_de_361_ate_1080_dias': {
            'description': 'Comércio - Operações a vencer entre 361 a 1080 dias.',
            'type': 'numeric',
            'raw_csv_header': 'Comércio, Reparação de Veículos Automotores e Motocicletas - A Vencer Entre 361 a 1080 Dias',
        },
        'comercio_a_vencer_de_1081_ate_1800_dias': {
            'description': 'Comércio - Operações a vencer entre 1081 a 1800 dias.',
            'type': 'numeric',
            'raw_csv_header': 'Comércio, Reparação de Veículos Automotores e Motocicletas - A Vencer Entre 1081 a 1800 Dias',
        },
        'comercio_a_vencer_de_1801_ate_5400_dias': {
            'description': 'Comércio - Operações a vencer entre 1801 a 5400 dias.',
            'type': 'numeric',
            'raw_csv_header': 'Comércio, Reparação de Veículos Automotores e Motocicletas - A Vencer Entre 1801 a 5400 Dias',
        },
        'comercio_a_vencer_acima_5400_dias': {
            'description': 'Comércio - Operações a vencer acima de 5400 dias.',
            'type': 'numeric',
            'raw_csv_header': 'Comércio, Reparação de Veículos Automotores e Motocicletas - A vencer Acima de 5400 Dias',
        },
        'comercio_total': {
            'description': 'Comércio - Total do grupo.',
            'type': 'numeric',
            'raw_csv_header': 'Comércio, Reparação de Veículos Automotores e Motocicletas - Total',
        },
        # Construção
        'construcao_vencido_a_partir_15_dias': {
            'description': 'Construção - Operações vencidas há, no mínimo, 15 dias.',
            'type': 'numeric',
            'raw_csv_header': 'Construção',
        },
        'construcao_a_vencer_ate_90_dias': {
            'description': 'Construção - Operações a vencer em até 90 dias ou vencidas há, no máximo, 14 dias.',
            'type': 'numeric',
            'raw_csv_header': 'Construção - A Vencer em 90 Dias',
        },
        'construcao_a_vencer_de_91_ate_360_dias': {
            'description': 'Construção - Operações a vencer entre 91 a 360 dias.',
            'type': 'numeric',
            'raw_csv_header': 'Construção - A Vencer Entre 91 a 360 Dias',
        },
        'construcao_a_vencer_de_361_ate_1080_dias': {
            'description': 'Construção - Operações a vencer entre 361 a 1080 dias.',
            'type': 'numeric',
            'raw_csv_header': 'Construção - A Vencer Entre 361 a 1080 Dias',
        },
        'construcao_a_vencer_de_1081_ate_1800_dias': {
            'description': 'Construção - Operações a vencer entre 1081 a 1800 dias.',
            'type': 'numeric',
            'raw_csv_header': 'Construção - A Vencer Entre 1081 a 1800 Dias',
        },
        'construcao_a_vencer_de_1801_ate_5400_dias': {
            'description': 'Construção - Operações a vencer entre 1801 a 5400 dias.',
            'type': 'numeric',
            'raw_csv_header': 'Construção - A Vencer Entre 1801 a 5400 Dias',
        },
        'construcao_a_vencer_acima_5400_dias': {
            'description': 'Construção - Operações a vencer acima de 5400 dias.',
            'type': 'numeric',
            'raw_csv_header': 'Construção - A vencer Acima de 5400 Dias',
        },
        'construcao_total': {
            'description': 'Construção - Total do grupo.',
            'type': 'numeric',
            'raw_csv_header': 'Construção - Total',
        },
        # Industrias Extrativas
        'industrias_extrativas_vencido_a_partir_15_dias': {
            'description': 'Indústrias Extrativas - Operações vencidas há, no mínimo, 15 dias.',
            'type': 'numeric',
            'raw_csv_header': 'Industrias Extrativas',
        },
        'industrias_extrativas_a_vencer_ate_90_dias': {
            'description': 'Indústrias Extrativas - Operações a vencer em até 90 dias ou vencidas há, no máximo, 14 dias.',
            'type': 'numeric',
            'raw_csv_header': 'Industrias Extrativas - A Vencer em 90 Dias',
        },
        'industrias_extrativas_a_vencer_de_91_ate_360_dias': {
            'description': 'Indústrias Extrativas - Operações a vencer entre 91 a 360 dias.',
            'type': 'numeric',
            'raw_csv_header': 'Industrias Extrativas - A Vencer Entre 91 a 360 Dias',
        },
        'industrias_extrativas_a_vencer_de_361_ate_1080_dias': {
            'description': 'Indústrias Extrativas - Operações a vencer entre 361 a 1080 dias.',
            'type': 'numeric',
            'raw_csv_header': 'Industrias Extrativas - A Vencer Entre 361 a 1080 Dias',
        },
        'industrias_extrativas_a_vencer_de_1081_ate_1800_dias': {
            'description': 'Indústrias Extrativas - Operações a vencer entre 1081 a 1800 dias.',
            'type': 'numeric',
            'raw_csv_header': 'Industrias Extrativas - A Vencer Entre 1081 a 1800 Dias',
        },
        'industrias_extrativas_a_vencer_de_1801_ate_5400_dias': {
            'description': 'Indústrias Extrativas - Operações a vencer entre 1801 a 5400 dias.',
            'type': 'numeric',
            'raw_csv_header': 'Industrias Extrativas - A Vencer Entre 1801 a 5400 Dias',
        },
        'industrias_extrativas_a_vencer_acima_5400_dias': {
            'description': 'Indústrias Extrativas - Operações a vencer acima de 5400 dias.',
            'type': 'numeric',
            'raw_csv_header': 'Industrias Extrativas - A vencer Acima de 5400 Dias',
        },
        'industrias_extrativas_total': {
            'description': 'Indústrias Extrativas - Total do grupo.',
            'type': 'numeric',
            'raw_csv_header': 'Industrias Extrativas - Total',
        },
        # Indústrias de Transformação
        'industrias_de_transformacao_vencido_a_partir_15_dias': {
            'description': 'Indústrias de Transformação - Operações vencidas há, no mínimo, 15 dias.',
            'type': 'numeric',
            'raw_csv_header': 'Indústrias de Transformação',
        },
        'industrias_de_transformacao_a_vencer_ate_90_dias': {
            'description': 'Indústrias de Transformação - Operações a vencer em até 90 dias ou vencidas há, no máximo, 14 dias.',
            'type': 'numeric',
            'raw_csv_header': 'Indústrias de Transformação - A Vencer em 90 Dias',
        },
        'industrias_de_transformacao_a_vencer_de_91_ate_360_dias': {
            'description': 'Indústrias de Transformação - Operações a vencer entre 91 a 360 dias.',
            'type': 'numeric',
            'raw_csv_header': 'Indústrias de Transformação - A Vencer Entre 91 a 360 Dias',
        },
        'industrias_de_transformacao_a_vencer_de_361_ate_1080_dias': {
            'description': 'Indústrias de Transformação - Operações a vencer entre 361 a 1080 dias.',
            'type': 'numeric',
            'raw_csv_header': 'Indústrias de Transformação - A Vencer Entre 361 a 1080 Dias',
        },
        'industrias_de_transformacao_a_vencer_de_1081_ate_1800_dias': {
            'description': 'Indústrias de Transformação - Operações a vencer entre 1081 a 1800 dias.',
            'type': 'numeric',
            'raw_csv_header': 'Indústrias de Transformação - A Vencer Entre 1081 a 1800 Dias',
        },
        'industrias_de_transformacao_a_vencer_de_1801_ate_5400_dias': {
            'description': 'Indústrias de Transformação - Operações a vencer entre 1801 a 5400 dias.',
            'type': 'numeric',
            'raw_csv_header': 'Indústrias de Transformação - A Vencer Entre 1801 a 5400 Dias',
        },
        'industrias_de_transformacao_a_vencer_acima_5400_dias': {
            'description': 'Indústrias de Transformação - Operações a vencer acima de 5400 dias.',
            'type': 'numeric',
            'raw_csv_header': 'Indústrias de Transformação - A vencer Acima de 5400 Dias',
        },
        'industrias_de_transformacao_total': {
            'description': 'Indústrias de Transformação - Total do grupo.',
            'type': 'numeric',
            'raw_csv_header': 'Indústrias de Transformação - Total',
        },
        # Outros
        'outros_vencido_a_partir_15_dias': {
            'description': 'Outros - Operações vencidas há, no mínimo, 15 dias.',
            'type': 'numeric',
            'raw_csv_header': 'Outros',
        },
        'outros_a_vencer_ate_90_dias': {
            'description': 'Outros - Operações a vencer em até 90 dias ou vencidas há, no máximo, 14 dias.',
            'type': 'numeric',
            'raw_csv_header': 'Outros - A Vencer em 90 Dias',
        },
        'outros_a_vencer_de_91_ate_360_dias': {
            'description': 'Outros - Operações a vencer entre 91 a 360 dias.',
            'type': 'numeric',
            'raw_csv_header': 'Outros - A Vencer Entre 91 a 360 Dias',
        },
        'outros_a_vencer_de_361_ate_1080_dias': {
            'description': 'Outros - Operações a vencer entre 361 a 1080 dias.',
            'type': 'numeric',
            'raw_csv_header': 'Outros - A Vencer Entre 361 a 1080 Dias',
        },
        'outros_a_vencer_de_1081_ate_1800_dias': {
            'description': 'Outros - Operações a vencer entre 1081 a 1800 dias.',
            'type': 'numeric',
            'raw_csv_header': 'Outros - a Vencer entre 1081 e 1800 Dias',
        },
        'outros_a_vencer_de_1801_ate_5400_dias': {
            'description': 'Outros - Operações a vencer entre 1801 a 5400 dias.',
            'type': 'numeric',
            'raw_csv_header': 'Outros - A Vencer Entre 1801 a 5400 Dias',
        },
        'outros_a_vencer_acima_5400_dias': {
            'description': 'Outros - Operações a vencer acima de 5400 dias.',
            'type': 'numeric',
            'raw_csv_header': 'Outros - A vencer Acima de 5400 Dias',
        },
        'outros_total': {
            'description': 'Outros - Total do grupo.',
            'type': 'numeric',
            'raw_csv_header': 'Outros - Total',
        },
        # Serviços Industriais de Utilidade Pública
        'producao_e_distribuicao_de_eletricidade_gas_e_agua_vencido_a_partir_15_dias': {
            'description': 'Serviços Industriais de Utilidade Pública - Operações vencidas há, no mínimo, 15 dias.',
            'type': 'numeric',
            'raw_csv_header': 'Serviços Industriais de Utilidade Pública',
        },
        'producao_e_distribuicao_de_eletricidade_gas_e_agua_a_vencer_ate_90_dias': {
            'description': 'Serviços Industriais de Utilidade Pública - Operações a vencer em até 90 dias ou vencidas há, no máximo, 14 dias.',
            'type': 'numeric',
            'raw_csv_header': 'Serviços Industriais de Utilidade Pública - A Vencer em 90 Dias',
        },
        'producao_e_distribuicao_de_eletricidade_gas_e_agua_a_vencer_de_91_ate_360_dias': {
            'description': 'Serviços Industriais de Utilidade Pública - Operações a vencer entre 91 a 360 dias.',
            'type': 'numeric',
            'raw_csv_header': 'Serviços Industriais de Utilidade Pública - A Vencer Entre 91 a 360 Dias',
        },
        'producao_e_distribuicao_de_eletricidade_gas_e_agua_a_vencer_de_361_ate_1080_dias': {
            'description': 'Serviços Industriais de Utilidade Pública - Operações a vencer entre 361 a 1080 dias.',
            'type': 'numeric',
            'raw_csv_header': 'Serviços Industriais de Utilidade Pública - A Vencer Entre 361 a 1080 Dias',
        },
        'producao_e_distribuicao_de_eletricidade_gas_e_agua_a_vencer_de_1081_ate_1800_dias': {
            'description': 'Serviços Industriais de Utilidade Pública - Operações a vencer entre 1081 a 1800 dias.',
            'type': 'numeric',
            'raw_csv_header': 'Serviços Industriais de Utilidade Pública - a Vencer entre 1081 e 1800 Dias',
        },
        'producao_e_distribuicao_de_eletricidade_gas_e_agua_a_vencer_de_1801_ate_5400_dias': {
            'description': 'Serviços Industriais de Utilidade Pública - Operações a vencer entre 1801 a 5400 dias.',
            'type': 'numeric',
            'raw_csv_header': 'Serviços Industriais de Utilidade Pública - A Vencer Entre 1801 a 5400 Dias',
        },
        'producao_e_distribuicao_de_eletricidade_gas_e_agua_a_vencer_acima_5400_dias': {
            'description': 'Serviços Industriais de Utilidade Pública - Operações a vencer acima de 5400 dias.',
            'type': 'numeric',
            'raw_csv_header': 'Serviços Industriais de Utilidade Pública - A vencer Acima de 5400 Dias',
        },
        'producao_e_distribuicao_de_eletricidade_gas_e_agua_total': {
            'description': 'Serviços Industriais de Utilidade Pública - Total do grupo.',
            'type': 'numeric',
            'raw_csv_header': 'Serviços Industriais de Utilidade Pública - Total',
        },
        # Serviços
        'servicos_vencido_a_partir_15_dias': {
            'description': 'Serviços - Operações vencidas há, no mínimo, 15 dias.',
            'type': 'numeric',
            'raw_csv_header': 'Serviços',
        },
        'servicos_a_vencer_ate_90_dias': {
            'description': 'Serviços - Operações a vencer em até 90 dias ou vencidas há, no máximo, 14 dias.',
            'type': 'numeric',
            'raw_csv_header': 'Serviços - A Vencer em 90 Dias',
        },
        'servicos_a_vencer_de_91_ate_360_dias': {
            'description': 'Serviços - Operações a vencer entre 91 a 360 dias.',
            'type': 'numeric',
            'raw_csv_header': 'Serviços - A Vencer Entre 91 a 360 Dias',
        },
        'servicos_a_vencer_de_361_ate_1080_dias': {
            'description': 'Serviços - Operações a vencer entre 361 a 1080 dias.',
            'type': 'numeric',
            'raw_csv_header': 'Serviços - A Vencer Entre 361 a 1080 Dias',
        },
        'servicos_a_vencer_de_1081_ate_1800_dias': {
            'description': 'Serviços - Operações a vencer entre 1081 a 1800 dias.',
            'type': 'numeric',
            'raw_csv_header': 'Serviços - A Vencer Entre 1081 a 1800 Dias',
        },
        'servicos_a_vencer_de_1801_ate_5400_dias': {
            'description': 'Serviços - Operações a vencer entre 1801 a 5400 dias.',
            'type': 'numeric',
            'raw_csv_header': 'Serviços - A Vencer Entre 1801 a 5400 Dias',
        },
        'servicos_a_vencer_acima_5400_dias': {
            'description': 'Serviços - Operações a vencer acima de 5400 dias.',
            'type': 'numeric',
            'raw_csv_header': 'Serviços - A vencer Acima de 5400 Dias',
        },
        'servicos_total': {
            'description': 'Serviços - Total do grupo.',
            'type': 'numeric',
            'raw_csv_header': 'Serviços - Total',
        },
        # Transporte, Armazenagem e Correio
        'transporte_vencido_a_partir_15_dias': {
            'description': 'Transporte - Operações vencidas há, no mínimo, 15 dias.',
            'type': 'numeric',
            'raw_csv_header': 'Transporte, Armazenagem e Correio',
        },
        'transporte_a_vencer_ate_90_dias': {
            'description': 'Transporte - Operações a vencer em até 90 dias ou vencidas há, no máximo, 14 dias.',
            'type': 'numeric',
            'raw_csv_header': 'Transporte, Armazenagem e Correio - A Vencer em 90 Dias',
        },
        'transporte_a_vencer_de_91_ate_360_dias': {
            'description': 'Transporte - Operações a vencer entre 91 a 360 dias.',
            'type': 'numeric',
            'raw_csv_header': 'Transporte, Armazenagem e Correio - A Vencer Entre 91 a 360 Dias',
        },
        'transporte_a_vencer_de_361_ate_1080_dias': {
            'description': 'Transporte - Operações a vencer entre 361 a 1080 dias.',
            'type': 'numeric',
            'raw_csv_header': 'Transporte, Armazenagem e Correio - A Vencer Entre 361 a 1080 Dias',
        },
        'transporte_a_vencer_de_1081_ate_1800_dias': {
            'description': 'Transporte - Operações a vencer entre 1081 a 1800 dias.',
            'type': 'numeric',
            'raw_csv_header': 'Transporte, Armazenagem e Correio - A Vencer Entre 1081 a 1800 Dias',
        },
        'transporte_a_vencer_de_1801_ate_5400_dias': {
            'description': 'Transporte - Operações a vencer entre 1801 a 5400 dias.',
            'type': 'numeric',
            'raw_csv_header': 'Transporte, Armazenagem e Correio - A Vencer Entre 1801 a 5400 Dias',
        },
        'transporte_a_vencer_acima_5400_dias': {
            'description': 'Transporte - Operações a vencer acima de 5400 dias.',
            'type': 'numeric',
            'raw_csv_header': 'Transporte, Armazenagem e Correio - A vencer Acima de 5400 Dias',
        },
        'transporte_total': {
            'description': 'Transporte - Total do grupo.',
            'type': 'numeric',
            'raw_csv_header': 'Transporte, Armazenagem e Correio - Total',
        },
        # Total Exterior
        'total_exterior_pessoa_juridica': {
            'description': (
                'Volume das operações de crédito realizadas por IFs brasileiras no exterior para pessoas jurídicas.'
            ),
            'type': 'numeric',
            'raw_csv_header': 'Total Exterior Pessoa Jurídica',
        },
        'atividade_nao_informada': {
            'description': 'Atividade econômica não informada ou não se aplica.',
            'type': 'numeric',
            'raw_csv_header': 'Atividade não Informada ou não se Aplica',
        },
        'total_nao_individualizado_pessoa_juridica': {
            'description': 'Total não individualizado para pessoa jurídica.',
            'type': 'numeric',
            'raw_csv_header': 'Total não Individualizado Pessoa Jurídica',
        },
    }
