import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()
# Paramètres de l'API
API_KEY = os.getenv("API_KEY")
CONTRACT_NAME = "lyon"
OUTPUT_FILE = "velo_lyon.json"

# URL de l'API
url = f"https://api.jcdecaux.com/vls/v1/stations?contract={CONTRACT_NAME}&apiKey={API_KEY}"

def fetch_data_and_save():
    try:
        response = requests.get(url)
        response.raise_for_status()
        stations = response.json()

        # save station en JSON
        with open(OUTPUT_FILE, "w") as f:
            for station in stations:
                json.dump(station, f)
                f.write("\n")

        print(f"Données sauvegardées dans {OUTPUT_FILE} ({len(stations)} stations).")

    except Exception as e:
        print(f"Erreur : {e}")

if __name__ == "__main__":
    fetch_data_and_save()