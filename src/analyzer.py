"""
Analyzer for road accident data
This module provides functionality to analyze road accident data,
filter based on traffic conditions and create interactive maps of accidents.
"""

import pandas as pd # Data manipulation
import folium # Interactive map creation
import os # File path management
from config import OUTPUT_DIR, DEFAULT_ZOOM # Global configurations


class IncidentAnalyzer:
    """Analyzes road accident data and creates visualizations"""
    
    def __init__(self, dataframe: pd.DataFrame): # Constructor initializes analyzer with a DataFrame
        self.df = dataframe
    
    def filter_traffic_conditions(self, 
                                 traffic_condition: str = 'Intenso', 
                                 min_vehicles: int = 2) -> pd.DataFrame:
        """
        Filter accidents based on traffic conditions and number of vehicles involved
        
        Args:
            traffic_condition: Traffic condition to filter
            min_vehicles: Minimum number of vehicles involved
            
        Returns:
            Filtered DataFrame
        """
        try:
            # Check existence of necessary columns
            traffic_col = 'Condizioni traffico'
            vehicles_col = 'N. veicoli coinvolti'
            
            if traffic_col not in self.df.columns:
                print(f"Column '{traffic_col}' not found in dataset")
                return pd.DataFrame()
            
            if vehicles_col not in self.df.columns:
                print(f"Column '{vehicles_col}' not found in dataset")
                return pd.DataFrame()
            
            # Apply filters on traffic conditions and number of vehicles involved
            filtered_df = self.df[
                (self.df[traffic_col] == traffic_condition) & 
                (self.df[vehicles_col] > min_vehicles)
            ]
            
            # Clean result. 
            # Remove missing values like (NaN, None, Null) from DataFrame columns
            filtered_df = filtered_df.dropna(axis=1, how='all') # Remove only completely empty columns
            
            print(f"Found {len(filtered_df)} accidents with {traffic_condition} traffic and more than {min_vehicles} vehicles involved")
            
            return filtered_df
            
        except Exception as e:
            print(f"Error during data filtering: {e}")
            return pd.DataFrame()
    
    def create_incidents_map(self, 
                           filtered_df: pd.DataFrame, 
                           filename: str = 'mappa_incidenti.html') -> bool:
        """
        Create an accident map using Folium
        
        Args:
            filtered_df: DataFrame with filtered accident data
            filename: Output HTML file name
            
        Returns:
            True if map was created successfully
        """
        try:
            if filtered_df.empty:
                print("No data available to create map")
                return False
            
            # Check if coordinate columns exist
            lat_col = 'Latitudine'
            lon_col = 'Longitudine'
            
            if lat_col not in filtered_df.columns or lon_col not in filtered_df.columns:
                print(f"Coordinate columns ({lat_col}, {lon_col}) not found in dataset")
                return False
            
            # Remove rows with missing coordinates
            valid_coords = filtered_df.dropna(subset=[lat_col, lon_col])
            
            if valid_coords.empty:
                print("No valid coordinates found to create map")
                return False
            
            # Use average coordinates to automatically center the map.
            center_lat = valid_coords[lat_col].mean()
            center_lon = valid_coords[lon_col].mean()
            
            # Create map by transforming coordinates into a Folium object
            incidents_map = folium.Map(
                location=[center_lat, center_lon], 
                zoom_start=DEFAULT_ZOOM
            )
            
            """
             Iteration over each row of the filtered DataFrame, for each row with valid coordinates,
             create a marker on the map with the specified coordinates.
             The marker popup shows the accident index.
            """
            for idx, row in valid_coords.iterrows():
                folium.Marker(
                    [row[lat_col], row[lon_col]],
                    popup=f"Accident {idx}"
                ).add_to(incidents_map)
            
            # Save map to HTML file
            filepath = os.path.join(OUTPUT_DIR, filename)
            incidents_map.save(filepath)
            
            print(f"Map created and saved in {filepath}")
            print(f"Added {len(valid_coords)} markers to map")
            
            return True
            
        except Exception as e:
            print(f"Error during map creation: {e}")
            return False
    
    def get_data_summary(self) -> dict:
        """Returns a data summary"""
        return {
            'total_records': len(self.df),
            'columns': list(self.df.columns),
            'missing_data': self.df.isnull().sum().to_dict(),
            'data_types': self.df.dtypes.to_dict()
        }
