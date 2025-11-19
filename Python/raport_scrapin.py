import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
from utils import completer_url

def find_rapport(team1, team2):
    """
    Recherche le lien du rapport de match entre deux équipes
    dans la page Wikipedia de la CAN 2025.
    
    :param team1: Nom de la première équipe
    :param team2: Nom de la deuxième équipe
    :return: URL du rapport de match ou None si introuvable
    """

    # =============================== URL Wikipédia ===============================
    url = "https://en.wikipedia.org/wiki/2024_Africa_Cup_of_Nations"
    headers = {
        "User-Agent": "CAF2025Scraper/1.0 (contact: tonemail@example.com)"
    }

    # =============================== Requête HTTP ===============================
    try:
        res = requests.get(url, headers=headers, timeout=10)
        res.raise_for_status()
    except Exception as e:
        print(f"❌ Erreur lors du chargement de la page : {e}")
        return None

    # =============================== Parsing HTML ===============================
    soup = BeautifulSoup(res.text, 'html.parser')
    blocs_matchs = soup.find_all('div', class_="footballbox")

    # =============================== Analyse des matchs ===============================
    for bloc in blocs_matchs:
        equipes = []  # On recrée la liste pour chaque bloc

        # --- Trouver la table des équipes ---
        table_teams = bloc.find('table', class_="fevent")
        if not table_teams:
            continue

        # --- Récupérer les équipes (spans avec itemprop="name") ---
        tr_team = table_teams.find('tr', itemprop="name")
        if not tr_team:
            continue

        span_teams = tr_team.find_all('span', itemprop="name")
        for span in span_teams:
            equipe_nom = span.find('a').get_text(strip=True)
            equipes.append(equipe_nom)

        # --- Vérifier si le match correspond à team1 vs team2 ---
        if team1 in equipes and team2 in equipes:
            tr_rapport = table_teams.find('tr', class_="fgoals")
            if not tr_rapport:
                return None

            td_rapport = tr_rapport.find('td', class_="")
            if not td_rapport:
                return None

            # --- Retourner le lien du rapport si disponible ---
            lien = td_rapport.find('a')
            if lien:
                return lien.get("href")

            return None

    # Aucun match trouvé
    return None

    #============================== connextion a mongosdb ==================
try:
        client=MongoClient("mongodb://127.0.0.1:27017/")
        db=client['CAF']
        collection_match=db['Match']
        collection_team=db['Team']
except Exception as e:
        print(f"he has a problem in connextion a data basse: {e}")
        exit()
    
for match in collection_match.find():
        tm1=collection_team.find_one({"_id":match['team1']})
        tm2=collection_team.find_one({"_id":match['team2']})
        matche_id=match['_id']
        if tm1 or tm2:
            link_rapport=find_rapport(tm1['name'],tm2['name'])
            if link_rapport:
                collection_match.update_one({'_id':matche_id},{'$set':{'raport':completer_url(link_rapport)}})

        


