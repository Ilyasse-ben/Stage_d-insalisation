import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
# ===================== connextion a mongodb================================================
try:
    client=MongoClient("mongodb://localhost:27017/")
    db=client['CAF']
    collection_match=db['Match']    
except Exception as e:
    print(f'connextion filed :{e}')
    exit(-1)
for match in collection_match.find():
    if 'raport' in match:
        print("ok")

