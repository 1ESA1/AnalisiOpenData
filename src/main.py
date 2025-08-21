"""
Main application for Open Data analysis
This application allows you to retrieve, filter and analyze open data from dati.gov.it.
Manages the complete workflow, from package search to results visualization.
Includes functionality for:
- Retrieving and saving the package list
- Filtering packages by keyword
- Selecting a specific package
- Downloading and analyzing CSV data
- Road accident analysis (if applicable)
- Visualizing results in CSV and Excel format

Author: [ESA]
Date: [01-07-2024]
Version: 1.0.0
Last update: [Last update date]
"""
import pandas as pd
import os
import sys

# Add the src path to PYTHONPATH 
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services import CkanApiService, DataService
from file_manager import FileManager
from analyzer import IncidentAnalyzer
from ui import UserInterface
from config import (
    PACKAGE_LIST_FILE, FILTERED_DATA_FILE, SELECTED_DATA_FILE,
    OUTPUT_CSV_FILE, OUTPUT_EXCEL_FILE, CONDITIONS_EXCEL_FILE,
    MAP_HTML_FILE, PANDAS_MAX_COLUMNS
)


class OpenDataAnalyzer:
    """Main class for Open Data analysis"""
    
    def __init__(self):
        """Initialize services and user interface"""
        self.ckan_service = CkanApiService()
        self.data_service = DataService()
        self.file_manager = FileManager()
        self.ui = UserInterface()
        
        # Configure pandas to display more columns
        pd.set_option("display.max_columns", PANDAS_MAX_COLUMNS)
    
    def run(self):
        """
        Executes the main application flow with failure checks for each step
        Manages the entire data analysis process:
        1. Retrieves and saves the package list
        2. Filters packages by keyword
        3. Selects a specific package
        4. Retrieves package details
        5. Finds and downloads CSV data
        6. Saves basic data in CSV and Excel format
        7. Analyzes accidents (if applicable)
        Handles exceptions and errors in a way that does not interrupt application execution.
        If a step fails, the user is informed and the process stops. 
        """
        try:
            # 1. Retrieve and save the package list
            self.ui.show_info("Retrieving package list from dati.gov.it...")
            if not self._fetch_and_save_packages(): 
                return
            
            # 2. Filter packages by keyword
            filtered_packages = self._filter_packages()
            if not filtered_packages:
                return
            
            # 3. Select a specific package
            selected_package = self._select_package(filtered_packages)
            if not selected_package:
                return
            
            # 4. Retrieve package details
            package_data = self._get_package_details(selected_package)
            if not package_data:
                return
            
            # 5. Find and download CSV data
            dataframe = self._download_csv_data(package_data)
            if dataframe is None:
                return
            
            # 6. Save basic data
            self._save_basic_data(dataframe)
            
            # 7. Analyze accidents (if applicable)
            self._analyze_incidents(dataframe)
            
            self.ui.show_success("Analysis completed successfully!")
            
        except KeyboardInterrupt:
            self.ui.show_info("Operation cancelled by user.")
        except Exception as e:
            self.ui.show_error(f"Unexpected error: {e}")
    
    def _fetch_and_save_packages(self) -> bool:
        """Retrieves and saves the package list indicating success/failure"""
        package_data = self.ckan_service.get_package_list()
        if not package_data:
            self.ui.show_error("Unable to retrieve package list")
            return False
        
        success = self.file_manager.save_json(package_data, PACKAGE_LIST_FILE)
        if success:
            self.ui.show_success(f"Package list saved in {PACKAGE_LIST_FILE}")
        return success
    
    def _filter_packages(self) -> list:
        """Filter packages by keyword"""
        # Load data
        data = self.file_manager.load_json(PACKAGE_LIST_FILE)
        if not data:
            self.ui.show_error("Unable to load package list")
            return []
        
        # Ask for keyword
        keyword = self.ui.get_keyword_input()
        
        # Filter packages
        packages = data.get('result', [])
        filtered_packages = self.data_service.filter_packages_by_keyword(packages, keyword)
        
        if not filtered_packages:
            self.ui.show_error(f"No results found for '{keyword}'")
            return []
        
        # Save filtered results
        self.file_manager.save_json(filtered_packages, FILTERED_DATA_FILE)
        self.ui.show_success(f"Found {len(filtered_packages)} packages for '{keyword}'")
        
        return filtered_packages
    
    def _select_package(self, filtered_packages: list) -> str:
        """Allows package selection"""
        return self.ui.get_package_selection(filtered_packages)
    
    def _get_package_details(self, package_name: str) -> dict:
        """Retrieves details of a specific package"""
        self.ui.show_info(f"Retrieving details for '{package_name}'...")
        
        package_data = self.ckan_service.get_package_details(package_name)
        if not package_data:
            self.ui.show_error(f"Unable to retrieve details for '{package_name}'")
            return {}
        
        # Save details
        self.file_manager.save_json(package_data, SELECTED_DATA_FILE)
        self.ui.show_success("Package details saved")
        
        return package_data
    
    def _download_csv_data(self, package_data: dict) -> pd.DataFrame:
        """Download CSV data from package"""
        # Search for CSV URL automatically in package metadata
        self.ui.show_info("Searching for CSV files in package metadata...")
        
        resources = package_data.get('result', {}).get('resources', [])
        if not resources:
            self.ui.show_error("No resources found in package")
            return None
        
        # Find CSV URL
        csv_url = self.data_service.find_csv_resource_url(package_data)
        
        if not csv_url:
            self.ui.show_info("No CSV file found automatically")
            csv_url = self.ui.get_manual_csv_url()
        
        self.ui.show_info(f"Downloading data from: {csv_url}")
        dataframe = self.data_service.get_dataframe_from_url(csv_url)
        
        if dataframe is not None: # User feedback on download outcome
            self.ui.show_success(f"Downloaded {len(dataframe)} records")
        else:
            self.ui.show_error("Unable to download CSV data")
        
        return dataframe
    
    def _save_basic_data(self, dataframe: pd.DataFrame):
        """Save basic data in CSV and Excel format"""
        self.file_manager.save_dataframe_csv(dataframe, OUTPUT_CSV_FILE)
        self.file_manager.save_dataframe_excel(dataframe, OUTPUT_EXCEL_FILE)
    
    def _analyze_incidents(self, dataframe: pd.DataFrame):
        """
        Analyzes accident data if appropriate columns are present
        Checks for the presence of necessary columns and starts accident analysis.
        If required columns are not present, informs the user and ends the analysis.
        """
        self.ui.show_info("Starting accident analysis...")
        analyzer = IncidentAnalyzer(dataframe) # Create an incident analyzer instance with data downloaded from CSV
        
        # Show data summary by extracting main information and displaying it
        summary = analyzer.get_data_summary()
        self.ui.display_summary(summary)
        
        # Check if there are columns for accident analysis
        required_cols = ['Condizioni traffico', 'N. veicoli coinvolti']
        if all(col in dataframe.columns for col in required_cols): # Check if all required columns are present
            self.ui.show_info("Detected columns for accident analysis. Starting analysis...")
            
            # Filter for specific conditions
            filtered_incidents = analyzer.filter_traffic_conditions()
            
            if not filtered_incidents.empty:
                # Save filtered data
                self.file_manager.save_dataframe_excel(
                    filtered_incidents, 
                    CONDITIONS_EXCEL_FILE
                )
                
                # Create map if there are coordinates
                if all(col in filtered_incidents.columns for col in ['Latitudine', 'Longitudine']):
                    analyzer.create_incidents_map(filtered_incidents, MAP_HTML_FILE)
                else:
                    self.ui.show_info("Coordinates not available for map creation")
            else:
                self.ui.show_info("No accidents found with specified criteria")
        else:
            self.ui.show_info("Data not suitable for accident analysis")


def main():
    """Main function"""
    print("=== OPEN DATA ANALYZER ===")
    print("Open data analysis from dati.gov.it\n")
    
    app = OpenDataAnalyzer()
    app.run()


if __name__ == "__main__":
    main()
