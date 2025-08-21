#!/usr/bin/env python
# encoding: utf-8

# ------------------------------------------------------------------------------
#  Name: capital_information.py
#  Version: 0.0.1
#
#  Summary: Project Name
#           Quick description of the project.
#
#  Author: Alexsander Lopes Camargos
#  Author-email: alcamargos@vivaldi.net
#
#  License: MIT
# ------------------------------------------------------------------------------

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


class PrudentialConglomerateCapitalInformationSchema:
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
        'capital_principal_para_comparacao_com_rwa': {
            'description': 'Parcela do capital de melhor qualidade e imediatamente disponível para absorver perdas.',
            'type': 'numeric'
        },
        'capital_complementar': {
            'description': 'Instrumentos de capital e dívida perpétuos, elegíveis como patrimônio regulatório.',
            'type': 'numeric'
        },
        'patrimonio_referencia_nivel_i_para_comparacao_com_rwa': {
            'description': 'Soma das parcelas do Capital Principal e Capital Complementar.',
            'type': 'numeric'
        },
        'capital_nivel_ii': {
            'description': ('Parcela do capital composta por instrumentos subordinados, elegíveis como patrimônio '
                            'regulatório, aptos a absorver perdas durante o funcionamento da instituição.'),
            'type': 'numeric'
        },
        'patrimonio_referencia_para_comparacao_com_rwa': {
            'description': 'Montante de capital regulatório (Nível I + Nível II).',
            'type': 'numeric'
        },
        'rwa_risco_credito': {
            'description': ('Parcela dos ativos ponderados pelo risco (RWA) referente à exposição ao risco de '
                            'crédito. Segundo abordagem padronizada (RWAcpad) ou segundo modelo interno IRB (RWAcirb).'),
            'type': 'numeric'
        },
        'rwacam': {
            'description': 'Parcela do RWA referente a exposições em ouro, moeda estrangeira e variação cambial.',
            'type': 'numeric'
        },
        'rwacom': {
            'description': 'Parcela do RWA referente ao risco de variação do preço de mercadorias (commodities).',
            'type': 'numeric'
        },
        'rwajur': {
            'description': 'Parcela do RWA referente a exposições sujeitas à variação de taxas de juros e cupons.',
            'type': 'numeric'
        },
        'rwaacs': {
            'description': 'Parcela do RWA referente ao risco de operações sujeitas à variação do preço de ações.',
            'type': 'numeric'
        },
        'rwacva': {
            'description': 'Parcela do RWA referente ao ajuste para derivativos por variação de qualidade creditícia (CVA).',
            'type': 'numeric'
        },
        'rwadrc': {
            'description': ('Parcela do RWA relativa às exposições ao risco de crédito dos instrumentos '
                            'financeiros classificados na carteira de negociação.'),
            'type': 'numeric'
        },
        'rwa_risco_mercado': {
            'description': 'Parcela do RWA referente à exposição ao risco de mercado.',
            'type': 'numeric'
        },
        'rwa_risco_operacional': {
            'description': 'Parcela do RWA referente à exposição ao risco operacional.',
            'type': 'numeric'
        },
        'rwasp': {
            'description': 'Parcela do RWA relativa ao cálculo de capital para riscos de serviços de pagamento.',
            'type': 'numeric'
        },
        'ativos_ponderados_pelo_risco_rwa': {
            'description': 'Soma das parcelas de RWA para os riscos de Crédito, Mercado, Operacional e Serviço de Pagamento.',
            'type': 'numeric'
        },
        'exposicao_total': {
            'description': 'Exposição Total, sem ponderação de risco, conforme Circular nº 3.748/2015.',
            'type': 'numeric'
        },
        'indice_capital_principal': {
            'description': 'Relação entre o Capital Principal e os Ativos Ponderados pelo Risco (RWA).',
            'type': 'percentage'
        },
        'indice_capital_nivel_i': {
            'description': 'Relação entre o Patrimônio de Referência Nível I e os Ativos Ponderados pelo Risco (RWA).',
            'type': 'percentage'
        },
        'indice_basileia': {
            'description': 'Relação entre o Patrimônio de Referência e os Ativos Ponderados pelo Risco (RWA).',
            'type': 'percentage'
        },
        'adicional_capital_principal': {
            'description': 'Requerimento de adicional de capital principal (ACP Conservação, Contracíclico, Sistêmico).',
            'type': 'numeric'
        },
        'razao_alavancagem': {
            'description': 'Relação entre o Patrimônio de Referência Nível I e a Exposição Total.',
            'type': 'percentage'
        },
        'indice_imobilizacao': {
            'description': 'Relação entre o Ativo Permanente e o Patrimônio de Referência.',
            'type': 'percentage'
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
    def percentage_columns(self) -> list[str]:
        """Return dynamically the percentage columns."""

        return self.__get_columns_by_type('percentage')

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
