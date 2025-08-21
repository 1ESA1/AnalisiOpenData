"""
Manages JSON, Excel and CSV file operations, including reading and writing.
This module provides a `FileManager` class to facilitate file management
in a project, ensuring that necessary directories exist and providing methods
to save and load data in various formats.
"""

import json # For JSON file handling
import pandas as pd # For DataFrame manipulation
import os # For file and directory operations
from typing import Any, Dict, Optional # Type hints for documentation
from config import DATA_DIR, OUTPUT_DIR # Import configuration directories


class FileManager:
    """Manages file read and write operations"""
    
    def __init__(self):
        """Initialize the file manager and ensure directories exist"""
        self._ensure_directories_exist() # Create necessary directories if they don't exist
    
    def _ensure_directories_exist(self):
        """Create necessary directories if they don't exist"""
        for directory in [DATA_DIR, OUTPUT_DIR]: # Iterate over both directories
            os.makedirs(directory, exist_ok=True)
    
    def save_json(self, data: Any, filename: str, directory: str = DATA_DIR) -> bool:
        """Save data in JSON format"""
        try:
            # Create directory if it doesn't exist
            os.makedirs(directory, exist_ok=True)
            
            filepath = os.path.join(directory, filename) # Build complete file path
            with open(filepath, 'w', encoding='utf-8') as f: # Open file in write mode
                if isinstance(data, dict):
                    json.dump(data, f, indent=4, ensure_ascii=False)
                else:
                    json.dump(data, f, indent=4, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error saving JSON file {filename}: {e}")
            return False
    
    def load_json(self, filename: str, directory: str = DATA_DIR) -> Optional[Dict[str, Any]]:
        """Load data from a JSON file"""
        try:
            filepath = os.path.join(directory, filename) # Build complete file path
            with open(filepath, 'r', encoding='utf-8') as f: # Open file in read mode
                return json.load(f)
        except Exception as e:
            print(f"Error loading JSON file {filename}: {e}")
            return None
    
    def save_dataframe_csv(self, df: pd.DataFrame, filename: str, directory: str = OUTPUT_DIR) -> bool:
        """Save a DataFrame in CSV format"""
        try:
            # Create directory if it doesn't exist
            os.makedirs(directory, exist_ok=True)
            
            filepath = os.path.join(directory, filename) # Build complete file path
            df.to_csv(filepath, index=False) # Save DataFrame in CSV format
            print(f"Data saved in {filepath}")
            return True
        except Exception as e:
            print(f"Error saving CSV {filename}: {e}")
            return False
    
    def save_dataframe_excel(self, df: pd.DataFrame, filename: str, directory: str = OUTPUT_DIR) -> bool:
        """Save a DataFrame in Excel format"""
        try:
            # Create directory if it doesn't exist
            os.makedirs(directory, exist_ok=True)
            
            filepath = os.path.join(directory, filename) # Build complete file path
            df.to_excel(filepath, index=False) # Save DataFrame in Excel format
            print(f"Data saved in {filepath}")
            return True
        except Exception as e:
            print(f"Error saving Excel {filename}: {e}")
            return False
