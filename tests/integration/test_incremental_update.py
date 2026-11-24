"""Exercise release publication with historical revisions and a real dbt test.

Args:
    None.

Returns:
    None.

Raises:
    None.
"""

import subprocess
from datetime import date
from pathlib import Path

import duckdb
import pytest
from pytest_mock import MockerFixture

from bacen_ifdata.application import Application
from bacen_ifdata.data_transformer.controller import TransformerController
from bacen_ifdata.scraper.storage.collection import (
    publish_report,
    report_checksum,
)
from bacen_ifdata.utilities.configurations import Config
from bacen_ifdata.utilities.releases import (
    CURRENT_RELEASE,
    current_release,
    warehouse_path,
)
from ifdata import get_arguments, run_pipeline


def test_update_revises_one_period_and_preserves_last_release(
    tmp_path: Path, mocker: MockerFixture,
) -> None:
    """Replace one historical period and reject a failing Gold candidate.

    Args:
        tmp_path: Isolated workspace for test data and dbt files.
        mocker: Pytest mock fixture used to observe actual calls.

    Returns:
        None.

    Raises:
        AssertionError: The observed release does not match the scenario.
    """
    directory = tmp_path / 'raw/financial_conglomerates/summary'
    project = tmp_path / 'dbt'
    for path in (directory, project / 'models', project / 'tests'):
        path.mkdir(parents=True)
    (project / 'dbt_project.yml').write_text(
        'name: acceptance\nprofile: acceptance\n'
        'models:\n  acceptance:\n    +materialized: table\n',
        encoding='utf-8',
    )
    (project / 'profiles.yml').write_text(
        "acceptance:\n  target: test\n  outputs:\n    test:\n"
        "      type: duckdb\n      path: \"{{ env_var('GOLD_DB_PATH') }}\"\n"
        "      attach:\n        - path: \"{{ env_var('SILVER_DB_PATH') }}\"\n"
        "          alias: silver\n          read_only: true\n",
        encoding='utf-8',
    )
    (project / 'models/resumo.sql').write_text(
        'select codigo, data_base, ativo_total '
        'from silver.main.financial_conglomerates_summary',
        encoding='utf-8',
    )
    (project / 'tests/sem_valor_rejeitado.sql').write_text(
        "select * from {{ ref('resumo') }} where ativo_total = 999",
        encoding='utf-8',
    )
    mocker.patch.object(Config, 'DATA_DIRECTORY', tmp_path)
    mocker.patch.object(Config, 'DOWNLOAD_DIRECTORY', tmp_path / 'raw')
    mocker.patch.object(Config, 'SCRATCH_DIRECTORY', tmp_path / 'scratch')
    mocker.patch.object(Config, 'DATA_ANALYTICS_DIRECTORY', project)
    mocker.patch('sys.argv', ['ifdata', '--update'])
    transform = mocker.spy(TransformerController, 'transform')
    dbt_runner = mocker.spy(subprocess, 'run')

    header = 'Instituição;Código;Data;Ativo Total;\n'
    march = directory / '2023-03.csv'
    june = directory / '2023-06.csv'
    march.write_text(
        header + 'A;101;03/2023;100\nB;102;03/2023;200\n',
        encoding='utf-8',
    )
    june.write_text(header + 'A;101;06/2023;300\n', encoding='utf-8')
    baseline_march = report_checksum(march)
    args = get_arguments()
    with Application() as app:
        run_pipeline(app.pipeline_manager, args)
        initial = current_release(tmp_path)
        assert initial is not None
        assert transform.call_count == 2
        assert dbt_runner.call_count == 1

        revised = tmp_path / 'revised.csv'
        revised.write_text(header + 'A;101;03/2023;150\n', encoding='utf-8')
        publish_report(
            revised, directory / march.stem, Config.URL,
            Config.SCRATCH_DIRECTORY,
        )
        run_pipeline(app.pipeline_manager, args)
        published = current_release(tmp_path)
        assert published is not None
        assert published != initial
        assert transform.call_count == 3
        assert dbt_runner.call_count == 2
        with duckdb.connect(str(published.silver), read_only=True) as conn:
            assert conn.execute(
                'SELECT codigo, data_base, ativo_total '
                'FROM financial_conglomerates_summary ORDER BY data_base',
            ).fetchall() == [
                (101, date(2023, 3, 1), 150),
                (101, date(2023, 6, 1), 300),
            ]
            assert conn.execute(
                'SELECT data_base, sha256, row_count, '
                'collected_at IS NOT NULL '
                'FROM ifdata_control.applied_inputs ORDER BY data_base',
            ).fetchall() == [
                (date(2023, 3, 1), report_checksum(revised), 1, True),
                (date(2023, 6, 1), report_checksum(june), 1, False),
            ]
        assert report_checksum(march) == baseline_march
        pointer = tmp_path / CURRENT_RELEASE
        published_manifest = pointer.read_bytes()

        run_pipeline(app.pipeline_manager, args)
        assert transform.call_count == 3
        assert dbt_runner.call_count == 2
        assert pointer.read_bytes() == published_manifest

        revised.write_text(header + 'A;101;03/2023;999\n', encoding='utf-8')
        publish_report(
            revised, directory / march.stem, Config.URL,
            Config.SCRATCH_DIRECTORY,
        )
        with pytest.raises(subprocess.CalledProcessError):
            run_pipeline(app.pipeline_manager, args)
        assert transform.call_count == 4
        assert dbt_runner.call_count == 3

    assert pointer.read_bytes() == published_manifest
    assert current_release(tmp_path) == published
    for layer, path, table in (
        ('silver', published.silver, 'financial_conglomerates_summary'),
        ('gold', published.gold, 'resumo'),
    ):
        assert warehouse_path(layer, tmp_path) == path
        with duckdb.connect(str(path), read_only=True) as conn:
            assert conn.execute(
                f'SELECT ativo_total FROM {table} ORDER BY data_base',
            ).fetchall() == [(150,), (300,)]
    assert initial.gold.is_file()
    assert initial.silver.is_file()
    assert len(list(published.gold.parent.parent.iterdir())) == 2
