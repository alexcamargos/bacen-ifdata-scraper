#!/usr/bin/env python
# encoding: utf-8
#
#  ------------------------------------------------------------------------------
#  Name: income_statement.py
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


class IndividualInstitutionIncomeStatementSchema(BaseSchema):
    """
    Define e categoriza os nomes das colunas para os relatórios de DEMONSTRAÇÃO DO RESULTADO
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
        'rendas_operacoes_de_credito': {
            'description': 'Rendas de Operações de Crédito.',
            'type': 'numeric',
        },
        'rendas_operacoes_de_arrendamento_mercantil': {
            'description': 'Rendas de Operações de Arrendamento Mercantil.',
            'type': 'numeric',
        },
        'rendas_operacoes_tvm': {
            'description': 'Rendas de Operações com Títulos e Valores Mobiliários.',
            'type': 'numeric',
        },
        'rendas_operacoes_instrumentos_financeiros_derivativos': {
            'description': 'Rendas de Operações com Instrumentos Financeiros Derivativos.',
            'type': 'numeric',
        },
        'resultado_operacoes_cambio': {
            'description': 'Resultado de Operações de Câmbio.',
            'type': 'numeric',
        },
        'rendas_aplicacoes_compulsorias': {
            'description': 'Rendas de Aplicações Compulsórias.',
            'type': 'numeric',
        },
        'receitas_intermediacao_financeira': {
            'description': (
                'Somatório de Rendas de Operações de Crédito, Rendas de Operações de Arrendamento Mercantil, '
                'Rendas de Operações com TVM, Rendas de Operações com Instrumentos Financeiros Derivativos, '
                'Resultado de Operações de Câmbio e Rendas de Aplicações Compulsórias.'
            ),
            'type': 'numeric',
        },
        'despesas_captacao': {
            'description': 'Despesas de Captação.',
            'type': 'numeric',
        },
        'despesas_obrigacoes_emprestimos_repasses': {
            'description': 'Despesas de Obrigações por Empréstimos e Repasses.',
            'type': 'numeric',
        },
        'despesas_operacoes_arrendamento_mercantil': {
            'description': 'Despesas de Operações de Arrendamento Mercantil.',
            'type': 'numeric',
        },
        'despesas_operacoes_cambio': {
            'description': 'Resultado de Operações de Câmbio.',
            'type': 'numeric',
        },
        'resultado_provisao_creditos_dificil_liquidacao': {
            'description': 'Resultado de Provisão para Créditos de Difícil Liquidação.',
            'type': 'numeric',
        },
        'despesas_intermediacao_financeira': {
            'description': (
                'Somatório de Despesas de Captação, Despesas de Obrigações por Empréstimos e Repasses, '
                'Despesas de Operações de Arrendamento Mercantil, Resultado de Operações de Câmbio e '
                'Resultado de Provisão para Créditos de Difícil Liquidação.'
            ),
            'type': 'numeric',
        },
        'resultado_intermediacao_financeira': {
            'description': 'Somatório de Receitas de Intermediação Financeira e Despesas de Intermediação Financeira.',
            'type': 'numeric',
        },
        'rendas_prestacao_servicos': {
            'description': 'Rendas de Prestação de Serviços.',
            'type': 'numeric',
        },
        'rendas_tarifas_bancarias': {
            'description': 'Rendas de Tarifas Bancárias.',
            'type': 'numeric',
        },
        'despesas_pessoal': {
            'description': 'Despesas de Pessoal.',
            'type': 'numeric',
        },
        'despesas_administrativas': {
            'description': 'Despesas Administrativas.',
            'type': 'numeric',
        },
        'despesas_tributarias': {
            'description': 'Despesas Tributárias.',
            'type': 'numeric',
        },
        'resultado_participacoes': {
            'description': 'Resultado de Participações.',
            'type': 'numeric',
        },
        'outras_receitas_operacionais': {
            'description': 'Outras Receitas Operacionais.',
            'type': 'numeric',
        },
        'outras_despesas_operacionais': {
            'description': 'Outras Despesas Operacionais.',
            'type': 'numeric',
        },
        'outras_receitas_despesas_operacionais': {
            'description': (
                'Somatório de Rendas de Prestação de Serviços, Rendas de Tarifas Bancárias, '
                'Despesas de Pessoal, Despesas Administrativas, Despesas Tributárias, '
                'Resultado de Participações, Outras Receitas Operacionais e Outras Despesas Operacionais.'
            ),
            'type': 'numeric',
        },
        'resultado_operacional': {
            'description': 'Somatório do Resultado de Intermediação Financeira e de Outras Receitas/Despesas Operacionais.',
            'type': 'numeric',
        },
        'resultado_nao_operacional': {
            'description': 'Resultado Não Operacional.',
            'type': 'numeric',
        },
        'resultado_antes_tributacao_lucro_participacao': {
            'description': 'Somatório do Resultado Operacional e do Resultado Não Operacional.',
            'type': 'numeric',
        },
        'imposto_renda_contribuicao_social': {
            'description': 'Imposto de Renda e Contribuição Social.',
            'type': 'numeric',
        },
        'participacao_lucros': {
            'description': 'Participação nos Lucros.',
            'type': 'numeric',
        },
        'lucro_liquido': {
            'description': (
                'Resultado antes da Tributação, Lucro e Participação deduzido de Imposto de Renda e '
                'Contribuição Social e de Participação nos Lucros.'
            ),
            'type': 'numeric',
        },
        'juros_sobre_capital_social_cooperativas': {
            'description': 'Juros Sobre Capital Social de Cooperativas.',
            'type': 'numeric',
        },
    }
