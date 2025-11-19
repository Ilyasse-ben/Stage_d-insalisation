import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

# ===================== MongoDB Connection =====================
try:
    client = MongoClient("mongodb://localhost:27017/")
    db = client["CAF"]
    collection = db["Team"]  # Collection of teams
except Exception as e:
    print(f"MongoDB connection error: {e}")
    exit()

# ===================== Scraping Wikipedia =====================
for team_doc in collection.find():
    if "team_link" not in team_doc:
        continue  # skip if team link is missing

    url = team_doc["team_link"]
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        print(f"Scraping successful: {url}")
    except Exception as e:
        print(f"Error loading page {url}: {e}")
        continue  # skip only this team

    # ===================== Parse HTML =====================
    soup = BeautifulSoup(response.text, "html.parser")

    # --------------------- Scrape Coaching Staff ---------------------
    coaching_staff = {}
    for table in soup.find_all("table"):
        if "Position" in table.get_text(strip=True) and "Name" in table.get_text(strip=True):
            rows = table.find_all("tr")

            for row in rows:
                # Skip header row
                if "Position" in row.get_text(strip=True) or "Name" in row.get_text(strip=True):
                    continue

                cells = row.find_all("td")
                if not cells:
                    continue

                if len(cells) > 1:
                    position = cells[0].get_text(strip=True)
                    names = [cells[1].get_text(strip=True)]
                else:
                    # continuation of previous names (assistant coaches etc.)
                    names = [cells[0].get_text(strip=True)]

                # Merge into dictionary (avoid overwriting)
                if position in coaching_staff:
                    coaching_staff[position].extend(names)
                else:
                    coaching_staff[position] = names

            # Remove duplicates from names
            for key in coaching_staff:
                coaching_staff[key] = list(set(coaching_staff[key]))

            # Update MongoDB
            collection.update_one(
                {"name": team_doc["name"]},
                {"$set": {"Coaching": coaching_staff}}
            )
            print(f"Updated coaching staff for {team_doc['name']}")

    # --------------------- Scrape Players ---------------------
    players = []
    for table in soup.find_all("table"):
        if (
            "Pos" in table.get_text(strip=True)
            and "Player" in table.get_text(strip=True)
            and "No." in table.get_text(strip=True)
        ):
            for row in table.find_all("tr"):
                cells = row.find_all("td")
                if "Pos" in row.get_text(strip=True) or len(cells) <= 1:
                    continue

                player = {
                    "number": cells[0].get_text(strip=True),
                    "name": row.find("th").get_text(strip=True) if row.find("th") else "",
                    "position": cells[1].find('a').get_text(strip=True) if len(cells) > 1 else "",
                }
                players.append(player)

            # Update MongoDB
            collection.update_one(
                {"name": team_doc["name"]},
                {"$set": {"players": players}}
            )
