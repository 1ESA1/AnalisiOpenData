"""
Interface for the application.
This module defines the main application class that orchestrates the workflow of retrieving, 
processing, and analyzing open data from dati.gov.it. It manages the complete process, from package search to results visualization,
including error handling to ensure that the application continues to run even if some steps fail
"""
import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import os
import sys
from analyzer import IncidentAnalyzer
from services import DataService, CkanApiService
from config import OUTPUT_DIR, OUTPUT_CSV_FILE, MAP_HTML_FILE

# Define th route for the application
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

# Helper function to format analysis results
def format_summary_results(summary):
    """Convert summary data to a readable table format"""
    if not summary:
        return pd.DataFrame()
    
    # Convert to readable table
    summary_data = {
        'Metric': [],
        'Value': []
    }
    
    for key, value in summary.items():
        if key == 'missing_data':
            # Format missing data count
            missing_count = sum([1 for v in value.values() if v > 0]) if isinstance(value, dict) else 0
            summary_data['Metric'].append('Missing Data Entries')
            summary_data['Value'].append(missing_count)
        elif key == 'data_types':
            # Count data types
            if isinstance(value, dict):
                summary_data['Metric'].append('Data Columns')
                summary_data['Value'].append(len(value))
        elif key == 'columns':
            # List columns
            if isinstance(value, list):
                summary_data['Metric'].append('Column Names')
                summary_data['Value'].append(', '.join([str(c)[:30] for c in value[:5]]) + (f'... (+{len(value)-5} more)' if len(value) > 5 else ''))
        else:
            # Generic key-value pair
            summary_data['Metric'].append(str(key).replace('_', ' ').title())
            summary_data['Value'].append(str(value))
    
    return pd.DataFrame(summary_data)

def format_filtered_data(filtered_data):
    """Convert filtered data to readable format"""
    if not filtered_data:
        return None
    
    filtered_info = {
        'Metric': [],
        'Value': []
    }
    
    for key, value in filtered_data.items():
        if key == 'sample' and isinstance(value, dict):
            filtered_info['Metric'].append('Sample Records')
            filtered_info['Value'].append(f"{len(value)} records")
        else:
            filtered_info['Metric'].append(str(key).replace('_', ' ').title())
            filtered_info['Value'].append(str(value))
    
    return pd.DataFrame(filtered_info) if filtered_info['Metric'] else None
    
# Configuration of the Streamlit application
st.set_page_config(page_title="Open Data Analysis", layout="wide")

st.title("Open Data Analysis - dati.gov.it")
st.markdown("Transform your open data into actionable insights with our comprehensive analysis tool")

# Initialize session state for storing analysis results
if 'all_data' not in st.session_state:
    st.session_state.all_data = pd.DataFrame()
if 'analysis_done' not in st.session_state:
    st.session_state.analysis_done = False
if 'search_results' not in st.session_state:
    st.session_state.search_results = []
if 'selected_packages' not in st.session_state:
    st.session_state.selected_packages = []
if 'selected_package_data' not in st.session_state:
    st.session_state.selected_package_data = pd.DataFrame()

# Sidebar for user input
st.sidebar.title("Open Data Analysis")
keyword = st.sidebar.text_input("Enter a keyword to search for datasets", "incidenti stradali")
search_button = st.sidebar.button("🔍 Search Datasets")

# Logic to handle the search
if search_button:
    # Reset previous search results AND session state
    st.session_state.search_results = []
    st.session_state.selected_packages = []
    st.session_state.all_data = pd.DataFrame()
    st.session_state.analysis_done = False
    st.session_state.selected_package_data = pd.DataFrame()
    
    with st.spinner("Searching for datasets..."):
        try:
            # Initialize services
            ckan_service = CkanApiService()

            # Search for packages based on the keyword
            packages = ckan_service.search_packages(keyword)
            if not packages:
                st.warning("No datasets found for the given keyword.")
            else:
                st.session_state.search_results = packages
                st.success(f"Found {len(packages)} datasets!")
        except Exception as e:
            st.error(f"Error during search: {str(e)}")

# Display search results and allow selection
if st.session_state.search_results:
    st.markdown("---")
    st.header("📋 Search Results")
    
    # Create tabs for different View options
    tab1, tab2 = st.tabs(["List View", "Analyze All"])
    
    with tab1:
        st.subheader("Available Datasets")
        
        # Create a table with search results
        results_data = []
        for idx, pkg in enumerate(st.session_state.search_results):
            results_data.append({
                'Select': idx,
                'Title': pkg.get('title', 'N/A'),
                'Notes': pkg.get('notes', '')[:100] + '...' if pkg.get('notes') else 'No description',
                'Resources': len(pkg.get('resources', []))
            })
        
        results_df = pd.DataFrame(results_data)
        st.dataframe(results_df, use_container_width=True, hide_index=True)
        
        # Selector for individual packages
        st.subheader("🎯 Select Dataset to Analyze")
        
        # Create options with index and title
        package_options = [f"[{idx+1}] {pkg['title']}" for idx, pkg in enumerate(st.session_state.search_results)]
        selected_option = st.selectbox(
            "Choose a dataset:",
            package_options,
            key="package_selector"
        )
        
        analyze_single = st.button("📊 Analyze Selected Dataset")
        
        if analyze_single and selected_option:
            # Extract the actual title from the selected option (remove the index part)
            selected_title = selected_option.split('] ', 1)[1] if '] ' in selected_option else selected_option
            
            # Find the selected package
            selected_package = next(pkg for pkg in st.session_state.search_results if pkg['title'] == selected_title)
            
            with st.spinner(f"Analyzing {selected_title}..."):
                try:
                    data_service = DataService()
                    
                    # Retrieve and process the dataset
                    dataset = data_service.retrieve_dataset(selected_package)
                    
                    if dataset is None or dataset.empty:
                        st.error(f"❌ No CSV data found for this package")
                    else:
                        processed_data = data_service.process_dataset(dataset)
                        
                        if processed_data is None or processed_data.empty:
                            st.error(f"❌ No valid data after processing")
                        else:
                            # Save the selected package data
                            st.session_state.selected_package_data = processed_data
                            processed_data['source_package'] = selected_title
                            
                            # Create analyzer
                            analyzer = IncidentAnalyzer(processed_data)
                            analysis_results = analyzer.analyze()
                            
                            # Display results
                            st.success(f"✅ Analysis completed for: {selected_title}")
                            
                            # Debug: Show what was found
                            if analysis_results.get('has_coordinates'):
                                coords = analysis_results.get('coordinate_columns', [])
                                points = analysis_results.get('total_points_on_map', 0)
                                st.write(f"🔍 Debug - Coordinate columns: {coords}")
                                st.write(f"🔍 Debug - Points on map: {points}")
                                st.write(f"🔍 Debug - Map created: {analysis_results.get('map_created')}")
                            
                            st.subheader("📊 Analysis Results")
                            
                            # Display summary in a readable format
                            st.subheader("Dataset Summary")
                            summary_df = format_summary_results(analysis_results.get('summary', {}))
                            if not summary_df.empty:
                                st.dataframe(summary_df, use_container_width=True, hide_index=True)
                            else:
                                st.info("No summary data available")
                            
                            # Display filtered data results
                            st.subheader("Filter Results")
                            if analysis_results.get('filtered_data'):
                                filtered_df = format_filtered_data(analysis_results.get('filtered_data', {}))
                                if filtered_df is not None:
                                    st.dataframe(filtered_df, use_container_width=True, hide_index=True)
                                else:
                                    st.info("No additional filter information available")
                            else:
                                st.info("ℹ️ No data matched the filter criteria (looking for heavy traffic conditions with multiple vehicles)")
                            
                            # Display map status
                            if analysis_results.get('has_coordinates'):
                                coord_cols = analysis_results.get('coordinate_columns', [])
                                points_count = analysis_results.get('total_points_on_map', 0)
                                st.success(f"🗺️ Geographic data found: {', '.join(coord_cols)} ({points_count} points)")
                            
                            if analysis_results.get('map_created'):
                                st.success(f"✅ Interactive map created with {analysis_results.get('total_points_on_map', 0)} geographic locations")
                            elif analysis_results.get('has_coordinates'):
                                st.warning("⚠️ Coordinates found but map could not be generated (insufficient valid data or coordinate issues)")
                            else:
                                st.info("ℹ️ No geographic coordinates (latitude/longitude) found in this dataset. Map generation skipped.")
                            
                            st.subheader("Full Dataset")
                            st.dataframe(processed_data, use_container_width=True)
                            
                            # Save to CSV
                            os.makedirs(OUTPUT_DIR, exist_ok=True)
                            output_csv_path = os.path.join(OUTPUT_DIR, OUTPUT_CSV_FILE)
                            processed_data.to_csv(output_csv_path, index=False)
                            st.info(f"✅ Data saved to {OUTPUT_CSV_FILE}")
                            
                except Exception as e:
                    st.error(f"Error analyzing package: {str(e)}")
    
    with tab2:
        st.subheader("Analyze All Results")
        analyze_all = st.button("▶️ Process All Datasets", use_container_width=True)
        
        if analyze_all:
            # Reset previous data
            st.session_state.all_data = pd.DataFrame()
            st.session_state.analysis_done = False
            
            with st.spinner("Processing all datasets..."):
                try:
                    # Initialize services
                    data_service = DataService()

                    st.success(f"Found {len(st.session_state.search_results)} datasets. Processing...")

                    # Accumulator for all processed data
                    all_datasets = []
                    success_count = 0
                    
                    # Process each package and analyze the data
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    for idx, package in enumerate(st.session_state.search_results):
                        progress_bar.progress((idx + 1) / len(st.session_state.search_results))
                        status_text.text(f"Processing {idx + 1}/{len(st.session_state.search_results)}: {package['title'][:50]}...")
                        
                        try:
                            # Retrieve and process the dataset
                            dataset = data_service.retrieve_dataset(package)
                            
                            # Check if dataset was retrieved successfully
                            if dataset is None or dataset.empty:
                                st.warning(f"⚠️ No CSV data found for package: {package['title']}")
                                continue
                            
                            processed_data = data_service.process_dataset(dataset)
                            
                            # Check if processed data is valid
                            if processed_data is None or processed_data.empty:
                                st.warning(f"⚠️ No valid data after processing for package: {package['title']}")
                                continue

                            # Add package name column to track data source
                            processed_data['source_package'] = package['title']
                            all_datasets.append(processed_data)
                            success_count += 1

                            # Create analyzer with the processed data
                            analyzer = IncidentAnalyzer(processed_data)
                            
                            # Analyze the processed data
                            analysis_results = analyzer.analyze()

                            # Display results
                            with st.expander(f"✅ {package['title']} ({len(processed_data)} records)"):
                                col1, col2 = st.columns(2)
                                with col1:
                                    st.write("**Summary**")
                                    summary_df = format_summary_results(analysis_results.get('summary', {}))
                                    if not summary_df.empty:
                                        st.dataframe(summary_df, use_container_width=True, hide_index=True)
                                    
                                    # Show geographic data indicator
                                    if analysis_results.get('has_coordinates'):
                                        coord_cols = analysis_results.get('coordinate_columns', [])
                                        points_count = analysis_results.get('total_points_on_map', 0)
                                        st.success(f"🗺️ Geographic: {', '.join(coord_cols)} ({points_count} points)")
                                        if analysis_results.get('map_created'):
                                            st.success("✅ Map created")
                                        else:
                                            st.warning("⚠️ Map generation failed")
                                    else:
                                        st.info("No geographic data")
                                
                                with col2:
                                    st.write("**Filter Results**")
                                    if analysis_results.get('filtered_data'):
                                        filtered_df = format_filtered_data(analysis_results.get('filtered_data', {}))
                                        if filtered_df is not None:
                                            st.dataframe(filtered_df, use_container_width=True, hide_index=True)
                                        else:
                                            st.info("No matches")
                                    else:
                                        st.info("No filtered data")
                                
                                st.write("**Sample Data**")
                                st.dataframe(processed_data.head(10), use_container_width=True)

                        except Exception as e:
                            st.error(f"❌ Error processing package {package['title']}: {str(e)}")
                    
                    status_text.empty()
                    progress_bar.empty()
                    
                    # Combine all datasets and save
                    if all_datasets:
                        combined_data = pd.concat(all_datasets, ignore_index=True)
                        st.session_state.all_data = combined_data
                        st.session_state.analysis_done = True
                        
                        # Save to CSV file
                        os.makedirs(OUTPUT_DIR, exist_ok=True)
                        output_csv_path = os.path.join(OUTPUT_DIR, OUTPUT_CSV_FILE)
                        combined_data.to_csv(output_csv_path, index=False)
                        st.success(f"✅ Processed {success_count} datasets with {len(combined_data)} total records")
                    else:
                        st.warning("❌ No valid data was found in any of the packages.")
                except Exception as e:
                    st.error(f"Error during processing: {str(e)}")

# Divider
st.markdown("---")

# Visual results - Show only if analysis was done in THIS session (not old saved data)
if st.session_state.analysis_done:
    st.header("📈 Results Summary")
    
    # Determine data source and show appropriate indicator
    data_source = "Unknown source"
    display_data = None
    record_count = 0
    
    if st.session_state.analysis_done and not st.session_state.all_data.empty:
        data_source = "Current analysis results (All datasets)"
        display_data = st.session_state.all_data
        record_count = len(display_data)
    elif st.session_state.selected_package_data is not None and not st.session_state.selected_package_data.empty:
        data_source = "Selected dataset analysis"
        display_data = st.session_state.selected_package_data
        record_count = len(display_data)
    
    if display_data is not None and not display_data.empty:
        # Show data source indicator
        st.info(f"📌 Source: **{data_source}** | 📊 Records: **{record_count}**")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📊 Dati Estratti")
            st.dataframe(display_data.head(20), use_container_width=True)
            
            # Add download button
            csv = display_data.to_csv(index=False)
            st.download_button(
                label="📥 Download CSV",
                data=csv,
                file_name=f"analysis_results_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
        
        with col2:
            st.subheader("🗺️ Interactive Map")
            
            # Try multiple possible locations for the map file
            possible_paths = [
                os.path.join(OUTPUT_DIR, MAP_HTML_FILE),  # ./output/mappa_incidenti.html
                os.path.abspath(os.path.join(OUTPUT_DIR, MAP_HTML_FILE)),  # Absolute path
                os.path.join("src", OUTPUT_DIR, MAP_HTML_FILE),  # ./src/output/mappa_incidenti.html
            ]
            
            st.write("🔍 **Debug - Percorsi cercati:**")
            for path in possible_paths:
                exists = os.path.exists(path)
                st.write(f"  - {path}: {'✅ Esiste' if exists else '❌ Non esiste'}")
                if exists:
                    size = os.path.getsize(path)
                    st.write(f"    Dimensione: {size} bytes")
            
            map_loaded = False
            for map_path in possible_paths:
                if os.path.exists(map_path):
                    try:
                        with open(map_path, "r", encoding='utf-8', errors='ignore') as f:
                            map_html = f.read()
                        if map_html.strip():
                            st.success(f"✅ Mappa caricata da: {map_path}")
                            components.html(map_html, height=500)
                            map_loaded = True
                            break
                    except Exception as e:
                        st.warning(f"Errore nel caricare la mappa da {map_path}: {str(e)}")
                        continue
            
            if not map_loaded:
                st.info("ℹ️ Mappa generata per i dataset con coordinate geografiche. Verifica che le coordinate siano presenti e valide.")
    else:
        # Show just the map if no data but map exists
        st.subheader("🗺️ Interactive Map")
        
        # Try multiple possible locations for the map file
        possible_paths = [
            os.path.join(OUTPUT_DIR, MAP_HTML_FILE),  # ./output/mappa_incidenti.html
            os.path.abspath(os.path.join(OUTPUT_DIR, MAP_HTML_FILE)),  # Absolute path
            os.path.join("src", OUTPUT_DIR, MAP_HTML_FILE),  # ./src/output/mappa_incidenti.html
        ]
        
        st.write("🔍 **Debug - Percorsi cercati:**")
        for path in possible_paths:
            exists = os.path.exists(path)
            st.write(f"  - {path}: {'✅ Esiste' if exists else '❌ Non esiste'}")
            if exists:
                size = os.path.getsize(path)
                st.write(f"    Dimensione: {size} bytes")
        
        map_loaded = False
        for map_path in possible_paths:
            if os.path.exists(map_path):
                try:
                    with open(map_path, "r", encoding='utf-8', errors='ignore') as f:
                        map_html = f.read()
                    if map_html.strip():
                        st.success(f"✅ Mappa caricata da: {map_path}")
                        components.html(map_html, height=500)
                        map_loaded = True
                        break
                except Exception as e:
                    st.warning(f"Errore nel caricare la mappa da {map_path}: {str(e)}")
                    continue
        
        if not map_loaded:
            st.info("ℹ️ La mappa sarà visualizzata qui quando analizzerai un dataset con coordinate geografiche.")
elif st.session_state.search_results:
    st.info("ℹ️ Select a dataset and click 'Analyze Selected Dataset' or 'Process All Datasets' to see results here.")
        
# Footer
st.info("Progetto di tesi [ESA] - L8 - Ingegneria Informatica")