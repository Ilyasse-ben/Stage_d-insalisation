from bs4 import BeautifulSoup
import requests
from pymongo import MongoClient
from datetime import datetime
import re

# ==================== CONFIGURATION MONGODB ==================== #
try:
    client = MongoClient("mongodb://localhost:27017/")
    db = client['CAF']  # Base de données
    collection_match = db['Match']
    collection_equipe = db['Team']
    collection_stade = db['Stadium']  # Correction de nom pour cohérence
except Exception as e:
    print(f"Problème de connexion à MongoDB: {e}")
    exit()

# ==================== CONFIGURATION SCRAPING ==================== #
url = "https://en.wikipedia.org/wiki/2025_Africa_Cup_of_Nations"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

# ==================== FONCTIONS UTILITAIRES ==================== #
def correction_date(date_str):
    # Supprimer le contenu entre parenthèses
    date_str_clean = re.sub(r"\(.*?\)", "", date_str)
    # Supprimer les caractères indésirables
    date_str_clean = date_str_clean.replace("�", "").strip()
    # Conversion en date
    try:
        date_obj = datetime.strptime(date_str_clean, "%d %B %Y")
        return date_obj.date()
    except ValueError as e:
        print(f" Erreur de conversion date '{date_str_clean}': {e}")
        return None


def extraire_matchs(blocs_html):
    """
    Extrait la liste des matchs depuis des balises HTML de Wikipédia.
    Retourne une liste de dictionnaires contenant les infos du match.
    """
    matchs_info = []

    for bloc in blocs_html:
        # --- Informations date et heure ---
        date_div = bloc.find('div', class_="fleft")
        if not date_div:
            continue
        date_match = correction_date(date_div.find('div', class_="fdate").get_text())
        heure_match = date_div.find('div', class_="ftime").get_text()

        # --- Équipes ---
        table_teams = bloc.find('table', class_="fevent")
        equipes = table_teams.find_all('a') or table_teams.find_all('span', itemprop="name")
        equipe1 = equipes[0].get_text() if len(equipes) > 0 else None
        equipe2 = equipes[1].get_text() if len(equipes) > 1 else None

        # --- Stade ---
        stade_div = bloc.find('div', class_="fright")
        stade_nom = stade_div.find('a').get_text() if stade_div else None

        matchs_info.append({
            'date': date_match,
            'time': heure_match,
            'team1': equipe1,
            'team2': equipe2,
            'stadium': stade_nom
        })

    return matchs_info


def recuperer_id(collection, champ, valeur):

    doc = collection.find_one({champ: valeur})
    return doc["_id"] if doc else valeur

# ==================== ETAPE 1 : RÉCUPÉRATION PAGE HTML ==================== #
try:
    res = requests.get(url, headers=headers)
    res.raise_for_status()
except Exception as e:
    print(f" Problème lors du chargement de la page: {e}")
    exit()

# ==================== ETAPE 2 : PARSING HTML ==================== #
soup = BeautifulSoup(res.text, "html.parser")
blocs_matchs = soup.find_all('div', class_="footballbox")

# Extraction des données
matchs = extraire_matchs(blocs_matchs)

# ==================== ETAPE 3 : INSERTION DANS MONGODB ==================== #
for match in matchs:
    if not match['date'] or not match['team1'] or not match['team2']:
        continue  # On ignore les données incomplètes

    # Récupération des ObjectId pour les équipes et le stade
    id_team1 = recuperer_id(collection_equipe, "name", match['team1'])
    id_team2 = recuperer_id(collection_equipe, "name", match['team2'])
    id_stade = recuperer_id(collection_stade, "name", match['stadium'])

    # Conversion heure/minute
    try:
        heure, minute = map(int, match["time"].split(":"))
    except ValueError:
        heure, minute = 0, 0  # Valeur par défaut si parsing échoue

    # Préparation des données MongoDB
    doc_match = {
        'team1': id_team1,
        'team2': id_team2,
        'stade': id_stade,
        'date': datetime.combine(match["date"], datetime.min.time()).replace(hour=heure, minute=minute),
    }

    # Insertion dans MongoDB
    collection_match.insert_one(doc_match)

print(" Importation terminée avec succès dans MongoDB.")

