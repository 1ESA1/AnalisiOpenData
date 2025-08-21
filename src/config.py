"""
Application configuration for Open Data analysis
This module contains constants used in the application, such as base URLs for the CKAN API,
file paths and file names. These constants are used throughout the project to ensure
consistency and ease of maintenance.
"""

# CKAN API base URL
CKAN_BASE_URL = "https://dati.gov.it/opendata/api/3/action"

# File paths
DATA_DIR = "./data"
OUTPUT_DIR = "./output"

# File names
PACKAGE_LIST_FILE = "DatiGovIt.json"
FILTERED_DATA_FILE = "DatiGovItFiltrati.json"
SELECTED_DATA_FILE = "DatiSelezionati.json"
OUTPUT_CSV_FILE = "output.csv"
OUTPUT_EXCEL_FILE = "output.xlsx"
CONDITIONS_EXCEL_FILE = "Condizioni.xlsx"
MAP_HTML_FILE = "mappa_incidenti.html"

# Pandas column display configuration - no limit
PANDAS_MAX_COLUMNS = None

# Map configuration
DEFAULT_ZOOM = 13
