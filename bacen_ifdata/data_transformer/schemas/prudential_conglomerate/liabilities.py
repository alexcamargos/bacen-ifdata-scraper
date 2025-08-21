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


class PrudentialConglomerateLiabilitiesSchema:
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
        'tipo_de_consolidacao': {
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
        'depositos_vista': {
            'description': 'Depósitos à vista.',
            'type': 'numeric'
        },
        'depositos_poupanca': {
            'description': 'Depósitos Poupança.',
            'type': 'numeric'
        },
        'depositos_interfinanceiros': {
            'description': 'Depósitos interfinanceiros.',
            'type': 'numeric'
        },
        'depositos_a_prazo': {
            'description': 'Depósitos a prazo.',
            'type': 'numeric'
        },
        'conta_de_pagamento_pre_paga': {
            'description': 'Conta de pagamento pré-paga.',
            'type': 'numeric'
        },
        'depositos_outros': {
            'description': ('(+) Depósitos sob aviso (+) Obrigações por depósitos especiais e de fundos e '
                            'programas (+) APE - Depósitos especiais (+) Depósitos em moedas estrangeiras '
                            '(+) Outros depósitos (-) Conta de pagamento pré-paga.'),
            'type': 'numeric'
        },
        'deposito_total': {
            'description': 'Depósito Totais.',
            'type': 'numeric'
        },
        'obrigações_operações_compromissadas': {
            'description': 'Obrigações por Operações Compromissadas.',
            'type': 'numeric'
        },
        'letras_de_credito_imobiliario': {
            'description': 'LCI - Obrigações por Emissão de Letras de Crédito Imobiliário.',
            'type': 'numeric'
        },
        'letras_de_credito_agronegocio': {
            'description': 'LCA - Obrigações por Emissão de Letras de Crédito do Agronegócio.',
            'type': 'numeric'
        },
        'letras_financeiras': {
            'description': 'LF - Obrigações por Emissão de Letras Financeiras.',
            'type': 'numeric'
        },
        'obrigacoes_titulos_e_valores_mobiliarios_exterior': {
            'description': 'Obrigações por Títulos e Valores Mobiliários no Exterior.',
            'type': 'numeric'
        },
        'outros_recursos_de_aceites_e_emissao_de_titulos': {
            'description': ('(+) Recursos de aceites cambiais, letras imobiliárias e hipotecárias, debêntures, '
                            'e similares (-) Obrigações por Emissão de Letras de Crédito Imobiliário (-) '
                            'Obrigações por Emissão de Letras de Crédito do Agronegócio (-) Obrigações por '
                            'Emissão de Letras Financeiras (-) Obrigações por Títulos e Valores Mobiliários no Exterior.'),
            'type': 'numeric'
        },
        'recursos_de_aceites_e_emissao_de_titulos': {
            'description': 'Recursos de aceites cambiais, letras imobiliárias e hipotecárias, debêntures, e similares.',
            'type': 'numeric'
        },
        'obrigacoes_emprestimos_e_repasses': {
            'description': 'Obrigações por empréstimos e repasses.',
            'type': 'numeric'
        },
        'captacoes': {
            'description': ('(+) Depósitos (+) Obrigações por Operações Compromissadas (+) Recursos de aceites '
                            'cambiais, letras imobiliárias e hipotecárias, debêntures, e similares (+) Obrigações '
                            'por empréstimos e repasses.'),
            'type': 'numeric'
        },
        'instrumentos_derivativos': {
            'description': 'Instrumentos financeiros derivativos.',
            'type': 'numeric'
        },
        'outras_obrigações': {
            'description': '(+) Relações Interfinanceiras (+) Relações interdependências (+) Outras obrigações.',
            'type': 'numeric'
        },
        'passivo_circulante_exigível_a_longo_prazo': {
            'description': 'Passivo circulante e exigível a longo prazo.',
            'type': 'numeric'
        },
        'patrimonio_liquido': {
            'description': '(+) Patrimônio Líquido (+) Contas de resultado credoras (+) Contas de resultado devedoras',
            'type': 'numeric'
        },
        'passivo_total': {
            'description': ('(+) Passivo circulante e exigível a longo prazo (+) Patrimônio Líquido (+) '
                            'Contas de resultado credoras (+) Contas de resultado devedoras.'),
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

    def get_type(self, column_name: str) -> str | None:
        """Return the type of a specific column from the schema definition."""

        return self.SCHEMA_DEFINITION.get(column_name, {}).get('type')

    def get_description(self, column_name: str) -> str | None:
        """Return the description of a specific column."""

        return self.SCHEMA_DEFINITION.get(column_name, {}).get('description')

    def get_mapping(self, column_name: str) -> dict | None:
        """Return the mapping dictionary for a categorical column if it exists."""

        return self.SCHEMA_DEFINITION.get(column_name, {}).get('mapping')
