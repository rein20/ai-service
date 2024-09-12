import logging
import os
import sys
import urllib
sys.path.insert(0, "..")
from collections.abc import MutableMapping
from pydantic import BaseModel
from typing import Union

import certifi
from fastapi import FastAPI
from pymongo import MongoClient
from pymongo.server_api import ServerApi


from utils import cosine_similarity, extract_keywords
from utils import get_embedding, get_most_relevant_indices


# 몽고DB 연결
username = urllib.parse.quote_plus(os.environ['MONGODB_USERNAME'])
password = urllib.parse.quote_plus(os.environ['MONGODB_PASSWORD'])
uri = f"mongodb+srv://{username}:{password}@cluster0.61sar.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri, server_api=ServerApi('1'), tlsCAFile=certifi.where())
db = client.menu_db
collection = db.menu_info
menu_db = list(collection.find({}))

app = FastAPI()


class QueryModel(BaseModel):
    query_text: str


@app.get("/health")
def health():
    return "OK"


@app.post("/recommend")
def recommend(query: QueryModel):
    query = extract_keywords(query.query_text)
    if query == []:
        return []

    query_embedding = get_embedding(query, model='text-embedding-3-large')
    context_embeddings = [menu["embeddings"] for menu in menu_db]
    indices, scores = get_most_relevant_indices(query_embedding, context_embeddings)

    result = []
    top_k = 10
    for i in range(top_k):
        result.append({
            "_id": menu_db[indices[i]]["_id"],
            "score": scores[indices[i]],
            "menu": menu_db[indices[i]]["menu"],
            "restaurant": menu_db[indices[i]]["restaurant"],
            "url": menu_db[indices[i]]["url"]
        })
    return result