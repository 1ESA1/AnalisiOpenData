"""
This module provides classes to retrieve packages and details
from the dati.gov.it CKAN API, plus methods to filter packages and find CSV resources.
Also includes functionality to convert CSV URLs to Pandas DataFrames.
The main classes are `CkanApiService` and `DataService`.
These classes handle API calls, data manipulation
and retrieval of specific resources such as CSV files.
"""

import requests # For HTTP API calls
import json     # For JSON data handling
import pandas as pd # For DataFrame manipulation
from io import StringIO # For converting strings to readable streams
from typing import Optional, List, Dict, Any # Type hints for documentation
from config import CKAN_BASE_URL # Base API URL imported from configuration


class CkanApiService:
    """Manages CKAN API calls"""
    
    def __init__(self): 
        """Initialize the service with the API base URL"""
        # The API base URL is imported from configuration
        # This allows to easily change the endpoint without modifying the code
        self.base_url = CKAN_BASE_URL
    
    def get_package_list(self) -> Optional[Dict[str, Any]]: # Return function, can be a dictionary or None
        """Retrieve the complete list of available packages"""
        # Build the URL for the package list request
        url = f"{self.base_url}/package_list"
        # Make GET request to API
        try:
            response = requests.get(url)
            response.raise_for_status() # Raise HTTPError exception if HTTP response indicates error (4xx or 5xx status codes)
            return json.loads(response.text) # Transform JSON response into Python dictionary
        except requests.RequestException as e: # Handle request exceptions 
            print(f"Error retrieving package list: {e}")
            return None
    
    def get_package_details(self, package_id: str) -> Optional[Dict[str, Any]]: # Return function, can be a dictionary or None
        """Retrieve details of a specific package"""
        # Build the URL for the package details request
        # The package_id is passed as parameter to identify the package
        url = f"{self.base_url}/package_show?id={package_id}"
        try:
            response = requests.get(url)
            response.raise_for_status() # Raise HTTPError exception if HTTP response indicates error (4xx or 5xx status codes)
            return json.loads(response.text) # Transform JSON response into Python dictionary
        except requests.RequestException as e: # Handle request exceptions
            print(f"Error retrieving package details {package_id}: {e}")
            return None


class DataService:
    """Manages CSV data retrieval and manipulation"""
    
    @staticmethod
    def get_dataframe_from_url(url: str) -> Optional[pd.DataFrame]: # Return function as a df object
        """Retrieve a DataFrame from a CSV URL"""
        try:
            response = requests.get(url)
            response.raise_for_status() # Raise HTTPError exception if HTTP response indicates error (4xx or 5xx status codes)
            data = response.content.decode('utf-8')
            df = pd.read_csv(StringIO(data))
            return df
        except requests.RequestException as e:
            print(f"Error retrieving data from {url}: {e}")
            return None
        except Exception as e:
            print(f"Error converting to DataFrame: {e}")
            return None
    
    @staticmethod
    def filter_packages_by_keyword(packages: List[str], keyword: str) -> List[str]:
        """Filter packages based on a keyword"""
        return [package for package in packages if keyword.lower() in package.lower()]
    
    @staticmethod
    def find_csv_resource_url(package_data: Dict[str, Any]) -> Optional[str]:
        """Find CSV resource URL in a package"""
        resources = package_data.get('result', {}).get('resources', []) # Get the resource list from package
        # Iterate over resources to find the one with CSV format
        for resource in resources:
            format_type = resource.get('format', '')
            url = resource.get('url', '')
            # Check for CSV format and URL containing .csv or accessType=DOWNLOAD for CSV
            if format_type == 'CSV' and ('.csv' in url or 'accessType=DOWNLOAD' in url):
                return resource.get('url')
        return None
