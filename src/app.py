"""
Interface for the application.
This module defines the main application class that orchestrates the workflow of retrieving, 
processing, and analyzing open data from dati.gov.it. It manages the complete process, from package search to results visualization,
including error handling to ensure that the application continues to run even if some steps fail
"""
import streamlit as st
import pandas as pd
import os
import sys
from analyzer import IncidentAnalyzer
from services import DataService, CkanApiService

# Define th route for the application
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)
    
# Configuration of the Streamlit application
st.set_page_config(page_title="Open Data Analysis", layout="wide")

st.title("Open Data Analysis - dati.gov.it")
st.markdown("Transform your open data into actionable insights with our comprehensive analysis tool")

# Sidebar for user input
st.sidebar.title("Open Data Analysis")
keyword = st.sidebar.text_input("Enter a keyword to search for datasets", "incidenti stradali")
run_analysis = st.sidebar.button("Search and Analyze")

# Logic to handle the search and analysis process
if run_analysis:
    with st.spinner("Searching for datasets..."):
        try:
            # Initialize services
            ckan_service = CkanApiService()
            data_service = DataService()
            analyzer = IncidentAnalyzer()

            # Search for packages based on the keyword
            packages = ckan_service.search_packages(keyword)
            if not packages:
                st.warning("No datasets found for the given keyword.")
                st.stop()

            st.success(f"Found {len(packages)} datasets. Processing...")

            # Process each package and analyze the data
            for package in packages:
                try:
                    # Retrieve and process the dataset
                    dataset = data_service.retrieve_dataset(package)
                    processed_data = data_service.process_dataset(dataset)

                    # Analyze the processed data
                    analysis_results = analyzer.analyze(processed_data)

                    # Display results
                    st.subheader(f"Analysis for {package['title']}")
                    st.write(analysis_results)

                except Exception as e:
                    st.error(f"Error processing package {package['title']}: {str(e)}")
        except Exception as e:
            st.error(f"Error during search: {str(e)}")

    st.balloons()
 
# Final message after processing all packages
st.success("Analysis completed for all datasets.")

# Visual results
col1,col2 = st.columns(2)
with col1:
    st.subheader("📊 Dati Estratti")
    if os.path.exists("output/output.csv"):
        df_visual = pd.read_csv("output/output.csv")
        st.dataframe(df_visual.head(10)) # Display only the first 10 rows for better readability
    else:
        st.warning("No data available to display. Please run the analysis first.")

with col2:
    st.subheader("🗺️ Interactive Map")
    if os.path.exists("output/mappa_incidenti.html"):
        with open("output/mappa_incidenti.html", "r") as f:
            map_html = f.read()
        st.components.v1.html(map_html, height=500)    
    else:
        st.warning("No map available to display. Please run the analysis first.")
        
# Footer
st.info("Progetto di tesi [ESA] - L8 - Ingegneria Informatica")