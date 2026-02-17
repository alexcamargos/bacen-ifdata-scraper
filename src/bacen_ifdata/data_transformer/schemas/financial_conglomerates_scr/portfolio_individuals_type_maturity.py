#!/usr/bin/env python
# encoding: utf-8
#
#  ------------------------------------------------------------------------------
#  Name: portfolio_individuals_type_maturity.py
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


class FinancialConglomerateSCRPortfolioIndividualsTypeMaturitySchema(BaseSchema):
    """
    Define e categoriza os nomes das colunas para os relatórios de
    Carteira de Pessoa Física por Tipo e por Prazo de Vencimento de
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
        },
        'data_base': {
            'description': 'Data-base do relatório.',
            'type': 'date',
            'raw_csv_header': 'Data',
        },
        'total_da_carteira_de_pessoa_fisica': {
            'description': (
                'Volume de crédito disponibilizado a pessoas físicas por instituições financeiras, '
                'excluindo carteiras adquiridas em cessão de crédito com retenção de risco por outra '
                'instituição financeira.'
            ),
            'type': 'numeric',
            'raw_csv_header': 'Total da Carteira de Pessoa Física',
        },
        # Empréstimo com Consignação em Folha
        'emprestimo_com_consignacao_em_folha': {
            'description': 'Empréstimo com Consignação em Folha.',
            'type': 'numeric',
            'raw_csv_header': 'Empréstimo com Consignação em Folha',
        },
        'emprestimo_com_consignacao_em_folha_vencer_ate_90_dias': {
            'description': 'Empréstimo com Consignação em Folha - A Vencer em até 90 Dias.',
            'type': 'numeric',
            'raw_csv_header': 'Empréstimo com Consignação em Folha - A Vencer em até 90 Dias',
        },
        'emprestimo_com_consignacao_em_folha_vencer_91_360_dias': {
            'description': 'Empréstimo com Consignação em Folha - A Vencer Entre 91 a 360 Dias.',
            'type': 'numeric',
            'raw_csv_header': 'Empréstimo com Consignação em Folha - A Vencer Entre 91 a 360 Dias',
        },
        'emprestimo_com_consignacao_em_folha_vencer_361_1080_dias': {
            'description': 'Empréstimo com Consignação em Folha - A Vencer Entre 361 a 1080 Dias.',
            'type': 'numeric',
            'raw_csv_header': 'Empréstimo com Consignação em Folha - A Vencer Entre 361 a 1080 Dias',
        },
        'emprestimo_com_consignacao_em_folha_vencer_1081_1800_dias': {
            'description': 'Empréstimo com Consignação em Folha - A Vencer Entre 1081 a 1800 Dias.',
            'type': 'numeric',
            'raw_csv_header': 'Empréstimo com Consignação em Folha - A Vencer Entre 1081 a 1800 Dias',
        },
        'emprestimo_com_consignacao_em_folha_vencer_1801_5400_dias': {
            'description': 'Empréstimo com Consignação em Folha - A Vencer Entre 1801 a 5400 Dias.',
            'type': 'numeric',
            'raw_csv_header': 'Empréstimo com Consignação em Folha - A Vencer Entre 1801 a 5400 Dias',
        },
        'emprestimo_com_consignacao_em_folha_vencer_acima_5400_dias': {
            'description': 'Empréstimo com Consignação em Folha - A vencer Acima de 5400 Dias.',
            'type': 'numeric',
            'raw_csv_header': 'Empréstimo com Consignação em Folha - A vencer Acima de 5400 Dias',
        },
        'emprestimo_com_consignacao_em_folha_total': {
            'description': 'Empréstimo com Consignação em Folha - Total das operações.',
            'type': 'numeric',
            'raw_csv_header': 'Empréstimo com Consignação em Folha - Total',
        },
        # Empréstimo sem Consignação em Folha
        'emprestimo_sem_consignacao_em_folha': {
            'description': 'Empréstimo sem Consignação em Folha.',
            'type': 'numeric',
            'raw_csv_header': 'Empréstimo sem Consignação em Folha',
        },
        'emprestimo_sem_consignacao_em_folha_vencer_ate_90_dias': {
            'description': 'Empréstimo sem Consignação em Folha - A Vencer em até 90 Dias.',
            'type': 'numeric',
            'raw_csv_header': 'Empréstimo sem Consignação em Folha - A Vencer em até 90 Dias',
        },
        'emprestimo_sem_consignacao_em_folha_vencer_91_360_dias': {
            'description': 'Empréstimo sem Consignação em Folha - A Vencer Entre 91 a 360 Dias.',
            'type': 'numeric',
            'raw_csv_header': 'Empréstimo sem Consignação em Folha - A Vencer Entre 91 a 360 Dias',
        },
        'emprestimo_sem_consignacao_em_folha_vencer_361_1080_dias': {
            'description': 'Empréstimo sem Consignação em Folha - A Vencer Entre 361 a 1080 Dias.',
            'type': 'numeric',
            'raw_csv_header': 'Empréstimo sem Consignação em Folha - A Vencer Entre 361 a 1080 Dias',
        },
        'emprestimo_sem_consignacao_em_folha_vencer_1081_1800_dias': {
            'description': 'Empréstimo sem Consignação em Folha - A Vencer Entre 1081 a 1800 Dias.',
            'type': 'numeric',
            'raw_csv_header': 'Empréstimo sem Consignação em Folha - A Vencer Entre 1081 a 1800 Dias',
        },
        'emprestimo_sem_consignacao_em_folha_vencer_1801_5400_dias': {
            'description': 'Empréstimo sem Consignação em Folha - A Vencer Entre 1801 a 5400 Dias.',
            'type': 'numeric',
            'raw_csv_header': 'Empréstimo sem Consignação em Folha - A Vencer Entre 1801 a 5400 Dias',
        },
        'emprestimo_sem_consignacao_em_folha_vencer_acima_5400_dias': {
            'description': 'Empréstimo sem Consignação em Folha - A vencer Acima de 5400 Dias.',
            'type': 'numeric',
            'raw_csv_header': 'Empréstimo sem Consignação em Folha - A vencer Acima de 5400 Dias',
        },
        'emprestimo_sem_consignacao_em_folha_total': {
            'description': 'Empréstimo sem Consignação em Folha - Total das operações.',
            'type': 'numeric',
            'raw_csv_header': 'Empréstimo sem Consignação em Folha - Total',
        },
        # Veículos
        'veiculos': {
            'description': 'Veículos.',
            'type': 'numeric',
            'raw_csv_header': 'Veículos',
        },
        'veiculos_vencer_ate_90_dias': {
            'description': 'Veículos - A Vencer em até 90 Dias.',
            'type': 'numeric',
            'raw_csv_header': 'Veículos - A Vencer em até 90 Dias',
        },
        'veiculos_vencer_91_360_dias': {
            'description': 'Veículos - A Vencer Entre 91 a 360 Dias.',
            'type': 'numeric',
            'raw_csv_header': 'Veículos - A Vencer Entre 91 a 360 Dias',
        },
        'veiculos_vencer_361_1080_dias': {
            'description': 'Veículos - A Vencer Entre 361 a 1080 Dias.',
            'type': 'numeric',
            'raw_csv_header': 'Veículos - A Vencer Entre 361 a 1080 Dias',
        },
        'veiculos_vencer_1081_1800_dias': {
            'description': 'Veículos - A Vencer Entre 1081 a 1800 Dias.',
            'type': 'numeric',
            'raw_csv_header': 'Veículos - A Vencer Entre 1081 a 1800 Dias',
        },
        'veiculos_vencer_1801_5400_dias': {
            'description': 'Veículos - A Vencer Entre 1801 a 5400 Dias.',
            'type': 'numeric',
            'raw_csv_header': 'Veículos - A Vencer Entre 1801 a 5400 Dias',
        },
        'veiculos_vencer_acima_5400_dias': {
            'description': 'Veículos - A vencer Acima de 5400 Dias.',
            'type': 'numeric',
            'raw_csv_header': 'Veículos - A vencer Acima de 5400 Dias',
        },
        'veiculos_total': {
            'description': 'Veículos - Total das operações.',
            'type': 'numeric',
            'raw_csv_header': 'Veículos - Total',
        },
        # Habitação
        'habitacao': {
            'description': 'Habitação.',
            'type': 'numeric',
            'raw_csv_header': 'Habitação',
        },
        'habitacao_vencer_ate_90_dias': {
            'description': 'Habitação - A Vencer em até 90 Dias.',
            'type': 'numeric',
            'raw_csv_header': 'Habitação - A Vencer em até 90 Dias',
        },
        'habitacao_vencer_91_360_dias': {
            'description': 'Habitação - A Vencer Entre 91 a 360 Dias.',
            'type': 'numeric',
            'raw_csv_header': 'Habitação - A Vencer Entre 91 a 360 Dias',
        },
        'habitacao_vencer_361_1080_dias': {
            'description': 'Habitação - A Vencer Entre 361 a 1080 Dias.',
            'type': 'numeric',
            'raw_csv_header': 'Habitação - A Vencer Entre 361 a 1080 Dias',
        },
        'habitacao_vencer_1081_1800_dias': {
            'description': 'Habitação - A Vencer Entre 1081 a 1800 Dias.',
            'type': 'numeric',
            'raw_csv_header': 'Habitação - A Vencer Entre 1081 a 1800 Dias',
        },
        'habitacao_vencer_1801_5400_dias': {
            'description': 'Habitação - A Vencer Entre 1801 a 5400 Dias.',
            'type': 'numeric',
            'raw_csv_header': 'Habitação - A Vencer Entre 1801 a 5400 Dias',
        },
        'habitacao_vencer_acima_5400_dias': {
            'description': 'Habitação - A vencer Acima de 5400 Dias.',
            'type': 'numeric',
            'raw_csv_header': 'Habitação - A vencer Acima de 5400 Dias',
        },
        'habitacao_total': {
            'description': 'Habitação - Total das operações.',
            'type': 'numeric',
            'raw_csv_header': 'Habitação - Total',
        },
        # Cartão de Crédito
        'cartao_de_credito': {
            'description': 'Cartão de Crédito.',
            'type': 'numeric',
            'raw_csv_header': 'Cartão de Crédito',
        },
        'cartao_de_credito_vencer_ate_90_dias': {
            'description': 'Cartão de Crédito - A Vencer em até 90 Dias.',
            'type': 'numeric',
            'raw_csv_header': 'Cartão de Crédito - A Vencer em até 90 Dias',
        },
        'cartao_de_credito_vencer_91_360_dias': {
            'description': 'Cartão de Crédito - A Vencer Entre 91 a 360 Dias.',
            'type': 'numeric',
            'raw_csv_header': 'Cartão de Crédito - A Vencer Entre 91 a 360 Dias',
        },
        'cartao_de_credito_vencer_361_1080_dias': {
            'description': 'Cartão de Crédito - A Vencer Entre 361 a 1080 Dias.',
            'type': 'numeric',
            'raw_csv_header': 'Cartão de Crédito - A Vencer Entre 361 a 1080 Dias',
        },
        'cartao_de_credito_vencer_1081_1800_dias': {
            'description': 'Cartão de Crédito - A Vencer Entre 1081 a 1800 Dias.',
            'type': 'numeric',
            'raw_csv_header': 'Cartão de Crédito - A Vencer Entre 1081 a 1800 Dias',
        },
        'cartao_de_credito_vencer_1801_5400_dias': {
            'description': 'Cartão de Crédito - A Vencer Entre 1801 a 5400 Dias.',
            'type': 'numeric',
            'raw_csv_header': 'Cartão de Crédito - A Vencer Entre 1801 a 5400 Dias',
        },
        'cartao_de_credito_vencer_acima_5400_dias': {
            'description': 'Cartão de Crédito - A vencer Acima de 5400 Dias.',
            'type': 'numeric',
            'raw_csv_header': 'Cartão de Crédito - A vencer Acima de 5400 Dias',
        },
        'cartao_de_credito_total': {
            'description': 'Cartão de Crédito - Total das operações.',
            'type': 'numeric',
            'raw_csv_header': 'Cartão de Crédito - Total',
        },
        # Rural e Agroindustrial
        'rural_e_agroindustrial': {
            'description': 'Rural e Agroindustrial.',
            'type': 'numeric',
            'raw_csv_header': 'Rural e Agroindustrial',
        },
        'rural_e_agroindustrial_vencer_ate_90_dias': {
            'description': 'Rural e Agroindustrial - A Vencer em até 90 Dias.',
            'type': 'numeric',
            'raw_csv_header': 'Rural e Agroindustrial - A Vencer em até 90 Dias',
        },
        'rural_e_agroindustrial_vencer_91_360_dias': {
            'description': 'Rural e Agroindustrial - A Vencer Entre 91 a 360 Dias.',
            'type': 'numeric',
            'raw_csv_header': 'Rural e Agroindustrial - A Vencer Entre 91 a 360 Dias',
        },
        'rural_e_agroindustrial_vencer_361_1080_dias': {
            'description': 'Rural e Agroindustrial - A Vencer Entre 361 a 1080 Dias.',
            'type': 'numeric',
            'raw_csv_header': 'Rural e Agroindustrial - A Vencer Entre 361 a 1080 Dias',
        },
        'rural_e_agroindustrial_vencer_1081_1800_dias': {
            'description': 'Rural e Agroindustrial - A Vencer Entre 1081 a 1800 dias.',
            'type': 'numeric',
            'raw_csv_header': 'Rural e Agroindustrial - A Vencer Entre 1081 a 1800 dias',
        },
        'rural_e_agroindustrial_vencer_1801_5400_dias': {
            'description': 'Rural e Agroindustrial - A Vencer Entre 1801 a 5400 Dias.',
            'type': 'numeric',
            'raw_csv_header': 'Rural e Agroindustrial - A Vencer Entre 1801 a 5400 Dias',
        },
        'rural_e_agroindustrial_vencer_acima_5400_dias': {
            'description': 'Rural e Agroindustrial - A Vencer Acima de 5400 Dias.',
            'type': 'numeric',
            'raw_csv_header': 'Rural e Agroindustrial - A Vencer Acima de 5400 Dias',
        },
        'rural_e_agroindustrial_total': {
            'description': 'Rural e Agroindustrial - Total das operações.',
            'type': 'numeric',
            'raw_csv_header': 'Rural e Agroindustrial - Total',
        },
        # Outros Créditos
        'outros_creditos': {
            'description': 'Outros Créditos.',
            'type': 'numeric',
            'raw_csv_header': 'Outros Créditos',
        },
        'outros_creditos_vencer_ate_90_dias': {
            'description': 'Outros Créditos - A Vencer em até 90 Dias.',
            'type': 'numeric',
            'raw_csv_header': 'Outros Créditos - A Vencer em até 90 Dias',
        },
        'outros_creditos_vencer_91_360_dias': {
            'description': 'Outros Créditos - A Vencer Entre 91 a 360 Dias.',
            'type': 'numeric',
            'raw_csv_header': 'Outros Créditos - A Vencer Entre 91 a 360 Dias',
        },
        'outros_creditos_vencer_361_1080_dias': {
            'description': 'Outros Créditos - A Vencer Entre 361 a 1080 Dias.',
            'type': 'numeric',
            'raw_csv_header': 'Outros Créditos - A Vencer Entre 361 a 1080 Dias',
        },
        'outros_creditos_vencer_1081_1800_dias': {
            'description': 'Outros Créditos - A Vencer Entre 1081 a 1800 Dias.',
            'type': 'numeric',
            'raw_csv_header': 'Outros Créditos - A Vencer Entre 1081 a 1800 Dias',
        },
        'outros_creditos_vencer_1801_5400_dias': {
            'description': 'Outros Créditos - A Vencer Entre 1801 a 5400 Dias.',
            'type': 'numeric',
            'raw_csv_header': 'Outros Créditos - A Vencer Entre 1801 a 5400 Dias',
        },
        'outros_creditos_vencer_acima_5400_dias': {
            'description': 'Outros Créditos - A vencer Acima de 5400 Dias.',
            'type': 'numeric',
            'raw_csv_header': 'Outros Créditos - A vencer Acima de 5400 Dias',
        },
        'outros_creditos_total': {
            'description': 'Outros Créditos - Total das operações.',
            'type': 'numeric',
            'raw_csv_header': 'Outros Créditos - Total',
        },
        'total_exterior_pessoa_fisica': {
            'description': (
                'Volume das operações de crédito realizadas por IFs brasileiras no exterior para pessoas físicas.'
            ),
            'type': 'numeric',
            'raw_csv_header': 'Total Exterior Pessoa Física',
        },
    }
