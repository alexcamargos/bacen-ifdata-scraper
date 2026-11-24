"""Cache structural validation for unchanged originals in scratch.

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
from tempfile import TemporaryDirectory

from loguru import logger

from bacen_ifdata.scraper.exceptions import IfDataScraperException
from bacen_ifdata.scraper.storage.collection import validate_report_csv
from bacen_ifdata.scraper.storage.processing import move_artifact

# Increment when the structural CSV validation rules change.
CACHE_VERSION = 1


class ValidationCache:
    """Remember valid CSVs without writing to the raw layer.

    Args:
        root: Raw data directory to index.
        scratch: Directory allowed to contain disposable data.
    Returns:
        A validation cache for the raw data directory.
    Raises:
        None.
    """

    def __init__(self, root: Path, scratch: Path) -> None:
        """Load available validation records for one raw directory.

        Args:
            root: Raw data directory to index.
            scratch: Directory allowed to contain disposable data.
        Returns:
            None.
        Raises:
            None.
        """
        self._root = root
        identity = sha256(str(root.resolve()).encode()).hexdigest()[:16]
        self._file = scratch / f'ifdata-csv-validation-{identity}.json'
        self._records = {}
        self._changed = False
        try:
            records = json.loads(self._file.read_text(encoding='utf-8'))
            if records.get('version') == CACHE_VERSION:
                self._records = records['files']
                if not isinstance(self._records, dict):
                    raise ValueError('Invalid validation entries.')
        except FileNotFoundError:
            logger.debug(f'No CSV validation cache at {self._file}.')
        except (AttributeError, KeyError, OSError, ValueError) as error:
            self._records = {}
            logger.warning(f'Could not read CSV validation cache: {error}')

    def _signature(self, path: Path, period: str) -> list[int | str]:
        """Get the file identity and timestamps for a cached validation.

        Args:
            path: Active raw CSV.
            period: Reference month in YYYY-MM format.
        Returns:
            The attributes that identify the validated file revision.
        Raises:
            OSError: The original is inaccessible.
        """
        stat = path.stat()
        return [
            stat.st_dev, stat.st_ino, stat.st_size, stat.st_mtime_ns,
            stat.st_ctime_ns, period,
        ]

    def validate(
        self, path: Path, period: str, *, force: bool = False,
    ) -> None:
        """Validate the dated file unless its validation is still current.

        Args:
            path: Active raw CSV.
            period: Reference month in YYYY-MM format.
            force: Read the original even if it matches the cached signature.
        Returns:
            None.
        Raises:
            IfDataScraperException: The CSV is invalid or changed mid-read.
            OSError: The original is inaccessible.
        """
        key = path.relative_to(self._root).as_posix()
        signature = self._signature(path, period)
        if self._records.get(key) == signature and not force:
            return
        year, month = period.split('-')
        try:
            validate_report_csv(path, f'{month}/{year}')
            if signature != self._signature(path, period):
                raise IfDataScraperException(f'Original changed: {path}')
        except (IfDataScraperException, OSError):
            if key in self._records:
                del self._records[key]
                self._changed = True
            raise
        if self._records.get(key) != signature:
            self._records[key] = signature
            self._changed = True

    def remember(self, path: Path, period: str) -> None:
        """Record the signature of a just-validated published original.

        Args:
            path: Published CSV that the collector validated before commit.
            period: Reference month in YYYY-MM format.
        Returns:
            None.
        Raises:
            None.
        """
        try:
            key = path.relative_to(self._root).as_posix()
            self._records[key] = self._signature(path, period)
            self._changed = True
        except OSError as error:
            logger.warning(f'Could not cache validation for {path}: {error}')

    def save(self) -> None:
        """Persist validated entries together with an atomic replacement.

        Args:
            None.
        Returns:
            None.
        Raises:
            None.
        """
        if not self._changed:
            return
        try:
            self._file.parent.mkdir(parents=True, exist_ok=True)
            with TemporaryDirectory(dir=self._file.parent) as stage:
                draft = Path(stage) / self._file.name
                draft.write_text(json.dumps({
                    'version': CACHE_VERSION,
                    'files': self._records,
                }), encoding='utf-8')
                move_artifact(draft, self._file, replace=True)
        except OSError as error:
            logger.warning(f'Could not save CSV validation cache: {error}')
