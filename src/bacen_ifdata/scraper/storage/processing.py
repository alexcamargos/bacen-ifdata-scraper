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
from collections.abc import Callable
from pathlib import Path
from typing import TypeVar

from loguru import logger

T = TypeVar('T')


def retry_file_lock(operation: Callable[[], T], artifact: Path) -> T:
    """Retry a filesystem operation while another process holds the file.

    Args:
        operation: A file operation that can be safely attempted again.
        artifact: Path to report while waiting.

    Returns:
        The result of the successful operation.

    Raises:
        OSError: The operation failed beyond the lock retry window.
    """
    deadline = time.monotonic() + 8
    while True:
        try:
            return operation()
        except PermissionError as error:
            if time.monotonic() >= deadline:
                raise
            logger.debug(f'Waiting for access to {artifact}: {error}')
            time.sleep(0.25)


def move_artifact(
    source: Path, destination: Path, *, replace: bool = False,
) -> None:
    """Publish a file or directory despite short-lived filesystem locks.

    Args:
        source: Complete staged artifact.
        destination: Visible destination on the same volume.
        replace: Use atomic replacement for a mutable destination.

    Returns:
        None.

    Raises:
        OSError: The artifact could not be moved.
    """
    move = source.replace if replace else source.rename
    retry_file_lock(lambda: move(destination), source)


def process_downloaded_files(source_path: Path, destination_path: Path) -> None:
    """Check if the downloaded file is complete and move it to the destination folder.

    Args:
        source_path(Path): Source path of the downloaded file.
        destination_path(Path): Destination path where the file should be moved.

    Raises:
        FileNotFoundError: If the source file does not exist.

    Note:
        This function uses Path.rename() which moves the file atomically
        on the same filesystem.
    """

    # Check if the file exists.
    if not source_path.exists():
        raise FileNotFoundError(f'File {source_path} does not exist.')

    # Move the file to the destination folder.
    source_path.rename(destination_path)


def build_directory_path(base_dir: Path, *parts: str) -> Path:
    """
    Constructs a safe and absolute directory path from provided components.

    This function takes multiple arguments (parts) that are joined together
    to form a complete and absolute directory path, resolves the final path
    to ensure it is absolute and removes any relative or redundant references.

    Parameters:
        base_dir (Path): The base directory where the path will be created.
        *parts (str): Variable components of the directory path.
                      Each argument is a part of the final path,
                      such as the name of a subdirectory or file.

    Returns:
        Path: A Path object representing the absolute and resolved path.

    Example:
        >>> build_directory_path(Path('/path/to/DOWNLOAD_DIRECTORY'), 'folder1', 'subfolder2')
            PosixPath('/path/to/DOWNLOAD_DIRECTORY/folder1/subfolder2')
    """

    return Path(base_dir, *parts).resolve()


def ensure_directory(path: Path) -> None:
    """
    Ensures that the directory exists.

    Args:
        path (Path): The path to the directory.
    """

    # Creates the directory if it does not exist.
    path.mkdir(parents=True, exist_ok=True)


def move_completed_download(
    source: Path, destination: Path, timeout: int,
) -> None:
    """Wait for Firefox to release the finished export, then move it.

    Args:
        source: Exact filename expected from the portal.
        destination: Unique path for the completed export.
        timeout: Maximum time to wait, in seconds.

    Returns:
        None.

    Raises:
        TimeoutError: The expected file could not be moved before timeout.
        OSError: Another filesystem error prevented moving the file.
    """
    deadline = time.monotonic() + timeout
    previous = None
    while time.monotonic() < deadline:
        if source.is_file() and not any(source.parent.glob('*.part')):
            try:
                stat = source.stat()
                signature = (stat.st_size, stat.st_mtime_ns)
                if signature == previous:
                    source.rename(destination)
                    return
                previous = signature
            except (FileNotFoundError, PermissionError) as error:
                logger.debug(f'Firefox has not released {source}: {error}')
        else:
            previous = None
        time.sleep(0.25)

    raise TimeoutError(
        f'Firefox did not finish writing {source} within {timeout}s.'
    )


def check_file_already_downloaded(file: Path) -> bool:
    """
    Checks if the file has already been downloaded.

    Args:
        file (str): The path to the file.

    Returns:
        bool: True if the file exists, False otherwise.
    """

    return Path(file).exists()
