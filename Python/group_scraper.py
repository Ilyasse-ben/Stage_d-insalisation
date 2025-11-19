import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
def est_tableau_groupe(table_html):
    """Vérifie si le tableau contient les en-têtes d'un classement de groupe."""
    entetes_requises = ["Pos", "Team", "Pld", "W", "D", "L", "GF", "GA", "GD", "Pts"]
    entetes_table = [th.get_text(strip=True) for th in table_html.find_all('th')]

    # Vérifie que chaque en-tête requis est présent dans le tableau
    return all(entete in entetes_table for entete in entetes_requises)


def extraire_infos_group(groupe_name, table_html):
    """
    Extrait les infos d'un tableau de groupe (Wikipedia)
    et retourne une liste de dictionnaires avec équipe + stats.
    """
    resultats = []
    rows = table_html.find_all('tr')[1:]  # on saute l'en-tête

    for row in rows:
        cols = row.find_all('td')
        if not cols or len(cols) < 9:  # sécurité si ligne vide ou mal formée
            continue

        position = cols[0].get_text(strip=True)
        equipe_name = row.find('th').get_text(strip=True) if row.find('th') else ""
        pld = cols[1].get_text(strip=True)  # matches joués
        w = cols[2].get_text(strip=True)    # victoires
        d = cols[3].get_text(strip=True)    # nuls
        l = cols[4].get_text(strip=True)    # défaites
        gf = cols[5].get_text(strip=True)   # buts marqués
        ga = cols[6].get_text(strip=True)   # buts encaissés
        gd = cols[7].get_text(strip=True)   # différence
        pts = cols[8].get_text(strip=True)  # points

        resultats.append({
        "team": equipe_name,
        "group": groupe_name,
        "position": position,
        "matches_played": pld,
        "wins": w,
        "draws": d,
        "losses": l,
        "goals_for": gf,
        "goals_against": ga,
        "goal_difference": gd,
        "points": pts
    })

    return resultats
# Connexion à MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["CAF"]
collection = db["Team"]
# ===================== URL Wikipédia =====================
url = "https://en.wikipedia.org/wiki/2025_Africa_Cup_of_Nations"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}
try:
    res = requests.get(url, headers=headers)
    res.raise_for_status()
except Exception as e:
    print(f"Erreur lors du chargement de la page : {e}")
    exit()

# ===================== Parsing HTML =====================
soup = BeautifulSoup(res.text, "html.parser")
# Exemple d'utilisation après avoir fait soup = BeautifulSoup(page_html, 'html.parser')
groupes = ["A", "B", "C", "D","E","F"]
tables = soup.find_all("table", class_="wikitable")  # à adapter si autre classe

for  i in range(6):
    data_group = extraire_infos_group(groupes[i], tables[i+3])
    for equipe in data_group:
        # Ajouter un champ "group" à un document qui a le nom "Morocco"
        name_team=equipe['team'].replace("(H)","")
        del equipe['team']
        collection.update_one(
            {"name": {"$regex":name_team, "$options": "i" }},   # Filtre : document à modifier
            {"$set": {"group": equipe}}  # Nouveau champ à ajouter ou mettre à jour
        )
