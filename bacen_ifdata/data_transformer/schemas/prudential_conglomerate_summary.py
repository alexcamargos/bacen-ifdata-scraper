#!/usr/bin/env python
# encoding: utf-8
#
#  ------------------------------------------------------------------------------
#  Name: prudential_conglomerate_summary.py
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


class PrudentialConglomerateSummarySchema:
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
        'ativo_total': {
            'description': 'Ativo Circulante e Realizável a Longo Prazo + Ativo Permanente.',
            'type': 'numeric'
        },
        'carteira_de_credito_classificada': {
            'description': 'Carteira de Crédito Classificada.',
            'type': 'numeric'
        },
        'passivo_circulante_e_exigivel_a_longo_prazo': {
            'description': 'Passivo Circulante e Exigível a Longo Prazo + Resultados de Exercícios Futuros.',
            'type': 'numeric'
        },
        'captacoes': {
            'description': ('Depósitos + Obrigações por Operações Compromissadas + Recursos de Aceites Cambiais, '
                            'Letras Imobiliárias e Hipotecárias, Debêntures e Similares + Obrigações por Empréstimos e Repasses.'),
            'type': 'numeric'
        },
        'patrimonio_liquido': {
            'description': 'Patrimônio Líquido + Contas de Resultado Credoras + Contas de Resultado Devedoras.',
            'type': 'numeric'
        },
        'lucro_liquido': {
            'description': ('Lucro Líquido, excluindo despesas de juros sobre capital '
                            '(Contas de Resultado Credoras + Contas de Resultado Devedoras - '
                            'Despesas de Juros sobre o Capital Social de Cooperativas).'),
            'type': 'numeric'
        },
        'patrimonio_de_referencia': {
            'description': 'Montante de capital regulatório formado pela soma das parcelas de Capital Nível I e Capital Nível II.',
            'type': 'numeric'
        },
        'indice_de_basileia': {
            'description': 'Relação entre o Patrimônio de Referência e Ativos ponderados pelo risco.',
            'type': 'numeric'
        },
        'indice_de_imobilizacao': {
            'description': 'Relação entre Ativo Permanente e Patrimônio de Referência.',
            'type': 'numeric'
        },
        'numero_de_agencias': {
            'description': 'Número de agências da instituição ou do conglomerado, incluídas as sedes (exceto para cooperativas).',
            'type': 'numeric'
        },
        'numero_de_postos_de_atendimento': {
            'description': 'Número de postos de atendimento da instituição ou do conglomerado.',
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
