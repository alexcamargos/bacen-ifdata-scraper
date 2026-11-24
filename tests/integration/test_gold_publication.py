"""Check that dbt must pass before a candidate replaces the published Gold.

Args:
    None.

Returns:
    None.

Raises:
    None.
"""

import subprocess
from pathlib import Path

import pytest
from pytest_mock import MockerFixture

from bacen_ifdata.manager import PipelineManager
from bacen_ifdata.utilities.configurations import Config


@pytest.mark.parametrize('passes', [False, True])
def test_gold_publication(
    tmp_path: Path, mocker: MockerFixture, passes: bool,
) -> None:
    """Preserve the current Gold on failure and publish a successful build.

    Args:
        tmp_path: Isolated data directory.
        mocker: Pytest mock fixture.
        passes: Whether the simulated dbt build succeeds.

    Returns:
        None.

    Raises:
        AssertionError: The wrong warehouse was published.
    """
    silver = tmp_path / 'silver.duckdb'
    gold = tmp_path / 'gold.duckdb'
    silver.touch()
    gold.write_bytes(b'published')
    mocker.patch.object(Config, 'DATA_DIRECTORY', tmp_path)
    mocker.patch.object(Config, 'SILVER_DATABASE_FILE', silver)
    mocker.patch.object(Config, 'GOLD_DATABASE_FILE', gold)
    mocker.patch.object(Config, 'SCRATCH_DIRECTORY', tmp_path / 'scratch')
    mocker.patch('bacen_ifdata.manager.load_dotenv')
    manager = PipelineManager(mocker.Mock(), database_service=mocker.Mock())

    def simulate_dbt(
        args: list[str], cwd: Path, env: dict[str, str], check: bool,
    ) -> None:
        """Write a candidate and optionally fail the simulated build.

        Args:
            args: Arguments passed to the dbt command.
            cwd: Directory of the dbt project.
            env: Environment with the staging database paths.
            check: Whether the caller expects errors to propagate.

        Returns:
            None.

        Raises:
            subprocess.CalledProcessError: Simulated build failure.
        """
        assert cwd == Config.DATA_ANALYTICS_DIRECTORY
        assert check
        assert Path(env['SILVER_DB_PATH']) == silver
        Path(env['GOLD_DB_PATH']).write_bytes(b'candidate')
        if not passes:
            raise subprocess.CalledProcessError(1, args)

    mocker.patch(
        'bacen_ifdata.manager.subprocess.run', side_effect=simulate_dbt,
    )
    if passes:
        manager.run_analytics()
        assert gold.read_bytes() == b'candidate'
    else:
        with pytest.raises(subprocess.CalledProcessError):
            manager.run_analytics()
        assert gold.read_bytes() == b'published'
