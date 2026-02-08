#!/usr/bin/env python
# encoding: utf-8

# ------------------------------------------------------------------------------
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


class PrudentialConglomeratesAssetsSchema(BaseSchema):
    """
    Define e categoriza os nomes das colunas para os relatórios de ATIVOS
    de conglomerados prudenciais, enriquecido com metadados do dicionário de dados.
    """

    SCHEMA_DEFINITION: Final[dict[str, dict[str, Any]]] = {
        'instituicao_financeira': {
            'description': 'Nome da instituição ou do conglomerado no cadastro do Banco Central.',
            'type': 'text',
        },
        'codigo': {
            'description': 'Código da instituição ou do conglomerado no cadastro do Banco Central.',
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
        'tipo_de_consolidacao': {
            'description': 'Tipo de Consolidação (I) identifica uma Instituição Independente e (C) identifica um Conglomerado.',
            'type': 'categorical',
            'mapping': {
                'i': 'Instituição Independente',
                'c': 'Conglomerado',
            },
        },
        'tipo_de_controle': {
            'description': (
                'Tipo de Controle: Identifica a origem do controle de capital dos conglomerados '
                'bancários ou das instituições independentes.'
            ),
            'type': 'categorical',
            'mapping': {'1': 'Público', '2': 'Privado Nacional', '3': 'Controle Estrangeiro'},
        },
        'cidade': {'description': 'Cidade onde fica localizada a sede da instituição.', 'type': 'text'},
        'uf': {'description': 'Unidade da Federação onde fica a sede da instituição.', 'type': 'categorical'},
        'data_base': {'description': 'Data-base do Relatório.', 'type': 'date'},
        'disponibilidades': {'description': 'Disponibilidades.', 'type': 'numeric'},
        'aplicacoes_interfinanceiras_liquidez': {
            'description': 'Aplicações Interfinanceiras de Liquidez.',
            'type': 'numeric',
        },
        'tvm_e_instrumentos_financeiros_derivativos': {
            'description': 'Títulos e Valores Mobiliários e Instrumentos Financeiros Derivativos.',
            'type': 'numeric',
        },
        'operacoes_de_credito': {
            'description': 'Operações de Crédito - Provisão para Operações de Crédito.',
            'type': 'numeric',
        },
        'provisao_operacoes_de_credito': {'description': 'Provisão para Operações de Crédito.', 'type': 'numeric'},
        'operacoes_de_credito_liquidas_provisao': {
            'description': 'Operações de Crédito Líquidas de Provisão.',
            'type': 'numeric',
        },
        'arrendamento_mercantil_a_receber': {
            'description': 'Operações de Arrendamento Mercantil - Provisões para Operações de Arrendamento Mercantil.',
            'type': 'numeric',
        },
        'imobilizado_de_arrendamento': {'description': 'Imobilizado de Arrendamento.', 'type': 'numeric'},
        'credores_antecipacao_valor_residual': {
            'description': 'Credores por Antecipação de Valor Residual.',
            'type': 'numeric',
        },
        'provisao_arrendamento_mercantil': {
            'description': 'Provisões para Operações de Arrendamento Mercantil.',
            'type': 'numeric',
        },
        'arrendamento_mercantil_liquido_de_provisao': {
            'description': 'Operações de Arrendamento Mercantil + Imobilizado de Arrendamento + Credores por Antecipação de Valor Residual.',
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
        'permanente_ajustado': {'description': 'Ativo Permanente - Imobilizado de Arrendamento.', 'type': 'numeric'},
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
