#!/usr/bin/env python
# encoding: utf-8

# ------------------------------------------------------------------------------
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


class PrudentialConglomerateIncomeStatementSchema(BaseSchema):
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
        'rendas_operacoes_de_credito': {
            'description': 'Rendas de Operações de Crédito.',
            'type': 'numeric',
            'raw_csv_header': 'Resultado de Intermediação Financeira - Rendas de Operações de Crédito (a1)',
        },
        'rendas_operacoes_de_arrendamento_mercantil': {
            'description': 'Rendas de Operações de Arrendamento Mercantil.',
            'type': 'numeric',
            'raw_csv_header': 'Resultado de Intermediação Financeira - Rendas de Operações de Arrendamento Mercantil (a2)',
        },
        'rendas_operacoes_tvm': {
            'description': 'Rendas de Operações com Títulos e Valores Mobiliários.',
            'type': 'numeric',
            'raw_csv_header': 'Resultado de Intermediação Financeira - Rendas de Operações com TVM (a3)',
        },
        'rendas_operacoes_instrumentos_financeiros_derivativos': {
            'description': 'Rendas de Operações com Instrumentos Financeiros Derivativos.',
            'type': 'numeric',
            'raw_csv_header': 'Resultado de Intermediação Financeira - Rendas de Operações com Instrumentos Financeiros Derivativos (a4)',
        },
        'rendas_operacoes_cambio': {
            'description': 'Rendas de Operações de Câmbio.',
            'type': 'numeric',
            'raw_csv_header': 'Resultado de Intermediação Financeira - Resultado de Operações de Câmbio (a5)',
        },
        'rendas_aplicacoes_compulsorias': {
            'description': 'Rendas de Aplicações Compulsórias.',
            'type': 'numeric',
            'raw_csv_header': 'Resultado de Intermediação Financeira - Rendas de Aplicações Compulsórias (a6)',
        },
        'receitas_intermediacao_financeira': {
            'description': 'Somatório das receitas de Intermediação Financeira.',
            'type': 'numeric',
            'raw_csv_header': 'Resultado de Intermediação Financeira - Receitas de Intermediação Financeira (a) = (a1) + (a2) + (a3) + (a4) + (a5) + (a6)',
        },
        'despesas_captacao': {
            'description': 'Despesas de Captação.',
            'type': 'numeric',
            'raw_csv_header': 'Resultado de Intermediação Financeira - Despesas de Captação (b1)',
        },
        'despesas_obrigacoes_emprestimos_repasses': {
            'description': 'Despesas de Obrigações por Empréstimos e Repasses.',
            'type': 'numeric',
            'raw_csv_header': 'Resultado de Intermediação Financeira - Despesas de Obrigações por Empréstimos e Repasses (b2)',
        },
        'despesas_operacoes_arrendamento_mercantil': {
            'description': 'Despesas de Operações de Arrendamento Mercantil.',
            'type': 'numeric',
            'raw_csv_header': 'Resultado de Intermediação Financeira - Despesas de Operações de Arrendamento Mercantil (b3)',
        },
        'despesas_operacoes_cambio': {
            'description': 'Despesas de Operações de Câmbio.',
            'type': 'numeric',
            'raw_csv_header': 'Resultado de Intermediação Financeira - Resultado de Operações de Câmbio (b4)',
        },
        'resultado_provisao_creditos_dificil_liquidacao': {
            'description': 'Resultado de Provisão para Créditos de Difícil Liquidação.',
            'type': 'numeric',
            'raw_csv_header': 'Resultado de Intermediação Financeira - Resultado de Provisão para Créditos de Difícil Liquidação (b5)',
        },
        'despesas_intermediacao_financeira': {
            'description': 'Somatório das despesas de Intermediação Financeira.',
            'type': 'numeric',
            'raw_csv_header': 'Resultado de Intermediação Financeira - Despesas de Intermediação Financeira (b) = (b1) + (b2) + (b3) + (b4) + (b5)',
        },
        'resultado_intermediacao_financeira': {
            'description': 'Resultado de Intermediação Financeira.',
            'type': 'numeric',
            'raw_csv_header': 'Resultado de Intermediação Financeira (c) = (a) + (b)',
        },
        'rendas_prestacao_servicos': {
            'description': 'Rendas de Prestação de Serviços.',
            'type': 'numeric',
            'raw_csv_header': 'Outras Receitas/Despesas Operacionais - Rendas de Prestação de Serviços (d1)',
        },
        'rendas_tarifas_bancarias': {
            'description': 'Rendas de Tarifas Bancárias.',
            'type': 'numeric',
            'raw_csv_header': 'Outras Receitas/Despesas Operacionais - Rendas de Tarifas Bancárias (d2)',
        },
        'despesas_pessoal': {
            'description': 'Despesas de Pessoal.',
            'type': 'numeric',
            'raw_csv_header': 'Outras Receitas/Despesas Operacionais - Despesas de Pessoal (d3)',
        },
        'despesas_administrativas': {
            'description': 'Despesas Administrativas.',
            'type': 'numeric',
            'raw_csv_header': 'Outras Receitas/Despesas Operacionais - Despesas Administrativas (d4)',
        },
        'despesas_tributarias': {
            'description': 'Despesas Tributárias.',
            'type': 'numeric',
            'raw_csv_header': 'Outras Receitas/Despesas Operacionais - Despesas Tributárias (d5)',
        },
        'resultado_participacoes': {
            'description': 'Resultado de Participações.',
            'type': 'numeric',
            'raw_csv_header': 'Outras Receitas/Despesas Operacionais - Resultado de Participações (d6)',
        },
        'outras_receitas_operacionais': {
            'description': 'Outras Receitas Operacionais.',
            'type': 'numeric',
            'raw_csv_header': 'Outras Receitas/Despesas Operacionais - Outras Receitas Operacionais (d7)',
        },
        'outras_despesas_operacionais': {
            'description': 'Outras Despesas Operacionais.',
            'type': 'numeric',
            'raw_csv_header': 'Outras Receitas/Despesas Operacionais - Outras Despesas Operacionais (d8)',
        },
        'outras_receitas_despesas_operacionais': {
            'description': 'Somatório de outras receitas/despesas operacionais.',
            'type': 'numeric',
            'raw_csv_header': 'Outras Receitas/Despesas Operacionais - Outras Receitas/Despesas  Operacionais (d) = (d1) + (d2) + (d3) + (d4) + (d5) + (d6) + (d7) + (d8)',
        },
        'resultado_operacional': {
            'description': 'Somatório do Resultado de Intermediação Financeira e de Outras Receitas/Despesas Operacionais.',
            'type': 'numeric',
            'raw_csv_header': 'Resultado Operacional (e) = (c) + (d)',
        },
        'resultado_nao_operacional': {
            'description': 'Resultado Não Operacional.',
            'type': 'numeric',
            'raw_csv_header': 'Resultado Não Operacional (f)',
        },
        'resultado_antes_tributacao_participacao': {
            'description': 'Resultado antes da Tributação e Participação.',
            'type': 'numeric',
            'raw_csv_header': 'Resultado antes da Tributação, Lucro e Participação (g) = (e) + (f)',
        },
        'imposto_renda_contribuicao_social': {
            'description': 'Imposto de Renda e Contribuição Social.',
            'type': 'numeric',
            'raw_csv_header': 'Imposto de Renda e Contribuição Social (h)',
        },
        'participacao_lucros': {
            'description': 'Participação nos Lucros.',
            'type': 'numeric',
            'raw_csv_header': 'Participação nos Lucros (i)',
        },
        'lucro_liquido': {
            'description': (
                'Resultado antes da Tributação e Participação deduzido de Imposto de Renda e '
                'Contribuição Social e de Participação nos Lucros.'
            ),
            'type': 'numeric',
            'raw_csv_header': 'Lucro Líquido (j) = (g) + (h) + (i)',
        },
        'juros_sobre_capital_proprio': {
            'description': 'Despesas de Juros Sobre Capital Próprio de Cooperativas.',
            'type': 'numeric',
            'raw_csv_header': 'Juros Sobre Capital Próprio (k)',
        },
    }
