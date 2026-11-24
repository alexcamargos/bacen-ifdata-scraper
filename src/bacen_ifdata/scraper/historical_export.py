"""Run the IF.data portals' native CSV export in the browser.

Both portals expose the same report selection and CSV export functions.

Args:
    None.
Returns:
    None.
Raises:
    None.
"""

from base64 import b64decode
from functools import cache
from importlib.resources import files

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait

from bacen_ifdata.scraper.catalog import HistoricalReport
from bacen_ifdata.scraper.exceptions import IfDataScraperException


@cache
def _load_script(name: str) -> str:
    """Wrap a packaged historical portal function for Selenium.

    Args:
        name: Filename of the JavaScript resource.
    Returns:
        Script body that invokes the function with WebDriver arguments.
    Raises:
        OSError: The packaged resource could not be read.
        UnicodeError: The source could not be decoded as UTF-8.
    """
    resource = files('bacen_ifdata.scraper').joinpath(
        'javascript', 'historical', name,
    )
    source = resource.read_text(encoding='utf-8')
    return f'return ({source})(...arguments);'


def export_historical_csv(
    driver: WebDriver,
    target: HistoricalReport,
    timeout: int,
    *,
    reuse: bool,
) -> bytes:
    """Capture the exact native export bytes for one catalog entry.

    Args:
        driver: Firefox session on the portal for the selected reference month.
        target: Catalog IDs and expected data files.
        timeout: Maximum time to wait for each source load, in seconds.
        reuse: Reuse the loaded data for the same period and institution.
    Returns:
        Original CSV, including its BOM and line endings.
    Raises:
        IfDataScraperException: The report is incomplete or cannot be exported.
        WebDriverException: The browser could not load or execute the export.
        OSError: A packaged script resource could not be read.
        UnicodeError: A script could not be decoded as UTF-8.
    """
    wait = WebDriverWait(driver, timeout)
    wait.until(lambda browser: browser.execute_script(
        'return Array.isArray(window.listaRelatorios) && '
        'window.listaRelatorios.length > 0 && '
        'typeof window.selectRelatorio === "function";'
    ))
    month = int(target.period.replace('-', ''))
    selection = (month, target.institution_id, target.report_id)
    reason = driver.execute_script(
        _load_script('select_report.js'),
        *selection, list(target.data_files), reuse,
    )
    if reason:
        raise IfDataScraperException(f'Portal rejected selection: {reason}.')
    status_script = _load_script('report_status.js')
    state = wait.until(lambda browser: browser.execute_script(
        status_script, *selection, len(target.data_files),
    ))
    if state != 'ready':
        raise IfDataScraperException(f'Portal export unavailable: {state}.')

    encoded = driver.execute_async_script(
        _load_script('capture_csv.js'), *selection,
    )
    if not encoded:
        raise IfDataScraperException('The portal did not produce a CSV.')
    try:
        return b64decode(encoded, validate=True)
    except (TypeError, ValueError) as error:
        raise IfDataScraperException('Invalid browser CSV payload.') from error
