#!/usr/bin/env python3
"""
Central configurations for all AnalisiOpenData project tests.
Contains constants, paths and shared configurations.
"""

import os
import tempfile
from typing import Dict, List, Any

# ===== GENERAL CONFIGURATIONS =====
TEST_TIMEOUT = 30
TEST_MAX_RETRIES = 3
VERBOSE_OUTPUT = True

# ===== PATHS =====
# Project base path (main folder)
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Main directory paths
SRC_DIR = os.path.join(PROJECT_ROOT, 'src')
TESTS_DIR = os.path.join(PROJECT_ROOT, 'tests')
DATA_DIR = os.path.join(PROJECT_ROOT, 'data')
OUTPUT_DIR = os.path.join(PROJECT_ROOT, 'output')

# ===== MODULES TO TEST =====
MODULES_TO_TEST = [
    ("config.py", os.path.join(SRC_DIR, "config.py")),
    ("services.py", os.path.join(SRC_DIR, "services.py")),
    ("file_manager.py", os.path.join(SRC_DIR, "file_manager.py")),
    ("analyzer.py", os.path.join(SRC_DIR, "analyzer.py")),
    ("ui.py", os.path.join(SRC_DIR, "ui.py")),
    ("main.py", os.path.join(SRC_DIR, "main.py")),
    ("migrate.py", os.path.join(SRC_DIR, "migrate.py"))
]

# ===== TEST DATA =====
# Sample data for JSON tests
SAMPLE_JSON_DATA: Dict[str, Any] = {
    "test": "data",
    "numbers": [1, 2, 3],
    "nested": {
        "key": "value",
        "array": ["a", "b", "c"]
    }
}

# Sample data for DataFrame tests
SAMPLE_DATAFRAME_DATA: Dict[str, List[Any]] = {
    "col1": [1, 2, 3, 4],
    "col2": ["a", "b", "c", "d"],
    "col3": [1.1, 2.2, 3.3, 4.4]
}

# Dati di esempio per test Analyzer
SAMPLE_INCIDENT_DATA: Dict[str, List[Any]] = {
    'Condizioni traffico': ['Intenso', 'Normale', 'Intenso', 'Scorrevole'],
    'N. veicoli coinvolti': [3, 1, 4, 2],
    'Latitudine': [45.464, 45.465, 45.466, 45.467],
    'Longitudine': [9.190, 9.191, 9.192, 9.193],
    'Altre_colonne': ['a', 'b', 'c', 'd']
}

# ===== CONFIGURAZIONI TEMPORANEE =====
def get_temp_directory() -> str:
    """
    Crea e restituisce un percorso per directory temporanea sicura.
    Cross-platform e thread-safe.
    
    Returns:
        Percorso della directory temporanea
    """
    return tempfile.mkdtemp(prefix="analisi_opendata_test_")

def get_temp_file(suffix: str = "") -> str:
    """
    Crea e restituisce un percorso per file temporaneo sicuro.
    
    Args:
        suffix: Estensione del file (es. ".json", ".csv")
        
    Returns:
        Percorso del file temporaneo
    """
    fd, path = tempfile.mkstemp(suffix=suffix, prefix="analisi_opendata_test_")
    os.close(fd)  # Chiude il file descriptor
    return path

# ===== CONFIGURAZIONI DI RETE =====
# Per test che richiedono connessioni (se necessari)
NETWORK_TIMEOUT = 30
MAX_DOWNLOAD_SIZE = 10 * 1024 * 1024  # 10MB

# ===== CONFIGURAZIONI OUTPUT =====
# Messaggi standard per i test
SUCCESS_EMOJI = "✅"
FAILURE_EMOJI = "❌"
INFO_EMOJI = "ℹ️"
WARNING_EMOJI = "⚠️"
ROCKET_EMOJI = "🚀"
PARTY_EMOJI = "🎉"

# Pattern per separatori
SEPARATOR_LONG = "=" * 60
SEPARATOR_SHORT = "-" * 40

# ===== VALIDAZIONI =====
def validate_project_structure() -> bool:
    """
    Valida che la struttura del progetto sia corretta.
    
    Returns:
        True se la struttura è valida, False altrimenti
    """
    required_dirs = [SRC_DIR, TESTS_DIR, DATA_DIR, OUTPUT_DIR]
    
    for directory in required_dirs:
        if not os.path.exists(directory):
            print(f"{WARNING_EMOJI} Directory mancante: {directory}")
            return False
    
    return True

def get_available_modules() -> List[tuple]:
    """
    Restituisce solo i moduli che esistono effettivamente.

    Returns:
        Lista di tuple (nome_modulo, percorso) per moduli esistenti
    """
    available = []
    for module_name, module_path in MODULES_TO_TEST:
        if os.path.exists(module_path):
            available.append((module_name, module_path))
        else:
            print(f"{WARNING_EMOJI} Modulo non trovato: {module_path}")
    
    return available
