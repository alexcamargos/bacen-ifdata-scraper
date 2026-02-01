#!/usr/bin/env python
# encoding: utf-8

# ------------------------------------------------------------------------------
#  Name: loader.py
#  Version: 0.0.1
#
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
# ------------------------------------------------------------------------------

"""Bacen IF.data AutoScraper & Data Manager"""

from pathlib import Path
from typing import Any, Final, Optional

import pandas as pd
from loguru import logger

from bacen_ifdata.utilities.csv_loader import load_csv_data

# Nomes das colunas definidos com base na ordem do arquivo CSV e nas descrições do PDF.
COLUMN_NAMES: Final[list[str]] = [
    # --- Identificação da Instituição ---
    "instituicao_financeira",  # Nome da instituição [cite: 1]
    # Código da instituição no cadastro do Banco Central [cite: 1]
    "codigo_instituicao",
    # Nome do conglomerado prudencial [cite: 1]
    "nome_conglomerado_prudencial",
    # Código do conglomerado financeiro [cite: 1]
    "codigo_conglomerado_financeiro",
    # Código do conglomerado prudencial [cite: 1]
    "codigo_conglomerado_prudencial",
    # --- Classificação ---
    "tcb",  # Tipo de Consolidado Bancário [cite: 1]
    # Tipo de Controle (Público, Privado Nacional, etc.) [cite: 1]
    "tc",
    # Tipo de Instituição (Banco Múltiplo, Comercial, etc.) [cite: 1]
    "ti",
    # --- Localização e Data ---
    "cidade",  # Cidade sede da instituição [cite: 2]
    "uf",  # Unidade da Federação da sede [cite: 2]
    # Data-base do Relatório (MM/YYYY) [cite: 2]
    "data_base",
    # --- Dados Financeiros e Operacionais ---
    "ativo_total",  # Valor do Ativo Total [cite: 2]
    # Valor da Carteira de Crédito Classificada [cite: 2]
    "carteira_de_credito_classificada",
    # Passivo Circulante e Exigível a Longo Prazo [cite: 2]
    "passivo_circulante_e_exigivel_lp",
    # Principal componente de Captações (Depósitos) [cite: 2]
    "captacoes_depositos",
    "patrimonio_liquido",  # Valor do Patrimônio Líquido [cite: 2]
    "lucro_liquido",  # Valor do Lucro Líquido [cite: 2]
    # Quantidade de agências da instituição [cite: 2]
    "numero_de_agencias",
    # Quantidade de postos de atendimento [cite: 2]
    "numero_de_postos_atendimento",
]


# pylint: disable=too-few-public-methods
class LoaderController:
    """Controller for loading data from reports.

    This class is responsible for controlling the loading of data from reports.
    """

    def __init__(self) -> None:
        """Initializes a new instance of the LoaderController class."""

        self._data: Optional[pd.DataFrame] = None

        # CSV options for loading data.
        self._csv_options: dict[str, Any] = {'sep': ";", "header": None, "names": COLUMN_NAMES}

    def _load_data(self, csv_file_path: Path):
        """Load data from the source CSV file.

        This method is responsible for loading the data from the source CSV file.

        Args:
            csv_file_path (Path): The path to the CSV file to be loaded.
        """

        # Load the data from the input CSV file.
        self._data = load_csv_data(csv_file_path.as_posix(), self._csv_options)

    def loader_sample_data(self, input_data: Path, sample_size: int = 5) -> None:
        """Load a sample of the data

        This method loads a sample of the data from the input CSV file and prints it.

        Args:
            input_data (Path): The path to the CSV file to be loaded.
            sample_size (int): The number of sample rows to be printed. Default is 5.
        """

        # Load the data from the input CSV file.
        self._load_data(input_data)

        # Check if the data was loaded successfully.
        if self._data is None:
            raise RuntimeError("Data loading failed: self._data is None")

        # Print a sample of the loaded data.
        logger.info(self._data.sample(sample_size))
