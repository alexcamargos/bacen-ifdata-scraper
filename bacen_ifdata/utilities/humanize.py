#!/usr/bin/env python
# encoding: utf-8
#
#  ------------------------------------------------------------------------------
#  Name: humanize.py
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
Humanize module for Bacen IF.data AutoScraper & Data Manager

This module provides utility functions to support the automated scraping
and data management tasks for Banco Central's financial data. It includes
functions for converting time in seconds to a human-readable format, which
is essential for logging, reporting, and user interface displays.

- seconds_to_human_readable(seconds: int) -> str:
    Converts a number of seconds to a human-readable string, including hours,
    minutes, and seconds.

Author: Alexsander Lopes Camargos
License: MIT
"""


def seconds_to_human_readable(seconds: float) -> tuple:
    """
    Converts a number of seconds to a tuple representing the time in hours, minutes, and seconds.

    Given a duration in seconds, this function converts it to a tuple format
    expressed in hours, minutes, and seconds for easier interpretation and further processing.
    This format is useful for when you need to programmatically access the individual components
    of the time duration rather than having it in a human-readable string format.

    Parameters:
    - seconds (int): The time duration in seconds to be converted.

    Returns:
    - tuple: A tuple representation of the time duration, where the first element is hours,
      the second is minutes, and the third is seconds.
    """

    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    return hours, minutes, seconds
