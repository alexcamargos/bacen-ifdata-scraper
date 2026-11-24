"""Read the catalogs published by the IF.data portals.

Args:
    None.
Returns:
    None.
Raises:
    None.
"""

import json
from dataclasses import dataclass
from enum import StrEnum
from gzip import decompress
from http.client import HTTPException
from time import sleep
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen
from zlib import error as ZlibError

from loguru import logger

from bacen_ifdata.scraper.exceptions import IfDataScraperException
from bacen_ifdata.scraper.institutions import InstitutionType
from bacen_ifdata.scraper.reports import CURRENT_ONLY_REPORTS, REPORTS
from bacen_ifdata.scraper.storage.collection import PERIOD
from bacen_ifdata.utilities.configurations import Config


@dataclass(frozen=True, slots=True)
class HistoricalReport:
    """Identify one published export in the historical layout.

    Args:
        period: Reference month in YYYY-MM format.
        institution: Local institutional scope.
        report: Local report type.
        institution_id: Institutional scope ID in the portal.
        report_id: Report ID in the portal.
        data_files: Names of all source data files for the period.
        source_url: Current portal URL, or None for the historical portal.
    Returns:
        The report selection.
    Raises:
        None.
    """

    period: str
    institution: InstitutionType
    report: StrEnum
    institution_id: int
    report_id: int
    data_files: tuple[str, ...]
    source_url: str | None = None


def _read_catalog(timeout: int, url: str | None = None) -> list[dict]:
    """Fetch the source catalog with a bounded retry for transport errors.

    Args:
        timeout: Network timeout in seconds.
        url: Catalog endpoint. Defaults to the historical catalog.
    Returns:
        A catalog entry for each published month.
    Raises:
        IfDataScraperException: The catalog could not be fetched or decoded.
    """
    url = url or Config.HISTORICAL_CATALOG
    request = Request(url, headers={'Accept-Encoding': 'gzip'})
    for attempt in (1, 2):
        try:
            with urlopen(request, timeout=timeout) as response:
                payload = response.read()
                if response.headers.get('Content-Encoding') == 'gzip':
                    payload = decompress(payload)
                entries = json.loads(payload)
        except (OSError, EOFError, HTTPException, ValueError, ZlibError) as error:
            retryable = isinstance(
                error,
                (
                    URLError, TimeoutError, ConnectionError, EOFError,
                    HTTPException, ZlibError,
                ),
            )
            if isinstance(error, HTTPError):
                retryable = error.code in {408, 500, 502, 503, 504}
            if not retryable or attempt == 2:
                raise IfDataScraperException(
                    f'Could not read {url}: {error}'
                ) from error
            logger.warning(f'Retrying IF.data catalog {url}: {error}')
            sleep(1)
            continue

        break

    if not isinstance(entries, list) or not entries:
        raise IfDataScraperException(f'IF.data catalog is empty: {url}.')
    return entries


def historical_reports(
    timeout: int, *, current: bool = False,
) -> list[HistoricalReport]:
    """Resolve supported targets by month from the published catalog.

    Args:
        timeout: Network timeout in seconds.
        current: Read the catalog for data from 2025 onward.
    Returns:
        Exports ordered by descending month, scope and report ID.
    Raises:
        IfDataScraperException: The catalog is unavailable or inconsistent.
    """
    extra_reports = CURRENT_ONLY_REPORTS if current else {}
    supported = {
        ' '.join(institution.value.split()).casefold(): (
            institution,
            {
                ' '.join(report.value.split()).casefold(): report
                for report in (
                    *reports,
                    *extra_reports.get(institution, ()),
                )
            },
        )
        for institution, reports in REPORTS.items()
    }
    entries = (
        _read_catalog(timeout, Config.CURRENT_CATALOG)
        if current else _read_catalog(timeout)
    )
    source_url = Config.CURRENT_URL if current else None
    selections = {}
    try:
        for entry in entries:
            date = str(entry['dt'])
            period = f'{date[:4]}-{date[4:]}'
            if (
                not PERIOD.fullmatch(period)
                or (period > Config.HISTORICAL_END) != current
            ):
                raise ValueError(f'unexpected reference month {date}')

            files = entry['files']
            data_files = tuple(
                file['f'] for file in files
                if file['f'].rsplit('/', 1)[-1].startswith('dados')
            )
            scopes = {
                scope['id']: supported.get(
                    ' '.join(scope['n'].split()).casefold()
                )
                for file in files for scope in file.get('sel', [])
            }
            for file in files:
                definition = file.get('trel')
                if definition is None:
                    continue
                name = ' '.join(definition['n'].split()).casefold()
                for scope in definition['s']:
                    scope_id = scope['id']
                    target = scopes.get(scope_id)
                    if target is None:
                        continue
                    institution, reports = target
                    report = reports.get(name)
                    if report is None:
                        continue
                    key = (period, institution, report)
                    if key in selections or not data_files:
                        raise ValueError(f'invalid source selection for {key}')
                    selections[key] = HistoricalReport(
                        period, institution, report, scope_id,
                        definition['id'], data_files, source_url,
                    )
    except (AttributeError, KeyError, TypeError, ValueError) as error:
        raise IfDataScraperException(
            f'Invalid IF.data catalog for {source_url or Config.URL}: {error}'
        ) from error
    if not selections:
        raise IfDataScraperException(
            f'No known reports in catalog for {source_url or Config.URL}.'
        )
    return sorted(
        selections.values(),
        key=lambda target: (
            target.period, target.institution_id, target.report_id,
        ),
        reverse=True,
    )
