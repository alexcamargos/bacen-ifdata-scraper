#!/usr/bin/env python
# encoding: utf-8
#
#  ------------------------------------------------------------------------------
#  Name: portfolio_legal_person_type_maturity.py
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


class FinancialConglomerateSCRPortfolioLegalPersonTypeMaturitySchema(BaseSchema):
    """
    Define e categoriza os nomes das colunas para os relatórios de
    Carteira de Pessoa Jurídica por Tipo e por Prazo de Vencimento de
    instituições financeiras independentes (SCR), enriquecido com metadados do dicionário de dados.
    """

    SCHEMA_DEFINITION: Final[dict[str, dict[str, Any]]] = {
        'instituicao': {
            'description': 'Nome da instituição.',
            'type': 'text',
        },
        'codigo': {
            'description': 'Conglomerado ou CNPJ.',
            'type': 'numeric',
        },
        'consolidado_bancario': {
            'description': 'Tipo de Consolidado Bancário (B1, B2, B3S, B3C, B4, N1, N2, N4).',
            'type': 'categorical',
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
            'mapping': {
                'i': 'Instituição Independente',
                'c': 'Conglomerado',
            },
        },
        'tipo_de_controle': {
            'description': 'Tipo de Controle.',
            'type': 'categorical',
            'mapping': {'1': 'Público', '2': 'Privado Nacional', '3': 'Controle Estrangeiro'},
        },
        'segmento_resolucao': {
            'description': 'Segmento conforme Resolução n.º 4.553/2017 (S1, S2, S3, S4, S5).',
            'type': 'categorical',
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
        },
        'uf': {
            'description': 'Unidade da Federação onde fica a sede da instituição.',
            'type': 'categorical',
        },
        'regiao': {
            'description': 'Região geográfica onde fica a sede da instituição.',
            'type': 'categorical',
        },
        'data_base': {
            'description': 'Data-base do relatório.',
            'type': 'date',
        },
        'total_da_carteira_de_pessoa_juridica': {
            'description': (
                'Volume de crédito disponibilizado a pessoas jurídicas por instituições financeiras, '
                'excluindo carteiras adquiridas em cessão de crédito com retenção de risco por outra '
                'instituição financeira.'
            ),
            'type': 'numeric',
        },
        # Capital de Giro
        'capital_de_giro_vencido_a_partir_15_dias': {
            'description': 'Capital de Giro - Operações vencidas há, no mínimo, 15 dias.',
            'type': 'numeric',
        },
        'capital_de_giro_a_vencer_ate_90_dias': {
            'description': 'Capital de Giro - Operações a vencer em até 90 dias ou vencidas há, no máximo, 14 dias.',
            'type': 'numeric',
        },
        'capital_de_giro_a_vencer_de_91_ate_360_dias': {
            'description': 'Capital de Giro - Operações a vencer entre 91 a 360 dias.',
            'type': 'numeric',
        },
        'capital_de_giro_a_vencer_de_361_ate_1080_dias': {
            'description': 'Capital de Giro - Operações a vencer entre 361 a 1080 dias.',
            'type': 'numeric',
        },
        'capital_de_giro_a_vencer_de_1081_ate_1800_dias': {
            'description': 'Capital de Giro - Operações a vencer entre 1081 a 1800 dias.',
            'type': 'numeric',
        },
        'capital_de_giro_a_vencer_de_1801_ate_5400_dias': {
            'description': 'Capital de Giro - Operações a vencer entre 1801 a 5400 dias.',
            'type': 'numeric',
        },
        'capital_de_giro_a_vencer_acima_5400_dias': {
            'description': 'Capital de Giro - Operações a vencer acima de 5400 dias.',
            'type': 'numeric',
        },
        'capital_de_giro_total': {
            'description': 'Capital de Giro - Total do grupo.',
            'type': 'numeric',
        },
        # Investimento
        'investimento_vencido_a_partir_15_dias': {
            'description': 'Investimento - Operações vencidas há, no mínimo, 15 dias.',
            'type': 'numeric',
        },
        'investimento_a_vencer_ate_90_dias': {
            'description': 'Investimento - Operações a vencer em até 90 dias ou vencidas há, no máximo, 14 dias.',
            'type': 'numeric',
        },
        'investimento_a_vencer_de_91_ate_360_dias': {
            'description': 'Investimento - Operações a vencer entre 91 a 360 dias.',
            'type': 'numeric',
        },
        'investimento_a_vencer_de_361_ate_1080_dias': {
            'description': 'Investimento - Operações a vencer entre 361 a 1080 dias.',
            'type': 'numeric',
        },
        'investimento_a_vencer_de_1081_ate_1800_dias': {
            'description': 'Investimento - Operações a vencer entre 1081 a 1800 dias.',
            'type': 'numeric',
        },
        'investimento_a_vencer_de_1801_ate_5400_dias': {
            'description': 'Investimento - Operações a vencer entre 1801 a 5400 dias.',
            'type': 'numeric',
        },
        'investimento_a_vencer_acima_5400_dias': {
            'description': 'Investimento - Operações a vencer acima de 5400 dias.',
            'type': 'numeric',
        },
        'investimento_total': {
            'description': 'Investimento - Total do grupo.',
            'type': 'numeric',
        },
        # Capital de Giro Rotativo
        'capital_de_giro_rotativo_vencido_a_partir_15_dias': {
            'description': 'Capital de Giro Rotativo - Operações vencidas há, no mínimo, 15 dias.',
            'type': 'numeric',
        },
        'capital_de_giro_rotativo_a_vencer_ate_90_dias': {
            'description': 'Capital de Giro Rotativo - Operações a vencer em até 90 dias ou vencidas há, no máximo, 14 dias.',
            'type': 'numeric',
        },
        'capital_de_giro_rotativo_a_vencer_de_91_ate_360_dias': {
            'description': 'Capital de Giro Rotativo - Operações a vencer entre 91 a 360 dias.',
            'type': 'numeric',
        },
        'capital_de_giro_rotativo_a_vencer_de_361_ate_1080_dias': {
            'description': 'Capital de Giro Rotativo - Operações a vencer entre 361 a 1080 dias.',
            'type': 'numeric',
        },
        'capital_de_giro_rotativo_a_vencer_de_1081_ate_1800_dias': {
            'description': 'Capital de Giro Rotativo - Operações a vencer entre 1081 a 1800 dias.',
            'type': 'numeric',
        },
        'capital_de_giro_rotativo_a_vencer_de_1801_ate_5400_dias': {
            'description': 'Capital de Giro Rotativo - Operações a vencer entre 1801 a 5400 dias.',
            'type': 'numeric',
        },
        'capital_de_giro_rotativo_a_vencer_acima_5400_dias': {
            'description': 'Capital de Giro Rotativo - Operações a vencer acima de 5400 dias.',
            'type': 'numeric',
        },
        'capital_de_giro_rotativo_total': {
            'description': 'Capital de Giro Rotativo - Total do grupo.',
            'type': 'numeric',
        },
        # Operações com Recebíveis
        'operacoes_com_recebiveis_vencido_a_partir_15_dias': {
            'description': 'Operações com Recebíveis - Operações vencidas há, no mínimo, 15 dias.',
            'type': 'numeric',
        },
        'operacoes_com_recebiveis_a_vencer_ate_90_dias': {
            'description': 'Operações com Recebíveis - Operações a vencer em até 90 dias ou vencidas há, no máximo, 14 dias.',
            'type': 'numeric',
        },
        'operacoes_com_recebiveis_a_vencer_de_91_ate_360_dias': {
            'description': 'Operações com Recebíveis - Operações a vencer entre 91 a 360 dias.',
            'type': 'numeric',
        },
        'operacoes_com_recebiveis_a_vencer_de_361_ate_1080_dias': {
            'description': 'Operações com Recebíveis - Operações a vencer entre 361 a 1080 dias.',
            'type': 'numeric',
        },
        'operacoes_com_recebiveis_a_vencer_de_1081_ate_1800_dias': {
            'description': 'Operações com Recebíveis - Operações a vencer entre 1081 a 1800 dias.',
            'type': 'numeric',
        },
        'operacoes_com_recebiveis_a_vencer_de_1801_ate_5400_dias': {
            'description': 'Operações com Recebíveis - Operações a vencer entre 1801 a 5400 dias.',
            'type': 'numeric',
        },
        'operacoes_com_recebiveis_a_vencer_acima_5400_dias': {
            'description': 'Operações com Recebíveis - Operações a vencer acima de 5400 dias.',
            'type': 'numeric',
        },
        'operacoes_com_recebiveis_total': {
            'description': 'Operações com Recebíveis - Total do grupo.',
            'type': 'numeric',
        },
        # Comércio Exterior
        'comercio_exterior_vencido_a_partir_15_dias': {
            'description': 'Comércio Exterior - Operações vencidas há, no mínimo, 15 dias.',
            'type': 'numeric',
        },
        'comercio_exterior_a_vencer_ate_90_dias': {
            'description': 'Comércio Exterior - Operações a vencer em até 90 dias ou vencidas há, no máximo, 14 dias.',
            'type': 'numeric',
        },
        'comercio_exterior_a_vencer_de_91_ate_360_dias': {
            'description': 'Comércio Exterior - Operações a vencer entre 91 a 360 dias.',
            'type': 'numeric',
        },
        'comercio_exterior_a_vencer_de_361_ate_1080_dias': {
            'description': 'Comércio Exterior - Operações a vencer entre 361 a 1080 dias.',
            'type': 'numeric',
        },
        'comercio_exterior_a_vencer_de_1081_ate_1800_dias': {
            'description': 'Comércio Exterior - Operações a vencer entre 1081 a 1800 dias.',
            'type': 'numeric',
        },
        'comercio_exterior_a_vencer_de_1801_ate_5400_dias': {
            'description': 'Comércio Exterior - Operações a vencer entre 1801 a 5400 dias.',
            'type': 'numeric',
        },
        'comercio_exterior_a_vencer_acima_5400_dias': {
            'description': 'Comércio Exterior - Operações a vencer acima de 5400 dias.',
            'type': 'numeric',
        },
        'comercio_exterior_total': {
            'description': 'Comércio Exterior - Total do grupo.',
            'type': 'numeric',
        },
        # Outros Créditos
        'outros_creditos_vencido_a_partir_15_dias': {
            'description': 'Outros Créditos - Operações vencidas há, no mínimo, 15 dias.',
            'type': 'numeric',
        },
        'outros_creditos_a_vencer_ate_90_dias': {
            'description': 'Outros Créditos - Operações a vencer em até 90 dias ou vencidas há, no máximo, 14 dias.',
            'type': 'numeric',
        },
        'outros_creditos_a_vencer_de_91_ate_360_dias': {
            'description': 'Outros Créditos - Operações a vencer entre 91 a 360 dias.',
            'type': 'numeric',
        },
        'outros_creditos_a_vencer_de_361_ate_1080_dias': {
            'description': 'Outros Créditos - Operações a vencer entre 361 a 1080 dias.',
            'type': 'numeric',
        },
        'outros_creditos_a_vencer_de_1081_ate_1800_dias': {
            'description': 'Outros Créditos - Operações a vencer entre 1081 a 1800 dias.',
            'type': 'numeric',
        },
        'outros_creditos_a_vencer_de_1801_ate_5400_dias': {
            'description': 'Outros Créditos - Operações a vencer entre 1801 a 5400 dias.',
            'type': 'numeric',
        },
        'outros_creditos_a_vencer_acima_5400_dias': {
            'description': 'Outros Créditos - Operações a vencer acima de 5400 dias.',
            'type': 'numeric',
        },
        'outros_creditos_total': {
            'description': 'Outros Créditos - Total do grupo.',
            'type': 'numeric',
        },
        # Financiamento de Infraestrutura/Desenvolvimento/Projeto e Outros Créditos
        'financiamento_infraestrutura_vencido_a_partir_15_dias': {
            'description': 'Financiamento de Infraestrutura - Operações vencidas há, no mínimo, 15 dias.',
            'type': 'numeric',
        },
        'financiamento_infraestrutura_a_vencer_ate_90_dias': {
            'description': 'Financiamento de Infraestrutura - Operações a vencer em até 90 dias ou vencidas há, no máximo, 14 dias.',
            'type': 'numeric',
        },
        'financiamento_infraestrutura_a_vencer_de_91_ate_360_dias': {
            'description': 'Financiamento de Infraestrutura - Operações a vencer entre 91 a 360 dias.',
            'type': 'numeric',
        },
        'financiamento_infraestrutura_a_vencer_de_361_ate_1080_dias': {
            'description': 'Financiamento de Infraestrutura - Operações a vencer entre 361 a 1080 dias.',
            'type': 'numeric',
        },
        'financiamento_infraestrutura_a_vencer_de_1081_ate_1800_dias': {
            'description': 'Financiamento de Infraestrutura - Operações a vencer entre 1081 a 1800 dias.',
            'type': 'numeric',
        },
        'financiamento_infraestrutura_a_vencer_de_1801_ate_5400_dias': {
            'description': 'Financiamento de Infraestrutura - Operações a vencer entre 1801 a 5400 dias.',
            'type': 'numeric',
        },
        'financiamento_infraestrutura_a_vencer_acima_5400_dias': {
            'description': 'Financiamento de Infraestrutura - Operações a vencer acima de 5400 dias.',
            'type': 'numeric',
        },
        'financiamento_infraestrutura_total': {
            'description': 'Financiamento de Infraestrutura - Total do grupo.',
            'type': 'numeric',
        },
        # Rural e Agroindustrial
        'rural_e_agroindustrial_vencido_a_partir_15_dias': {
            'description': 'Rural e Agroindustrial - Operações vencidas há, no mínimo, 15 dias.',
            'type': 'numeric',
        },
        'rural_e_agroindustrial_a_vencer_ate_90_dias': {
            'description': 'Rural e Agroindustrial - Operações a vencer em até 90 dias ou vencidas há, no máximo, 14 dias.',
            'type': 'numeric',
        },
        'rural_e_agroindustrial_a_vencer_de_91_ate_360_dias': {
            'description': 'Rural e Agroindustrial - Operações a vencer entre 91 a 360 dias.',
            'type': 'numeric',
        },
        'rural_e_agroindustrial_a_vencer_de_361_ate_1080_dias': {
            'description': 'Rural e Agroindustrial - Operações a vencer entre 361 a 1080 dias.',
            'type': 'numeric',
        },
        'rural_e_agroindustrial_a_vencer_de_1081_ate_1800_dias': {
            'description': 'Rural e Agroindustrial - Operações a vencer entre 1081 a 1800 dias.',
            'type': 'numeric',
        },
        'rural_e_agroindustrial_a_vencer_de_1801_ate_5400_dias': {
            'description': 'Rural e Agroindustrial - Operações a vencer entre 1801 a 5400 dias.',
            'type': 'numeric',
        },
        'rural_e_agroindustrial_a_vencer_acima_5400_dias': {
            'description': 'Rural e Agroindustrial - Operações a vencer acima de 5400 dias.',
            'type': 'numeric',
        },
        'rural_e_agroindustrial_total': {
            'description': 'Rural e Agroindustrial - Total do grupo.',
            'type': 'numeric',
        },
        # Habitacional
        'habitacional_vencido_a_partir_15_dias': {
            'description': 'Habitacional - Operações vencidas há, no mínimo, 15 dias.',
            'type': 'numeric',
        },
        'habitacional_a_vencer_ate_90_dias': {
            'description': 'Habitacional - Operações a vencer em até 90 dias ou vencidas há, no máximo, 14 dias.',
            'type': 'numeric',
        },
        'habitacional_a_vencer_de_91_ate_360_dias': {
            'description': 'Habitacional - Operações a vencer entre 91 a 360 dias.',
            'type': 'numeric',
        },
        'habitacional_a_vencer_de_361_ate_1080_dias': {
            'description': 'Habitacional - Operações a vencer entre 361 a 1080 dias.',
            'type': 'numeric',
        },
        'habitacional_a_vencer_de_1081_ate_1800_dias': {
            'description': 'Habitacional - Operações a vencer entre 1081 a 1800 dias.',
            'type': 'numeric',
        },
        'habitacional_a_vencer_de_1801_ate_5400_dias': {
            'description': 'Habitacional - Operações a vencer entre 1801 a 5400 dias.',
            'type': 'numeric',
        },
        'habitacional_a_vencer_acima_5400_dias': {
            'description': 'Habitacional - Operações a vencer acima de 5400 dias.',
            'type': 'numeric',
        },
        'habitacional_total': {
            'description': 'Habitacional - Total do grupo.',
            'type': 'numeric',
        },
        # Exterior
        'total_exterior_pessoa_juridica': {
            'description': (
                'Volume das operações de crédito realizadas por IFs brasileiras no exterior para pessoas jurídicas.'
            ),
            'type': 'numeric',
        },
    }
