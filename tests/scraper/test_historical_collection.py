"""Test planning, reruns and recovery for historical IF.data collection.

Args:
    None.
Returns:
    None.
Raises:
    None.
"""

import json
from gzip import compress
from hashlib import sha256
from pathlib import Path

import pytest
from pytest_mock import MockerFixture

from bacen_ifdata.scraper import catalog
from bacen_ifdata.scraper.catalog import HistoricalReport, historical_reports
from bacen_ifdata.scraper.exceptions import IfDataScraperException
from bacen_ifdata.scraper.historical_collection import (
    run_historical_collection,
)
from bacen_ifdata.scraper.institutions import InstitutionType
from bacen_ifdata.scraper.reports import REPORTS
from bacen_ifdata.scraper.storage import validation_cache
from bacen_ifdata.utilities.configurations import Config

SCR = InstitutionType.FINANCIAL_CONGLOMERATES_SCR
PRUDENTIAL = InstitutionType.PRUDENTIAL_CONGLOMERATES
SUMMARY = REPORTS[PRUDENTIAL].SUMMARY
ASSETS = REPORTS[PRUDENTIAL].ASSETS
CSV = 'Instituição;Código;Data;Ativo Total\nBanco;101;12/2024;100\n'


@pytest.fixture
def isolated_raw(tmp_path: Path, mocker: MockerFixture) -> Path:
    """Redirect all collection writes to a test directory.

    Args:
        tmp_path: Pytest temporary directory.
        mocker: Pytest mocking fixture.
    Returns:
        The test raw directory.
    Raises:
        None.
    """
    raw = tmp_path / 'raw'
    mocker.patch.object(Config, 'DOWNLOAD_DIRECTORY', raw)
    mocker.patch.object(Config, 'SCRATCH_DIRECTORY', tmp_path / 'scratch')
    return raw


def test_catalog_includes_first_scr_period(mocker: MockerFixture) -> None:
    """Select the published first SCR period and normalize display names.

    Args:
        mocker: Pytest mocking fixture.
    Returns:
        None.
    Raises:
        None.
    """
    report = REPORTS[SCR].PORTFOLIO_LEGAL_PERSON_ECONOMIC_ACTIVITY
    files = [
        {'f': 'ifdata/201206/dados201206_1.json'},
        {'f': 'sel201206.json', 'sel': [{'id': 1007, 'n': SCR.value}]},
        {'f': 'trel201206_12.json', 'trel': {
            'id': 12,
            'n': report.value.replace('por atividade', 'por  atividade'),
            's': [{'id': 1007}],
        }},
    ]
    mocker.patch(
        'bacen_ifdata.scraper.catalog._read_catalog',
        return_value=[{'dt': 201206, 'files': files}],
    )

    assert historical_reports(5) == [
        HistoricalReport('2012-06', SCR, report, 1007, 12, (files[0]['f'],)),
    ]


@pytest.mark.parametrize('encoding', ['gzip', 'identity'])
def test_catalog_transport_decodes_response(
    encoding: str, mocker: MockerFixture,
) -> None:
    """Accept the same catalog with or without compressed transport.

    Args:
        encoding: Encoding returned by the source.
        mocker: Pytest mocking fixture.
    Returns:
        None.
    Raises:
        None.
    """
    records = [{'dt': 202412, 'files': []}]
    payload = json.dumps(records).encode()
    response = mocker.MagicMock()
    response.__enter__.return_value = response
    response.headers = {'Content-Encoding': encoding}
    response.read.return_value = (
        compress(payload) if encoding == 'gzip' else payload
    )
    fetch = mocker.patch.object(catalog, 'urlopen', return_value=response)

    assert catalog._read_catalog(5) == records
    assert fetch.call_args.args[0].full_url == Config.HISTORICAL_CATALOG
    assert fetch.call_args.args[0].get_header('Accept-encoding') == 'gzip'


def test_rerun_reuses_validation_without_browser(
    isolated_raw: Path, mocker: MockerFixture,
) -> None:
    """Validate an existing CSV once and invalidate the cache after edits.

    Args:
        isolated_raw: Test raw directory.
        mocker: Pytest mocking fixture.
    Returns:
        None.
    Raises:
        None.
    """
    directory = isolated_raw / PRUDENTIAL.name.lower() / SUMMARY.name.lower()
    directory.mkdir(parents=True)
    original = directory / '2024-12.csv'
    original.write_text(CSV, encoding='utf-8')
    selection = HistoricalReport('2024-12', PRUDENTIAL, SUMMARY, 1009, 104, ())
    catalog = mocker.patch(
        'bacen_ifdata.scraper.historical_collection.historical_reports',
        return_value=[selection],
    )
    validate = mocker.spy(validation_cache, 'validate_report_csv')
    session_factory = mocker.Mock()

    for _ in range(2):
        run_historical_collection(
            [(PRUDENTIAL, SUMMARY)], session_factory,
            period='2024-12', refresh=False, repair=False,
        )

    validate.assert_called_once_with(original, '12/2024')
    session_factory.assert_not_called()

    run_historical_collection(
        [(PRUDENTIAL, SUMMARY)], session_factory,
        period='2024-12', refresh=False, repair=True,
    )
    assert validate.call_count == 2
    assert catalog.call_count == 2

    original.write_text(CSV.replace('101', '9999'), encoding='utf-8')
    run_historical_collection(
        [(PRUDENTIAL, SUMMARY)], session_factory,
        period='2024-12', refresh=False, repair=False,
    )

    assert validate.call_count == 3
    session_factory.assert_not_called()


def test_failed_export_does_not_interrupt_other_reports(
    isolated_raw: Path, mocker: MockerFixture,
) -> None:
    """Retry an unavailable export and still commit the next valid report.

    Args:
        isolated_raw: Test raw directory.
        mocker: Pytest mocking fixture.
    Returns:
        None.
    Raises:
        None.
    """
    first = HistoricalReport('2024-12', PRUDENTIAL, SUMMARY, 1009, 104, ())
    second = HistoricalReport('2024-12', PRUDENTIAL, ASSETS, 1009, 111, ())
    mocker.patch(
        'bacen_ifdata.scraper.historical_collection.historical_reports',
        return_value=[first, second],
    )
    session = mocker.Mock()
    session.export_historical_report.side_effect = [
        IfDataScraperException('Transient failure'),
        IfDataScraperException('Still unavailable'),
        CSV.encode('utf-8'),
    ]

    with pytest.raises(IfDataScraperException, match='1 pending exports'):
        run_historical_collection(
            [(PRUDENTIAL, SUMMARY), (PRUDENTIAL, ASSETS)], lambda: session,
            period='2024-12', refresh=False, repair=False,
        )

    assert session.export_historical_report.call_args_list == [
        mocker.call(first, fresh=False),
        mocker.call(first, fresh=True),
        mocker.call(second, fresh=False),
    ]
    files = list(isolated_raw.rglob('report.csv'))
    assert len(files) == 1
    assert files[0].relative_to(isolated_raw).parts[:3] == (
        'prudential_conglomerates', 'assets', '2024-12',
    )
    manifest = json.loads(
        files[0].with_name('metadata.json').read_text(encoding='utf-8'),
    )
    assert manifest['source_selection'] == {
        'institution_id': 1009, 'report_id': 111,
    }
    assert manifest['sha256'] == sha256(files[0].read_bytes()).hexdigest()


def test_modern_period_is_rejected_before_discovery(
    mocker: MockerFixture,
) -> None:
    """Keep the historical layout away from post-2024 data.

    Args:
        mocker: Pytest mocking fixture.
    Returns:
        None.
    Raises:
        None.
    """
    catalog = mocker.patch(
        'bacen_ifdata.scraper.historical_collection.historical_reports',
    )
    session_factory = mocker.Mock()
    with pytest.raises(ValueError, match='ends at 2024-12'):
        run_historical_collection(
            [(PRUDENTIAL, SUMMARY)], session_factory,
            period='2025-03', refresh=False, repair=False,
        )
    catalog.assert_not_called()
    session_factory.assert_not_called()
