import os
import urllib

import certifi
from fastapi import FastAPI
from pymongo import MongoClient
from pymongo.server_api import ServerApi


MAPPING_EN2KO = {
    "hangover": "해장",
    "diet": "다이어트"
}
MAPPING_KO2EN = {v: k for k, v in MAPPING_EN2KO.items()}

app = FastAPI()

username = urllib.parse.quote_plus(os.environ['MONGODB_USERNAME'])
password = urllib.parse.quote_plus(os.environ['MONGODB_PASSWORD'])
uri = f"mongodb+srv://{username}:{password}@cluster0.61sar.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri, server_api=ServerApi('1'), tlsCAFile=certifi.where())
db = client.recommendations_db
collection = db.recommendations


@app.get("/health")
def health():
    return "OK"


@app.get("/recommend/{query_en}")
def recommend(query_en: str = "hangover"):
    query_ko = MAPPING_EN2KO[query_en]
    data = list(collection.find({"_id": query_ko}, {'_id': 0}))
    return data