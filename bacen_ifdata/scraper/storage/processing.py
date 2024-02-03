#!/usr/bin/env python
# encoding: utf-8
#
#  ------------------------------------------------------------------------------
#  Name: processing.py
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
import time
from pathlib import Path


def process_downloaded_files(src: Path, dst: Path) -> None:
    """
    Check if the downloaded files are complete and move
    them to the destination folder.
    """

    # Check if the file exists.
    if src.exists():
        # Move the file to the destination folder.
        src.rename(dst)
    else:
        raise FileNotFoundError(f'File {src} does not exist.')


def build_directory_path(base_dir: Path, *parts):
    """
    Constructs a safe and absolute directory path from provided components.

    This function takes multiple arguments (parts) that are joined together
    to form a complete and absolute directory path, resolves the final path
    to ensure it is absolute and removes any relative or redundant references.

    Parameters:
        base_dir (str): The base directory where the path will be created.
        *parts (str): Variable components of the directory path.
                      Each argument is a part of the final path,
                      such as the name of a subdirectory or file.

    Returns:
        Path: A Path object representing the absolute and resolved path.

    Example:
    >>> build_directory_path('folder1', 'subfolder2')
    PosixPath('/path/to/DOWNLOAD_DIRECTORY/folder1/subfolder2')
    """

    return Path(base_dir, *parts).resolve()


def ensure_directory(path: Path) -> None:
    """
    Ensures that the directory exists.

    Args:
        path (str): The path to the directory.
    """

    # Creates the directory if it does not exist.
    path.mkdir(parents=True, exist_ok=True)


def wait_for_download_completion(directory: Path, filename: str, timeout: int = 300) -> bool:
    """
    Waits until a file has been completely downloaded.

    This function checks the specified download directory for the presence of a
    fully downloaded file. It waits until the file with the specified beginning
    of the filename is present and no longer has a temporary '.part' or other
    browser-specific temporary extension.

    Args:
        directory (str): The directory where the file is being downloaded.
        filename (str): The beginning of the filename to check for.
        timeout (int): The maximum amount of time to wait for the file to download, in seconds.
                       Defaults to 300 seconds.

    Returns:
        bool: True if the file was downloaded completely within
              the timeout, False otherwise.
    """

    start_time = time.time()
    directory_path = Path(directory)

    while time.time() - start_time < timeout:
        # Check if the filename exists in the directory.
        for file_path in directory_path.glob(f'{filename}*'):
            if (not file_path.name.endswith('.crdownload') and not
                    file_path.name.endswith('.part')):
                # The file has been completely downloaded.
                return True

        # Wait for the file to be downloaded.
        time.sleep(1)

    return False


def check_file_already_downloaded(file: Path) -> bool:
    """
    Checks if the file has already been downloaded.

    Args:
        file (str): The path to the file.

    Returns:
        bool: True if the file exists, False otherwise.
    """

    return Path(file).exists()
