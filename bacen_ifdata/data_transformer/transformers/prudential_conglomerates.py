#!/usr/bin/env python
# encoding: utf-8
#
#  ------------------------------------------------------------------------------
#  Name: prudential_conglomerates.py
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

from bacen_ifdata.data_transformer.interfaces.prudential_conglomerates import PrudentialConglomeratesInterface
from bacen_ifdata.data_transformer.parser.bank_consolidation import BankConsolidationTypeParser
from bacen_ifdata.data_transformer.parser.consolidation import ConsolidationTypeParser
from bacen_ifdata.data_transformer.parser.control import ControlTypeParser
from bacen_ifdata.data_transformer.parser.database import DataBaseParser
from bacen_ifdata.data_transformer.parser.financial_institution import FinancialInstitutionParser
from bacen_ifdata.data_transformer.parser.prudential_summary import PrudentialSummaryInformationParser
from bacen_ifdata.data_transformer.parser.segment import SegmentClassificationParser


# pylint: disable=missing-class-docstring, missing-function-docstring
class PrudentialConglomeratesTransformer(PrudentialConglomeratesInterface):
    def __init__(self):
        self.bank_consolidation_type_parser = BankConsolidationTypeParser()
        self.consolidation_type_parser = ConsolidationTypeParser()
        self.control_type_parser = ControlTypeParser()
        self.database_parser = DataBaseParser()
        self.financial_institution_parser = FinancialInstitutionParser()
        self.prudential_summary_information_parser = PrudentialSummaryInformationParser()
        self.segment_classification_parser = SegmentClassificationParser()

    def transform_bank_consolidation_type(self, data):
        consolidation_type = data['TipoConsBancario']

        return self.bank_consolidation_type_parser.parser(consolidation_type)

    def transform_consolidation_type(self, data):
        consolidation_type = data['TipoConsolidacao']

        return self.consolidation_type_parser.parser(consolidation_type)

    def transform_control_type(self, data):
        control_type = data['TipoControle']

        return self.control_type_parser.parser(control_type)

    def transform_data_base(self, data):
        database = data['DataBase'].split('/')

        return self.database_parser.parser(database)

    def transform_financial_institution(self, data):

        return self.financial_institution_parser.parser(data)

    def transform_prudential_summary_information(self, data):

        return self.prudential_summary_information_parser.parser(data)

    def transform_segment_classification(self, data):
        segment = data['Segmento']

        return self.segment_classification_parser.parser(segment)
