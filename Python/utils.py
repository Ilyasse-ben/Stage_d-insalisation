import datetime
import random
import string
import requests
from bs4 import BeautifulSoup
# =============== Fonction pour générer un nom de fichier unique ===============
def generer_nom_unique(prefixe="fichier", extension="", dosser=""):
    horodatage = datetime.datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    aleatoire = ''.join(random.choices(string.ascii_letters + string.digits, k=4))
    nom_fichier = f"{dosser}/{prefixe}_{horodatage}_{aleatoire}"
    if extension:
        if not extension.startswith("."):
            nom_fichier += "."
        nom_fichier += extension
    return nom_fichier

# =============== Fonction pour extraire une courte description depuis un lien Wikipedia ===============
def scrop_desc(path, nb_paragraphes=2):
    try:
        res = requests.get(path)
        if res.status_code != 200:
            return f"Erreur HTTP {res.status_code}"

        soup = BeautifulSoup(res.text, 'html.parser')
        div = soup.find('div', class_="mw-content-ltr mw-parser-output")
        if not div:
            return "Contenu principal non trouvé."

        desc = ""
        count = 0

        for p in div.find_all('p'):
            texte = p.get_text(strip=True)
            if texte and len(texte) > 30:
                desc += texte + "\n\n"
                count += 1
                if count >= nb_paragraphes:
                    break

        return desc if desc else "Aucun paragraphe significatif trouvé."
    
    except Exception as e:
        return f"Erreur inattendue lors du scraping : {e}"

# =============== Fonction corrige ou complète les chemins relatifs en les transformant en URLs absolues. =============== 

def completer_url(relative_url, base="https://en.wikipedia.org"):
    """
    Corrige une URL relative en URL absolue, en ajoutant le préfixe approprié.
    
    - Si l'URL commence par 'http' ou 'https', elle est déjà complète.
    - Si elle commence par '//', on ajoute 'http:' devant.
    - Sinon, on ajoute le préfixe de base.
    """
    if not relative_url:
        return None
    if relative_url.startswith("http"):
        return relative_url
    elif relative_url.startswith("//"):
        return "http:" + relative_url
    elif relative_url.startswith("/"):
        return base + relative_url
    else:
        return base + "/" + relative_url
