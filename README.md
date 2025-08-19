# AnalisiOpenData

## Description
> Progetto che implemanta lo sviluppo di un software in linguaggio Pythone per l'estrapolazione di open data dal portale ufficiale di ricerca dati.gov.it

## Main Features
 - Visualizzazione della lista completa di tutti i dati presenti sul portale;
 - Sistema di filtraggio tramite parola chiave;
 - Analisi finale e visualizzazione mappa;

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
- Utilizzabile solo su dati che contengono file json e csv, unica versione.

## Usage
- Esempio esplicativo già presente nel codice
```bash
python main.py
```

## Project Structure
- /AnalisiOpenData.py
  Il file principale del programma, che probabilmente contiene la logica per l’analisi dei dati open data.

- /README.md
  Il file di documentazione, dove sarà descritta la struttura e il funzionamento del progetto.
  
- /DatiGovIt.json,
  /DatiGovItFiltrati.json,
  /DatiSelezionati.json
  Diversi file di dati in formato JSON, utilizzati per l’elaborazione e filtraggio delle   informazioni.
  
- /Condizioni.xlsx,
  /ouput.xlsx,
  /output.csv
  File di dati in formato Excel e CSV, probabilmente per input, output e condizioni dell’analisi.

- /mappa_incidenti.html
  Un file HTML che potrebbe rappresentare una visualizzazione dei dati analizzati su una mappa.

-/LICENSE
 /.gitignore
 File di configurazione e licenza.

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
