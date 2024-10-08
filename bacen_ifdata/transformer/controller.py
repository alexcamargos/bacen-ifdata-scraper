#!/usr/bin/env python
# encoding: utf-8
#
#  ------------------------------------------------------------------------------
#  Name: controller.py
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

from bacen_ifdata.transformer.transformers.prudential_conglomerates import PrudentialConglomeratesTransformer


# pylint: disable=too-few-public-methods, missing-function-docstring
class TransformerController:
    """Controller for transforming data from reports.

    This class is responsible for controlling the transformation of data from reports.
    """
    def __init__(self):
        # Initializing the PrudentialConglomeratesTransformer interface.
        self.prudential_conglomerates_transformer = PrudentialConglomeratesTransformer()

    @property
    def __prudential_conglomerates(self) -> list:
        """List of transformations for prudential conglomerates."""

        return [self.prudential_conglomerates_transformer.transform_financial_institution,
                self.prudential_conglomerates_transformer.transform_data_base,
                self.prudential_conglomerates_transformer.transform_control_type,
                self.prudential_conglomerates_transformer.transform_bank_consolidation_type,
                self.prudential_conglomerates_transformer.transform_consolidation_type,
                self.prudential_conglomerates_transformer.transform_prudential_summary_information,
                self.prudential_conglomerates_transformer.transform_segment_classification
                ]

    def transform_prudential_conglomerates(self, data):
        """Transforms data from prudential conglomerates reports.

        This method is responsible for transforming the data from prudential conglomerates reports.

        Args:
            data (DataFrame): The data to be transformed.
        """

        for _, row in data.iterrows():
            for transform in self.__prudential_conglomerates:
                print(transform(row))
