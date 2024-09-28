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

from abc import ABC, abstractmethod


# pylint: disable=too-few-public-methods, missing-function-docstring
class PrudentialConglomeratesInterface(ABC):
    """Represents the interface for the PrudentialConglomeratesTransformer class."""

    @abstractmethod
    def transform_bank_consolidation_type(self, data):
        raise NotImplementedError("You should implement this method.")

    @abstractmethod
    def transform_consolidation_type(self, data):
        raise NotImplementedError("You should implement this method.")

    @abstractmethod
    def transform_control_type(self, data):
        raise NotImplementedError("You should implement this method.")

    @abstractmethod
    def transform_data_base(self, data):
        raise NotImplementedError("You should implement this method.")

    @abstractmethod
    def transform_financial_institution(self, data):
        raise NotImplementedError("You should implement this method.")

    @abstractmethod
    def transform_prudential_summary_information(self, data):
        raise NotImplementedError("You should implement this method.")

    @abstractmethod
    def transform_segment_classification(self, data):
        raise NotImplementedError("You should implement this method.")
