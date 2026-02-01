#!/usr/bin/env python
# encoding: utf-8

# ------------------------------------------------------------------------------
#  Name: controller.py
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

"""Bacen IF.data AutoScraper & Data Manager"""

from pathlib import Path
from typing import Protocol

import pandas as pd


# pylint: disable=too-few-public-methods
class TransformerControllerInterface(Protocol):
    """Represents the interface for the Transformer Controller."""

    def transform(self, file_path: Path, schema) -> pd.DataFrame:
        """Transforms the data from the given file path according to the specified schema.

        Args:
            file_path (Path): The path to the file to be transformed.
            schema: The schema to be used for transformation.

        Returns:
            pd.DataFrame: The transformed DataFrame.
        """
