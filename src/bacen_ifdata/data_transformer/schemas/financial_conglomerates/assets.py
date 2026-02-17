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


class FinancialConglomeratesAssetsSchema(BaseSchema):
    """
    Define e categoriza os nomes das colunas para os relatórios de ATIVOS
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
            'description': 'Cidade onde fica localizada a sede da instituição financeira.',
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
        'disponibilidades': {
            'description': 'Disponibilidades.',
            'type': 'numeric',
            'raw_csv_header': 'Disponibilidades (a)',
        },
        'aplicacoes_interfinanceiras_liquidez': {
            'description': 'Aplicações Interfinanceiras de Liquidez.',
            'type': 'numeric',
            'raw_csv_header': 'Aplicações Interfinanceiras de Liquidez (b)',
        },
        'tvm_e_instrumentos_financeiros_derivativos': {
            'description': 'Títulos e Valores Mobiliários e Instrumentos Financeiros Derivativos.',
            'type': 'numeric',
            'raw_csv_header': 'TVM e Instrumentos Financeiros Derivativos (c)',
        },
        'operacoes_de_credito': {
            'description': 'Operações de Crédito.',
            'type': 'numeric',
            'raw_csv_header': 'Operações de Crédito',
        },
        'provisao_operacoes_de_credito': {
            'description': 'Provisão sobre Operações de Crédito.',
            'type': 'numeric',
            'raw_csv_header': 'Operações de Crédito - Provisão sobre Operações de Crédito (d2)',
        },
        'operacoes_de_credito_liquidas_provisao': {
            'description': 'Operações de Crédito Líquidas de Provisão.',
            'type': 'numeric',
            'raw_csv_header': 'Operações de Crédito - Operações de Crédito Líquidas de Provisão (d)',
        },
        'arrendamento_mercantil_a_receber': {
            'description': 'Operações de Arrendamento Mercantil - Arrendamento Mercantil a Receber.',
            'type': 'numeric',
            'raw_csv_header': 'Arrendamento Mercantil',
        },
        'imobilizado_de_arrendamento': {
            'description': 'Imobilizado de Arrendamento.',
            'type': 'numeric',
            'raw_csv_header': 'Arrendamento Mercantil - Imobilizado de Arrendamento (e2)',
        },
        'credores_antecipacao_valor_residual': {
            'description': 'Credores por Antecipação de Valor Residual.',
            'type': 'numeric',
            'raw_csv_header': 'Arrendamento Mercantil - Credores por Antecipação de Valor Residual (e3)',
        },
        'provisao_arrendamento_mercantil': {
            'description': 'Provisão sobre Arrendamento Mercantil.',
            'type': 'numeric',
            'raw_csv_header': 'Arrendamento Mercantil - Provisão sobre Arrendamento Mercantil (e4)',
        },
        'arrendamento_mercantil_liquido_de_provisao': {
            'description': (
                'Operações de Arrendamento Mercantil + Imobilizado de Arrendamento + '
                'Credores por Antecipação de Valor Residual.'
            ),
            'type': 'numeric',
            'raw_csv_header': 'Arrendamento Mercantil - Arrendamento Mercantil Líquido de Provisão (e)',
        },
        'outros_creditos_liquido_de_provisao': {
            'description': 'Outros Créditos - Líquido de Provisão.',
            'type': 'numeric',
            'raw_csv_header': 'Outros Créditos - Líquido de Provisão (f)',
        },
        'outros_ativos_realizaveis': {
            'description': 'Outros Valores e Bens + Relações Interfinanceiras + Relações Interdependências.',
            'type': 'numeric',
            'raw_csv_header': 'Outros Ativos Realizáveis (g)',
        },
        'permanente_ajustado': {
            'description': 'Ativo Permanente - Imobilizado de Arrendamento.',
            'type': 'numeric',
            'raw_csv_header': 'Permanente Ajustado (h)',
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
            'raw_csv_header': 'Ativo Total Ajustado (i) = (a) + (b) + (c) + (d) + (e) + (f) + (g) + (h)',
        },
        'credores_antecipacao_valor_residual_j': {
            'description': 'Credores por Antecipação de Valor Residual.',
            'type': 'numeric',
            'raw_csv_header': 'Credores por Antecipação de Valor Residual (j)',
        },
        'ativo_total': {
            'description': 'Ativo Circulante e Realizável a Longo Prazo + Ativo Permanente.',
            'type': 'numeric',
            'raw_csv_header': 'Ativo Total (k) = (i) - (j)',
        },
    }
