"""This script performs a comprehensive audit of the BTG Pactual (Individual) institution's financial summary data
in the Gold database against the original source CSV files. It checks all key financial accounts for both the first
and last available dates, ensuring complete parity between Gold and Source.
"""

import sys
from pathlib import Path

import duckdb
import pandas as pd
from loguru import logger

# pylint: disable=wrong-import-position
# Add the project root to the sys.path to allow absolute imports
project_root = Path(__file__).resolve().parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.bacen_ifdata.utilities.configurations import Config as Cfg

# Define the directory where the transformed CSV files are located
TRANSFORMED_DIR = Cfg.TRANSFORMED_FILES_DIRECTORY / 'individual_institutions' / 'summary'

# Define the institution details for BTG Pactual (Individual)
INSTITUTION_NAME = "BANCO BTG PACTUAL S.A."
INSTITUTION_ID = 30306294


def get_source_data(date_id: int) -> dict | None:
    """Reads the source CSV for a given date_id (YYYYMMDD) and returns the BTG row.

    Args:
        date_id (int): The date identifier in the format YYYYMMDD.

    Returns:
        dict | None: A dictionary of the source data for BTG Pactual, or None if not found.
    """

    # Convert 20000301 -> 2000-03
    date_str = str(date_id)
    file_name = f"{date_str[:4]}-{date_str[4:6]}.csv"
    file_path = TRANSFORMED_DIR / file_name

    if not file_path.exists():
        logger.warning(f"Source file not found: {file_path}")
        return None

    try:
        source_dataframe = pd.read_csv(file_path)
        # Always use codigo for comparison to handle name changes
        row = source_dataframe[source_dataframe['codigo'] == INSTITUTION_ID]
        if row.empty:
            return None

        return row.iloc[0].to_dict()
    except (FileNotFoundError, pd.errors.ParserError, KeyError) as error:
        logger.error(f"Error reading source {file_path}: {error}")
        return None


def main():
    """Main function to execute the audit."""

    if not Cfg.GOLD_DATABASE_FILE.exists():
        logger.error(f"Gold DB not found at {Cfg.GOLD_DATABASE_FILE}")
        return

    gold_db_connection = duckdb.connect(str(Cfg.GOLD_DATABASE_FILE), read_only=True)

    try:
        # 1. Get Institution ID and Dates
        logger.info(f"Looking for Gold data for {INSTITUTION_NAME}...")
        meta_query = f"""
        SELECT 
            id_instituicao,
            MIN(id_data) as first_date,
            MAX(id_data) as last_date
        FROM
            fato_resumo_financeiro
        WHERE
            id_instituicao IN (
                SELECT
                    id_instituicao
                FROM
                    dim_instituicao 
                WHERE
                    codigo_origem = {INSTITUTION_ID} AND tipo_instituicao = 'Instituicao Individual'
            )
        GROUP BY id_instituicao
        """

        meta = gold_db_connection.execute(meta_query).fetchone()

        if not meta:
            logger.error(f"Institution {INSTITUTION_NAME} not found in fato_resumo_financeiro.")
            return

        institution_id, first_date, last_date = meta

        # 2. Extract Summary for first and last dates
        report_query = f"""
            SELECT 
                t.data as data_base,
                i.nome as instituicao,
                f.ativo_total,
                f.carteira_credito,
                f.patrimonio_liquido,
                f.lucro_liquido,
                f.quantidade_agencias,
                f.quantidade_postos_atendimento,
                f.id_data
            FROM
                fato_resumo_financeiro f
            JOIN dim_instituicao i ON f.id_instituicao = i.id_instituicao
            JOIN dim_tempo t ON f.id_data = t.id_data
            WHERE
                f.id_instituicao = '{institution_id}' AND f.id_data IN ({first_date}, {last_date})
            ORDER BY f.id_data ASC
        """

        gold_df = gold_db_connection.execute(report_query).fetch_df()

        # 3. Perform Comparison with Source CSVs
        logger.info("Comparing Gold results with Source CSVs for all fields (In-Memory)...")

        # Mapping Source -> Gold
        field_map = {
            "ativo_total": "ativo_total",
            "carteira_de_credito_classificada": "carteira_credito",
            "patrimonio_liquido": "patrimonio_liquido",
            "lucro_liquido": "lucro_liquido",
            "numero_de_agencias": "quantidade_agencias",
            "numero_de_postos_de_atendimento": "quantidade_postos_atendimento",
        }

        logger.info(f"{INSTITUTION_NAME} COMPREHENSIVE AUDIT REPORT: GOLD vs SOURCE")
        logger.info(f"Institution ID: {institution_id}")

        all_matches = True
        for _, gold_row in gold_df.iterrows():
            source_row = get_source_data(int(gold_row['id_data']))
            logger.info(f"\n>>> PERIOD: {gold_row['data_base']} <<<")
            logger.info(f"Source Name: {source_row['instituicao'] if source_row else 'NOT FOUND'}")

            if not source_row:
                logger.error(f"Could not find source data for {gold_row['data_base']}")
                all_matches = False
                continue

            comparison_data = []
            for source_column, gold_column in field_map.items():
                source_value = source_row.get(source_column, 0.0)
                gold_value = gold_row.get(gold_column, 0.0)

                # Handle potential NaNs in source
                source_value = 0.0 if pd.isna(source_value) else source_value

                is_match = abs(float(source_value) - float(gold_value)) < 0.01
                if not is_match:
                    all_matches = False

                comparison_data.append(
                    {
                        "Account": gold_column.upper(),
                        "Source Value": f"{float(source_value):,.2f}",
                        "Gold Value": f"{float(gold_value):,.2f}",
                        "Match": "✅" if is_match else "❌",
                    }
                )

            logger.info(pd.DataFrame(comparison_data).to_string(index=False))

        if not all_matches:
            logger.error("AUDIT FAILED: Discrepancies found in one or more accounts!")
        else:
            logger.info("AUDIT PASSED: Perfect parity across all monitored accounts.")

    except duckdb.Error as error:
        logger.error(f"Error executing audit: {error}")
    finally:
        gold_db_connection.close()


if __name__ == "__main__":
    main()
