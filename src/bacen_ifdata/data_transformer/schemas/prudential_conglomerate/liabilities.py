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


class PrudentialConglomerateLiabilitiesSchema(BaseSchema):
    """
    Define e categoriza os nomes das colunas para os relatórios de
    conglomerados prudenciais, enriquecido com metadados do dicionário de dados.
    """

    SCHEMA_DEFINITION: Final[dict[str, dict[str, Any]]] = {
        'instituicao': {
            'description': 'Nome da instituição ou conglomerado no cadastro do Banco Central.',
            'type': 'text',
            'raw_csv_header': 'Instituição',
        },
        'codigo': {
            'description': 'Código da instituição ou conglomerado no cadastro do Banco Central.',
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
        'cidade': {
            'description': 'Cidade da sede da instituição.',
            'type': 'text',
            'raw_csv_header': 'Cidade',
        },
        'uf': {
            'description': 'Unidade da Federação onde fica a sede da institution.',
            'type': 'categorical',
            'raw_csv_header': 'UF',
        },
        'regiao': {
            'description': 'Região geográfica onde fica a sede da instituição.',
            'type': 'categorical',
        },
        'data_base': {
            'description': 'Data-Base do relatório.',
            'type': 'date',
            'raw_csv_header': 'Data',
        },
        'depositos_vista': {
            'description': 'Depósitos à vista.',
            'type': 'numeric',
            'raw_csv_header': ['Captações', 'Captações - Depósitos à Vista (a1)'],
        },
        'depositos_poupanca': {
            'description': 'Depósitos Poupança.',
            'type': 'numeric',
            'raw_csv_header': 'Captações - Depósitos de Poupança (a2)',
        },
        'depositos_interfinanceiros': {
            'description': 'Depósitos interfinanceiros.',
            'type': 'numeric',
            'raw_csv_header': 'Captações - Depósitos Interfinanceiros (a3)',
        },
        'depositos_a_prazo': {
            'description': 'Depósitos a prazo.',
            'type': 'numeric',
            'raw_csv_header': 'Captações - Depósitos a Prazo (a4)',
        },
        'conta_de_pagamento_pre_paga': {
            'description': 'Conta de pagamento pré-paga.',
            'type': 'numeric',
            'raw_csv_header': ['Captações - Conta de Pagamento Pré-Paga (a5)', 'Captações - Conta de Pagamento Pré-Paga (a4)'],
        },
        'depositos_outros': {
            'description': (
                '(+) Depósitos sob aviso (+) Obrigações por depósitos especiais e de fundos e '
                'programas (+) APE - Depósitos especiais (+) Depósitos em moedas estrangeiras '
                '(+) Outros depósitos (-) Conta de pagamento pré-paga.'
            ),
            'type': 'numeric',
            'raw_csv_header': 'Captações - Outros Depósitos (a5)',
        },
        'deposito_total': {
            'description': 'Depósito Totais.',
            'type': 'numeric',
            'raw_csv_header': 'Captações - Depósito Total (a)',
        },
        'obrigações_operações_compromissadas': {
            'description': 'Obrigações por Operações Compromissadas.',
            'type': 'numeric',
            'raw_csv_header': 'Captações - Obrigações por Operações Compromissadas (b)',
        },
        'letras_de_credito_imobiliario': {
            'description': 'LCI - Obrigações por Emissão de Letras de Crédito Imobiliário.',
            'type': 'numeric',
            'raw_csv_header': 'Captações - Letras de Crédito Imobiliário (c1)',
        },
        'letras_de_credito_agronegocio': {
            'description': 'LCA - Obrigações por Emissão de Letras de Crédito do Agronegócio.',
            'type': 'numeric',
            'raw_csv_header': 'Captações - Letras de Crédito do Agronegócio (c2)',
        },
        'letras_financeiras': {
            'description': 'LF - Obrigações por Emissão de Letras Financeiras.',
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
                '(+) Recursos de aceites cambiais, letras imobiliárias e hipotecárias, debêntures, '
                'e similares (-) Obrigações por Emissão de Letras de Crédito Imobiliário (-) '
                'Obrigações por Emissão de Letras de Crédito do Agronegócio (-) Obrigações por '
                'Emissão de Letras Financeiras (-) Obrigações por Títulos e Valores Mobiliários no Exterior.'
            ),
            'type': 'numeric',
            'raw_csv_header': 'Captações - Outros Recursos de Aceites e Emissão de Títulos (c5)',
        },
        'recursos_de_aceites_e_emissao_de_titulos': {
            'description': 'Recursos de aceites cambiais, letras imobiliárias e hipotecárias, debêntures, e similares.',
            'type': 'numeric',
            'raw_csv_header': 'Captações - Recursos de Aceites e Emissão de Títulos (c)',
        },
        'obrigacoes_emprestimos_e_repasses': {
            'description': 'Obrigações por empréstimos e repasses.',
            'type': 'numeric',
            'raw_csv_header': 'Captações - Obrigações por Empréstimos e Repasses (d)',
        },
        'captacoes': {
            'description': (
                '(+) Depósitos (+) Obrigações por Operações Compromissadas (+) Recursos de aceites '
                'cambiais, letras imobiliárias e hipotecárias, debêntures, e similares (+) Obrigações '
                'por empréstimos e repasses.'
            ),
            'type': 'numeric',
            'raw_csv_header': 'Captações - Captações (e) = (a) + (b) + (c) + (d)',
        },
        'instrumentos_derivativos': {
            'description': 'Instrumentos financeiros derivativos.',
            'type': 'numeric',
            'raw_csv_header': 'Instrumentos Derivativos (f)',
        },
        'outras_obrigações': {
            'description': '(+) Relações Interfinanceiras (+) Relações interdependências (+) Outras obrigações.',
            'type': 'numeric',
            'raw_csv_header': 'Outras Obrigações (g)',
        },
        'passivo_circulante_exigível_a_longo_prazo': {
            'description': 'Passivo circulante e exigível a longo prazo.',
            'type': 'numeric',
            'raw_csv_header': 'Passivo Circulante e Exigível a Longo Prazo (h) = (e) + (f) + (g)',
        },
        'resultados_exercicios_futuros': {
            'description': 'Resultados de Exercícios Futuros.',
            'type': 'numeric',
            'raw_csv_header': 'Resultados de Exercícios Futuros (i)',
        },
        'patrimonio_liquido': {
            'description': '(+) Patrimônio Líquido (+) Contas de resultado credoras (+) Contas de resultado devedoras',
            'type': 'numeric',
            'raw_csv_header': 'Patrimônio Líquido (j)',
        },
        'passivo_total': {
            'description': (
                '(+) Passivo circulante e exigível a longo prazo (+) Patrimônio Líquido (+) '
                'Contas de resultado credoras (+) Contas de resultado devedoras.'
            ),
            'type': 'numeric',
            'raw_csv_header': 'Passivo Total (k) = (h) + (i) + (j)',
        },
    }
