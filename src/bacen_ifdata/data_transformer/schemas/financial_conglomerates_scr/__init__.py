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

from bacen_ifdata.data_transformer.schemas.financial_conglomerates_scr.portfolio_geographic_region import (
    FinancialConglomerateSCRPortfolioGeographicRegionSchema,
)
from bacen_ifdata.data_transformer.schemas.financial_conglomerates_scr.portfolio_indexer import (
    FinancialConglomerateSCRPortfolioIndexerSchema,
)
from bacen_ifdata.data_transformer.schemas.financial_conglomerates_scr.portfolio_individuals_type_maturity import (
    FinancialConglomerateSCRPortfolioIndividualsTypeMaturitySchema,
)
from bacen_ifdata.data_transformer.schemas.financial_conglomerates_scr.portfolio_legal_person_business_size import (
    FinancialConglomerateSCRPortfolioLegalPersonBusinessSizeSchema,
)
from bacen_ifdata.data_transformer.schemas.financial_conglomerates_scr.portfolio_legal_person_economic_activity import (
    FinancialConglomerateSCRPortfolioLegalPersonEconomicActivitySchema,
)
from bacen_ifdata.data_transformer.schemas.financial_conglomerates_scr.portfolio_legal_person_type_maturity import (
    FinancialConglomerateSCRPortfolioLegalPersonTypeMaturitySchema,
)
from bacen_ifdata.data_transformer.schemas.financial_conglomerates_scr.portfolio_number_clients_operations import (
    FinancialConglomerateSCRPortfolioNumberClientsOperationsSchema,
)
from bacen_ifdata.data_transformer.schemas.financial_conglomerates_scr.portfolio_risk_level import (
    FinancialConglomerateSCRPortfolioRiskLevelSchema,
)

__all__ = [
    'FinancialConglomerateSCRPortfolioIndividualsTypeMaturitySchema',
    'FinancialConglomerateSCRPortfolioLegalPersonTypeMaturitySchema',
    'FinancialConglomerateSCRPortfolioLegalPersonEconomicActivitySchema',
    'FinancialConglomerateSCRPortfolioLegalPersonBusinessSizeSchema',
    'FinancialConglomerateSCRPortfolioNumberClientsOperationsSchema',
    'FinancialConglomerateSCRPortfolioRiskLevelSchema',
    'FinancialConglomerateSCRPortfolioIndexerSchema',
    'FinancialConglomerateSCRPortfolioGeographicRegionSchema',
]
