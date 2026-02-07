#!/usr/bin/env python
# encoding: utf-8
#
#  ------------------------------------------------------------------------------
#  Name: session.py
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
Session Protocol for Bacen IF.data

This module defines the interface for session management, enabling
dependency inversion and facilitating testing with mocks.
"""

from typing import Protocol


# pylint: disable=too-few-public-methods
class SessionProtocol(Protocol):
    """Protocol defining the interface for session management.

    This protocol specifies the methods that any Session implementation
    must provide for managing web sessions with the IF.data tool.
    """

    def open(self) -> None:
        """Opens the session by initializing the browser."""

    def cleanup(self) -> None:
        """Cleans up the session and releases resources."""

    def get_data_bases(self) -> list[str]:
        """Returns a list of available data bases.

        Returns:
            A list of available data bases.
        """

    def download_reports(self, data_base: str, institution_type: str, report_type: str) -> None:
        """Downloads reports from the IF.data tool.

        Args:
            data_base: The base date for the reports to be downloaded.
            institution_type: The institution type for the reports to be downloaded.
            report_type: The report type to be downloaded.
        """
