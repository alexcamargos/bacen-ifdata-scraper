#!/usr/bin/env python
# encoding: utf-8
#
#  ------------------------------------------------------------------------------
#  Name: transformer.py
#  Version: 0.0.1
#  Summary: Bacen IF.data AutoScraper & Data Manager
#           Este sistema foi projetado para automatizar o download dos
#           relatórios da ferramenta IF.data do Banco Central do Brasil.
#           Criado para facilitar a integração com ferramentas automatizadas de
#           análise e visualização de dados, garantido acesso fácil e oportuno
#           aos dados.
#
#  Author: Alexsander Lopes Camargos
#  Author-email: alcamargos@vivaldi.net
#
#  License: MIT
#  ------------------------------------------------------------------------------

"""
Bacen IF.data AutoScraper & Data Manager

This script is designed to automate the download of reports from the Banco Central do Brasil's
IF.data tool. It facilitates the integration with automated data analysis and visualization tools,
ensuring easy and timely access to data.

Author: Alexsander Lopes Camargos
License: MIT
"""

import pandas as pd

from bacen_ifdata.scraper.institutions import InstitutionType as Institutions
from bacen_ifdata.scraper.reports import ReportsPrudentialConglomerates
from bacen_ifdata.data_transformer.controller import TransformerController


def main(data_frame: pd.DataFrame,
         institution: Institutions,
         report: ReportsPrudentialConglomerates) -> None:
    """Main function for the transformer.

    This function orchestrates the transformation process for the reports
    downloaded from the Banco Central do Brasil's IF.data tool.

    Arguments:
        data_frame (pd.DataFrame): The data frame containing the report data.
    """

    # Create the controller object.
    controller = TransformerController()

    # Run the transformation process.
    if institution.value == Institutions.PRUDENTIAL_CONGLOMERATES:
        if report.value == ReportsPrudentialConglomerates.SUMMARY:
            controller.transform_prudential_conglomerates(data_frame)
