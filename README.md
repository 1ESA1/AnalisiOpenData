# 🚀 AnalisiOpenData - Open Data Analyzer

## 📋 Description
> Python software development project for analyzing and extracting open data from the official dati.gov.it search portal.

## ✨ Main Features
- 🔍 **Search and filtering** of available datasets
- 📊 **Automatic download and analysis** of CSV data
- 🗺️ **Geographic visualization** of road accidents
- 📈 **Export** to CSV and Excel formats
- 🏗️ **Modular architecture** well organized
- 🧪 **Complete test suite** for validation
- ⚙️ **Centralized configuration** for easy maintenance

## 🚀 Installation
Installation instructions:
```bash
git clone https://github.com/1ESA1/AnalisiOpenData.git
cd AnalisiOpenData
```

## 📋 Requirements
- Python 3.6 or higher
- Main dependencies: `requests`, `pandas`, `folium`
- Support files: JSON and CSV management
- Compatible with datasets in JSON and CSV format

## 🎯 Usage

### **Streamlit Web Application (Recommended) ⭐**
```bash
cd src
streamlit run app.py
```

**Local Access (Same Machine):**
```
http://localhost:8501
```

**Deploy to Streamlit Cloud (External Users) 🌐**
1. Create a GitHub repository with your project
2. Sign up at [streamlit.io/cloud]
3. Click "New app" and select your repository
4. Share the public URL with users worldwide

**🚀 App Live: Public URL**
```
https://brluhecnkuvhp99tuzhzv3.streamlit.app/
```
Click the link above to access the live application!

**Features:**
- 🔍 Interactive dataset search with keyword filtering
- 📋 Browse and select datasets from dati.gov.it
- 📊 Analyze individual datasets or process all results
- 🗺️ View interactive maps for geographic data
- 📥 Download analysis results as CSV
- 📈 View data summaries and statistics

### **Modular Version CLI (Recommended)**
```bash
cd src
python main.py
```

### **Original Version (Compatibility)**
```bash
cd src
python AnalisiOpenData.py
```

### **Application Testing**
```bash
# Run all tests
cd tests
python run_unified_tests.py

# Specific tests
python test_config.py      # Configuration tests
python test_unified.py     # Unified tests
python test_utils.py       # Utility tests
```

## ⚙️ Features
1. **🔍 Dataset Search**: Enter a keyword to filter available datasets
2. **📋 Dataset Selection**: Choose the desired dataset from the filtered list
3. **⬇️ Automatic Download**: The system automatically downloads CSV data
4. **📊 Accident Analysis**: If available, analyzes road accident data
5. **🗺️ Visualization**: Creates interactive maps of accidents

## 📁 Output
- **`data/`**: JSON files with dataset metadata
- **`output/`**: Output files (CSV, Excel, HTML maps)
  - `🗺️ mappa_incidenti.html` - Interactive map
  - `📊 output.xlsx` - Excel report
  - `📄 output.csv` - Data exported to CSV

## 🏆 Improvements Implemented
1. **🔧 Separation of Concerns**: Each module has specific role
2. **📦 Modular Architecture**: Independent and reusable components
3. **⚙️ Configuration Management**: Centralized settings
4. **🛡️ Error Handling**: Robust error handling
5. **🧪 Test-Driven**: Complete test suite for validation
6. **📝 Documentation**: Detailed documentation
7. **🔄 Backward Compatibility**: Legacy code maintained

### 📊 Implemented Improvements
- ✅ **Separation of responsibilities** into modules
- ✅ **Robust error handling** with exception management
- ✅ **Centralized configuration**
- ✅ **Improved user interface**
- ✅ **Code documentation**
- ✅ **Data validation**
- ✅ **Automatic directory management**
- ✅ **Complete test suite**

## ✨ Latest Updates

### **New Streamlit Web Application v2.0** 🎉
- ✅ **Interactive Web Interface**: Modern Streamlit-based UI for easy data exploration
- ✅ **Advanced Search**: Filter datasets by keyword from dati.gov.it
- ✅ **Batch Processing**: Analyze all search results simultaneously
- ✅ **Enhanced Maps**: Intelligent coordinate detection (latitude/longitude variations)
- ✅ **CSV Analysis Tools**: Automatic CSV separator detection
- ✅ **Live Statistics**: Real-time data summaries and metrics
- ✅ **Download Support**: Export analyzed data as CSV files
- ✅ **Progress Tracking**: Visual progress bars for batch operations

### **Analyzer Module Enhancements**
- ✅ **Flexible Coordinate Detection**: Supports multiple column naming conventions:
  - Latitude: `latitudine`, `latitude`, `lat`, `y_coord`, `y`
  - Longitude: `longitudine`, `longitude`, `lon`, `x_coord`, `x`
- ✅ **Multi-Dataset Maps**: Create comprehensive geographic visualizations
- ✅ **Enhanced Error Messages**: Detailed debug information for troubleshooting
- ✅ **Data Analysis Pipeline**: Complete automatic analysis workflow

### **Data Service Improvements**
- ✅ **CSV Separator Detection**: Auto-detect `,`, `;`, `\t`, `|` separators
- ✅ **Dataset Retrieval**: Integrated methods for package data extraction
- ✅ **Data Cleaning**: Automatic duplicate removal and validation
- ✅ **Resource Management**: Proper handling of multiple file formats

## 🏗️ Project Structure

### **Module Architecture**
```
AnalisiOpenData/
│
├── 📁 src/                   # Modular source code
│   ├── 🎯 main.py              # Main control
│   ├── ⚙️ config.py              # Centralized configuration (URLs, paths, constants)
│   ├── 🔌 services.py            # API and data services
│   ├── 📄 file_manager.py        # File I/O management (JSON, CSV, Excel)
│   ├── 📊 analyzer.py            # Accident analysis
│   ├── 💬 ui.py                  # User interface
│   └── 📜 AnalisiOpenData.py     # Original code (backup)
│
├── 🧪 tests/                 # Complete test suite
│   ├── 📄 base_test.py           # Base tests
│   ├── 📄 test_config.py         # Configuration tests
│   ├── 📄 test_unified.py        # Unified tests
│   ├── 📄 test_utils.py          # Test utilities
│   └── 🏃 run_unified_tests.py   # Unified test runner
│
├── 📊 data/                  # Input data
│   ├── 📊 Condizioni.xlsx        # Weather conditions
│   ├── 📄 DatiGovIt.json         # Raw data from data.gov.it
│   ├── 📄 DatiGovItFiltrati.json # Filtered data
│   └── 📄 DatiSelezionati.json # Data selected for analysis
│
├── 📈 output/                # Generated output files
│   ├── 🗺️ mappa_incidenti.html   # Interactive map
│   ├── 📊 output.xlsx             # Excel report
│   └── 📄 output.csv             # Data exported to CSV
│
├── 📖 README.md              # Complete documentation
└── 📄 LICENSE                # Apache 2.0 License
```

## 🎯 Advantages of the New Organization

### **Test Separation ✅**
- ✅ Tests isolated in dedicated directory
- ✅ Do not interfere with production code
- ✅ Facilitates maintenance and development
- ✅ Follow Python best practices

### **Modular Architecture ✅**
- ✅ Each module has specific responsibility
- ✅ Reusable and testable code
- ✅ Easy debugging and maintenance
- ✅ Extensible for future features

### **Complete Test Coverage ✅**
- ✅ Tests for configuration and utilities
- ✅ Import and structure tests
- ✅ Component functionality tests
- ✅ Complete integration tests

## 📊 Successfully Completed Tests
- ✅ **Modules**: 6/6 source files validated
- ✅ **Configuration**: Working settings tests  
- ✅ **Functionality**: Core components tested
- ✅ **Integration**: Complete system validated

## 🧪 Testing

### **Run All Tests**
```bash
cd tests
python run_unified_tests.py
```

### **Individual Tests**
```bash
cd tests
python test_config.py      # Configuration tests
python test_unified.py     # Unified tests
python test_utils.py       # Utility tests
```

### **Project Structure Verification**
```bash
# Display project structure
tree -I '__pycache__'

# Check main files
ls -la src/
ls -la tests/
ls -la data/
ls -la output/
```

## 🤝 Contributing
Guidelines for those who wish to contribute:

### **Opening an Issue**
- Before opening a new issue, verify that it has not already been reported
- Clearly describe the problem, expected behavior and actual behavior
- If possible, attach screenshots, logs or code examples that help clarify the issue

### **Proposing a Pull Request**
- Fork the repository and create a new branch for your changes
- Make sure your code is well formatted and doesn't introduce errors
- Clearly describe the changes in the Pull Request message
- Link the Pull Request to an Issue, if relevant
- Respond to comments and review requests from maintainers

### **Coding Standards**
- Follow the project's style conventions (e.g. PEP8 for Python)
- If you modify existing functionality, make sure everything continues to work correctly
- Update documentation, if necessary

### **Testing**
- If possible, add tests that cover new functionality or fixes
- Make sure all existing tests continue to pass

### **Discussion**
- For questions or proposals, open a discussion in the Issues section

## 📝 Notes on Improvements

### **Applied Structural Corrections:**
- ✅ Updated file structure to reflect project reality
- ✅ Corrected test commands to use actually present files
- ✅ Updated module and component counts
- ✅ Improved documentation of data and output directories

### **Observations:**
- 📋 The file `ouput.xlsx` in `/output/` contains a spelling error in the name
- 🔧 Tests could be extended to cover more use cases
- 📚 Documentation can be enriched with practical examples

## 📄 License
This project is distributed under the [Apache 2.0 License](http://www.apache.org/licenses/LICENSE-2.0).

## 👨‍💻 Authors
The project was developed by:
- [1ESA1](https://github.com/1ESA1)
