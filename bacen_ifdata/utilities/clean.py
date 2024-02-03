#!/usr/bin/env python
# encoding: utf-8
#
#  ------------------------------------------------------------------------------
#  Name: clean.py
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

This module is designed to facilitate automatic data scraping and management tasks
for the Banco Central's financial data (Bacen IF.data). It provides utilities to
check for empty files and clean up directories by removing empty CSV files, ensuring
that data storage remains efficient and organized.

The module contains the following main functions:

- __files_is_empty(file: Path) -> bool:
  Checks if a specified file is empty based on its size. It works with any file type,
  ensuring versatility in data management tasks.

- clean_empty_csv_files(path: Path) -> None:
  Removes all empty CSV files from a specified directory, aiding in the maintenance
  of a clean and efficient data storage environment.

These utilities are essential for anyone looking to automate the management of large
volumes of financial data, particularly when dealing with frequent updates or the
need to ensure data integrity and storage efficiency.

Note: The __files_is_empty function is intended for internal use within this module
to support the functionality of cleaning up empty CSV files but can be utilized
directly if necessary.

Author: Alexsander Lopes Camargos
License: MIT
"""

from pathlib import Path


def __files_is_empty(file: Path) -> bool:
    """
        Checks if the specified file is empty.

        Determines if a file is empty by checking its size. This function can be used for any file type,
        not limited to CSV files, despite the function name suggesting it's specific to CSV files.

        Parameters:
        - file (Path): The path of the file to be checked.

        Returns:
        - bool: True if the file is empty (size is 0), otherwise False.
        """
    return file.stat().st_size == 0


def clean_empty_csv_files(path: Path) -> None:
    """
    Clean up the directory by removing empty CSV files.

    Iterates over all CSV files in the specified directory
    and removes each one that is empty.

    Parameters:
    - path (Path): The path of the directory to be cleaned.
    """

    empty_files = False

    for file in path.rglob('*.csv'):
        if __files_is_empty(file):
            print(f'Removing empty file: {file.name}')
            file.unlink()
            empty_files = True

    if not empty_files:
        print('No empty files found.')


def clean_download_base_directory(path: Path) -> None:
    """
    Clean up the download base directory by removing CSV files that were
    downloaded by scraping processes and have not been moved to the storage directory.

    This function iterates over all CSV files in the specified directory and its subdirectories.
    It removes each CSV file, assuming that any file in this directory is no longer needed.
    This operation is intended for cleanup after files have been processed and should be used
    with caution to avoid deleting files unintentionally.

    Parameters:
    - path (Path): The path of the download base directory to be cleaned.
    """

    for file in path.glob('*.csv'):
        file.unlink()
