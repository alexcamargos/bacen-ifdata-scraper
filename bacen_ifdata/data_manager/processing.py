#!/usr/bin/env python
# encoding: utf-8
#
#  ------------------------------------------------------------------------------
#  Name: run.py
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

from enum import StrEnum
from pathlib import Path

from loguru import logger

from bacen_ifdata.scraper.storage.processing import build_directory_path
from bacen_ifdata.utilities import config


def check_file_already_processed(output_directory: Path, file: str) -> bool:
    """Checks if the file has already been processed."""

    # Check if the file exists.
    if (output_directory / file).exists():
        return True
    else:
        return False


def normalize_csv(institution: StrEnum, report: StrEnum, file: str) -> bool:
    """
    Normalizes a CSV file from Bacen If.Data by correcting its header
    structure and removing inconsistent lines at both the start and end
    of the file.

    The normalization process involves several steps:
    1. Correcting header inconsistencies due to non-standard CSV formatting by Bacen,
       where column titles might appear in different lines based on header groupings.
    2. Removing any empty final column in the header.
    3. Discarding additional lines at the end of the file that contain consolidated
       report information and do not conform to the standard data format.

    The function checks if the file has already been normalized before proceeding.

    Args:
        institution (StrEnum): An enumerated value representing the institution.
        report (StrEnum): An enumerated value representing the report type.
        file (str): The name of the file to be normalized.

    Returns:
        bool: True if the file is successfully normalized, False otherwise.

    Raises:
        FileNotFoundError: If the specified file is not found in the input directory.
        IOError: If an input/output error occurs during file processing.

    Note:
        The function assumes the presence of a specific directory structure
        for input (downloaded CSV files) and output (normalized CSV files),
        as defined in the configuration module (`CONFIG`).
    """

    # Diretório onde os arquivos CSV baixados são armazenados.
    input_path = build_directory_path(config.DOWNLOAD_DIRECTORY,
                                      institution.name.lower(),
                                      report.name.lower())

    # Diretório onde os arquivos CSV normalizados serão armazenados.
    output_path = build_directory_path(config.PROCESSED_FILES_DIRECTORY,
                                       institution.name.lower(),
                                       report.name.lower())

    # Check if the file has already been normalized.
    if check_file_already_processed(output_path, file):
        logger.info(f'File {file} has already been normalized, skipping...')
        return False

    # Normalize the file.
    try:
        with open(f'{input_path}\\{file}', 'r', encoding='utf-8') as input_file, \
                open(f'{output_path}\\{file}', 'w', encoding='utf-8') as output_file:
            data = input_file.readlines()

            # The developers responsible for the Bacen website deviated from
            # the standard CSV format. They implemented an unusual approach
            # by including groups of headers within the CSV file.
            # This results in an inconsistent structure where the column
            # title may appear in either the first or third line, varying
            # according to the number of groupings in the headers.
            # This peculiarity presents a unique challenge in handling these files.
            header = data[0].split(';')
            start = 1

            for index in range(1, 6):
                current_line = data[index].split(';')
                if current_line[0] == '':
                    start += 1
                else:
                    break

            if start > 1:
                for column_index, column_value in enumerate(header):
                    if column_value == '':
                        for row_index in range(start - 1, 0, -1):
                            cols = data[row_index].split(';')
                            if len(cols) > column_index and cols[column_index].strip():
                                header[column_index] = cols[column_index].strip()
                                break

            # On certain occasions, the CSV files provided by Bacen
            # feature a final column with no data in the header.
            # To ensure the integrity and consistency of the data,
            # this empty column will be identified and removed.
            if header[-1] in ('\n', ''):
                # Remove the last column.
                header.pop()

            # Remove the inconsistent header.
            data = data[start:]

            # The CSV files provided by Bacen include additional lines
            # at the end containing consolidated report information.
            # These extra lines do not conform to the standard format
            # of the rest of the file and thus need to be removed for
            # an accurate data analysis. The approach involves identifying
            # and discarding all lines following the first one that does
            # not have the same number of columns as the header.
            mismatch_index = next(
                (index for index, line in enumerate(data)
                 if len(line.rstrip().split(';')) != len(header)), len(data)
            )
            data = data[:mismatch_index]

            # Save the normalized file.
            output_file.writelines(data)

        # Return True if the file was successfully normalized.
        return True

    # Handle exceptions.
    except FileNotFoundError as error:
        logger.error(f'File not found: {error.filename}')
        return False
    except IOError as error:
        logger.error(f'Input/output error: {error}')
        return False
