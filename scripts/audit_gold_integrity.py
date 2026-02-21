"""Check data integrity between Bronze, Silver, and Gold layers of the Bacen IFData project."""

import argparse
import os
import sys
import tempfile
from pathlib import Path
from typing import Dict

import duckdb
from loguru import logger

# pylint: disable=wrong-import-position
# Add the project root to the sys.path to allow absolute imports
project_root = Path(__file__).resolve().parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.bacen_ifdata.utilities.configurations import Config as Cfg


def get_bronze_row_counts() -> Dict[str, int]:
    """Scans the data/processed directory to count rows in CSV files (Bronze Layer).

    Maps folder structure to Silver table names.

    Returns:
        Dict[silver_table_name, row_count]
    """

    logger.info("Scanning Bronze Layer (CSVs) for row counts...")

    # Mapping heuristic: folder/subfolder -> table_name
    # Example: financial_conglomerates/assets -> financial_conglomerates_assets
    counts = {}
    for root, _, files in os.walk(Cfg.PROCESSED_FILES_DIRECTORY):
        csv_files = [file for file in files if file.endswith('.csv')]
        if not csv_files:
            continue

        relative_directory_path = Path(root).relative_to(Cfg.PROCESSED_FILES_DIRECTORY)
        # Construct table name from path parts
        # e.g., financial_conglomerates \ assets -> financial_conglomerates_assets
        table_name = "_".join(relative_directory_path.parts).replace("-", "_")

        total_rows = 0
        for csv_file in csv_files:
            file_path = Path(root) / csv_file
            try:
                # Count lines minus header
                with open(file_path, 'rb') as file:
                    lines = sum(1 for _ in file)
                if lines > 0:
                    total_rows += lines - 1  # Subtract header
            except IOError as error:
                logger.error(f"IOError reading {file_path}: {error}")
            except Exception as error:  # pylint: disable=broad-except
                logger.error(f"Error reading {file_path}: {error}")

        counts[table_name] = total_rows

    return counts


def check_bronze_silver_integrity(silver_db_connection: duckdb.DuckDBPyConnection) -> bool:
    """Compares Bronze CSV row counts with Silver DuckDB table row counts.

    Logs results and returns True if all counts match, False otherwise.

    Args:
        silver_db_connection (duckdb.DuckDBPyConnection): Connection to the Silver DuckDB database.

    Returns:
        bool: True if all counts match, False otherwise.
    """

    logger.info(" Starting Bronze vs Silver Integrity Check ")

    bronze_counts = get_bronze_row_counts()

    # Get Silver tables
    silver_tables = silver_db_connection.execute("SHOW TABLES").fetchall()
    silver_table_names = [t[0] for t in silver_tables]

    success = True
    for table, bronze_count in bronze_counts.items():
        if table not in silver_table_names:
            logger.warning(f"[SKIP] Table '{table}' found in Bronze but not in Silver DB.")
            continue

        row = silver_db_connection.execute(f"SELECT COUNT(*) FROM {table}").fetchone()
        if not row:
            logger.warning(f"[SKIP] Table '{table}' exists in Bronze but is empty or inaccessible in Silver DB.")
            continue

        silver_count = row[0]

        if bronze_count == silver_count:
            logger.info(f"[PASS] {table}: Bronze={bronze_count}, Silver={silver_count}")
        else:
            logger.error(
                f"[FAIL] {table}: Bronze={bronze_count}, Silver={silver_count} (Diff: {silver_count - bronze_count})"
            )
            success = False

    return success


def check_silver_gold_integrity(
    silver_db_connection: duckdb.DuckDBPyConnection, gold_db_connection: duckdb.DuckDBPyConnection
) -> bool:
    """Compares Aggregated Sums between Silver and Gold layers, segmented by type.

    For each segment (Prudential Conglomerates, Financial Conglomerates, Individual Institutions):
    - Calculate the sum of 'ativo_total' from the Silver table (source).
    - Calculate the sum of 'ativo_total' from the Gold fact table for the corresponding 'tipo_consolidado' (target).
    - Logs results and returns True if all segments match within a reasonable tolerance, False otherwise.

    Args:
        silver_db_connection (duckdb.DuckDBPyConnection): Connection to the Silver DuckDB database.
        gold_db_connection (duckdb.DuckDBPyConnection): Connection to the Gold DuckDB database.

    Returns:
        bool: True if all segments match, False otherwise.
    """

    logger.info("\n Starting Segmented Silver vs Gold Integrity Check ")

    segments = [
        {
            "name": "Prudential Conglomerates",
            "silver_table": "prudential_conglomerates_assets",
            "gold_type": "Conglomerado Prudencial",
        },
        {
            "name": "Financial Conglomerates",
            "silver_table": "financial_conglomerates_assets",
            "gold_type": "Conglomerado Financeiro",
        },
        {
            "name": "Individual Institutions",
            "silver_table": "individual_institutions_assets",
            "gold_type": "Instituicao Individual",
        },
    ]

    all_passed = True
    for segment in segments:
        logger.info(f"Checking Segment: {segment['name']}")

        # Silver Sum (Source)
        try:
            silver_query = f"""
                SELECT
                    SUM(ativo_total) 
                FROM (
                    SELECT ativo_total 
                    FROM {segment['silver_table']} 
                    QUALIFY ROW_NUMBER() OVER (PARTITION BY codigo, data_base ORDER BY codigo) = 1
                )
            """

            row = silver_db_connection.execute(silver_query).fetchone()
            if not row:
                logger.warning(f"[SKIP] Silver table '{segment['silver_table']}' is empty or inaccessible.")
                continue

            total_silver_assets = row[0]
        except Exception as e:
            logger.error(f"Error querying Silver {segment['silver_table']}: {e}")
            all_passed = False
            continue

        # Gold Sum (Target)
        gold_query = f"""
            SELECT
                SUM(f.ativo_total) 
            FROM
                fato_balanco_patrimonial f
            WHERE
                f.tipo_consolidado = '{segment['gold_type']}'
        """

        try:
            row = gold_db_connection.execute(gold_query).fetchone()
            if not row:
                logger.warning(f"[SKIP] Gold table for segment '{segment['gold_type']}' is empty or inaccessible.")
                all_passed = False
                continue

            total_gold_assets = row[0]
        except duckdb.Error as error:
            logger.error(f"Error querying Gold for {segment['gold_type']}: {error}")
            all_passed = False
            continue

        total_silver_assets = total_silver_assets or 0.0
        total_gold_assets = total_gold_assets or 0.0
        assets_difference = abs(total_silver_assets - total_gold_assets)

        logger.info(f"  Silver Sum: {total_silver_assets:,.2f}")
        logger.info(f"  Gold Sum:   {total_gold_assets:,.2f}")

        if assets_difference < 10.0:  # Tolerance for rounding/floating point
            logger.info(f"  [PASS] {segment['name']} matches.")
        else:
            logger.error(f"  [FAIL] {segment['name']} MISMATCH! Diff: {assets_difference:,.2f}")
            all_passed = False

    return all_passed


def check_silver_duplicates(silver_db_connection: duckdb.DuckDBPyConnection) -> bool:
    """Checks for duplicates in Silver tables using PK (codigo, data_base).

    Args:
        con_silver (duckdb.DuckDBPyConnection): Connection to the Silver DuckDB database.

    Returns:
        bool: True if no duplicates are found, False otherwise.
    """

    logger.info("\n Checking Silver Duplicates ")

    silver_table = [
        "financial_conglomerates_assets",
        "financial_conglomerates_capital_information",
        "financial_conglomerates_income_statement",
        "financial_conglomerates_liabilities",
        "financial_conglomerates_portfolio_geographic_region",
        "financial_conglomerates_portfolio_indexer",
        "financial_conglomerates_portfolio_individuals_type_maturity",
        "financial_conglomerates_portfolio_legal_person_business_size",
        "financial_conglomerates_portfolio_legal_person_economic_activity",
        "financial_conglomerates_portfolio_legal_person_type_maturity",
        "financial_conglomerates_portfolio_number_clients_operations",
        "financial_conglomerates_portfolio_risk_level",
        "financial_conglomerates_scr_portfolio_geographic_region",
        "financial_conglomerates_scr_portfolio_indexer",
        "financial_conglomerates_scr_portfolio_individuals_type_maturity",
        "financial_conglomerates_scr_portfolio_legal_person_business_size",
        "financial_conglomerates_scr_portfolio_legal_person_economic_activity",
        "financial_conglomerates_scr_portfolio_legal_person_type_maturity",
        "financial_conglomerates_scr_portfolio_number_clients_operations",
        "financial_conglomerates_scr_portfolio_risk_level",
        "financial_conglomerates_summary",
        "foreign_exchange_quarterly_foreign_currency_flow",
        "individual_institutions_assets",
        "individual_institutions_income_statement",
        "individual_institutions_liabilities",
        "individual_institutions_summary",
        "prudential_conglomerates_assets",
        "prudential_conglomerates_capital_information",
        "prudential_conglomerates_income_statement",
        "prudential_conglomerates_liabilities",
        "prudential_conglomerates_segmentation",
        "prudential_conglomerates_summary",
    ]

    has_duplicates = False
    for table in silver_table:
        try:
            # Check for generic table existing
            if not silver_db_connection.execute(f"SELECT 1 FROM {table} LIMIT 1").fetchone():
                continue

            query = f"""
                SELECT
                    count(*) - count(distinct codigo || '_' || data_base) as dups
                FROM {table}
            """

            row = silver_db_connection.execute(query).fetchone()
            if not row:
                logger.warning(
                    f"[SKIP] Could not retrieve duplicate count for {table}. Table may be empty or inaccessible."
                )
                continue

            duplicates = row[0]
            if duplicates > 0:
                logger.warning(f"[WARN] {table} has {duplicates} duplicate primary keys (codigo, data_base).")
                logger.warning(
                    f"Consider reviewing the Silver transformation logic for {table} to ensure proper deduplication."
                )
                has_duplicates = True
            else:
                logger.info(f"[PASS] {table}: No duplicates.")
        except duckdb.Error as error:
            logger.error(f"Error checking duplicates in {table}: {error}")

    return not has_duplicates


def check_gold_duplicates(gold_database_connection: duckdb.DuckDBPyConnection) -> bool:
    """Checks for duplicates in Gold tables using PK (id_instituicao, id_data).

    Args:
        gold_database_connection (duckdb.DuckDBPyConnection): Connection to the Gold DuckDB database.

    Returns:
        bool: True if no duplicates are found, False otherwise.
    """

    logger.info("\nChecking Gold Duplicates")

    total_rows_query = """
        SELECT
            count(*)
        FROM
            fato_balanco_patrimonial
    """

    distinct_rows_query = """
        SELECT
            count(*)
        FROM
            (
                SELECT
                    DISTINCT id_instituicao, id_data, tipo_consolidado
                FROM
                    fato_balanco_patrimonial
            )
    """

    try:
        row = gold_database_connection.execute(total_rows_query).fetchone()
        if not row:
            logger.warning("[SKIP] Could not retrieve total row count for fato_balanco_patrimonial.")
            return False

        total_rows = row[0]

        row = gold_database_connection.execute(distinct_rows_query).fetchone()
        if not row:
            logger.warning("[SKIP] Could not retrieve distinct key count for fato_balanco_patrimonial.")
            return False

        distinct_rows = row[0]
        duplicates = total_rows - distinct_rows

        logger.info(f"Gold Total Rows: {total_rows}")
        logger.info(f"Gold Distinct Keys: {distinct_rows}")

        if duplicates > 0:
            logger.error(f"[FAIL] fato_balanco_patrimonial has {duplicates} duplicate rows!")
            logger.error(f"(Rows: {total_rows}, Distinct Keys: {distinct_rows})")
            return False

        logger.info("[PASS] fato_balanco_patrimonial: No duplicates.")

        return True
    except duckdb.Error as error:
        logger.error(f"Error checking duplicates in Gold: {error}")
        return False


def generate_institution_report(
    gold_db_connection: duckdb.DuckDBPyConnection, institution_id: str, report_type: str
) -> None:
    """Generates a CSV report for a specific institution from the Gold layer.

    Reconstructs the view to mimic the original report.

    Args:
        gold_db_connection (duckdb.DuckDBPyConnection): Connection to the Gold DuckDB database
        institution_id (str): Institution ID (could be id_instituicao or codigo_origem)
        report_type (str): Type of report to generate (e.g., 'summary', 'detailed')
    """

    logger.info(f"\n Generating {report_type} Report for Institution ID: {institution_id} ")

    with tempfile.NamedTemporaryFile(
        mode="w", suffix=f"_report_{institution_id}_{report_type}.csv", delete=False
    ) as output_file:
        if report_type == 'summary':
            # Need to join dim_instituicao to get the name and other details
            # And fato_balanco_patrimonial for the data
            # Note: 'Summary' in Bacen usually means the 'Resumo' report which has different fields.
            # For this PoC, we will export the Balance Sheet (Balanco Patrimonial) as it's the core fact we checked.

            query = f"""
                SELECT 
                    d.ano,
                    d.mes,
                    i.nome as instituicao,
                    f.*,
                    i.tipo_instituicao,
                    i.id_segmento
                FROM
                    fato_balanco_patrimonial f
                JOIN dim_tempo d ON f.id_data = d.id_data
                JOIN dim_instituicao i ON f.id_instituicao = i.id_instituicao
                WHERE
                    f.id_instituicao = '{institution_id}' OR i.codigo_origem = '{institution_id}'
                ORDER BY d.ano DESC, d.mes DESC
            """

            try:
                balance_sheet_df = gold_db_connection.execute(query).fetch_df()
                if balance_sheet_df.empty:
                    logger.warning(f"No data found for Institution ID {institution_id} in Gold DB.")
                else:
                    balance_sheet_df.to_csv(output_file, index=False)
                    logger.info(f"Report saved to: {output_file}")
                    logger.info(f"Sample data from report:\n\n{balance_sheet_df.head()}")
            except duckdb.Error as error:
                logger.error(f"Error generating report: {error}")
        else:
            logger.error(f"Report type '{report_type}' not implemented yet.")


def main():
    """Main function to run the audit checks and optionally generate a report."""

    parser = argparse.ArgumentParser(description="Audit data integrity between Bronze, Silver, and Gold layers.")
    parser.add_argument("--generate-report", type=str, help="Institution ID to generate a report for.")
    parser.add_argument(
        "--report-type", type=str, default="summary", help="Type of report to generate (default: summary)."
    )

    args = parser.parse_args()

    # Connect databases
    if not Cfg.SILVER_DATABASE_FILE.exists():
        logger.error(f"Silver DB not found at {Cfg.SILVER_DATABASE_FILE}")
        return
    if not Cfg.GOLD_DATABASE_FILE.exists():
        logger.error(f"Gold DB not found at {Cfg.GOLD_DATABASE_FILE}")
        return

    silver_db_connection = duckdb.connect(str(Cfg.SILVER_DATABASE_FILE), read_only=True)
    gold_db_connection = duckdb.connect(str(Cfg.GOLD_DATABASE_FILE), read_only=True)

    all_passed = True

    # 1. Bronze vs Silver Check
    if not check_bronze_silver_integrity(silver_db_connection):
        all_passed = False

    # 2. Duplicate Checks
    check_silver_duplicates(silver_db_connection)  # Warn only
    if not check_gold_duplicates(gold_db_connection):
        all_passed = False

    # 3. Silver vs Gold Check (Sums)
    if not check_silver_gold_integrity(silver_db_connection, gold_db_connection):
        all_passed = False

    # 4. Report Generation (Optional)
    if args.generate_report:
        generate_institution_report(gold_db_connection, args.generate_report, args.report_type)

    silver_db_connection.close()
    gold_db_connection.close()

    if not all_passed:
        logger.error("Audit FAILED. See logs for details.")
    else:
        logger.info("Audit PASSED successfully.")


if __name__ == "__main__":
    main()
