"""Cover content deduplication and active-version selection for local CSVs.

Args:
    None.
Returns:
    None.
Raises:
    None.
"""

import json
from pathlib import Path

import pytest

from bacen_ifdata.scraper.exceptions import IfDataScraperException
from bacen_ifdata.scraper.storage.collection import (
    publish_report,
    report_checksum,
    report_inputs,
)
from bacen_ifdata.scraper.storage.local_versioning import (
    version_local_reports,
)
from bacen_ifdata.updates import _inventory
from bacen_ifdata.utilities.configurations import Config

CSV = 'Instituição;Código;Data;Ativo\nBanco;101;12/2024;100\n'
DIRECTORY = Path('prudential_conglomerates/summary')


def test_local_versioning_is_repeatable_and_preserves_active_selection(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Import a flat original and archive a later, different local copy.

    Args:
        tmp_path: Isolated archive and scratch directories.
        monkeypatch: Redirect the incremental inventory to this archive.
    Returns:
        None.
    Raises:
        OSError: A source or published bundle cannot be accessed.
    """
    raw = tmp_path / 'raw'
    scratch = tmp_path / 'scratch'
    directory = raw / DIRECTORY
    directory.mkdir(parents=True)
    source = directory / '2024-12.csv'
    source.write_text(CSV, encoding='utf-8')
    monkeypatch.setattr(Config, 'DOWNLOAD_DIRECTORY', raw)

    version_local_reports(raw, scratch)
    active = report_inputs(directory)['2024-12']
    assert active != source
    assert active.read_bytes() == source.read_bytes()
    metadata = json.loads(
        active.with_name('metadata.json').read_text(encoding='utf-8'),
    )
    assert metadata['source_type'] == 'local_csv'
    assert metadata['source_path'] == f'{DIRECTORY.as_posix()}/{source.name}'
    assert metadata['sha256'] == report_checksum(source)
    assert 'collected_at' not in metadata
    entry = next(iter(_inventory().values()))
    assert entry.path == active
    assert entry.source_url == source.as_uri()
    assert entry.collected_at is None

    version_local_reports(raw, scratch)
    assert len(list(directory.rglob('metadata.json'))) == 1

    source.write_text(CSV.replace(';100', ';200'), encoding='utf-8')
    version_local_reports(raw, scratch)
    version_local_reports(raw, scratch)
    assert report_inputs(directory)['2024-12'] == active
    bundles = list(directory.rglob('report.csv'))
    assert len(bundles) == 2
    assert any(path.read_bytes() == source.read_bytes() for path in bundles)


def test_local_versioning_validates_dates_and_reuses_portal_bundles(
    tmp_path: Path,
) -> None:
    """Skip a portal duplicate and preserve an invalid flat source.

    Args:
        tmp_path: Isolated archive and scratch directories.
    Returns:
        None.
    Raises:
        OSError: A source or published bundle cannot be accessed.
    """
    raw = tmp_path / 'raw'
    scratch = tmp_path / 'scratch'
    directory = raw / DIRECTORY
    directory.mkdir(parents=True)
    original = directory / '2024-12.csv'
    original.write_text(CSV, encoding='utf-8')
    downloaded = publish_report(
        original, directory / original.stem, Config.URL, scratch,
    )
    invalid = directory / '2024-09.csv'
    invalid.write_bytes(original.read_bytes())

    with pytest.raises(IfDataScraperException, match='expected data-base'):
        version_local_reports(raw, scratch)
    assert report_inputs(directory)['2024-12'] == downloaded
    assert list(directory.rglob('report.csv')) == [downloaded]
    assert invalid.read_bytes() == original.read_bytes()
