#!/usr/bin/env python
# encoding: utf-8
#
#  ------------------------------------------------------------------------------
#  Name: institutions.py
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
Institution Type Definitions for Bacen IF.data AutoScraper & Data Manager

This module defines the InstitutionType enumeration, which categorizes the
different types of institutions that the Banco Central do Brasil's IF.data
tool reports on. It's crucial for ensuring that the scraper can accurately
target and retrieve data for the correct type of institution during its
operation. The enumeration provides a standardized way to reference these
institution types across the entire tool, enhancing maintainability
and consistency.

The InstitutionType enum makes it clear and manageable to reference and
work with the various types of institutions, streamlining the process
of adjusting the scraper to work with different data sources or to add
support for new institution types as they become relevant.

Enumeration:
- InstitutionType: Enumerates the different types of institutions including
                    - Prudential Conglomerates
                    - Financial Conglomerates
                    - Individual Institutions
                    - Foreign Exchange Institutions
"""

from enum import StrEnum


# Type of institution for the report.
class InstitutionType(StrEnum):
    """Enumeration of the types of institutions for the report."""

    PRUDENTIAL_CONGLOMERATES = 'Conglomerados Prudenciais e Instituições Independentes'
    FINANCIAL_CONGLOMERATES = 'Conglomerados Financeiros e Instituições Independentes'
    FINANCIAL_CONGLOMERATES_SCR = 'Conglomerados Financeiros e Instituições Independentes (SCR)'
    INDIVIDUAL_INSTITUTIONS = 'Instituições Individuais'
    FOREIGN_EXCHANGE = 'Instituições com Operações de Câmbio'
