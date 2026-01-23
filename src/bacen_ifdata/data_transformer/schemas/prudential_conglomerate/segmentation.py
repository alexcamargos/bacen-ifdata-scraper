#!/usr/bin/env python
# encoding: utf-8
#
#  ------------------------------------------------------------------------------
#  Name: segmentation.py
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


class PrudentialConglomerateSegmentationSchema:
    """
    Define e categoriza os nomes das colunas para os relatórios de Segmentação
    de conglomerados prudenciais, enriquecido com metadados do dicionário de dados.
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
        'consolidado_bancario': {
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
        'tipo_de_consolidacao': {
            'description': 'Tipo de Consolidação (I) identifica uma Instituição Independente e (C) identifica um Conglomerado.',
            'type': 'categorical',
            'mapping': {
                'i': 'Instituição Independente',
                'c': 'Conglomerado',
            }
        },
        'tipo_de_controle': {
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
        'instituicao_sujeita_apuracao_exposicao_total': {
            'description': ('Para cálculo do porte da instituição é considerada a exposição total, calculada '
                            'conforme metodologia definida pelo Banco Central do Brasil. Se a instituição não for '
                            'sujeita a apuração da exposição total, deve substituir pelo valor do ativo total '
                            '(art 3º, Res 4553/2017).'),
            'type': 'text'
        },
        'instituicao_sujeita_apuracao_patrimonio_referencia': {
            'description': 'Informação se a instituição é sujeita à apuração do Patrimônio de Referência (art. 2º, Res 4553/2007).',
            'type': 'text'
        },
        'instituicao_utiliza_metodologia_simplificada': {
            'description': (
                'Informação se a instituição utiliza a metodologia facultativa simplificada para apuração '
                'dos requerimentos mínimos de Patrimônio de Referência, de Nível I e de Capital Principal (art. 2º, Res 4553/2007).'),
            'type': 'text'
        },
        'exposicao_total_ou_ativo_total': {
            'description': ('Para cálculo do porte da instituição é considerada a exposição total, calculada '
                            'conforme metodologia definida pelo Banco Central do Brasil. Se a instituição não for '
                            'sujeita a apuração da exposição total, deve substituir pelo valor do ativo total '
                            '(art 3º, Res 4553/2017). Exposição total é definida segundo a metodologia expressa '
                            'na Circular n° 3.748, de 27 de fevereiro de 2015'),
            'type': 'numeric'
        },
        'total_ativos_consolidados_exterior': {
            'description': ('Valor total de ativos consolidados no exterior, convertido em dólares com base na taxa '
                            'de câmbio de venda informada pelo Banco Central do Brasil para efeito de balancete ou '
                            'balanço patrimonial (art. 4º Res 4553/2017).'),
            'type': 'numeric'
        },
        'data_ultima_alteracao_segmento': {
            'description': 'Data da última alteração do segmento da instituição.',
            'type': 'date'
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
        'tcip': {
            'description': 'Classificação das instituições conforme Resolução nº 197/2022 (Tipo 1, Tipo 2, Tipo 3).',
            'type': 'categorical',
            'mapping': {
                '1': ('Tipo 1: conglomerado prudencial cuja instituição líder seja instituição financeira ou'
                      ' outra instituição autorizada a funcionar pelo Banco Central do Brasil sujeita à Lei'
                      ' nº 4.595, de 31 de dezembro de 1964.'),
                '2': ('Tipo 2: conglomerado prudencial cuja instituição líder seja instituição de pagamento'
                      ' e que não seja integrado por instituição financeira ou por outra instituição'
                      ' autorizada a funcionar pelo Banco Central do Brasil sujeita à Lei nº 4.595, de 1964,'
                      ' ou sujeita à Lei nº 10.194, de 14 de fevereiro de 2001.'),
                '3': ('Tipo 3: conglomerado prudencial cuja instituição líder seja instituição de pagamento'
                      ' e que seja integrado por instituição financeira ou por outra instituição autorizada'
                      ' a funcionar pelo Banco Central do Brasil sujeita à Lei nº 4.595, de 1964, ou sujeita'
                      ' à Lei nº 10.194, de 2001.'),
                'Em branco': 'Conglomerados ou instituições que não realizem serviços de pagamento.'
            }
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

    def get_type(self, column_name: str) -> str | None:
        """Return the type of a specific column from the schema definition."""

        return self.SCHEMA_DEFINITION.get(column_name, {}).get('type')

    def get_description(self, column_name: str) -> str | None:
        """Return the description of a specific column."""

        return self.SCHEMA_DEFINITION.get(column_name, {}).get('description')

    def get_mapping(self, column_name: str) -> dict | None:
        """Return the mapping dictionary for a categorical column if it exists."""

        return self.SCHEMA_DEFINITION.get(column_name, {}).get('mapping')
