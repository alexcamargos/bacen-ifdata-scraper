"""This script performs a comprehensive audit of the SICOOB Credijequitinhonha institution's financial summary data
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

# SICOOB Credijequitinhonha Metadata
INSTITUTION_ID = 71243034
DATES = [20221201, 20231201, 20241201]


def get_source_data(date_id: int) -> dict | None:
    """Reads the source CSV for a given date_id (YYYYMMDD) and returns the SICOOB row.
    Scans files to handle naming mismatches in historical data.

    Args:
        date_id (int): The date identifier in the format YYYYMMDD.

    Returns:
        dict | None: A dictionary of the source data for SICOOB, or None if not found.
    """

    target_date_str = f"{str(date_id)[:4]}-{str(date_id)[4:6]}-01"

    # Try the most likely file first
    likely_file = TRANSFORMED_DIR / f"{str(date_id)[:4]}-{str(date_id)[4:6]}.csv"
    files_to_check = [likely_file] if likely_file.exists() else []

    # Add adjacent months to check if not found (historical shifts)
    all_files = list(TRANSFORMED_DIR.glob("*.csv"))
    files_to_check.extend([f for f in all_files if f != likely_file])

    for file_path in files_to_check:
        try:
            # Quick check for date base in the first row
            df_sample = pd.read_csv(file_path, nrows=1)
            if df_sample.empty:
                continue

            file_date = str(df_sample['data_base'].iloc[0])
            if target_date_str in file_date:
                df = pd.read_csv(file_path)
                row = df[df['codigo'].astype(float).astype(int) == INSTITUTION_ID]
                if not row.empty:
                    logger.info(f"Found {target_date_str} in {file_path.name}")
                    return row.iloc[0].to_dict()
        except (FileNotFoundError, pd.errors.ParserError, KeyError):
            continue

    logger.warning(f"Could not find source data for {target_date_str} in any CSV.")

    return None


def main():
    """Main function to execute the audit."""

    if not Cfg.GOLD_DATABASE_FILE.exists():
        logger.error(f"Gold DB not found at {Cfg.GOLD_DATABASE_FILE}")
        return

    gold_db_connection = duckdb.connect(str(Cfg.GOLD_DATABASE_FILE), read_only=True)

    try:
        # 1. Fetch Gold Data
        logger.info(f"Fetching Gold data for SICOOB (Code: {INSTITUTION_ID})...")

        report_query = f"""
            SELECT 
                t.data as data_base,
                i.nome as instituicao,
                f.*
            FROM
                fato_capital_prudencial f
            JOIN dim_instituicao i ON f.id_instituicao = i.id_instituicao
            JOIN dim_tempo t ON f.id_data = t.id_data
            WHERE
                i.codigo_origem = {INSTITUTION_ID} AND f.id_data IN ({','.join(map(str, DATES))})
            ORDER BY f.id_data ASC
        """

        gold_df = gold_db_connection.execute(report_query).fetch_df()

        if gold_df.empty:
            logger.error(f"No Gold data found for SICOOB in dates {DATES}")
            return

        # 2. Perform Comparison
        logger.info("Comparing Gold results with Source CSVs (In-Memory)...")

        field_map = {
            "capital_principal_para_comparacao_com_rwa": "capital_principal",
            "capital_complementar": "capital_complementar",
            "patrimonio_referencia_nivel_i_para_comparacao_com_rwa": "pr_nivel_1",
            "capital_nivel_ii": "capital_nivel_2",
            "patrimonio_referencia_para_comparacao_com_rwa": "pr_total",
            "ativos_ponderados_pelo_risco_rwa": "rwa_total",
            "indice_basileia": "indice_basileia",
        }

        logger.info("SICOOB CREDIJEQUITINHONHA CAPITAL AUDIT: GOLD vs SOURCE")
        logger.info(f"Institution Code: {INSTITUTION_ID}")

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
                gold_value = 0.0 if pd.isna(gold_value) else gold_value

                # Compare with a tolerance for floating point discrepancies.
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
            logger.info("AUDIT PASSED: Perfect parity across all monitored capital accounts.")

    except duckdb.Error as error:
        logger.error(f"Error executing audit: {error}")
    finally:
        gold_db_connection.close()


if __name__ == "__main__":
    main()
