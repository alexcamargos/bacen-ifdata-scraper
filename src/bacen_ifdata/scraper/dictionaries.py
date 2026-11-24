"""Download the official current IF.data column dictionaries.

Args:
    None.
Returns:
    None.
Raises:
    None.
"""

import json
from concurrent.futures import ThreadPoolExecutor
from hashlib import sha256
from http.client import HTTPException
from pathlib import Path
from tempfile import TemporaryDirectory
from urllib.parse import urlencode
from urllib.request import urlopen

from loguru import logger

from bacen_ifdata.scraper.catalog import HistoricalReport, historical_reports
from bacen_ifdata.scraper.exceptions import IfDataScraperException
from bacen_ifdata.scraper.storage.processing import move_artifact
from bacen_ifdata.utilities.configurations import Config

PDF_ENDPOINT = 'https://www3.bcb.gov.br/ifdata/rest/pdf'
METADATA_ENDPOINT = 'https://www3.bcb.gov.br/ifdata/rest/arquivos'


def _metadata_fallback(target: HistoricalReport) -> tuple[str, bytes]:
    """Retrieve the portal's structured definitions when its PDF is absent.

    Args:
        target: Report tied to the current dictionary endpoint.
    Returns:
        Primary metadata URL and UTF-8 JSON containing official definitions.
    Raises:
        ValueError: The portal did not return usable JSON.
        OSError: An official metadata file could not be retrieved.
        KeyError: The returned metadata lacks a required field.
    """
    pdf_file = target.pdf_file or ''
    directory = pdf_file.rsplit('/', 1)[0]
    month = target.period.replace('-', '')
    names = (
        f"{pdf_file.removesuffix('_0.pdf')}.json",
        f'{directory}/info{month}.json',
    )
    urls = [
        METADATA_ENDPOINT + '?' + urlencode({'nomeArquivo': name})
        for name in names
    ]
    with urlopen(urls[0], timeout=Config.TIMEOUT) as response:
        report = json.load(response)
    with urlopen(urls[1], timeout=Config.TIMEOUT) as response:
        fields = json.load(response)
    if report['id'] != target.report_id:
        raise ValueError(f'Unexpected report metadata: {urls[0]}')
    ids = {column['ifd'] for column in report['c']}
    definitions = [field for field in fields if field['id'] in ids]
    if not definitions:
        raise ValueError(f'No column definitions in {urls[1]}')
    document = {
        'fontes': urls,
        'relatorio': report,
        'campos': definitions,
    }
    contents = json.dumps(document, ensure_ascii=False, indent=2)
    return urls[0], (contents + '\n').encode('utf-8')


def _download_pdf(
    target: HistoricalReport, root: Path, scratch: Path,
) -> dict[str, str | int]:
    """Save the official PDF or its structured column definitions.

    Args:
        target: Published catalog selection with a PDF identifier.
        root: Documentation directory for the current layouts.
        scratch: Directory used to stage the complete file.
    Returns:
        Relative path, digest and official URL for the manifest.
    Raises:
        IfDataScraperException: The source did not deliver a valid PDF.
        OSError: The PDF could not be read or saved.
        ValueError: The structured column definitions are invalid.
    """
    if not target.pdf_file:
        raise IfDataScraperException(f'Missing PDF source for {target}.')
    query = urlencode({'nomeArquivo': target.pdf_file})
    url = f'{PDF_ENDPOINT}?{query}'
    relative = (
        Path(target.period) / target.institution.name.lower()
        / f'{target.report.name.lower()}.pdf'
    )
    pdf_url = url
    file_format = 'pdf'
    for attempt in (1, 2):
        try:
            with urlopen(url, timeout=Config.TIMEOUT) as response:
                contents = response.read()
            if not (
                contents.startswith(b'%PDF-')
                and contents.rstrip().endswith(b'%%EOF')
            ):
                raise IfDataScraperException(f'Invalid PDF received: {url}')
        except (IfDataScraperException, OSError, HTTPException) as error:
            if attempt == 2:
                if not isinstance(error, IfDataScraperException):
                    raise
                url, contents = _metadata_fallback(target)
                relative = relative.with_suffix('.json')
                file_format = 'json'
                logger.warning(f'PDF unavailable, saved metadata: {relative}')
                break
            logger.warning(f'Retrying PDF {relative}: {error}')
        else:
            break
    checksum = sha256(contents).hexdigest()
    destination = root / relative
    if not destination.is_file() or destination.read_bytes() != contents:
        destination.parent.mkdir(parents=True, exist_ok=True)
        with TemporaryDirectory(dir=scratch) as temporary:
            stage = Path(temporary) / destination.name
            stage.write_bytes(contents)
            move_artifact(stage, destination, replace=True)
    return {
        'path': relative.as_posix(), 'url': url, 'sha256': checksum,
        'format': file_format, 'pdf_url': pdf_url,
        'institution_id': target.institution_id, 'report_id': target.report_id,
    }


def download_dictionaries(
    *, period: str | None = None, institution: str | None = None,
    report: str | None = None,
) -> None:
    """Collect current dictionaries and update the source manifest.

    Args:
        period: Optional YYYY-MM reference month.
        institution: Optional name of an institutional scope.
        report: Optional name of a report.
    Returns:
        None.
    Raises:
        ValueError: No published report matches the selection.
        IfDataScraperException: At least one PDF could not be downloaded.
        OSError: A local artifact could not be published.
    """
    targets = [
        item for item in historical_reports(Config.TIMEOUT, current=True)
        if (period is None or item.period == period)
        and (
            institution is None or item.institution.name == institution.upper()
        )
        and (report is None or item.report.name == report.upper())
    ]
    if not targets:
        raise ValueError('No IF.data dictionaries match the selection.')
    root = (
        Config.BASE_DIRECTORY / 'docs' / 'dicionario_dados' / '2025_em_diante'
    )
    scratch = Config.SCRATCH_DIRECTORY
    scratch.mkdir(parents=True, exist_ok=True)
    manifest_path = root / 'manifesto.json'
    manifest = {}
    if manifest_path.is_file():
        manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
    failures = []
    with ThreadPoolExecutor(max_workers=4) as executor:
        jobs = {
            target: executor.submit(_download_pdf, target, root, scratch)
            for target in targets
        }
        for target, job in jobs.items():
            try:
                document = job.result()
            except (
                IfDataScraperException, OSError, HTTPException, KeyError,
                TypeError, ValueError,
            ) as error:
                logger.warning(f'Failed dictionary {target.pdf_file}: {error}')
                failures.append(target.pdf_file or target.period)
            else:
                manifest.pop(
                    Path(str(document['path'])).with_suffix(
                        '.json' if document['format'] == 'pdf' else '.pdf'
                    ).as_posix(),
                    None,
                )
                manifest[str(document['path'])] = document
    if manifest:
        with TemporaryDirectory(dir=scratch) as temporary:
            stage = Path(temporary) / manifest_path.name
            stage.write_text(
                json.dumps(manifest, indent=2, sort_keys=True) + '\n',
                encoding='utf-8',
            )
            move_artifact(stage, manifest_path, replace=True)
    logger.info(
        f'IF.data dictionaries: {len(targets) - len(failures)} acquired.'
    )
    if failures:
        raise IfDataScraperException('\n'.join(failures))
