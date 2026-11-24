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
OUTPUT_DIR = Path("data/processed/b3s_exports")
OUTPUT_FILE = OUTPUT_DIR / "b3s_resumo_financeiro.parquet"

# SQL Query using DuckDB COPY command
QUERY = f"""
    COPY (
        WITH individuais AS (
            SELECT *
            FROM view_resumo_financeiro_relatorios
            WHERE tipo_relatorio_bcb = 'Instituições Individuais'
              AND tcb = 'b3s'
        ),
        prudenciais AS (
            SELECT codigo_origem, data_base, max(segmento) as segmento_prudencial
            FROM view_resumo_financeiro_relatorios
            WHERE tipo_relatorio_bcb = 'Conglomerados Prudenciais e Instituições Independentes'
            GROUP BY codigo_origem, data_base
        )
        SELECT 
            i.id_instituicao,
            i.id_data,
            i.codigo_origem,
            i.nome_instituicao,
            i.nome_instituicao_historico,
            i.tipo_instituicao,
            i.nome_conglomerado,
            i.tipo_relatorio_bcb,
            COALESCE(i.segmento, p.segmento_prudencial) AS segmento,
            i.cidade,
            i.uf,
            i.regiao,
            i.tipo_de_controle,
            i.tcb,
            i.consolidado_bancario,
            i.data_base,
            i.ativo_total,
            i.carteira_credito,
            i.passivo_exigivel,
            i.captacoes,
            i.patrimonio_liquido,
            i.lucro_liquido,
            i.quantidade_agencias,
            i.quantidade_postos_atendimento,
            i.roe,
            i.roa
        FROM individuais i
        LEFT JOIN prudenciais p 
          ON i.codigo_origem = p.codigo_origem 
         AND i.data_base = p.data_base
    ) TO '{OUTPUT_FILE}' (FORMAT PARQUET);
"""

def export_resumo_financeiro() -> None:
    """Exports the Resumo Financeiro view to a Parquet file.

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
            logger.info(f"Executing export query for Resumo Financeiro...")
            con.execute(QUERY)
            
            # Verify row count written
            df = con.execute(f"SELECT COUNT(*) as row_count FROM '{OUTPUT_FILE}'").df()
            logger.info(f"Export successful. Wrote {df['row_count'][0]} rows to {OUTPUT_FILE}")
            
    except (duckdb.Error, OSError, ValueError, KeyError) as e:
        logger.error(f"Failed to export Resumo Financeiro data: {str(e)}")
        raise

if __name__ == "__main__":
    export_resumo_financeiro()
