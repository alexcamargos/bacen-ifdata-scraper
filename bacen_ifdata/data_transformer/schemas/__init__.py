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

from bacen_ifdata.data_transformer.schemas.prudential_conglomerate.assets import PrudentialConglomeratesAssetsSchema
from bacen_ifdata.data_transformer.schemas.prudential_conglomerate.capital_information import PrudentialConglomerateCapitalInformationSchema
from bacen_ifdata.data_transformer.schemas.prudential_conglomerate.income_statement import PrudentialConglomerateIncomeStatementSchema
from bacen_ifdata.data_transformer.schemas.prudential_conglomerate.liabilities import PrudentialConglomerateLiabilitiesSchema
from bacen_ifdata.data_transformer.schemas.prudential_conglomerate.summary import PrudentialConglomerateSummarySchema

# Instance a schema for report summary of prudential conglomerate.
PRUDENTIAL_CONGLOMERATE_SUMMARY_SCHEMA = PrudentialConglomerateSummarySchema()

# Instância única para ser importada em outras partes do projeto
PRUDENTIAL_CONGLOMERATE_ASSETS_SCHEMA = PrudentialConglomeratesAssetsSchema()

# Instance a schema for report liabilities of prudential conglomerate.
PRUDENTIAL_CONGLOMERATE_LIABILITIES_SCHEMA = PrudentialConglomerateLiabilitiesSchema()

# Instance a schema for report income statement of prudential conglomerate.
PRUDENTIAL_CONGLOMERATE_INCOME_STATEMENT_SCHEMA = PrudentialConglomerateIncomeStatementSchema()

# Instance a schema for report capital information of prudential conglomerate.
PRUDENTIAL_CONGLOMERATE_CAPITAL_INFORMATION_SCHEMA = PrudentialConglomerateCapitalInformationSchema()


__all__ = ['PRUDENTIAL_CONGLOMERATE_SUMMARY_SCHEMA',
           'PRUDENTIAL_CONGLOMERATE_ASSETS_SCHEMA',
           'PRUDENTIAL_CONGLOMERATE_LIABILITIES_SCHEMA',
           'PRUDENTIAL_CONGLOMERATE_INCOME_STATEMENT_SCHEMA',
           'PRUDENTIAL_CONGLOMERATE_CAPITAL_INFORMATION_SCHEMA']
