import requests
import os

def get_player_image(name, nationality, role="player"):
    """
    Récupère une image d'un joueur/coach depuis Wikimedia Commons.
    
    :param name: Nom du joueur ou coach (ex: "Hakim Ziyech")
    :param nationality: Nationalité (ex: "Morocco")
    :param role: "player" ou "coach"
    :return: chemin de l'image locale
    """
    search_url = "https://commons.wikimedia.org/w/api.php"
    
    params = {
        "action": "query",
        "format": "json",
        "prop": "imageinfo",
        "generator": "search",
        "gsrsearch": f"Category:{name}",
        "gsrlimit": 10,
        "iiprop": "url"
    }
    
    try:
        res = requests.get(search_url, params=params, headers={"User-Agent": "CAF-Scraper/1.0"})
        res.raise_for_status()
        data = res.json()
    except Exception as e:
        print(f"❌ Erreur de requête: {e}")
        return "default.jpg"

    images = []
    if "query" in data:
        for page in data["query"]["pages"].values():
            if "imageinfo" in page:
                img_url = page["imageinfo"][0]["url"]
                images.append(img_url)

    # 🔎 Filtrer par nationalité
    selected = None
    for img in images:
        if nationality.lower() in img.lower():
            selected = img
            break

    # Si aucune image ne correspond => image par défaut
    if not selected and images:
        selected = images[0]
    elif not selected:
        selected = "https://upload.wikimedia.org/wikipedia/commons/8/89/Portrait_Placeholder.png"  # image générique

    # 📥 Télécharger l'image
    os.makedirs("images", exist_ok=True)
    img_path = f"images/{name.replace(' ', '_')}_{role}.jpg"
    try:
        with requests.get(selected, stream=True, headers={"User-Agent": "CAF-Scraper/1.0"}) as r:
            with open(img_path, "wb") as f:
                for chunk in r.iter_content(1024):
                    f.write(chunk)
        print(f"Image sauvegardée : {img_path}")
    except Exception as e:
        print(f"❌ Erreur téléchargement : {e}")
        img_path = "default.jpg"

    return img_path


# =================== Exemple d’utilisation ===================
get_player_image("Hakim Ziyech", "Morocco", role="player")
get_player_image("Walid Regragui", "Morocco", role="coach")
