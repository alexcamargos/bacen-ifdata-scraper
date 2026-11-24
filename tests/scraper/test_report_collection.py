"""Verify that collection rejects a CSV from another reference period.

Args:
    None.

Returns:
    None.

Raises:
    None.
"""

import json
from hashlib import sha256
from pathlib import Path

import pytest
from pytest_mock import MockerFixture

from bacen_ifdata.main.scraper import main
from bacen_ifdata.scraper.exceptions import IfDataScraperException
from bacen_ifdata.scraper.institutions import InstitutionType
from bacen_ifdata.scraper.reports import REPORTS
from bacen_ifdata.scraper.storage.collection import (
    report_inputs,
    validate_report_csv,
)
from bacen_ifdata.scraper.storage.processing import move_completed_download
from bacen_ifdata.utilities.configurations import Config


def test_wrong_period_never_reaches_raw(
    tmp_path: Path, mocker: MockerFixture,
) -> None:
    """Reject the June export collected for March.

    Args:
        tmp_path: Temporary workspace for files.
        mocker: Pytest mock fixture.

    Returns:
        None.

    Raises:
        AssertionError: If collection accepts the wrong period.
    """
    raw = tmp_path / 'raw'
    mocker.patch.object(Config, 'DOWNLOAD_DIRECTORY', raw)
    mocker.patch.object(
        Config, 'SCRATCH_DIRECTORY', tmp_path, create=True
    )
    downloaded = tmp_path / 'dados.csv'
    downloaded.write_text(
        'Instituição;Código;Data;Ativo Total\n'
        'ITAU;10069;06/2023;1\n',
        encoding='utf-8-sig',
    )
    session = mocker.Mock()
    session.download_reports.return_value = downloaded
    institution = InstitutionType.FINANCIAL_CONGLOMERATES

    with pytest.raises(IfDataScraperException, match='06/2023'):
        main(session, '03/2023', institution, REPORTS[institution].SUMMARY)

    assert session.download_reports.call_count == 2
    assert not list(raw.rglob('*.csv'))


def test_mixed_periods_are_rejected(tmp_path: Path) -> None:
    """Verify that matching first rows cannot hide a different date.

    Args:
        tmp_path: Temporary workspace for the original.

    Returns:
        None.

    Raises:
        AssertionError: If the mixed file is accepted.
    """
    source = tmp_path / 'mixed.csv'
    source.write_text(
        'Instituição;Código;Data;Ativo Total\n'
        'BB;49906;03/2023;1\n'
        'ITAU;10069;06/2023;2\n',
        encoding='utf-8-sig',
    )

    with pytest.raises(IfDataScraperException, match='03/2023, 06/2023'):
        validate_report_csv(source, '03/2023')


def test_recollection_preserves_original_and_is_idempotent(
    tmp_path: Path, mocker: MockerFixture,
) -> None:
    """Publish a corrected original once and preserve the legacy bytes.

    Args:
        tmp_path: Temporary workspace for files.
        mocker: Pytest mock fixture.

    Returns:
        None.

    Raises:
        AssertionError: If the version or provenance is lost.
    """
    raw = tmp_path / 'raw'
    mocker.patch.object(Config, 'DOWNLOAD_DIRECTORY', raw)
    mocker.patch.object(Config, 'SCRATCH_DIRECTORY', tmp_path / 'scratch')
    institution = InstitutionType.FINANCIAL_CONGLOMERATES
    report = REPORTS[institution].SUMMARY
    directory = raw / institution.name.lower() / report.name.lower()
    directory.mkdir(parents=True)
    original = directory / '2023-03.csv'
    downloaded = tmp_path / 'dados.csv'
    header = 'Instituição;Código;Data;Ativo Total\n'
    original.write_text(
        header + 'ITAU;10069;06/2023;1\n', encoding='utf-8-sig',
    )
    original_bytes = original.read_bytes()
    downloaded.write_text(
        header + 'ITAU;10069;03/2023;1\n', encoding='utf-8-sig',
    )
    session = mocker.Mock()
    session.download_reports.return_value = downloaded

    main(session, '03/2023', institution, report)
    main(session, '03/2023', institution, report)

    session.download_reports.assert_called_once()
    assert original.read_bytes() == original_bytes
    selected = report_inputs(directory)['2023-03']
    assert selected != original
    assert selected.read_bytes() == downloaded.read_bytes()
    metadata = json.loads(
        selected.with_name('metadata.json').read_text(encoding='utf-8')
    )
    assert metadata['sha256'] == sha256(selected.read_bytes()).hexdigest()
    assert metadata['source_url'] == Config.URL


def test_locked_export_is_retried(
    tmp_path: Path, mocker: MockerFixture,
) -> None:
    """Wait for release when Firefox still holds a completed-looking CSV.

    Args:
        tmp_path: Temporary download directory.
        mocker: Pytest mock fixture.

    Returns:
        None.

    Raises:
        AssertionError: If the locked export is lost.
    """
    source = tmp_path / 'dados.csv'
    destination = tmp_path / 'export.csv'
    source.write_bytes(b'original')
    rename = Path.rename
    calls = 0

    def release_after_retry(path: Path, target: Path) -> Path:
        """Fail the first move and complete the second.

        Args:
            path: Download filename.
            target: Isolated destination.

        Returns:
            Path to the moved export.

        Raises:
            PermissionError: The browser still owns the file on first access.
        """
        nonlocal calls
        calls += 1
        if calls == 1:
            raise PermissionError('Download still open.')
        return rename(path, target)

    mocker.patch.object(
        Path, 'rename', autospec=True, side_effect=release_after_retry,
    )

    move_completed_download(source, destination, timeout=3)

    assert destination.read_bytes() == b'original'
    assert calls == 2


@pytest.mark.parametrize('value, versioned', [(100, False), (200, True)])
def test_refresh_versions_only_changed_bytes(
    tmp_path: Path, mocker: MockerFixture, value: int, versioned: bool,
) -> None:
    """Refresh a valid month and save a new version only for changed bytes.

    Args:
        tmp_path: Isolated raw and temporary directories.
        mocker: Pytest mock fixture.
        value: Asset value returned by the simulated portal.
        versioned: Whether the response differs from the prior export.

    Returns:
        None.

    Raises:
        AssertionError: A refresh lost an original or published a duplicate.
    """
    raw = tmp_path / 'raw'
    mocker.patch.object(Config, 'DOWNLOAD_DIRECTORY', raw)
    mocker.patch.object(Config, 'SCRATCH_DIRECTORY', tmp_path / 'scratch')
    institution = InstitutionType.FINANCIAL_CONGLOMERATES
    report = REPORTS[institution].SUMMARY
    directory = raw / 'financial_conglomerates/summary'
    directory.mkdir(parents=True)
    original = directory / '2023-03.csv'
    download = tmp_path / 'dados.csv'
    header = 'Instituição;Código;Data;Ativo Total\n'
    original.write_text(
        header + 'A;101;03/2023;100\n', encoding='utf-8',
    )
    original_bytes = original.read_bytes()
    download.write_text(
        header + f'A;101;03/2023;{value}\n', encoding='utf-8',
    )
    session = mocker.Mock()
    session.download_reports.return_value = download

    main(session, '03/2023', institution, report, refresh=True)

    session.download_reports.assert_called_once()
    assert original.read_bytes() == original_bytes
    selected = report_inputs(directory)['2023-03']
    assert (selected != original) is versioned
    assert selected.read_bytes() == download.read_bytes()
