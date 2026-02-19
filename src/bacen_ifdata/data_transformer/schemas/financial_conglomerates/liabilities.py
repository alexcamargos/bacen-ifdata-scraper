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


class FinancialConglomerateLiabilitiesSchema(BaseSchema):
    """
    Define e categoriza os nomes das colunas para os relatórios de PASSIVOS
    de conglomerados financeiros, enriquecido com metadados do dicionário de dados.
    """

    SCHEMA_DEFINITION: Final[dict[str, dict[str, Any]]] = {
        'instituicao': {
            'description': 'Nome da instituição ou do conglomerado no cadastro do Banco Central.',
            'type': 'text',
            'raw_csv_header': 'Instituição',
        },
        'codigo': {
            'description': 'Código do conglomerado ou CNPJ no cadastro do Banco Central.',
            'type': 'numeric',
            'raw_csv_header': 'Código',
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
        'segmento_resolucao': {
            'description': 'Segmento conforme Resolução nº 4.553/2017 (S1, S2, S3, S4, S5).',
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
            'description': (
                'Tipo de Controle: Identifica a origem do controle de capital dos conglomerados '
                'financeiros ou das instituições independentes.'
            ),
            'type': 'categorical',
            'raw_csv_header': 'TC',
            'mapping': {
                '1': 'Público',
                '2': 'Privado Nacional',
                '3': 'Privado com Controle Estrangeiro',
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
            'raw_csv_header': 'Depósitos à Vista',
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
            'raw_csv_header': 'Captações - Conta de Pagamento Pré-Paga (a5)',
        },
        'depositos_outros': {
            'description': (
                'Depósitos sob Aviso + Obrigações por Depósitos Especiais e de Fundos e Programas + '
                'APE - Depósitos Especiais + Depósitos em Moedas Estrangeiras + Outros Depósitos - '
                'Conta de Pagamento Pré-Paga.'
            ),
            'type': 'numeric',
            'raw_csv_header': 'Captações - Depósitos Outros (a6)',
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
            'raw_csv_header': ['Patrimônio Líquido (i)', 'Patrimônio Líquido (j)'],
        },
        'passivo_total': {
            'description': 'Passivo Circulante e Exigível a Longo Prazo + Patrimônio Líquido.',
            'type': 'numeric',
            'raw_csv_header': 'Passivo Total (j) = (h) + (i)',
        },
    }
