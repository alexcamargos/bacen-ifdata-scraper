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

from bacen_ifdata.data_transformer.schemas.financial_conglomerates.assets import FinancialConglomeratesAssetsSchema
from bacen_ifdata.data_transformer.schemas.financial_conglomerates.income_statement import (
    FinancialConglomerateIncomeStatementSchema,
)
from bacen_ifdata.data_transformer.schemas.financial_conglomerates.liabilities import (
    FinancialConglomerateLiabilitiesSchema,
)
from bacen_ifdata.data_transformer.schemas.financial_conglomerates.summary import FinancialConglomerateSummarySchema
from bacen_ifdata.data_transformer.schemas.individual_institutions.assets import IndividualInstitutionAssetsSchema
from bacen_ifdata.data_transformer.schemas.individual_institutions.income_statement import (
    IndividualInstitutionIncomeStatementSchema,
)
from bacen_ifdata.data_transformer.schemas.individual_institutions.liabilities import (
    IndividualInstitutionLiabilitiesSchema,
)
from bacen_ifdata.data_transformer.schemas.individual_institutions.summary import IndividualInstitutionSummarySchema
from bacen_ifdata.data_transformer.schemas.prudential_conglomerate.assets import PrudentialConglomeratesAssetsSchema
from bacen_ifdata.data_transformer.schemas.prudential_conglomerate.capital_information import (
    PrudentialConglomerateCapitalInformationSchema,
)
from bacen_ifdata.data_transformer.schemas.prudential_conglomerate.income_statement import (
    PrudentialConglomerateIncomeStatementSchema,
)
from bacen_ifdata.data_transformer.schemas.prudential_conglomerate.liabilities import (
    PrudentialConglomerateLiabilitiesSchema,
)
from bacen_ifdata.data_transformer.schemas.prudential_conglomerate.portfolio_individuals_type_maturity import (
    PrudentialConglomeratePortfolioIndividualsTypeMaturitySchema,
)
from bacen_ifdata.data_transformer.schemas.prudential_conglomerate.portfolio_legal_person_business_size import (
    PrudentialConglomeratePortfolioLegalPersonBusinessSizeSchema,
)
from bacen_ifdata.data_transformer.schemas.prudential_conglomerate.portfolio_legal_person_economic_activity import (
    PrudentialConglomeratePortfolioLegalPersonEconomicActivitySchema,
)
from bacen_ifdata.data_transformer.schemas.prudential_conglomerate.portfolio_number_clients_operations import (
    PrudentialConglomeratePortfolioNumberClientsOperationsSchema,
)
from bacen_ifdata.data_transformer.schemas.prudential_conglomerate.portfolio_risk_level import (
    PrudentialConglomeratePortfolioRiskLevelSchema,
)
from bacen_ifdata.data_transformer.schemas.prudential_conglomerate.portfolio_legal_person_type_maturity import (
    PrudentialConglomeratePortfolioLegalPersonTypeMaturitySchema,
)
from bacen_ifdata.data_transformer.schemas.prudential_conglomerate.segmentation import (
    PrudentialConglomerateSegmentationSchema,
)
from bacen_ifdata.data_transformer.schemas.prudential_conglomerate.summary import PrudentialConglomerateSummarySchema

# Prudential Conglomerate schemas
PRUDENTIAL_CONGLOMERATE_SUMMARY_SCHEMA = PrudentialConglomerateSummarySchema()
PRUDENTIAL_CONGLOMERATE_ASSETS_SCHEMA = PrudentialConglomeratesAssetsSchema()
PRUDENTIAL_CONGLOMERATE_LIABILITIES_SCHEMA = PrudentialConglomerateLiabilitiesSchema()
PRUDENTIAL_CONGLOMERATE_INCOME_STATEMENT_SCHEMA = PrudentialConglomerateIncomeStatementSchema()
PRUDENTIAL_CONGLOMERATE_CAPITAL_INFORMATION_SCHEMA = PrudentialConglomerateCapitalInformationSchema()
PRUDENTIAL_CONGLOMERATE_SEGMENTATION_SCHEMA = PrudentialConglomerateSegmentationSchema()
PRUDENTIAL_CONGLOMERATE_PORTFOLIO_INDIVIDUALS_TYPE_MATURITY_SCHEMA = (
    PrudentialConglomeratePortfolioIndividualsTypeMaturitySchema()
)
PRUDENTIAL_CONGLOMERATE_PORTFOLIO_LEGAL_PERSON_TYPE_MATURITY_SCHEMA = (
    PrudentialConglomeratePortfolioLegalPersonTypeMaturitySchema()
)
PRUDENTIAL_CONGLOMERATE_PORTFOLIO_LEGAL_PERSON_BUSINESS_SIZE_SCHEMA = (
    PrudentialConglomeratePortfolioLegalPersonBusinessSizeSchema()
)
PRUDENTIAL_CONGLOMERATE_PORTFOLIO_LEGAL_PERSON_ECONOMIC_ACTIVITY_SCHEMA = (
    PrudentialConglomeratePortfolioLegalPersonEconomicActivitySchema()
)
PRUDENTIAL_CONGLOMERATE_PORTFOLIO_NUMBER_CLIENTS_OPERATIONS_SCHEMA = (
    PrudentialConglomeratePortfolioNumberClientsOperationsSchema()
)
PRUDENTIAL_CONGLOMERATE_PORTFOLIO_RISK_LEVEL_SCHEMA = PrudentialConglomeratePortfolioRiskLevelSchema()

# Financial Conglomerates schemas
FINANCIAL_CONGLOMERATE_SUMMARY_SCHEMA = FinancialConglomerateSummarySchema()
FINANCIAL_CONGLOMERATE_ASSETS_SCHEMA = FinancialConglomeratesAssetsSchema()
FINANCIAL_CONGLOMERATE_LIABILITIES_SCHEMA = FinancialConglomerateLiabilitiesSchema()
FINANCIAL_CONGLOMERATE_INCOME_STATEMENT_SCHEMA = FinancialConglomerateIncomeStatementSchema()

# Individual Institutions schemas
INDIVIDUAL_INSTITUTION_SUMMARY_SCHEMA = IndividualInstitutionSummarySchema()
INDIVIDUAL_INSTITUTION_ASSETS_SCHEMA = IndividualInstitutionAssetsSchema()
INDIVIDUAL_INSTITUTION_LIABILITIES_SCHEMA = IndividualInstitutionLiabilitiesSchema()
INDIVIDUAL_INSTITUTION_INCOME_STATEMENT_SCHEMA = IndividualInstitutionIncomeStatementSchema()


__all__ = [
    # Prudential Conglomerate
    'PRUDENTIAL_CONGLOMERATE_SUMMARY_SCHEMA',
    'PRUDENTIAL_CONGLOMERATE_ASSETS_SCHEMA',
    'PRUDENTIAL_CONGLOMERATE_LIABILITIES_SCHEMA',
    'PRUDENTIAL_CONGLOMERATE_INCOME_STATEMENT_SCHEMA',
    'PRUDENTIAL_CONGLOMERATE_CAPITAL_INFORMATION_SCHEMA',
    'PRUDENTIAL_CONGLOMERATE_SEGMENTATION_SCHEMA',
    'PRUDENTIAL_CONGLOMERATE_PORTFOLIO_INDIVIDUALS_TYPE_MATURITY_SCHEMA',
    'PRUDENTIAL_CONGLOMERATE_PORTFOLIO_LEGAL_PERSON_TYPE_MATURITY_SCHEMA',
    'PRUDENTIAL_CONGLOMERATE_PORTFOLIO_LEGAL_PERSON_BUSINESS_SIZE_SCHEMA',
    'PRUDENTIAL_CONGLOMERATE_PORTFOLIO_LEGAL_PERSON_ECONOMIC_ACTIVITY_SCHEMA',
    'PRUDENTIAL_CONGLOMERATE_PORTFOLIO_NUMBER_CLIENTS_OPERATIONS_SCHEMA',
    'PRUDENTIAL_CONGLOMERATE_PORTFOLIO_RISK_LEVEL_SCHEMA',
    # Financial Conglomerates
    'FINANCIAL_CONGLOMERATE_SUMMARY_SCHEMA',
    'FINANCIAL_CONGLOMERATE_ASSETS_SCHEMA',
    'FINANCIAL_CONGLOMERATE_LIABILITIES_SCHEMA',
    'FINANCIAL_CONGLOMERATE_INCOME_STATEMENT_SCHEMA',
    # Individual Institutions
    'INDIVIDUAL_INSTITUTION_SUMMARY_SCHEMA',
    'INDIVIDUAL_INSTITUTION_ASSETS_SCHEMA',
    'INDIVIDUAL_INSTITUTION_LIABILITIES_SCHEMA',
    'INDIVIDUAL_INSTITUTION_INCOME_STATEMENT_SCHEMA',
]
