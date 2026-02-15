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
                           lat_col: str = None,
                           lon_col: str = None,
                           filename: str = 'mappa_incidenti.html') -> bool:
        """
        Create an accident map using Folium
        
        Args:
            filtered_df: DataFrame with accident data
            lat_col: Name of latitude column (if None, will search for it)
            lon_col: Name of longitude column (if None, will search for it)
            filename: Output HTML file name
            
        Returns:
            True if map was created successfully
        """
        try:
            if filtered_df.empty:
                print("No data available to create map")
                return False
            
            # If columns not provided, try to find them
            if lat_col is None or lon_col is None:
                coordinate_variations = {
                    'lat': ['latitudine', 'latitude', 'lat', 'y_coord', 'y'],
                    'lon': ['longitudine', 'longitude', 'lon', 'x_coord', 'x']
                }
                
                df_columns_lower = {col.lower(): col for col in filtered_df.columns}
                
                for lat_var in coordinate_variations['lat']:
                    if lat_var in df_columns_lower:
                        lat_col = df_columns_lower[lat_var]
                        break
                
                for lon_var in coordinate_variations['lon']:
                    if lon_var in df_columns_lower:
                        lon_col = df_columns_lower[lon_var]
                        break
            
            if lat_col is None or lon_col is None:
                print(f"❌ Coordinate columns not found. Available: {list(filtered_df.columns)}")
                return False
            
            print(f"✅ Using columns: lat={lat_col}, lon={lon_col}")
            
            # Remove rows with missing coordinates
            valid_coords = filtered_df.dropna(subset=[lat_col, lon_col])
            
            if valid_coords.empty:
                print("No valid coordinates found to create map")
                return False
            
            # Use average coordinates to automatically center the map.
            center_lat = valid_coords[lat_col].mean()
            center_lon = valid_coords[lon_col].mean()
            
            print(f"🗺️ Map center: ({center_lat}, {center_lon})")
            
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
            # Ensure the output directory exists
            os.makedirs(OUTPUT_DIR, exist_ok=True)
            
            filepath = os.path.join(OUTPUT_DIR, filename)
            
            # Convert to absolute path to avoid issues
            filepath = os.path.abspath(filepath)
            
            # Save the map
            incidents_map.save(filepath)
            
            # Debug: Print file details
            file_size = os.path.getsize(filepath) if os.path.exists(filepath) else 0
            print(f"🗺️ Map saved: {filepath}")
            print(f"   File size: {file_size} bytes")
            print(f"   File exists: {os.path.exists(filepath)}")
            print(f"   Total markers: {len(valid_coords)}")
            
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
    
    def analyze(self) -> dict:
        """
        Perform complete analysis on the dataset
        
        Returns:
            Dictionary with analysis results
        """
        results = {
            'summary': self.get_data_summary(),
            'filtered_data': None,
            'map_created': False,
            'has_coordinates': False,
            'coordinate_columns': [],
            'total_points_on_map': 0
        }
        
        try:
            # Check if dataset has coordinate columns (latitude and longitude)
            lat_col = None
            lon_col = None
            coordinate_variations = {
                'lat': ['latitudine', 'latitude', 'lat', 'y_coord', 'y'],
                'lon': ['longitudine', 'longitude', 'lon', 'x_coord', 'x']
            }
            
            # Find coordinate columns (case-insensitive)
            df_columns_lower = {col.lower(): col for col in self.df.columns}
            
            for lat_var in coordinate_variations['lat']:
                if lat_var in df_columns_lower:
                    lat_col = df_columns_lower[lat_var]
                    break
            
            for lon_var in coordinate_variations['lon']:
                if lon_var in df_columns_lower:
                    lon_col = df_columns_lower[lon_var]
                    break
            
            # If coordinates found, update results and create map with ALL geographic data
            if lat_col and lon_col:
                results['has_coordinates'] = True
                results['coordinate_columns'] = [lat_col, lon_col]
                
                print(f"🔍 Found coordinate columns: {lat_col}, {lon_col}")
                
                # Create map with ALL geographic data in the dataset
                # Pass the column names to avoid redundant searching
                try:
                    map_created = self.create_incidents_map(self.df, lat_col=lat_col, lon_col=lon_col)
                    results['map_created'] = map_created
                    
                    # Count valid points on the map
                    valid_coords = self.df.dropna(subset=[lat_col, lon_col])
                    results['total_points_on_map'] = len(valid_coords)
                    
                except Exception as e:
                    print(f"Error creating map: {e}")
                    results['map_created'] = False
            else:
                print(f"❌ No coordinate columns found. Available columns: {list(self.df.columns)}")
            
            # Filter data for traffic conditions (separate from map creation)
            filtered_df = self.filter_traffic_conditions()
            
            if not filtered_df.empty:
                results['filtered_data'] = {
                    'total_filtered_records': len(filtered_df),
                    'sample': filtered_df.head(5).to_dict()
                }
        
        except Exception as e:
            results['error'] = str(e)
            print(f"Error in analyze: {e}")
        
        return results
