#!/usr/bin/env python
# encoding: utf-8
#
#  ------------------------------------------------------------------------------
#  Name: browser.py
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
Browser Protocol for Bacen IF.data

This module defines the interface for browser interactions, enabling
dependency inversion and facilitating testing with mocks.
"""

from typing import Protocol


# pylint: disable=too-few-public-methods
class BrowserProtocol(Protocol):
    """Protocol defining the interface for browser interactions.

    This protocol specifies the methods that any Browser implementation
    must provide for web automation tasks.
    """

    @property
    def is_headless(self) -> bool:
        """Returns True if the browser is running in headless mode."""

    def initialize(self, url: str) -> None:
        """Initializes the browser and opens the specified URL.

        Args:
            url: The URL to open in the web browser.
        """

    def quit(self) -> None:
        """Quits the browser session."""

    def ensure_dropdown_content(self, dropdown_id: str, wait_time: int) -> None:
        """Ensures the dropdown is clickable.

        Args:
            dropdown_id: The ID of the dropdown menu element.
            wait_time: The maximum time to wait for the dropdown to become clickable.
        """

    def select_dropdown_option(self, option_text: str, wait_time: int) -> None:
        """Selects an option from a dropdown menu.

        Args:
            option_text: The text of the option to select.
            wait_time: The maximum time to wait for the option to become clickable.
        """

    def get_dropdown_options(self, dropdown_id: str) -> list[str]:
        """Returns a list of options from a dropdown menu.

        Args:
            dropdown_id: The ID of the dropdown menu element.

        Returns:
            A list of option texts from the dropdown menu.
        """

    def download_report(self, wait_time: int) -> None:
        """Downloads a report by clicking the export button.

        Args:
            wait_time: The maximum time to wait for the button to become clickable.
        """
