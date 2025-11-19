import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
import os
from utils import generer_nom_unique, scrop_desc, completer_url


# ==================== Fonction : Récupération de l'image du stade ====================
def img_stade(path=""):
    """
    Récupère l'URL de l'image d'un stade à partir de la page Wikipedia.
    Ignore les images contenant 'maps' dans leur URL.
    """
    headers = {
    "User-Agent": "MyCAFscraper/1.0 (contact: .com)"
    }
    try:

        res = requests.get(path,headers=headers)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, 'html.parser')
        table = soup.find('table', class_="infobox vcard")
        if not table:
            return ""

        for tr in table.find_all('tr'):
            img = tr.find("img")
            if img and img.has_attr("src"):
                src_text = img["src"]
                if "maps" not in src_text.lower():
                    return completer_url(src_text)
        return ""
    except Exception as e:
        print(f"Erreur inattendue lors du scraping de l'image : {e}")
        return ""


# ==================== Connexion à MongoDB ====================
try:
    client = MongoClient("mongodb://localhost:27017/")
    db = client["CAF"]
    collection = db["Stadium"]
except Exception as e:
    print(f"Erreur de connexion à MongoDB : {e}")
    exit()


# ==================== Création des dossiers nécessaires ====================
os.makedirs("Document/logos_stads", exist_ok=True)
os.makedirs("Document/files_stads", exist_ok=True)


# ==================== Récupération de la page Wikipedia ====================
url = 'https://en.wikipedia.org/wiki/2025_Africa_Cup_of_Nations'
try:
    res = requests.get(url)
    res.raise_for_status()
except Exception as e:
    print(f"Erreur lors du chargement de la page principale : {e}")
    exit()


# ==================== Parsing HTML pour trouver le tableau des stades ====================
soup = BeautifulSoup(res.text, 'html.parser')
table = soup.find('table', class_=lambda x: x and 'wikitable' in x and 'sortable' in x and 'plainrowheaders' in x)

if not table:
    print("Pas de table trouvée avec la classe 'wikitable sortable plainrowheaders'")
    exit()

tbody = table.find('tbody')
if not tbody:
    print("La table n’a pas de corps <tbody>")
    exit()

rows = tbody.find_all('tr')


# ==================== Parcours des lignes du tableau ====================
for row in rows:
    try:
        th = row.find('th')
        tds = row.find_all('td')

        # Ignorer les lignes d'en-tête ou incomplètes
        if not th or not tds or th.get_text(strip=True) == "City":
            continue

        # Extraction des données principales
        stad_city = th.get_text(strip=True)
        stad_name = tds[0].get_text(strip=True)
        Capacity_stad = tds[1].get_text(strip=True)

        # Génération et stockage de la description
        path_desc = generer_nom_unique("file", ".txt", "Document/files_stads")
        with open(path_desc, 'w', encoding='utf-8') as f:
            f.write(scrop_desc(completer_url(tds[0].find('a').get('href')), 1))

        # Récupération de l'image du stade
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        img_url = img_stade(completer_url(tds[0].find('a').get('href')))
        if img_url:
            img_data = requests.get(img_url, headers=headers).content
            path_img = generer_nom_unique("logo", "jpg", "Document/logos_stads")
            with open(path_img, 'wb') as f:
                f.write(img_data)
        else:
            path_img = None

        # Préparation des données pour MongoDB
        data = {
            'logo': path_img,
            'name': stad_name,
            'description': path_desc,
            'City': stad_city,
            'localisation':"",
            'Capacity': Capacity_stad
        }

        # Insertion dans MongoDB
        collection.insert_one(data)

    except Exception as e:
        print(f"Erreur lors du traitement d’une ligne : {e}")
        continue
