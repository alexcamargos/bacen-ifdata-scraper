#!/usr/bin/env python
# encoding: utf-8
#
#  ------------------------------------------------------------------------------
#  Name: config.py
#  Version: 0.0.1
#  Summary: Banco Central do Brasil IF.data Scraper
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
Configuration settings for Banco Central do Brasil IF.data Scraper

This module contains the configuration settings for scraping IF.data reports from
Banco Central do Brasil, including URLs, timeouts, and specific report details.

Author: Alexsander Lopes Camargos
License: MIT
"""

from enum import StrEnum

# URL of the page where the reports are located.
URL = 'https://www3.bcb.gov.br/ifdata/'

# Maximum waiting time for elements to load.
TIMEOUT = 120


# Type of institution for the report.
class InstitutionType(StrEnum):
    """Enumeration of the types of institutions for the report."""

    PRUDENTIAL_CONGLOMERATES = 'Conglomerados Prudenciais e Instituições Independentes'
    FINANCIAL_CONGLOMERATES = 'Conglomerados Financeiros e Instituições Independentes'
    INDIVIDUAL_INSTITUTIONS = 'Instituições Individuais'
    FOREIGN_EXCHANGE = 'Instituições com Operações de Câmbio'


# Type of report to download.
class ReportTypeForPrudentialConglomerates(StrEnum):
    """Enumeration of the types of reports to download."""

    SUMMARY = 'Resumo'
    ASSETS = 'Ativo'
    LIABILITIES = 'Passivo'
    INCOME_STATEMENT = 'Demonstração de Resultado'
    CAPITAL_INFORMATION = 'Informações de Capital'
    SEGMENTATION = 'Segmentação'


class ReportTypeForFinancialConglomerates(StrEnum):
    """Enumeration of the types of reports to download."""

    SUMMARY = 'Resumo'
    ASSETS = 'Ativo'
    LIABILITIES = 'Passivo'
    INCOME_STATEMENT = 'Demonstração de Resultado'
    CAPITAL_INFORMATION = 'Informações de Capital'
    SEGMENTATION = 'Segmentação'
    PORTFOLIO_INDIVIDUALS_TYPE_MATURITY = \
        'Carteira de crédito ativa Pessoa Física - modalidade e prazo de vencimento'
    PORTFOLIO_LEGAL_PERSON_TYPE_MATURITY = \
        'Carteira de crédito ativa Pessoa Jurídica - modalidade e prazo de vencimento'
    PORTFOLIO_LEGAL_PERSON_ECONOMIC_ACTIVITY = \
        'Carteira de crédito ativa Pessoa Jurídica -  por atividade econômica (CNAE)'
    PORTFOLIO_LEGAL_PERSON_BUSINESS_SIZE = \
        'Carteira de crédito ativa Pessoa Jurídica - por porte do tomador'
    PORTFOLIO_NUMBER_CLIENTS_OPERATIONS = \
        'Carteira de crédito ativa - quantidade de clientes e de operações'
    PORTFOLIO_RISK_LEVEL = 'Carteira de crédito ativa - por nível de risco da operação'
    PORTFOLIO_INDEXER = 'Carteira de crédito ativa - por indexador'
    PORTFOLIO_GEOGRAPHIC_REGION = 'Carteira de crédito ativa - por região geográfica'


class ReportTypeForIndividualInstitutions(StrEnum):
    """Enumeration of the types of reports to download."""

    SUMMARY = 'Resumo'
    ASSETS = 'Ativo'
    LIABILITIES = 'Passivo'
    INCOME_STATEMENT = 'Demonstração de Resultado'


class ReportTypeForForeignExchange(StrEnum):
    """Enumeration of the types of reports to download."""

    QUARTERLY_FOREIGN_CURRENCY_FLOW = 'Movimentação de Câmbio no Trimestre'


REPORTS = {
    InstitutionType.PRUDENTIAL_CONGLOMERATES: ReportTypeForPrudentialConglomerates,
    InstitutionType.FINANCIAL_CONGLOMERATES: ReportTypeForFinancialConglomerates,
    InstitutionType.INDIVIDUAL_INSTITUTIONS: ReportTypeForIndividualInstitutions,
    InstitutionType.FOREIGN_EXCHANGE: ReportTypeForForeignExchange
}

__all__ = ['URL', 'TIMEOUT', 'InstitutionType', 'REPORTS']
