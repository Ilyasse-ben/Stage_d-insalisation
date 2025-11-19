import requests
from bs4 import BeautifulSoup
import datetime
import random
import string
from pymongo import MongoClient
import os
from utils import generer_nom_unique, scrop_desc, completer_url
# =============== Connexion à MongoDB ===============
try:
    client = MongoClient("mongodb://localhost:27017/")
    db = client["CAF"]
    collection = db["Team"]
except Exception as e:
    print(f"Erreur de connexion à MongoDB : {e}")
    exit()

# =============== Création des dossiers si nécessaires ===============
os.makedirs("Document/logos_Equipes", exist_ok=True)
os.makedirs("Document/files_Equipes", exist_ok=True)

# =============== Récupération de la page Wikipedia principale ===============
url = 'https://en.wikipedia.org/wiki/2025_Africa_Cup_of_Nations'
try:
    res = requests.get(url)
    res.raise_for_status()
except Exception as e:
    print(f"Erreur lors du chargement de la page principale : {e}")
    exit()

# =============== Parsing de la page HTML ===============
soup = BeautifulSoup(res.text, 'html.parser')
table = soup.find('table', class_=lambda x: x and 'wikitable sortable' in x)
if not table:
    print("Pas de table trouvée avec la classe 'wikitable sortable'")
    exit()

tbody = table.find('tbody')
if not tbody:
    print("La table n’a pas de corps <tbody>")
    exit()

rows = tbody.find_all('tr')

# =============== Parcours des lignes du tableau ===============
for row in rows:
    try:
        cell = row.find('td')
        if cell is None:
            continue

        # Récupération de l’image (logo)
        img = cell.find('img')
        if img:
            img_url = completer_url(img.get('src'))
            img_data = requests.get(img_url).content
            path_img = generer_nom_unique("logo", "jpg", "Document/logos_Equipes")
            with open(path_img, 'wb') as f:
                f.write(img_data)
        else:
            path_img = False

        # Nom de l'équipe et lien vers la page détaillée
        a = cell.find('a')
        team_link=''
        if a:
            equipe_name = a.get_text(strip=True)
            team_link = completer_url(a.get('href')) 

        # Description depuis la page de l'équipe
        path_desc = generer_nom_unique("file", ".txt", "Document/files_Equipes")
        description = scrop_desc(team_link)
        with open(path_desc, 'w', encoding='utf-8') as f:
            f.write(description)

        # Préparation des données à insérer
        data = {
            'logo': path_img,
            'name': equipe_name,
            'description': path_desc,
            'team_link':team_link,
            'etat': 1,
        }

        # Suppression éventuelle d’un _id existant
        if '_id' in data:
            del data['_id']

        # Insertion dans MongoDB
        collection.insert_one(data)

    except Exception as e:
        print(f"Erreur lors du traitement d’une ligne : {e}")
        continue
