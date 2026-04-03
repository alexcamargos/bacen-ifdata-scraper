#!/usr/bin/env python
# encoding: utf-8
#
#  ------------------------------------------------------------------------------
#  Name: liabilities.py
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


class IndividualInstitutionLiabilitiesSchema(BaseSchema):
    """
    Define e categoriza os nomes das colunas para os relatórios de PASSIVOS
    de instituições individuais, enriquecido com metadados do dicionário de dados.
    """

    SCHEMA_DEFINITION: Final[dict[str, dict[str, Any]]] = {
        'instituicao': {
            'description': 'Nome da instituição no cadastro do Banco Central.',
            'type': 'text',
            'raw_csv_header': 'Instituição',
        },
        'codigo': {
            'description': 'Código do conglomerado ou CNPJ no cadastro do Banco Central.',
            'type': 'numeric',
            'raw_csv_header': 'Código',
        },
        'conglomerado': {
            'description': (
                'Nome do conglomerado a que pertence a instituição individual.'
                ' Caso a instituição não pertença a nenhum conglomerado, esse campo estará sem informação.'
            ),
            'type': 'text',
            'raw_csv_header': 'Conglomerado Financeiro.1',
        },
        'conglomerado_financeiro': {
            'description': (
                'Código do conglomerado financeiro a que pertence a instituição individual.'
                ' Caso a instituição não pertença a nenhum conglomerado, esse campo estará sem informação.'
            ),
            'type': 'numeric',
            'raw_csv_header': 'Conglomerado Financeiro',
        },
        'conglomerado_prudencial': {
            'description': (
                'Código do conglomerado prudencial a que pertence a instituição individual.'
                ' Caso a instituição não pertença a nenhum conglomerado, esse campo estará sem informação.'
            ),
            'type': 'numeric',
            'raw_csv_header': 'Conglomerado Prudencial',
        },
        'consolidado_bancario': {
            'description': 'Tipo de Consolidado Bancário (B1, B2, B3S, B3C, B4, N1, N2, N4).',
            'type': 'categorical',
            'raw_csv_header': 'TCB',
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
            'raw_csv_header': 'TC',
            'mapping': {
                '1': 'Público',
                '2': 'Privado Nacional',
                '3': 'Privado com Controle Estrangeiro',
            },
        },
        'tipo_de_instituicao': {
            'description': 'Tipo de Instituição.',
            'type': 'categorical',
            'raw_csv_header': 'TI',
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
            'description': 'Data-base do Relatório.',
            'type': 'date',
            'raw_csv_header': 'Data',
        },
        'depositos_vista': {
            'description': 'Depósitos à Vista.',
            'type': 'numeric',
            'raw_csv_header': ['Captações', 'Captações - Depósitos à Vista (a1)'],
        },
        'depositos_poupanca': {
            'description': 'Depósitos de Poupança.',
            'type': 'numeric',
            'raw_csv_header': 'Captações - Depósitos de Poupança (a2)',
        },
        'depositos_interfinanceiros': {
            'description': 'Depósitos Interfinanceiros.',
            'type': 'numeric',
            'raw_csv_header': 'Captações - Depósitos Interfinanceiros (a3)',
        },
        'depositos_a_prazo': {
            'description': 'Depósitos a Prazo.',
            'type': 'numeric',
            'raw_csv_header': 'Captações - Depósitos a Prazo (a4)',
        },
        'conta_de_pagamento_pre_paga': {
            'description': 'Conta de Pagamento Pré-Paga.',
            'type': 'numeric',
            'raw_csv_header': ['Captações - Conta de Pagamento Pré-Paga (a5)', 'Captações - Conta de Pagamento Pré-Paga (a4)'],
        },
        'depositos_outros': {
            'description': (
                'Depósitos sob Aviso + Obrigações por Depósitos Especiais e de Fundos e Programas + '
                'APE - Depósitos Especiais + Depósitos em Moedas Estrangeiras + Outros Depósitos - '
                'Conta de Pagamento Pré-Paga.'
            ),
            'type': 'numeric',
            'raw_csv_header': 'Captações - Outros Depósitos (a5)',
        },
        'deposito_total': {
            'description': 'Depósito Total.',
            'type': 'numeric',
            'raw_csv_header': 'Captações - Depósito Total (a)',
        },
        'obrigacoes_operacoes_compromissadas': {
            'description': 'Obrigações por Operações Compromissadas.',
            'type': 'numeric',
            'raw_csv_header': 'Captações - Obrigações por Operações Compromissadas (b)',
        },
        'letras_de_credito_imobiliario': {
            'description': 'LCI - Letras de Crédito Imobiliário.',
            'type': 'numeric',
            'raw_csv_header': 'Captações - Letras de Crédito Imobiliário (c1)',
        },
        'letras_de_credito_agronegocio': {
            'description': 'LCA - Letras de Crédito do Agronegócio.',
            'type': 'numeric',
            'raw_csv_header': 'Captações - Letras de Crédito do Agronegócio (c2)',
        },
        'letras_financeiras': {
            'description': 'LF - Letras Financeiras.',
            'type': 'numeric',
            'raw_csv_header': 'Captações - Letras Financeiras (c3)',
        },
        'obrigacoes_titulos_e_valores_mobiliarios_exterior': {
            'description': 'Obrigações por Títulos e Valores Mobiliários no Exterior.',
            'type': 'numeric',
            'raw_csv_header': 'Captações - Obrigações por Títulos e Valores Mobiliários no Exterior (c4)',
        },
        'outros_recursos_de_aceites_e_emissao_de_titulos': {
            'description': (
                'Recursos de Aceites e Emissão de Títulos - LCI - LCA - LF - '
                'Obrigações por Títulos e Valores Mobiliários no Exterior.'
            ),
            'type': 'numeric',
            'raw_csv_header': 'Captações - Outros Recursos de Aceites e Emissão de Títulos (c5)',
        },
        'recursos_de_aceites_e_emissao_de_titulos': {
            'description': 'Recursos de Aceites e Emissão de Títulos.',
            'type': 'numeric',
            'raw_csv_header': 'Captações - Recursos de Aceites e Emissão de Títulos (c)',
        },
        'obrigacoes_emprestimos_e_repasses': {
            'description': 'Obrigações por Empréstimos e Repasses.',
            'type': 'numeric',
            'raw_csv_header': 'Captações - Obrigações por Empréstimos e Repasses (d)',
        },
        'captacoes': {
            'description': (
                'Depósito Total + Obrigações por Operações Compromissadas + '
                'Recursos de Aceites e Emissão de Títulos + Obrigações por Empréstimos e Repasses.'
            ),
            'type': 'numeric',
            'raw_csv_header': 'Captações - Captações (e) = (a) + (b) + (c) + (d)',
        },
        'instrumentos_derivativos': {
            'description': 'Instrumentos Financeiros Derivativos.',
            'type': 'numeric',
            'raw_csv_header': 'Instrumentos Derivativos (f)',
        },
        'outras_obrigacoes': {
            'description': 'Outras Obrigações + Relações Interfinanceiras + Relações Interdependências.',
            'type': 'numeric',
            'raw_csv_header': 'Outras Obrigações (g)',
        },
        'passivo_circulante_exigivel_a_longo_prazo': {
            'description': 'Passivo Circulante e Exigível a Longo Prazo.',
            'type': 'numeric',
            'raw_csv_header': 'Passivo Circulante e Exigível a Longo Prazo (h) = (e) + (f) + (g)',
        },
        'patrimonio_liquido': {
            'description': 'Patrimônio Líquido + Contas de Resultado Credoras + Contas de Resultado Devedoras.',
            'type': 'numeric',
            'raw_csv_header': 'Patrimônio Líquido (j)',
        },
        'passivo_total': {
            'description': 'Passivo Circulante e Exigível a Longo Prazo + Patrimônio Líquido.',
            'type': 'numeric',
            'raw_csv_header': 'Passivo Total (k) = (h) + (i) + (j)',
        },
    }
