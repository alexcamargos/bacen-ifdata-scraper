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

    def run_scraper(
        self,
        institution: str | None = None,
        report: str | None = None,
        *,
        data_base: str | None = None,
        repair_raw: bool = False,
        refresh: bool = False,
    ) -> None:
        """Execute the scraping stage of the pipeline.

        Args:
            institution: Optional institutional scope.
            report: Optional report name.
            data_base: Optional reference month in YYYY-MM format.
            repair_raw: Limit collection to invalid originals already on disk.
            refresh: Download the selected month even if it is valid locally.

        Returns:
            None.

        Raises:
            IfDataScraperException: A requested export is invalid.
        """

    def run_csv_consolidation(
        self, institution: str | None = None, report: str | None = None,
    ) -> None:
        """Consolidate local originals into one CSV per scope and report.

        Args:
            institution: Optional institutional scope.
            report: Optional report name.
        Returns:
            None.
        Raises:
            IfDataScraperException: An original failed validation.
            OSError: A consolidated CSV could not be published.
            ValueError: The selection has no local originals.
        """

    def run_cleaner(self, institution: str | None = None, report: str | None = None) -> None:
        """Execute the cleaning stage of the pipeline."""

    def run_transformer(self, institution: str | None = None, report: str | None = None) -> None:
        """Execute the transformation stage of the pipeline."""

    def run_loader(self, institution: str | None = None, report: str | None = None) -> None:
        """Execute the loading stage of the pipeline."""

    def run_analytics(self) -> None:
        """Execute the analytics stage of the pipeline (dbt)."""

    def run_update(self) -> None:
        """Process changed inputs and publish the validated warehouse pair.

        Args:
            None.

        Returns:
            None.

        Raises:
            ValueError: An input is missing or invalid.
            OSError: Publication failed.
        """
