#!/usr/bin/env python
# encoding: utf-8
#
#  ------------------------------------------------------------------------------
#  Name: reports.py
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
Report Type Definitions for Bacen IF.data AutoScraper & Data Manager

This module defines enumerations for the various types of reports available for
different types of institutions from the Banco Central do Brasil's IF.data tool.
It categorizes reports into groups associated with specific institution types,
such as Prudential Conglomerates and Financial Conglomerates, among others,
and provides a mapping of report types to the corresponding institution types.

The module is designed to facilitate the selection and handling of different
reports during the scraping process, ensuring that the scraper can easily
identify and request the correct types of reports based on the institution
ype being processed.

Enumerations:
- ReportsPrudentialConglomerates: Reports for Prudential Conglomerates.
- ReportsFinancialConglomerates: Reports for Financial Conglomerates.
- ReportsFinancialConglomeratesSCR: Reports for Financial Conglomerates (SCR).
- ReportsIndividualInstitutions: Reports for Individual Institutions.
- ReportsForeignExchange: Reports for Foreign Exchange Institutions.

Mappings:
- REPORTS: A dictionary mapping institution types to their respective
           available report types.
"""

from enum import StrEnum

from bacen_ifdata_scraper.institutions import InstitutionType


# Type of report to download.
class ReportsPrudentialConglomerates(StrEnum):
    """Enumeration of the types of reports to download."""

    SUMMARY = 'Resumo'
    ASSETS = 'Ativo'
    LIABILITIES = 'Passivo'
    INCOME_STATEMENT = 'Demonstração de Resultado'
    CAPITAL_INFORMATION = 'Informações de Capital'
    SEGMENTATION = 'Segmentação'


class ReportsFinancialConglomerates(StrEnum):
    """Enumeration of the types of reports to download."""

    SUMMARY = 'Resumo'
    ASSETS = 'Ativo'
    LIABILITIES = 'Passivo'
    INCOME_STATEMENT = 'Demonstração de Resultado'
    CAPITAL_INFORMATION = 'Informações de Capital'
    PORTFOLIO_INDIVIDUALS_TYPE_MATURITY = \
        'Carteira de crédito ativa Pessoa Física - modalidade e prazo de vencimento'
    PORTFOLIO_LEGAL_PERSON_TYPE_MATURITY = \
        'Carteira de crédito ativa Pessoa Jurídica - modalidade e prazo de vencimento'
    PORTFOLIO_LEGAL_PERSON_ECONOMIC_ACTIVITY = \
        'Carteira de crédito ativa Pessoa Jurídica - por atividade econômica (CNAE)'
    PORTFOLIO_LEGAL_PERSON_BUSINESS_SIZE = \
        'Carteira de crédito ativa Pessoa Jurídica - por porte do tomador'
    PORTFOLIO_NUMBER_CLIENTS_OPERATIONS = \
        'Carteira de crédito ativa - quantidade de clientes e de operações'
    PORTFOLIO_RISK_LEVEL = 'Carteira de crédito ativa - por nível de risco da operação'
    PORTFOLIO_INDEXER = 'Carteira de crédito ativa - por indexador'
    PORTFOLIO_GEOGRAPHIC_REGION = 'Carteira de crédito ativa - por região geográfica'


class ReportsFinancialConglomeratesSCR(StrEnum):
    """Enumeration of the types of reports to download."""

    PORTFOLIO_INDIVIDUALS_TYPE_MATURITY = \
        'Carteira de crédito ativa Pessoa Física - modalidade e prazo de vencimento'
    PORTFOLIO_LEGAL_PERSON_TYPE_MATURITY = \
        'Carteira de crédito ativa Pessoa Jurídica - modalidade e prazo de vencimento'
    PORTFOLIO_LEGAL_PERSON_ECONOMIC_ACTIVITY = \
        'Carteira de crédito ativa Pessoa Jurídica - por atividade econômica (CNAE)'
    PORTFOLIO_LEGAL_PERSON_BUSINESS_SIZE = \
        'Carteira de crédito ativa Pessoa Jurídica - por porte do tomador'
    PORTFOLIO_NUMBER_CLIENTS_OPERATIONS = \
        'Carteira de crédito ativa - quantidade de clientes e de operações'
    PORTFOLIO_RISK_LEVEL = 'Carteira de crédito ativa - por nível de risco da operação'
    PORTFOLIO_INDEXER = 'Carteira de Crédito Ativa - Por indexador'
    PORTFOLIO_GEOGRAPHIC_REGION = 'Carteira de crédito ativa - por região geográfica'


class ReportsIndividualInstitutions(StrEnum):
    """Enumeration of the types of reports to download."""

    SUMMARY = 'Resumo'
    ASSETS = 'Ativo'
    LIABILITIES = 'Passivo'
    INCOME_STATEMENT = 'Demonstração de Resultado'


class ReportsForeignExchange(StrEnum):
    """Enumeration of the types of reports to download."""

    QUARTERLY_FOREIGN_CURRENCY_FLOW = 'Movimentação de Câmbio no Trimestre'


# Mapping of the report types to the institution types.
REPORTS = {InstitutionType.PRUDENTIAL_CONGLOMERATES: ReportsPrudentialConglomerates,
           InstitutionType.FINANCIAL_CONGLOMERATES: ReportsFinancialConglomerates,
           InstitutionType.FINANCIAL_CONGLOMERATES_SCR: ReportsFinancialConglomeratesSCR,
           InstitutionType.INDIVIDUAL_INSTITUTIONS: ReportsIndividualInstitutions,
           InstitutionType.FOREIGN_EXCHANGE: ReportsForeignExchange}

__all__ = ['REPORTS']
