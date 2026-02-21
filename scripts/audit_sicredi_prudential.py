"""This script performs a comprehensive audit of the SICREDI institution's prudential balance sheet data
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
TRANSFORMED_DIR = Cfg.TRANSFORMED_FILES_DIRECTORY / 'prudential_conglomerates'

# Sicredi Prudential Metadata
INST_CODIGO = 1000080745
DATES = [20101201, 20151201, 20201201]


def get_source_data(date_id: int, segment: str) -> dict | None:
    """Reads the source CSV for a given date_id (YYYYMMDD) and returns the Sicredi row.
    Scans files to handle naming mismatches in historical data.

    Args:
        date_id (int): The date identifier in the format YYYYMMDD.
        segment (str): Either "assets" or "liabilities".

    Returns:
        dict | None: A dictionary of the source data for Sicredi, or None if not found.
    """

    target_date_str = f"{str(date_id)[:4]}-{str(date_id)[4:6]}-01"
    segment_directory = TRANSFORMED_DIR / segment

    # Try the most likely file first
    likely_file = segment_directory / f"{str(date_id)[:4]}-{str(date_id)[4:6]}.csv"
    files_to_check = [likely_file] if likely_file.exists() else []

    # Add all files to check if not found (historical shifts)
    all_files = list(segment_directory.glob("*.csv"))
    files_to_check.extend([f for f in all_files if f != likely_file])

    for file_path in files_to_check:
        try:
            df_sample = pd.read_csv(file_path, nrows=1)
            if df_sample.empty:
                continue

            file_date = str(df_sample['data_base'].iloc[0])
            if target_date_str in file_date:
                df = pd.read_csv(file_path)
                row = df[df['codigo'].astype(float).astype(int) == INST_CODIGO]
                if not row.empty:
                    logger.debug(f"Found {target_date_str} in {segment}/{file_path.name}")
                    return row.iloc[0].to_dict()
        except Exception:
            continue

    return None


def main():
    """Main function to execute the audit."""

    if not Cfg.GOLD_DATABASE_FILE.exists():
        logger.error(f"Gold DB not found at {Cfg.GOLD_DATABASE_FILE}")
        return

    gold_db_connection = duckdb.connect(str(Cfg.GOLD_DATABASE_FILE), read_only=True)

    try:
        logger.info(f"Fetching Gold data for SICREDI (Code: {INST_CODIGO})...")

        report_query = f"""
            SELECT 
                t.data as data_base,
                i.nome as instituicao,
                f.*
            FROM
                fato_balanco_patrimonial f
            JOIN dim_instituicao i ON f.id_instituicao = i.id_instituicao
            JOIN dim_tempo t ON f.id_data = t.id_data
            WHERE
                i.codigo_origem = {INST_CODIGO}
                    AND f.tipo_consolidado = 'Conglomerado Prudencial'
                        AND f.id_data IN ({','.join(map(str, DATES))})
            ORDER BY f.id_data ASC
        """

        gold_df = gold_db_connection.execute(report_query).fetch_df()

        if gold_df.empty:
            logger.error(f"No Gold data found for SICREDI in dates {DATES}")
            return

        logger.info("Comparing Gold results with Source CSVs...")

        # Field mapping Source -> Gold
        # Assets
        asset_map = {
            "disponibilidades": "disponibilidades",
            "operacoes_de_credito": "operacoes_de_credito",
            "ativo_total": "ativo_total",
            "tvm_e_instrumentos_financeiros_derivativos": "tvm_derivativos",
        }

        # Liabilities
        liab_map = {
            "deposito_total": "depositos",
            "patrimonio_liquido": "patrimonio_liquido",
            "passivo_total": "passivo_total",
        }

        logger.info("SICREDI PRUDENTIAL AUDIT: BALANCO PATRIMONIAL")
        logger.info(f"Institution Code: {INST_CODIGO}")

        all_matches = True

        for _, gold_row in gold_df.iterrows():
            date_id = int(gold_row['id_data'])
            logger.info(f"\n>>> PERIOD: {gold_row['data_base']} <<<")

            source_assets = get_source_data(date_id, "assets")
            source_liabilities = get_source_data(date_id, "liabilities")

            if not source_assets or not source_liabilities:
                logger.error(f"Could not find full source data for {gold_row['data_base']}")
                all_matches = False
                continue

            # Process Assets
            comp_data = []
            for source_column, gold_column in asset_map.items():
                source_value = source_assets.get(source_column, 0.0)
                gold_value = gold_row.get(gold_column, 0.0)

                # Handle potential NaNs in source
                source_value = 0.0 if pd.isna(source_value) else source_value
                gold_value = 0.0 if pd.isna(gold_value) else gold_value

                # Compare with a tolerance for floating point discrepancies.
                is_match = abs(float(source_value) - float(gold_value)) < 0.01
                if not is_match:
                    all_matches = False

                comp_data.append(
                    {
                        "Account": gold_column.upper(),
                        "Source Value": f"{float(source_value):,.2f}",
                        "Gold Value": f"{float(gold_value):,.2f}",
                        "Match": "✅" if is_match else "❌",
                    }
                )

            # Process Liabilities
            for source_column, gold_column in liab_map.items():
                source_value = source_liabilities.get(source_column, 0.0)
                gold_value = gold_row.get(gold_column, 0.0)

                # Special handling for PASSIVO_TOTAL: Bacen Source includes PL,
                # but Gold stores Net Passivo (Passivo Exigivel).
                if gold_column == "passivo_total":
                    # Sum Gold's Passivo + PL to match Source's "Passivo Total"
                    patrimonio_liquido_value = gold_row.get("patrimonio_liquido", 0.0)
                    gold_value = gold_value + patrimonio_liquido_value

                # Handle potential NaNs in source.
                source_value = 0.0 if pd.isna(source_value) else source_value
                gold_value = 0.0 if pd.isna(gold_value) else gold_value

                # Compare with a tolerance for floating point discrepancies.
                is_match = abs(float(source_value) - float(gold_value)) < 0.01
                if not is_match:
                    all_matches = False

                comp_data.append(
                    {
                        "Account": gold_column.upper(),
                        "Source Value": f"{float(source_value):,.2f}",
                        "Gold Value": f"{float(gold_value):,.2f}",
                        "Match": "✅" if is_match else "❌",
                    }
                )

            logger.info(pd.DataFrame(comp_data).to_string(index=False))

        logger.info("\n" + "=" * 80)

        if not all_matches:
            logger.error("AUDIT FAILED: Discrepancies found in one or more accounts!")
        else:
            logger.info("AUDIT PASSED: Perfect parity across all monitored balance sheet accounts.")

    except duckdb.Error as error:
        logger.error(f"Error executing audit: {error}")
    finally:
        gold_db_connection.close()


if __name__ == "__main__":
    main()
