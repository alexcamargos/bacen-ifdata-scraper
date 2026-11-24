"""Export IF.data records from the published Gold warehouse.

Args:
    None.

Returns:
    None.

Raises:
    None.
"""

import logging
from pathlib import Path

import duckdb

from bacen_ifdata.utilities.releases import warehouse_path

# Configure styling & logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Output directory and file
OUTPUT_DIR = Path("data/processed")
OUTPUT_FILE = OUTPUT_DIR / "cooperativas_descontinuadas.csv"

# SQL Query using DuckDB COPY command
QUERY = f"""
    COPY (
        WITH global_max as (
            SELECT MAX(data_base) as max_date 
            FROM view_resumo_financeiro_relatorios
        ),
        inst_max as (
            SELECT 
                codigo_origem,
                nome_instituicao,
                segmento,
                cidade,
                uf,
                regiao,
                tipo_de_controle,
                MAX(data_base) as ultima_data_base
            FROM view_resumo_financeiro_relatorios
            WHERE tipo_relatorio_bcb = 'Instituições Individuais'
              AND tcb = 'b3s'
            GROUP BY 
                codigo_origem,
                nome_instituicao,
                segmento,
                cidade,
                uf,
                regiao,
                tipo_de_controle
        )
        SELECT 
            i.codigo_origem,
            i.nome_instituicao,
            i.segmento,
            i.cidade,
            i.uf,
            i.regiao,
            i.tipo_de_controle,
            i.ultima_data_base
        FROM inst_max i
        CROSS JOIN global_max g
        WHERE i.ultima_data_base <= CAST(g.max_date - INTERVAL 6 MONTH AS DATE)
        ORDER BY i.ultima_data_base DESC, i.nome_instituicao
    ) TO '{OUTPUT_FILE}' (FORMAT CSV, HEADER);
"""

def export_cooperativas_descontinuadas() -> None:
    """Exports the list of discontinued cooperatives to a CSV file.

    Args:
        None.

    Returns:
        None.

    Raises:
        duckdb.Error: The warehouse query or export failed.
        OSError: The warehouse or export path could not be accessed.
        ValueError: The release pointer is invalid.
        KeyError: The release pointer is incomplete.
    """
    try:
        # Ensure output directory exists
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        
        gold_path = warehouse_path('gold')
        logger.info("Connecting to DuckDB at %s", gold_path)
        with duckdb.connect(str(gold_path), read_only=True) as con:
            logger.info("Executing export query for Discontinued Cooperatives...")
            con.execute(QUERY)
            
            # Check row count using pandas for simple count via the connection
            df = con.execute(f"SELECT COUNT(*) as row_count FROM read_csv_auto('{OUTPUT_FILE}')").df()
            logger.info(f"Export successful. Found {df['row_count'][0]} discontinued cooperatives saved to {OUTPUT_FILE}")
            
    except (duckdb.Error, OSError, ValueError, KeyError) as e:
        logger.error(f"Failed to export discontinued cooperatives data: {str(e)}")
        raise

if __name__ == "__main__":
    export_cooperativas_descontinuadas()
