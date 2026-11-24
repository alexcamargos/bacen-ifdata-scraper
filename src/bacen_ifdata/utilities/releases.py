"""Resolve the published IF.data DuckDB release.

Args:
    None.

Returns:
    None.

Raises:
    None.
"""

import json
from dataclasses import dataclass
from pathlib import Path

from bacen_ifdata.scraper.storage.processing import retry_file_lock
from bacen_ifdata.utilities.configurations import Config

CURRENT_RELEASE = Path('processed/current.json')


@dataclass(frozen=True)
class WarehouseRelease:
    """A published pair of Silver and Gold databases.

    Args:
        silver: Published Silver path.
        gold: Published Gold path.
        model_revision: Fingerprint of the dbt project used to build Gold.

    Returns:
        None.

    Raises:
        None.
    """

    silver: Path
    gold: Path
    model_revision: str


def current_release(directory: Path) -> WarehouseRelease | None:
    """Read the current pointer once and resolve both warehouse paths.

    Args:
        directory: Root of the data layers.

    Returns:
        The published pair, or None before the first release.

    Raises:
        ValueError: A path refers outside the data directory.
        KeyError: The pointer has an incomplete schema.
        OSError: The pointer or its warehouse files cannot be read.
    """
    root = directory.resolve()
    path = root / CURRENT_RELEASE
    try:
        pointer = retry_file_lock(
            lambda: path.read_text(encoding='utf-8'), path,
        )
    except FileNotFoundError:
        return None
    manifest = json.loads(pointer)
    silver = (root / manifest['silver']).resolve()
    gold = (root / manifest['gold']).resolve()
    for path in (silver, gold):
        if not path.is_relative_to(root):
            raise ValueError(f'Release path is outside the data root: {path}')
        if not path.is_file():
            raise FileNotFoundError(f'Published warehouse missing: {path}')
    return WarehouseRelease(silver, gold, manifest['model_revision'])


def warehouse_path(
    layer: str, directory: Path | None = None,
) -> Path:
    """Resolve one warehouse for an analytical reader.

    Args:
        layer: The requested warehouse, either silver or gold.
        directory: Optional data root for readers outside the project root.

    Returns:
        The file in the current release or the legacy warehouse path.

    Raises:
        ValueError: The layer or published pointer is invalid.
        OSError: The published pair cannot be accessed.
    """
    if layer not in {'silver', 'gold'}:
        raise ValueError(f'Unknown warehouse layer: {layer}')
    root = directory.resolve() if directory else Config.DATA_DIRECTORY
    release = current_release(root)
    if release is not None:
        return release.silver if layer == 'silver' else release.gold

    legacy = root / f'{layer}_warehouse.duckdb'
    if legacy.is_file():
        return legacy
    subdirectory = 'interim' if layer == 'silver' else 'processed'
    return root / subdirectory / legacy.name
