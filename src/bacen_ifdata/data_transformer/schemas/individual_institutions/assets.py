#!/usr/bin/env python
# encoding: utf-8
#
#  ------------------------------------------------------------------------------
#  Name: assets.py
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


class IndividualInstitutionAssetsSchema(BaseSchema):
    """
    Define e categoriza os nomes das colunas para os relatórios de ATIVOS
    de instituições individuais, enriquecido com metadados do dicionário de dados.
    """

    SCHEMA_DEFINITION: Final[dict[str, dict[str, Any]]] = {
        'instituicao': {
            'description': 'Nome da instituição no cadastro do Banco Central.',
            'type': 'text',
        },
        'codigo': {
            'description': 'Código do conglomerado ou CNPJ no cadastro do Banco Central.',
            'type': 'numeric',
        },
        'conglomerado': {
            'description': (
                'Nome do conglomerado a que pertence a instituição individual.'
                ' Caso a instituição não pertença a nenhum conglomerado, esse campo estará sem informação.'
            ),
            'type': 'text',
        },
        'conglomerado_financeiro': {
            'description': (
                'Código do conglomerado financeiro a que pertence a instituição individual.'
                ' Caso a instituição não pertença a nenhum conglomerado, esse campo estará sem informação.'
            ),
            'type': 'numeric',
        },
        'conglomerado_prudencial': {
            'description': (
                'Código do conglomerado prudencial a que pertence a instituição individual.'
                ' Caso a instituição não pertença a nenhum conglomerado, esse campo estará sem informação.'
            ),
            'type': 'numeric',
        },
        'consolidado_bancario': {
            'description': 'Tipo de Consolidado Bancário (B1, B2, B3S, B3C, B4, N1, N2, N4).',
            'type': 'categorical',
            'mapping': {
                'b1': 'Banco Comercial, Banco Múltiplo com Carteira Comercial ou Caixas Econômicas.',
                'b2': 'Banco Múltiplo sem Carteira Comercial ou Banco de Câmbio ou Banco de Investimento.',
                'b3s': 'Cooperativa de Crédito Singular.',
                'b3c': 'Central e Confederação de Cooperativas de Crédito.',
                'b4': 'Banco de Desenvolvimento.',
                'n1': 'Não bancário de Crédito.',
                'n2': 'Não bancário do Mercado de Capitais.',
                'n4': 'Instituições de Pagamento.',
            },
        },
        'tipo_de_controle': {
            'description': 'Tipo de Controle: Identifica a origem do controle de capital das instituições.',
            'type': 'categorical',
            'mapping': {
                '1': 'Público',
                '2': 'Privado Nacional',
                '3': 'Privado com Controle Estrangeiro',
            },
        },
        'tipo_de_instituicao': {
            'description': 'Tipo de Instituição.',
            'type': 'categorical',
            'mapping': {
                '1': 'Banco do Brasil - Banco Múltiplo',
                '2': 'Banco Comercial',
                '3': 'Banco Comercial Cooperativo',
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
            },
        },
        'cidade': {
            'description': 'Cidade onde fica localizada a sede da instituição.',
            'type': 'text',
        },
        'uf': {
            'description': 'Unidade da Federação onde fica a sede da instituição.',
            'type': 'categorical',
        },
        'data': {
            'description': 'Data-base do Relatório.',
            'type': 'date',
        },
        'disponibilidades': {
            'description': 'Disponibilidades.',
            'type': 'numeric',
        },
        'aplicacoes_interfinanceiras_liquidez': {
            'description': 'Aplicações Interfinanceiras de Liquidez.',
            'type': 'numeric',
        },
        'tvm_e_instrumentos_financeiros_derivativos': {
            'description': 'Títulos e Valores Mobiliários e Instrumentos Financeiros Derivativos.',
            'type': 'numeric',
        },
        'operacoes_de_credito': {
            'description': 'Operações de Crédito - Provisão sobre Operações de Crédito.',
            'type': 'numeric',
        },
        'provisao_operacoes_de_credito': {
            'description': 'Provisão sobre Operações de Crédito.',
            'type': 'numeric',
        },
        'operacoes_de_credito_liquidas_provisao': {
            'description': 'Operações de Crédito Líquidas de Provisão.',
            'type': 'numeric',
        },
        'arrendamento_mercantil_a_receber': {
            'description': 'Operações de Arrendamento Mercantil - Provisão sobre Arrendamento Mercantil.',
            'type': 'numeric',
        },
        'imobilizado_de_arrendamento': {
            'description': 'Imobilizado de Arrendamento.',
            'type': 'numeric',
        },
        'credores_antecipacao_valor_residual': {
            'description': 'Credores por Antecipação de Valor Residual.',
            'type': 'numeric',
        },
        'provisao_arrendamento_mercantil': {
            'description': 'Provisão sobre Arrendamento Mercantil.',
            'type': 'numeric',
        },
        'arrendamento_mercantil_liquido_de_provisao': {
            'description': (
                'Operações de Arrendamento Mercantil + Imobilizado de Arrendamento + '
                'Credores por Antecipação de Valor Residual.'
            ),
            'type': 'numeric',
        },
        'outros_creditos_liquido_de_provisao': {
            'description': 'Outros Créditos - Líquido de Provisão.',
            'type': 'numeric',
        },
        'outros_ativos_realizaveis': {
            'description': 'Outros Valores e Bens + Relações Interfinanceiras + Relações Interdependências.',
            'type': 'numeric',
        },
        'permanente_ajustado': {
            'description': 'Ativo Permanente - Imobilizado de Arrendamento.',
            'type': 'numeric',
        },
        'ativo_total_ajustado': {
            'description': (
                'Disponibilidades + Aplicações Interfinanceiras de Liquidez + Títulos e Valores '
                'Mobiliários e Instrumentos Financeiros Derivativos + Operações de Crédito + '
                'Operações de Arrendamento Mercantil + Credores por Antecipação de Valor Residual + '
                'Outros Créditos + Outros Valores e Bens + Relações Interfinanceiras + Relações '
                'Interdependências + Ativo Permanente.'
            ),
            'type': 'numeric',
        },
        'credores_antecipacao_valor_residual_j': {
            'description': 'Credores por Antecipação de Valor Residual.',
            'type': 'numeric',
        },
        'ativo_total': {
            'description': 'Ativo Circulante e Realizável a Longo Prazo + Ativo Permanente.',
            'type': 'numeric',
        },
    }
