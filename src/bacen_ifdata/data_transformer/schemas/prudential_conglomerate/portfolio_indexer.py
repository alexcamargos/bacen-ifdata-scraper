#!/usr/bin/env python
# encoding: utf-8
#
#  ------------------------------------------------------------------------------
#  Name: portfolio_indexer.py
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


class PrudentialConglomeratePortfolioIndexerSchema(BaseSchema):
    """
    Define e categoriza os nomes das colunas para os relatórios de
    Carteira de Crédito por Indexador de
    conglomerados prudenciais, enriquecido com metadados do dicionário de dados.
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
        'cidade': {'description': 'Cidade da sede da instituição.', 'type': 'text'},
        'uf': {'description': 'Unidade da Federação onde fica a sede da instituição.', 'type': 'categorical'},
        'data_base': {'description': 'Data-base do relatório.', 'type': 'date'},
        'total_geral': {
            'description': (
                'Volume de crédito disponibilizado por instituições financeiras, '
                'excluindo carteiras adquiridas em cessão de crédito com retenção de risco '
                'por outra instituição financeira.'
            ),
            'type': 'numeric',
        },
        'prefixado': {
            'description': 'Volume das operações de crédito com indexador prefixado.',
            'type': 'numeric',
        },
        'tr_tbf': {
            'description': 'Volume das operações de crédito com indexador TR / TBF.',
            'type': 'numeric',
        },
        'tjlp': {
            'description': 'Volume das operações de crédito com indexador TJLP.',
            'type': 'numeric',
        },
        'tlp': {
            'description': 'Taxa de Longo Prazo - TLP.',
            'type': 'numeric',
        },
        'libor': {
            'description': 'Volume das operações de crédito com indexador Libor.',
            'type': 'numeric',
        },
        'outras_taxas_pos_fixadas': {
            'description': 'Volume das operações de crédito com outras taxas pós-fixadas.',
            'type': 'numeric',
        },
        'carteira_ativa_com_indexador_cdi': {
            'description': 'Volume das operações de crédito com indexador CDI.',
            'type': 'numeric',
        },
        'selic': {
            'description': 'Volume das operações de crédito com indexador SELIC.',
            'type': 'numeric',
        },
        'outras_taxas_flutuantes': {
            'description': 'Volume das operações de crédito com outras taxas flutuantes.',
            'type': 'numeric',
        },
        'igpm': {
            'description': 'Volume das operações de crédito com indexador IGPM.',
            'type': 'numeric',
        },
        'ipca': {
            'description': 'Volume das operações de crédito com indexador IPCA.',
            'type': 'numeric',
        },
        'ipcc': {
            'description': 'Volume das operações de crédito com indexador IPCC.',
            'type': 'numeric',
        },
        'outros_indices_de_preco': {
            'description': 'Volume das operações de crédito com outros índices de preço.',
            'type': 'numeric',
        },
        'outros_indexadores': {
            'description': 'Volume das operações de crédito com outros indexadores.',
            'type': 'numeric',
        },
        'tcr_pre': {
            'description': 'Volume das operações de crédito com indexador TCR pré.',
            'type': 'numeric',
        },
        'tcr_pos': {
            'description': 'Volume das operações de crédito com indexador TCR pós.',
            'type': 'numeric',
        },
        'trfc_pre': {
            'description': 'Volume das operações de crédito com indexador TRFC pré.',
            'type': 'numeric',
        },
        'trfc_pos': {
            'description': 'Volume das operações de crédito com indexador TRFC pós.',
            'type': 'numeric',
        },
        'total_nao_individualizado': {
            'description': (
                'Volume das operações de crédito cujas dívidas totais dos clientes não supere R$ 1 mil, '
                'para as quais não há informação de indexadores.'
            ),
            'type': 'numeric',
        },
        'total_exterior': {
            'description': 'Volume das operações de crédito realizadas por IFs brasileiras no exterior.',
            'type': 'numeric',
        },
    }
