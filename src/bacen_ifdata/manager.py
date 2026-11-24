#!/usr/bin/env python
# encoding: utf-8

# ------------------------------------------------------------------------------
#  Name: manager.py
#  Version: 0.0.1
#
#  Summary: Project Name
#           Quick description of the project.
#
#  Author: Alexsander Lopes Camargos
#  Author-email: alcamargos@vivaldi.net
#
#  License: MIT
# ------------------------------------------------------------------------------

"""Orchestrate IF.data collection and analytical builds.

Args:
    None.

Returns:
    None.

Raises:
    None.
"""

import os
import subprocess
from enum import StrEnum
from pathlib import Path
from tempfile import TemporaryDirectory

from dotenv import load_dotenv
from loguru import logger

from bacen_ifdata import Pipeline
from bacen_ifdata.data_loader.storage import DatabaseService
from bacen_ifdata.scraper.historical_collection import (
    run_historical_collection,
)
from bacen_ifdata.scraper.institutions import InstitutionType as Institutions
from bacen_ifdata.scraper.reports import REPORTS
from bacen_ifdata.scraper.storage.processing import move_artifact
from bacen_ifdata.updates import update_warehouse
from bacen_ifdata.utilities.configurations import Config as Cfg


class PipelineManager:
    """Manages the IF.data pipeline, including scraping, cleaning, transforming, and loading data."""

    def __init__(self, pipeline: Pipeline, database_service: DatabaseService | None = None) -> None:
        """Initializes the PipelineManager with a pipeline instance.

        Args:
            pipeline (Pipeline): An instance of the Pipeline class.
            database_service (DatabaseService | None): An optional instance of DatabaseService for managing database
                                                       connections. If not provided, a new instance will be created
                                                       when needed.
        """

        # The Pipeline class orchestrates the entire data processing workflow,
        # including scraping, cleaning, transforming, and loading data.
        self.pipeline = pipeline
        # The DatabaseService is responsible for managing the connection to the DuckDB database.
        self._database_service = database_service or DatabaseService()

    def _reset_database(self) -> None:
        """Resets the database before loading to prevent data duplication.

        The pipeline performs a full reload on each execution.
        """

        self._database_service.reset_database()
        self._database_service.close()

    def _get_execution_targets(
        self, institution_filter: str | None = None, report_filter: str | None = None
    ) -> list[tuple[Institutions, StrEnum]]:
        """Determine which institutions and reports to process based on filters.

        Args:
            institution_filter: Optional name of the institution Enum to filter by.
            report_filter: Optional name of the report Enum to filter by.

        Returns:
            A list of tuples (Institution, Report) to process.
        """

        targets = []

        # Find matching institution enum if filter provided
        target_inst = None
        if institution_filter:
            try:
                # Get the enum member by its name (e.g. 'PRUDENTIAL_CONGLOMERATES')
                target_inst = Institutions[institution_filter.upper()]
            except KeyError as error:
                raise ValueError(
                    f'Unknown institution filter: {institution_filter}.'
                ) from error

        for institution in Institutions:
            if target_inst and institution != target_inst:
                continue

            for report in REPORTS[institution]:
                if report_filter and report.name.upper() != report_filter.upper():
                    continue

                targets.append((institution, report))

        return targets

    def run_scraper(
        self,
        institution: str | None = None,
        report: str | None = None,
        *,
        data_base: str | None = None,
        repair_raw: bool = False,
        refresh: bool = False,
    ) -> None:
        """Collect selected reports or repair invalid original exports.

        Args:
            institution: Optional name of an institutional scope.
            report: Optional name of a report.
            data_base: Optional reference month in YYYY-MM format.
            repair_raw: Recollect only invalid originals already on disk.
            refresh: Download the selected month even when it is valid locally.

        Returns:
            None.

        Raises:
            ValueError: The selection matches no published reports.
            IfDataScraperException: One or more repairs are still pending.
        """
        if refresh and (not data_base or repair_raw):
            raise ValueError('Refresh requires a date and excludes raw repair.')
        targets = self._get_execution_targets(institution, report)
        if not targets:
            raise ValueError(f'Unknown report for the selection: {report}.')

        run_historical_collection(
            targets,
            lambda: self.pipeline.session,
            period=data_base,
            refresh=refresh,
            repair=repair_raw,
        )

    def run_cleaner(self, institution: str | None = None, report: str | None = None) -> None:
        """Main function for executing the cleaner."""

        # Run the cleaner.
        targets = self._get_execution_targets(institution, report)
        for process_institution, process_report in targets:
            self.pipeline.cleaner(process_institution, process_report)

    def run_transformer(self, institution: str | None = None, report: str | None = None) -> None:
        """Main function for executing the transformer."""

        # Run the transformer for all institutions.
        targets = self._get_execution_targets(institution, report)
        for process_institution, process_report in targets:
            self.pipeline.transformer(process_institution, process_report)

    def run_loader(
        self, institution: str | None = None, report: str | None = None,
    ) -> None:
        """Reload the selected reports atomically in the manual warehouse.

        Args:
            institution: Optional institutional scope.
            report: Optional report name.

        Returns:
            None.

        Raises:
            ValueError: A transformed CSV has an invalid name, key or period.
            OSError: A transformed CSV cannot be read.
            duckdb.Error: DuckDB cannot complete the reload.
        """
        targets = self._get_execution_targets(institution, report)
        filtered = bool(institution or report)
        with self._database_service.transaction():
            if not filtered:
                self._reset_database()

            for loaded_institution, loaded_report in targets:
                if filtered:
                    table_name = (
                        f'{loaded_institution.name.lower()}_'
                        f'{loaded_report.name.lower()}'
                    )
                    self._database_service.drop_table(table_name)
                self.pipeline.loader(
                    loaded_institution, loaded_report,
                    database_service=self._database_service,
                )

    def run_analytics(self) -> None:
        """Build and test Gold before replacing the published warehouse.

        Args:
            None.

        Returns:
            None.

        Raises:
            FileNotFoundError: The dbt project or Silver database is missing.
            ValueError: Silver and Gold are configured with the same path.
            subprocess.CalledProcessError: A model or test failed.
            OSError: The tested warehouse could not be published.
        """
        dbt_project = Cfg.DATA_ANALYTICS_DIRECTORY
        load_dotenv(Cfg.BASE_DIRECTORY / '.env', override=False)
        load_dotenv(dbt_project / '.env', override=False)

        silver = Cfg.SILVER_DATABASE_FILE
        gold = Cfg.GOLD_DATABASE_FILE
        if Cfg.DATA_DIRECTORY == Cfg.BASE_DIRECTORY / 'data':
            silver = Path(os.getenv('SILVER_DB_PATH') or silver).resolve()
            gold = Path(os.getenv('GOLD_DB_PATH') or gold).resolve()
        if not silver.is_file():
            raise FileNotFoundError(f'Silver database not found: {silver}')
        if silver == gold:
            raise ValueError('Silver and Gold require separate paths.')

        Cfg.SCRATCH_DIRECTORY.mkdir(parents=True, exist_ok=True)
        gold.parent.mkdir(parents=True, exist_ok=True)
        with TemporaryDirectory(dir=Cfg.SCRATCH_DIRECTORY) as temporary:
            stage = Path(temporary)
            draft = stage / gold.name
            self._build_gold(silver, draft, stage)
            move_artifact(draft, gold, replace=True)
        logger.info(f'Validated Gold database published: {gold}')

    def run_update(self) -> None:
        """Process changed reports and publish the validated warehouse pair.

        Args:
            None.

        Returns:
            None.

        Raises:
            ValueError: An input is missing or fails validation.
            OSError: A candidate or pointer could not be published.
            duckdb.Error: The Silver load failed or another update is active.
            subprocess.CalledProcessError: The dbt build failed.
        """
        update_warehouse(self.pipeline.transformer_controller, self._build_gold)

    @staticmethod
    def _build_gold(silver: Path, draft: Path, stage: Path) -> None:
        """Run dbt on explicit candidate paths.

        Args:
            silver: Silver database to attach read-only.
            draft: Output path of the Gold build.
            stage: Temporary directory for dbt logs and target files.

        Returns:
            None.

        Raises:
            FileNotFoundError: The dbt project is missing.
            subprocess.CalledProcessError: The dbt build failed.
        """
        dbt_project = Cfg.DATA_ANALYTICS_DIRECTORY
        if not dbt_project.is_dir():
            raise FileNotFoundError(f'dbt project not found: {dbt_project}')
        env = os.environ.copy()
        env.update({
            'SILVER_DB_PATH': str(silver),
            'GOLD_DB_PATH': str(draft),
            'PYTHONUTF8': '1',
            'PYTHONIOENCODING': 'utf-8',
        })
        subprocess.run(
            [
                'uv', 'run', '--project', str(Cfg.BASE_DIRECTORY), '--locked',
                'dbt', 'build', '--project-dir', str(dbt_project),
                '--profiles-dir', str(dbt_project),
                '--target-path', str(stage / 'target'),
                '--log-path', str(stage / 'logs'),
            ],
            cwd=dbt_project,
            env=env,
            check=True,
        )
