#!/usr/bin/env python3
"""
Utility functions comuni per tutti i test del progetto AnalisiOpenData.
Contiene funzioni di supporto riutilizzabili per eliminare duplicazioni.
"""

import os
import sys
import shutil
import tempfile
import pandas as pd
from typing import Any, Dict, List, Optional, Tuple
from contextlib import contextmanager

# Aggiungi il percorso src al PYTHONPATH per i test
def setup_python_path():
    """
    Aggiunge la directory src al PYTHONPATH per permettere le importazioni.
    Deve essere chiamata all'inizio di ogni test.
    """
    src_path = os.path.join(os.path.dirname(__file__), '..', 'src')
    if src_path not in sys.path:
        sys.path.insert(0, src_path)

@contextmanager
def temporary_directory():
    """
    Context manager per creare una directory temporanea che viene automaticamente pulita.
    
    Usage:
        with temporary_directory() as temp_dir:
            # Usa temp_dir per operazioni temporanee
            pass
        # Directory automaticamente rimossa
    """
    temp_dir = tempfile.mkdtemp(prefix="analisi_opendata_test_")
    try:
        yield temp_dir
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)

@contextmanager
def temporary_file(suffix: str = ""):
    """
    Context manager per creare un file temporaneo che viene automaticamente pulito.
    
    Args:
        suffix: Estensione del file (es. ".json", ".csv")
        
    Usage:
        with temporary_file(".json") as temp_file:
            # Usa temp_file per operazioni temporanee
            pass
        # File automaticamente rimosso
    """
    fd, temp_path = tempfile.mkstemp(suffix=suffix, prefix="analisi_opendata_test_")
    os.close(fd)
    try:
        yield temp_path
    finally:
        try:
            os.unlink(temp_path)
        except OSError:
            pass

def safe_import(module_name: str) -> Optional[Any]:
    """
    Importa un modulo in modo sicuro, restituendo None se l'import fallisce.
    
    Args:
        module_name: Nome del modulo da importare
        
    Returns:
        Il modulo importato o None se l'import fallisce
    """
    try:
        return __import__(module_name)
    except ImportError as e:
        print(f"❌ Impossibile importare {module_name}: {e}")
        return None

def verify_module_attributes(module: Any, required_attributes: List[str]) -> Tuple[bool, List[str]]:
    """
    Verifica che un modulo abbia tutti gli attributi richiesti.
    
    Args:
        module: Il modulo da verificare
        required_attributes: Lista di nomi di attributi richiesti
        
    Returns:
        Tupla (successo, attributi_mancanti)
    """
    missing = []
    for attr in required_attributes:
        if not hasattr(module, attr):
            missing.append(attr)
    
    return len(missing) == 0, missing

def create_sample_dataframe(data: Optional[Dict[str, List[Any]]] = None) -> pd.DataFrame:
    """
    Crea un DataFrame di esempio per i test.
    
    Args:
        data: Dati personalizzati o None per usare dati predefiniti
        
    Returns:
        DataFrame di esempio
    """
    if data is None:
        data = {
            "col1": [1, 2, 3, 4],
            "col2": ["a", "b", "c", "d"],
            "col3": [1.1, 2.2, 3.3, 4.4]
        }
    
    return pd.DataFrame(data)

def validate_file_operations(file_manager, temp_dir: str) -> bool:
    """
    Testa le operazioni base del FileManager in modo standardizzato.
    
    Args:
        file_manager: Istanza del FileManager da testare
        temp_dir: Directory temporanea per i test
        
    Returns:
        True se tutte le operazioni riescono, False altrimenti
    """
    try:
        # Test JSON
        test_data = {"test": "data", "numbers": [1, 2, 3]}
        
        # Salva JSON
        json_success = file_manager.save_json(test_data, "test.json", temp_dir)
        if not json_success:
            print("❌ Fallimento salvataggio JSON")
            return False
        
        # Carica JSON
        loaded_data = file_manager.load_json("test.json", temp_dir)
        if loaded_data != test_data:
            print("❌ Fallimento caricamento JSON")
            return False
        
        # Test DataFrame
        df = create_sample_dataframe()
        
        csv_success = file_manager.save_dataframe_csv(df, "test.csv", temp_dir)
        excel_success = file_manager.save_dataframe_excel(df, "test.xlsx", temp_dir)
        
        if not (csv_success and excel_success):
            print("❌ Fallimento salvataggio DataFrame")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Errore durante test file operations: {e}")
        return False

def test_class_instantiation(class_type: type, *args, **kwargs) -> Tuple[bool, Optional[Any], Optional[str]]:
    """
    Testa l'istanziazione di una classe in modo sicuro.
    
    Args:
        class_type: La classe da istanziare
        *args: Argomenti posizionali per il costruttore
        **kwargs: Argomenti nominali per il costruttore
        
    Returns:
        Tupla (successo, istanza_o_None, messaggio_errore_o_None)
    """
    try:
        instance = class_type(*args, **kwargs)
        return True, instance, None
    except Exception as e:
        return False, None, str(e)

def compare_lists_ignore_order(list1: List[Any], list2: List[Any]) -> bool:
    """
    Confronta due liste ignorando l'ordine degli elementi.
    
    Args:
        list1: Prima lista
        list2: Seconda lista
        
    Returns:
        True se le liste contengono gli stessi elementi
    """
    return set(list1) == set(list2)

def format_test_header(test_name: str) -> str:
    """
    Formatta un header per sezione di test.
    
    Args:
        test_name: Nome del test
        
    Returns:
        Header formattato
    """
    return f"\n=== TEST {test_name.upper()} ===\n"

def format_success_message(message: str) -> str:
    """
    Formatta un messaggio di successo.
    
    Args:
        message: Messaggio da formattare
        
    Returns:
        Messaggio formattato con emoji
    """
    return f"✅ {message}"

def format_error_message(message: str) -> str:
    """
    Formatta un messaggio di errore.
    
    Args:
        message: Messaggio da formattare
        
    Returns:
        Messaggio formattato con emoji
    """
    return f"❌ {message}"

def format_info_message(message: str) -> str:
    """
    Formatta un messaggio informativo.
    
    Args:
        message: Messaggio da formattare
        
    Returns:
        Messaggio formattato con emoji
    """
    return f"ℹ️  {message}"

def print_separator(length: int = 50) -> None:
    """
    Stampa una linea separatrice.
    
    Args:
        length: Lunghezza della linea
    """
    print("=" * length)

def capture_function_output(func, *args, **kwargs) -> Tuple[Any, str]:
    """
    Cattura l'output di una funzione (utile per testare print statements).
    
    Args:
        func: Funzione da eseguire
        *args: Argomenti posizionali
        **kwargs: Argomenti nominali
        
    Returns:
        Tupla (risultato_funzione, output_catturato)
    """
    import io
    from contextlib import redirect_stdout
    
    captured_output = io.StringIO()
    with redirect_stdout(captured_output):
        result = func(*args, **kwargs)
    
    return result, captured_output.getvalue()
