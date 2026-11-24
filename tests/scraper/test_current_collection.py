"""Exercise the current catalog, publication and combined CSV contract.

Args:
    None.
Returns:
    None.
Raises:
    None.
"""

import csv
import json
from pathlib import Path

from pytest_mock import MockerFixture

from bacen_ifdata.scraper import catalog
from bacen_ifdata.scraper.catalog import HistoricalReport
from bacen_ifdata.scraper.historical_collection import (
    run_historical_collection,
)
from bacen_ifdata.scraper.institutions import InstitutionType
from bacen_ifdata.scraper.reports import ReportsPrudentialConglomerates
from bacen_ifdata.scraper.session import Session
from bacen_ifdata.scraper.storage.collection import report_inputs
from bacen_ifdata.scraper.storage.consolidation import consolidate_reports
from bacen_ifdata.utilities.configurations import Config


def test_current_export_joins_the_historical_csv_inventory(
    tmp_path: Path, mocker: MockerFixture,
) -> None:
    """Retain both layouts, trace their rows, and use current source IDs.

    Args:
        tmp_path: Isolated files for the download and consolidation.
        mocker: Pytest mocking fixture.
    Returns:
        None.
    Raises:
        OSError: The fixtures or results cannot be read or written.
    """
    scope = InstitutionType.PRUDENTIAL_CONGLOMERATES
    report = ReportsPrudentialConglomerates.ASSETS
    raw = tmp_path / 'raw'
    scratch = tmp_path / 'scratch'
    mocker.patch.object(Config, 'DOWNLOAD_DIRECTORY', raw)
    mocker.patch.object(Config, 'SCRATCH_DIRECTORY', scratch)
    directory = raw / scope.name.lower() / report.name.lower()
    directory.mkdir(parents=True)
    historical = directory / '2024-12.csv'
    historical.write_text(
        'Instituição;Código;Data;Crédito;;\n'
        ';;;Saldo;Provisão incorrida;\n'
        'Banco A;001;12/2024;10,50;1,00\n',
        encoding='utf-8',
    )
    files = [
        {'f': 'ifdata_2025_2030//202503/dados202503_1.json'},
        {'f': 'sel.json', 'sel': [{'id': 1009, 'n': scope.value}]},
        {'f': 'trel.json', 'trel': {
            'id': 105, 'n': report.value, 's': [{'id': 1009}],
        }},
    ]
    fetch = mocker.patch.object(
        catalog, '_read_catalog', return_value=[{'dt': 202503, 'files': files}],
    )
    session = mocker.Mock()
    session.export_historical_report.return_value = (
        'Instituição;Código;Data;Crédito;;\n'
        ';;;Saldo;Provisão esperada;\n'
        'Banco A;001;03/2025;15,50;2,00\n'
        'Total;;;15,50;2,00\n'
    ).encode('utf-8')
    run_historical_collection(
        [(scope, report)], lambda: session,
        period='2025-03', refresh=False, repair=False, include_current=True,
    )
    fetch.assert_called_once_with(Config.TIMEOUT, Config.CURRENT_CATALOG)
    target = session.export_historical_report.call_args.args[0]
    assert (target.institution_id, target.report_id) == (1009, 105)
    assert target.source_url == Config.CURRENT_URL

    inputs = report_inputs(directory)
    assert set(inputs) == {'2024-12', '2025-03'}
    manifest = inputs['2025-03'].with_name('metadata.json')
    metadata = json.loads(manifest.read_text(encoding='utf-8'))
    assert metadata['source_url'] == Config.CURRENT_URL
    assert metadata['source_selection']['report_id'] == 105

    output = tmp_path / 'interim' / 'series.csv'
    consolidate_reports(inputs, output, raw, scratch)
    with output.open(encoding='utf-8-sig', newline='') as stream:
        rows = list(csv.DictReader(stream, delimiter=';'))
    assert [row['data_base'] for row in rows] == ['2024-12', '2025-03']
    assert [row['Código'] for row in rows] == ['001', '001']
    assert [row['Crédito / Saldo'] for row in rows] == ['10,50', '15,50']
    assert rows[0]['Crédito / Provisão incorrida'] == '1,00'
    assert rows[1]['Crédito / Provisão incorrida'] == ''
    assert rows[0]['Crédito / Provisão esperada'] == ''
    assert rows[1]['Crédito / Provisão esperada'] == '2,00'
    assert raw / rows[1]['arquivo_origem'] == inputs['2025-03']



def test_session_switches_portals_before_reusing_report_data(
    tmp_path: Path, mocker: MockerFixture,
) -> None:
    """Use only the active portal's loaded data and reset on retry.

    Args:
        tmp_path: Isolated browser download directory.
        mocker: Pytest mocking fixture.
    Returns:
        None.
    Raises:
        None.
    """
    scope = InstitutionType.PRUDENTIAL_CONGLOMERATES
    report = ReportsPrudentialConglomerates.SUMMARY
    historical = HistoricalReport('2024-12', scope, report, 1009, 104, ())
    current = HistoricalReport(
        '2025-03', scope, report, 1009, 121, (), Config.CURRENT_URL,
    )
    browser = mocker.Mock()
    session = Session(browser, Config.URL, tmp_path)
    session.open()

    session.export_historical_report(historical)
    session.export_historical_report(current)
    session.export_historical_report(current)
    session.export_historical_report(current, fresh=True)
    session.export_historical_report(historical)

    assert browser.initialize.call_args_list == [
        mocker.call(Config.URL),
        mocker.call(Config.CURRENT_URL),
        mocker.call(Config.CURRENT_URL),
        mocker.call(Config.URL),
    ]
    assert [
        call.kwargs['reuse']
        for call in browser.export_historical_report.call_args_list
    ] == [False, False, True, False, False]
