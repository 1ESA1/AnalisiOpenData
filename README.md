# AnalisiOpenData

## Description
> Project implementing the development of software in Python for extracting open data from the official search portal dati.gov.it

## Main Features
 - Display of the complete list of all data available on the portal;
 - Filtering system using keywords;
 - Final analysis and map visualization;

## Installation
Instructions to install the project:
```bash
git clone https://github.com/1ESA1/AnalisiOpenData.git
cd AnalisiOpenData
```

## Requirements
- Python 3
- Main dependencies (requests, pandas)
- Other required software (json, folium)
- Usable only with data containing JSON and CSV files, single version.

## Usage
- Explanatory example already present in the code
```bash
python main.py
```

## Project Structure
- /AnalisiOpenData.py  
  The main program file, which likely contains the logic for open data analysis.

- /README.md  
  The documentation file, describing the structure and operation of the project.
  
- /DatiGovIt.json,  
  /DatiGovItFiltrati.json,  
  /DatiSelezionati.json  
  Various data files in JSON format, used for processing and filtering information.
  
- /Condizioni.xlsx,  
  /ouput.xlsx,  
  /output.csv  
  Data files in Excel and CSV format, probably for input, output, and analysis conditions.

- /mappa_incidenti.html  
  An HTML file that could represent a visualization of the analyzed data on a map.

- /LICENSE  
  /.gitignore  
  Configuration and license files.

## Contributing
Guidelines for those who wish to contribute:

- Open an Issue

  Before opening a new issue, check that it has not already been reported.
  Clearly describe the problem, the expected behavior, and the actual behavior.
  If possible, attach screenshots, logs, or code examples that help clarify the issue.

- Propose a Pull Request

  Fork the repository and create a new branch for your changes.
  Make sure your code is well formatted and does not introduce errors.
  Clearly describe the changes in the Pull Request message.
  Link the Pull Request to an Issue, if relevant.
  Respond to comments and review requests from maintainers.

- Coding Standards

  Follow the project's style conventions (e.g. PEP8 for Python).
  If you modify existing features, make sure everything continues to work correctly.
  Update the documentation, if necessary.

- Testing

  If possible, add tests that cover the new features or fixes.
  Make sure all existing tests continue to pass.

- Discussion

  For questions or proposals, open a discussion in the Issues section.

## License
This project is distributed under the [Apache License 2.0](http://www.apache.org/licenses/LICENSE-2.0).

## Authors
The project was developed by:
- [1ESA1](https://github.com/username)

—--
