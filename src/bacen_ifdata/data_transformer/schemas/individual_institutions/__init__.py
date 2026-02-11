#!/usr/bin/env python
# encoding: utf-8
#
#  ------------------------------------------------------------------------------
#  Name: __init__.py
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

from bacen_ifdata.data_transformer.schemas.individual_institutions.assets import IndividualInstitutionAssetsSchema
from bacen_ifdata.data_transformer.schemas.individual_institutions.income_statement import (
    IndividualInstitutionIncomeStatementSchema,
)
from bacen_ifdata.data_transformer.schemas.individual_institutions.liabilities import (
    IndividualInstitutionLiabilitiesSchema,
)
from bacen_ifdata.data_transformer.schemas.individual_institutions.summary import IndividualInstitutionSummarySchema

# Instance a schema for report summary of individual institutions.
INDIVIDUAL_INSTITUTION_SUMMARY_SCHEMA = IndividualInstitutionSummarySchema()

# Instance a schema for report assets of individual institutions.
INDIVIDUAL_INSTITUTION_ASSETS_SCHEMA = IndividualInstitutionAssetsSchema()

# Instance a schema for report liabilities of individual institutions.
INDIVIDUAL_INSTITUTION_LIABILITIES_SCHEMA = IndividualInstitutionLiabilitiesSchema()

# Instance a schema for report income statement of individual institutions.
INDIVIDUAL_INSTITUTION_INCOME_STATEMENT_SCHEMA = IndividualInstitutionIncomeStatementSchema()


__all__ = [
    'INDIVIDUAL_INSTITUTION_SUMMARY_SCHEMA',
    'INDIVIDUAL_INSTITUTION_ASSETS_SCHEMA',
    'INDIVIDUAL_INSTITUTION_LIABILITIES_SCHEMA',
    'INDIVIDUAL_INSTITUTION_INCOME_STATEMENT_SCHEMA',
]
