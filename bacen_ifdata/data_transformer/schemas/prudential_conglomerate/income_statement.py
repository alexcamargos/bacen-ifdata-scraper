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


class PrudentialConglomerateIncomeStatementSchema:
    """
    Define e categoriza os nomes das colunas para os relatórios de
    conglomerados prudenciais, enriquecido com metadados do dicionário de dados.
    """

    SCHEMA_DEFINITION = {
        'instituicao': {
            'description': 'Nome da instituição ou conglomerado no cadastro do Banco Central.',
            'type': 'text'
        },
        'codigo': {
            'description': 'Código da instituição ou conglomerado no cadastro do Banco Central.',
            'type': 'numeric'
        },
        'tcb': {
            'description': 'Tipo de Consolidado Bancário (B1, B2, B3S, B3C, B4, N1, N2, N4).',
            'type': 'categorical',
            'mapping': {
                'b1': ('Instituição individual do tipo Banco Comercial, Banco Múltiplo com Carteira Comercial '
                       'ou caixas econômicas e Conglomerado composto de pelo menos uma instituição do tipo Banco '
                       'Comercial, Banco Múltiplo com Carteira Comercial ou caixas econômicas.'),
                'b2': ('Instituição individual do tipo Banco Múltiplo sem Carteira Comercial ou Banco de Câmbio '
                       'ou Banco de Investimento e Conglomerado composto de pelo menos uma instituição do tipo '
                       'Banco Múltiplo sem Carteira Comercial ou Banco de Investimento, mas sem conter instituições '
                       'do tipo Banco Comercial e Banco Múltiplo com Carteira Comercial.'),
                'b3s': 'Cooperativa de Crédito Singular.',
                'b3c': 'Central e Confederação de Cooperativas de Crédito.',
                'b4': 'Banco de Desenvolvimento',
                'n1': 'Instituição não bancária atuante no mercado de crédito.',
                'n2': 'Instituição não bancária atuante no mercado de capitais.',
                'n4': 'Instituições de pagamento.'
            }
        },
        'segmento': {
            'description': 'Segmento conforme Resolução n.º 4.553/2017 (S1, S2, S3, S4, S5).',
            'type': 'categorical',
            'mapping': {
                's1': ('Bancos múltiplos, bancos comerciais, bancos de investimento, bancos de câmbio e caixas '
                       'econômicas que (i) tenham porte (Exposição/Produto Interno Bruto) superior a 10%; ou (ii) '
                       'exerçam atividade internacional relevante (ativos no exterior superiores a US$ 10 bilhões).'),
                's2': ('Composto por: (i) bancos múltiplos, bancos comerciais, bancos de investimento, '
                       'bancos de câmbio e caixas econômicas de porte inferior a 10% e igual ou superior '
                       'a 1%; e (ii) demais instituições autorizadas a funcionar pelo Banco Central do '
                       'Brasil de porte igual ou superior a 1% do PIB.'),
                's3': 'Instituições de porte inferior a 1% e igual ou superior a 0,1%.',
                's4': 'Instituições de porte inferior a 0,1%.',
                's5': ('Composto por: (i) instituições de porte inferior a 0,1% que utilizem metodologia '
                       'facultativa simplificada para apuração dos requerimentos mínimos de Patrimônio '
                       'de Referência (PR), de Nível I e de Capital Principal, exceto bancos múltiplos, '
                       'bancos comerciais, bancos de investimento, bancos de câmbio e caixas econômicas; '
                       'e (ii) não sujeitas a apuração de PR.'),
            }
        },
        'td': {
            'description': 'Tipo de Consolidação (I) identifica uma Instituição Independente e (C) identifica um Conglomerado.',
            'type': 'categorical',
            'mapping': {
                'i': 'Instituição Independente',
                'c': 'Conglomerado',
            }
        },
        'tc': {
            'description': 'Tipo de Controle.',
            'type': 'categorical',
            'mapping': {
                '1': 'Público',
                '2': 'Privado Nacional',
                '3': 'Controle Estrangeiro'
            }
        },
        'cidade': {
            'description': 'Cidade da sede da instituição.',
            'type': 'text'
        },
        'uf': {
            'description': 'Unidade da Federação onde fica a sede da instituição.',
            'type': 'categorical'
        },
        'data_base': {
            'description': 'Data-base do relatório.',
            'type': 'date'
        },

        'rendas_operacoes_de_credito': {
            'description': 'Rendas de Operações de Crédito.',
            'type': 'numeric'
        },
        'rendas_operacoes_de_arrendamento_mercantil': {
            'description': 'Rendas de Operações de Arrendamento Mercantil.',
            'type': 'numeric'
        },
        'rendas_operacoes_tvm': {
            'description': 'Rendas de Operações com Títulos e Valores Mobiliários.',
            'type': 'numeric'
        },
        'rendas_operacoes_instrumentos_financeiros_derivativos': {
            'description': 'Rendas de Operações com Instrumentos Financeiros Derivativos.',
            'type': 'numeric'
        },
        'rendas_operacoes_cambio': {
            'description': 'Rendas de Operações de Câmbio.',
            'type': 'numeric'
        },
        'rendas_aplicacoes_compulsorias': {
            'description': 'Rendas de Aplicações Compulsórias.',
            'type': 'numeric'
        },
        'receitas_intermediacao_financeira': {
            'description': 'Somatório das receitas de Intermediação Financeira.',
            'type': 'numeric'
        },
        'despesas_captacao': {
            'description': 'Despesas de Captação.',
            'type': 'numeric'
        },
        'despesas_obrigacoes_emprestimos_repasses': {
            'description': 'Despesas de Obrigações por Empréstimos e Repasses.',
            'type': 'numeric'
        },
        'despesas_operacoes_arrendamento_mercantil': {
            'description': 'Despesas de Operações de Arrendamento Mercantil.',
            'type': 'numeric'
        },
        'despesas_operacoes_cambio': {
            'description': 'Despesas de Operações de Câmbio.',
            'type': 'numeric'
        },

        'resultado_provisao_creditos_dificil_liquidacao': {
            'description': 'Resultado de Provisão para Créditos de Difícil Liquidação.',
            'type': 'numeric'
        },
        'despesas_intermediacao_financeira': {
            'description': 'Somatório das despesas de Intermediação Financeira.',
            'type': 'numeric'
        },
        'resultado_intermediacao_financeira': {
            'description': 'Resultado de Intermediação Financeira.',
            'type': 'numeric'
        },
        'rendas_prestacao_servicos': {
            'description': 'Rendas de Prestação de Serviços.',
            'type': 'numeric'
        },
        'rendas_tarifas_bancarias': {
            'description': 'Rendas de Tarifas Bancárias.',
            'type': 'numeric'
        },
        'despesas_pessoal': {
            'description': 'Despesas de Pessoal.',
            'type': 'numeric'
        },
        'despesas_administrativas': {
            'description': 'Despesas Administrativas.',
            'type': 'numeric'
        },
        'despesas_tributarias': {
            'description': 'Despesas Tributárias.',
            'type': 'numeric'
        },
        'resultado_participacoes': {
            'description': 'Resultado de Participações.',
            'type': 'numeric'
        },
        'outras_receitas_operacionais': {
            'description': 'Outras Receitas Operacionais.',
            'type': 'numeric'
        },
        'outras_despesas_operacionais': {
            'description': 'Outras Despesas Operacionais.',
            'type': 'numeric'
        },
        'outras_receitas_despesas_operacionais': {
            'description': 'Somatório de outras receitas/despesas operacionais.',
            'type': 'numeric'
        },
        'resultado_operacional': {
            'description': 'Somatório do Resultado de Intermediação Financeira e de Outras Receitas/Despesas Operacionais.',
            'type': 'numeric'
        },
        'resultado_nao_operacional': {
            'description': 'Resultado Não Operacional.',
            'type': 'numeric'
        },
        'resultado_antes_tributacao_participacao': {
            'description': 'Resultado antes da Tributação e Participação.',
            'type': 'numeric'
        },
        'imposto_renda_contribuicao_social': {
            'description': 'Imposto de Renda e Contribuição Social.',
            'type': 'numeric'
        },
        'participacao_lucros': {
            'description': 'Participação nos Lucros.',
            'type': 'numeric'
        },
        'lucro_liquido': {
            'description': ('Resultado antes da Tributação e Participação deduzido de Imposto de Renda e '
                            'Contribuição Social e de Participação nos Lucros.'),
            'type': 'numeric'
        },
        'juros_sobre_capital_proprio': {
            'description': 'Despesas de Juros Sobre Capital Próprio de Cooperativas.',
            'type': 'numeric'
        }
    }

    def __get_columns_by_type(self, data_type: str) -> list[str]:
        """Auxiliary function to filter columns by type."""

        return [col for col, meta in self.SCHEMA_DEFINITION.items() if meta['type'] == data_type]

    @property
    def column_names(self) -> list[str]:
        """Return all column names defined in the schema."""

        return list(self.SCHEMA_DEFINITION.keys())

    @property
    def numeric_columns(self) -> list[str]:
        """Return dynamically the numeric columns."""

        return self.__get_columns_by_type('numeric')

    @property
    def date_columns(self) -> list[str]:
        """Return dynamically the date columns."""

        return self.__get_columns_by_type('date')

    @property
    def categorical_columns(self) -> list[str]:
        """Return dynamically the categorical columns."""

        return self.__get_columns_by_type('categorical')

    @property
    def text_columns(self) -> list[str]:
        """Return dynamically the text columns."""

        return self.__get_columns_by_type('text')

    def get_description(self, column_name: str) -> str | None:
        """Return the description of a specific column."""

        return self.SCHEMA_DEFINITION.get(column_name, {}).get('description')

    def get_mapping(self, column_name: str) -> dict | None:
        """Return the mapping dictionary for a categorical column if it exists."""

        return self.SCHEMA_DEFINITION.get(column_name, {}).get('mapping')
