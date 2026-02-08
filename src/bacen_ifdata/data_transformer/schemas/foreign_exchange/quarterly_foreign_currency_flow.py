#!/usr/bin/env python
# encoding: utf-8
#
#  ------------------------------------------------------------------------------
#  Name: quarterly_foreign_currency_flow.py
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


class ForeignExchangeQuarterlyForeignCurrencyFlowSchema(BaseSchema):
    """
    Define e categoriza os nomes das colunas para os relatórios de
    Movimentação Trimestral no Mercado de Câmbio, enriquecido com metadados do dicionário de dados.
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
        'tcb': {
            'description': 'Tipo de Consolidado Bancário (B1, B2, B3S, B3C, B4, N1, N2, N4).',
            'type': 'categorical',
            'mapping': {
                'b1': (
                    'Banco Comercial, Banco Múltiplo com Carteira Comercial '
                    'ou Caixas Econômicas.'
                ),
                'b2': (
                    'Banco Múltiplo sem Carteira Comercial ou Banco de Câmbio '
                    'ou Banco de Investimento.'
                ),
                'b3s': 'Cooperativa de Crédito Singular.',
                'b3c': 'Central e Confederação de Cooperativas de Crédito.',
                'b4': 'Banco de Desenvolvimento.',
                'n1': 'Não bancário de Crédito.',
                'n2': 'Não bancário do Mercado de Capitais.',
                'n4': 'Instituições de Pagamento.',
            },
        },
        'td': {
            'description': 'Tipo de Consolidação (I) identifica uma Instituição Independente e (C) identifica um Conglomerado.',
            'type': 'categorical',
            'mapping': {
                'i': 'Instituição Independente',
                'c': 'Conglomerado',
            },
        },
        'tc': {
            'description': 'Tipo de Controle.',
            'type': 'categorical',
            'mapping': {
                '1': 'Público',
                '2': 'Privado Nacional',
                '3': 'Privado com Controle Estrangeiro',
            },
        },
        'sr': {
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
        'cidade': {
            'description': 'Cidade da sede da instituição.',
            'type': 'text',
        },
        'uf': {
            'description': 'Unidade da Federação onde fica a sede da instituição.',
            'type': 'categorical',
        },
        'data_base': {
            'description': 'Data-base do relatório.',
            'type': 'date',
        },
        # Operações Comerciais
        'operacoes_comerciais_compra_numero_operacoes': {
            'description': 'Número de registros de operações de câmbio de compra comerciais.',
            'type': 'numeric',
        },
        'operacoes_comerciais_compra_valor': {
            'description': 'Valor total equivalente em milhares de dólares dos Estados Unidos (USD) das operações de câmbio de compra comerciais.',
            'type': 'numeric',
        },
        'operacoes_comerciais_venda_numero_operacoes': {
            'description': 'Número de registros de operações de câmbio de venda comerciais.',
            'type': 'numeric',
        },
        'operacoes_comerciais_venda_valor': {
            'description': 'Valor total equivalente em milhares de dólares dos Estados Unidos (USD) das operações de câmbio de venda comerciais.',
            'type': 'numeric',
        },
        'operacoes_comerciais_total_numero_operacoes': {
            'description': 'Somatório do número de registros de operações de câmbio comerciais: exportações e importações.',
            'type': 'numeric',
        },
        'operacoes_comerciais_total_valor': {
            'description': 'Valor total equivalente em milhares de dólares dos Estados Unidos (USD) das operações de câmbio comerciais: exportações e importações.',
            'type': 'numeric',
        },
        # Operações Financeiras
        'operacoes_financeiras_compra_numero_operacoes': {
            'description': 'Número de registros de operações de câmbio de compra financeiras.',
            'type': 'numeric',
        },
        'operacoes_financeiras_compra_valor': {
            'description': 'Valor total equivalente em milhares de dólares dos Estados Unidos (USD) das operações de câmbio de compra financeiras.',
            'type': 'numeric',
        },
        'operacoes_financeiras_venda_numero_operacoes': {
            'description': 'Número de registros de operações de câmbio de venda financeiras.',
            'type': 'numeric',
        },
        'operacoes_financeiras_venda_valor': {
            'description': 'Valor total equivalente em milhares de dólares dos Estados Unidos (USD) das operações de câmbio de venda financeiras.',
            'type': 'numeric',
        },
        'operacoes_financeiras_total_numero_operacoes': {
            'description': 'Somatório do número de registros de operações de câmbio financeiras: do e para o exterior.',
            'type': 'numeric',
        },
        'operacoes_financeiras_total_valor': {
            'description': 'Valor total equivalente em milhares de dólares dos Estados Unidos (USD) das operações de câmbio financeiras: do e para o exterior.',
            'type': 'numeric',
        },
        # Mercado Primário
        'mercado_primario_total_numero_operacoes': {
            'description': 'Somatório do número de registros de operações de câmbio do Mercado Primário: comerciais e financeiras.',
            'type': 'numeric',
        },
        'mercado_primario_total_valor': {
            'description': 'Valor total equivalente em milhares de dólares dos Estados Unidos (USD) das operações de câmbio do Mercado Primário: comerciais e financeiras.',
            'type': 'numeric',
        },
        # Mercado Interbancário
        'mercado_interbancario_compra_numero_operacoes': {
            'description': 'Número de registros de operações de câmbio de compra do Mercado Interbancário.',
            'type': 'numeric',
        },
        'mercado_interbancario_compra_valor': {
            'description': 'Valor total equivalente em milhares de dólares dos Estados Unidos (USD) das operações de câmbio de compra do Mercado Interbancário.',
            'type': 'numeric',
        },
        'mercado_interbancario_venda_numero_operacoes': {
            'description': 'Número de registros de operações de câmbio de venda do Mercado Interbancário.',
            'type': 'numeric',
        },
        'mercado_interbancario_venda_valor': {
            'description': 'Valor total equivalente em milhares de dólares dos Estados Unidos (USD) das operações de câmbio de venda do Mercado Interbancário.',
            'type': 'numeric',
        },
        'mercado_interbancario_total_numero_operacoes': {
            'description': 'Somatório do número de registros de operações de câmbio do Mercado Interbancário.',
            'type': 'numeric',
        },
        'mercado_interbancario_total_valor': {
            'description': 'Valor total equivalente em milhares de dólares dos Estados Unidos (USD) das operações de câmbio do Mercado Interbancário.',
            'type': 'numeric',
        },
        # Totais Gerais
        'total_geral_numero_operacoes': {
            'description': 'Somatório do número de registros de operações de câmbio dos Mercados Primário e Interbancário.',
            'type': 'numeric',
        },
        'total_geral_valor': {
            'description': 'Valor total equivalente em milhares de dólares dos Estados Unidos (USD) das operações de câmbio dos Mercados Primário e Interbancário.',
            'type': 'numeric',
        },
    }
