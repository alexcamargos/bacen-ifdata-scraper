#!/usr/bin/env python
# encoding: utf-8
#
#  ------------------------------------------------------------------------------
#  Name: transformer_factory.py
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
Transformer Factory for Bacen IF.data

This module provides a factory function to retrieve the appropriate transformer
based on the institution type.
"""

from bacen_ifdata.data_transformer.transformers.base import BaseTransformer
from bacen_ifdata.data_transformer.transformers.financial_conglomerates import FinancialConglomeratesTransformer
from bacen_ifdata.data_transformer.transformers.individual_institutions import IndividualInstitutionsTransformer
from bacen_ifdata.data_transformer.transformers.prudential_conglomerates import PrudentialConglomeratesTransformer
from bacen_ifdata.scraper.institutions import InstitutionType as Institutions

# Mapping of institution types to their corresponding transformer classes.
TRANSFORMER_MAP: dict[Institutions, type[BaseTransformer]] = {
    Institutions.PRUDENTIAL_CONGLOMERATES: PrudentialConglomeratesTransformer,
    Institutions.FINANCIAL_CONGLOMERATES: FinancialConglomeratesTransformer,
    Institutions.INDIVIDUAL_INSTITUTIONS: IndividualInstitutionsTransformer,
}


def get_transformer(institution: Institutions) -> BaseTransformer:
    """Returns the appropriate transformer for the given institution type.

    Args:
        institution (Institutions): The institution type.

    Returns:
        BaseTransformer: The transformer instance for the institution.
    """

    transformer_class = TRANSFORMER_MAP.get(institution, BaseTransformer)

    return transformer_class()
