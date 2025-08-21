"""
Applicazione per l'analisi degli Open Data
Autore: 1ESA1
Data: 2024-01-01
Versione: 1.0

Descrizione:
Questa applicazione consente di recuperare, filtrare e analizzare i dati disponibili su dati.gov.it.
Utilizza le API CKAN per ottenere la lista dei pacchetti e permette di selezionare e visualizzare i dati in formato CSV ed Excel.
Inoltre, fornisce funzionalità di visualizzazione geografica tramite Folium.    
"""
import requests
import pandas as pd
import json
from io import StringIO

# Controllo risposta ottenuta dalla richiesta effettuata
def get_data_from_url(url):
    response = requests.get(url)
    if response.status_code == 200:
        data = response.content.decode('utf-8')
        df = pd.read_csv(StringIO(data))
        return df
    else:
        print(f"Errore durante il recupero dei dati: {response.status_code}")
        return None
    
# URL dell'API CKAN, con metodo package_list, importa lista dei pacchetti su Python 
url  = "https://dati.gov.it/opendata/api/3/action/package_list"

# Richiesta GET  all'URL per ottenere i pacchetti
response = requests.get(url)

# Conversione risposta alla richiesta in formato JSON in dizionario comprensibile da Python
data = json.loads(response.text) 

# Visualizzare tipo dizionario memorizzato nella variabile
type(data)  

# Formattazione informazioni ottenute in tipo json
text = json.dumps(data, sort_keys = True, indent = 4) 

# Creazione file di tipo json per lettura comprensibile della lista dati disponibili
with open("DatiGovIt.json", "w") as f:
    f.write(text) 

# Utilizzo di uan parola chiave per filtrare dati
word_key = input("Inserire una parola chiave per filtrare i dati: ")

# Apertura file e caricamento dati
with open("DatiGovIt.json", "r") as f:
    data = json.load(f)

# Ottieni la lista di stringhe dalla chiave 'result' e filtraggio lista con parola chiave
lista_stringhe = data['result']
lista_filtrata = [s for s in lista_stringhe if word_key in s]

#Controlla se la lista filtrata è vuota e restituisce
#un messaggio altrimenti crea una lista dati filtrata
if not lista_filtrata:
    print(f"Nessun risultato trovato per la parola chiave '{word_key}'")
else:
    # Salva la lista filtrata in un nuovo file json
    with open("DatiGovItFiltrati.json", "w") as f:
        json.dump(lista_filtrata, f, indent=4)

# Inserimento con input da tastiera dati selezionati e Apertura URL specifico 
#dalla lista DatiFiltrati
datiselezionati = input("Inserisci il nome del dato che desideri selezionare: ")

# URL dell'API CKAN, con metodo package_show, visualizza dettagli pacchetti specifici
url = f"https://dati.gov.it/opendata/api/3/action/package_show?id={datiselezionati}"

# Richiesta GET  all'URL per ottenere i pacchetti ( con selezione parametri se necessaria)
response = requests.get(url)

#Controllo che la risposta ricevuta dal server sia corretta altrimeti exit
if response.status_code != 200:
    print(f"Errore durante il recupero dei dati: {response.status_code}")
    exit()

# Conversione della risposta richiesta in formato JSON per dizionario comprensibile da Python
data1 = json.loads(response.text) 

# Formattazione informazioni ottenute in tipo json
text = json.dumps(data1, sort_keys=True, indent=4) 

# Visualizzare tipo dizionario memorizzato nella variabile
type(data1) 

# Creazione file di tipo json per lettura comprensibile della lista dati disponibili
with open("DatiSelezionati.json", "w") as f:
    f.write(text) 

# Tranformazione file json in un DataFrame pandas per manipolazione dati
pd.set_option("display.max_columns", None)

# Assegna il risultato alla variabile df
df = pd.json_normalize(data1['result'])

# Apertura file e caricamento dati
with open("DatiSelezionati.json", "r") as f:
    data = json.load(f)

# Inizializza l'URL come una stringa vuota
url = ""

# Itera su ogni risorsa nella lista 'resources' finchè il formato termina con .csv
for resource in data['result']['resources']:
    print(resource)
    if resource['format'] == 'CSV' and resource['url'].endswith('.csv'):
        url = resource['url']
        break
# Sè url è uguale alla risposta ottenuta salva i dati altrimenti stampa errore
if url:
    df = get_data_from_url(url) 
    if df is not None:
        df.to_csv('output.csv', index=False)
        print("Dati salvati in output.csv")
else:
    print("Nessun URL di file CSV trovato.")

# Se url non è uguale alla risposta ottenuta, inserire manualmente URL file
if not url:
    url = input("Inserisci l'URL del file CSV manualmente: ")
    df = get_data_from_url(url)
    if df is not None:
        df.to_csv("output.csv", index=False)
        print("Dati salvati in output.csv") 

        #Salva il DataFrame in un secondo file Excel
        df.to_excel('output.xlsx', index=False)
        print("Dati salvati in output.xlsx")
else:
    print(f"Errore durante il recupero dei dati: {response.status_code}")

Condizioni = df[(df[ 'Condizioni traffico'] == 'Intenso') & (df['N. veicoli coinvolti'] > 2)]

Condizioni = Condizioni.dropna(axis=1, how='all')

Condizioni.to_excel('Condizioni.xlsx', index=False)

# Importa la libreria folium
import folium

# Crea una mappa centrata sulla media delle coordinate
mappa_incidenti = folium.Map(location=[Condizioni['Latitudine'].mean(), Condizioni['Longitudine'].mean()], zoom_start=13)

# Aggiungi un marcatore per ogni punto di incidente
for idx, riga in Condizioni.iterrows():
    folium.Marker([riga['Latitudine'], riga['Longitudine']]).add_to(mappa_incidenti)

# Visualizza la mappa
mappa_incidenti.save('mappa_incidenti.html')
