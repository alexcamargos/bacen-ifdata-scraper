#!/usr/bin/env python
# encoding: utf-8
#
#  ------------------------------------------------------------------------------
#  Name: pipeline_manager.py
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
Pipeline Manager Protocol for Bacen IF.data

This module defines the interface for the PipelineManager, enabling
dependency inversion and facilitating testing with mocks.
"""

from typing import Protocol


# pylint: disable=too-few-public-methods
class PipelineManagerProtocol(Protocol):
    """Protocol defining the interface for pipeline management.

    This protocol specifies the methods that any PipelineManager implementation
    must provide for orchestrating the data pipeline stages.
    """

    def run_scraper(self) -> None:
        """Execute the scraping stage of the pipeline."""

    def run_cleaner(self) -> None:
        """Execute the cleaning stage of the pipeline."""

    def run_transformer(self) -> None:
        """Execute the transformation stage of the pipeline."""

    def run_loader(self) -> None:
        """Execute the loading stage of the pipeline."""

    def run_analytics(self) -> None:
        """Execute the analytics stage of the pipeline (dbt)."""
