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
OUTPUT_FILE = OUTPUT_DIR / "cooperativas_insolventes.csv"

# SQL Query using DuckDB COPY command
QUERY = f"""
    COPY (
        WITH ranked AS (
            SELECT 
                codigo_origem, 
                nome_instituicao, 
                segmento,
                cidade,
                uf,
                regiao,
                tipo_de_controle,
                data_base, 
                patrimonio_liquido, 
                roa, 
                roe, 
                ROW_NUMBER() OVER (PARTITION BY codigo_origem ORDER BY data_base DESC) as rn 
            FROM view_resumo_financeiro_relatorios 
            WHERE tipo_relatorio_bcb = 'Instituições Individuais' 
              AND tcb = 'b3s'
        ),
        recent as (
            SELECT * FROM ranked WHERE rn <= 4
        ),
        analise as (
            SELECT 
                codigo_origem,
                MAX(nome_instituicao) as nome_instituicao,
                MAX(segmento) as segmento,
                MAX(cidade) as cidade,
                MAX(uf) as uf,
                MAX(regiao) as regiao,
                MAX(tipo_de_controle) as tipo_de_controle,
                MAX(data_base) as ultima_data_base,
                -- Check if latest PL is negative
                MIN(CASE WHEN rn = 1 THEN patrimonio_liquido ELSE NULL END) as pl_recente,
                -- Check if ALL of the last 4 quarters were negative ROE or ROA
                SUM(CASE WHEN roa < 0 OR roe < 0 THEN 1 ELSE 0 END) as semestres_negativos_rentabilidade,
                -- Ensure they have 4 quarters of data to be 'persistently' negative
                COUNT(*) as total_trimestres
            FROM recent
            GROUP BY codigo_origem
        )
        SELECT 
            codigo_origem,
            nome_instituicao,
            segmento,
            cidade,
            uf,
            regiao,
            tipo_de_controle,
            ultima_data_base
        FROM analise
        WHERE pl_recente < 0 
           OR (semestres_negativos_rentabilidade = 4 AND total_trimestres = 4)
        ORDER BY ultima_data_base DESC, nome_instituicao
    ) TO '{OUTPUT_FILE}' (FORMAT CSV, HEADER);
"""

def export_cooperativas_insolventes() -> None:
    """Exports the list of insolvent cooperatives to a CSV file.

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
            logger.info("Executing export query for Insolvent Cooperatives...")
            con.execute(QUERY)
            
            # Check row count using pandas to quickly confirm output
            df = con.execute(f"SELECT COUNT(*) as row_count FROM read_csv_auto('{OUTPUT_FILE}')").df()
            logger.info(f"Export successful. Found {df['row_count'][0]} insolvent cooperatives saved to {OUTPUT_FILE}")
            
    except (duckdb.Error, OSError, ValueError, KeyError) as e:
        logger.error(f"Failed to export insolvent cooperatives data: {str(e)}")
        raise

if __name__ == "__main__":
    export_cooperativas_insolventes()
