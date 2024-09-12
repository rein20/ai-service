import os

import numpy as np
from openai import OpenAI


KEYWORDS_BLACKLIST = ['리뷰', 'zㅣ쀼', 'ZI쀼', 'Zl쀼', '리쀼', '찜', '이벤트', '추가', '소스']
KEYWORDS_CONTEXT = [
    '해장', '숙취',
    '다이어트'
]


def get_embedding(text, model='text-embedding-3-small'):
    client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])
    response = client.embeddings.create(
        input=text,
        model=model
    )
    return response.data[0].embedding


def get_embeddings(text, model='text-embedding-3-small'):
    client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])
    response = client.embeddings.create(
        input=text,
        model=model
    )
    output = []
    for i in range(len(response.data)):
        output.append(response.data[i].embedding)
    return output


def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


def get_most_relevant_indices(query_embedding, context_embeddings):
    query = np.array(query_embedding)
    context = np.array(context_embeddings)
    
    similarities = np.array([cosine_similarity(query, ctx) for ctx in context])
    
    sorted_indices = np.argsort(similarities)[::-1].tolist()
    
    return sorted_indices, similarities


def extract_keywords(review_text):
    keywords = []

    for word in review_text.split():
        if any(keyword in word for keyword in KEYWORDS_CONTEXT):
            keywords.append(word)
    return keywords


def is_valid_menu(menu_name):
    return True if not any(keyword in menu_name for keyword in KEYWORDS_BLACKLIST) else False


def call_openai(prompt, temperature=0.0, model='gpt-4o-2024-08-06'):
    client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])
    completion = client.chat.completions.create(
        model=model,
        messages=[{'role': 'user', 'content': prompt}],
        temperature=temperature
    )

    return completion.choices[0].message.content


# def retrieve_context(query, contexts):
#     query_embedding = get_embeddings([query], model='text-embedding-3-small')[0]
#     context_embeddings = get_embeddings(contexts, model='text-embedding-3-small')

#     similarities = [cosine_similarity(query_embedding, context_embedding) for context_embedding in context_embeddings]

#     most_relevant_index = np.argmax(similarities)
#     print(contexts[most_relevant_index])
#     return contexts[most_relevant_index]


# import numpy as np

# def retrieve_context(query, contexts):
#     query_embedding = get_embeddings([query], model='text-embedding-3-small')[0]
#     context_embeddings = get_embeddings(contexts, model='text-embedding-3-small')

#     similarities = [cosine_similarity(query_embedding, context_embedding) for context_embedding in context_embeddings]

#     # Create a list of (similarity, context) tuples
#     similarity_context_pairs = list(zip(similarities, contexts))
    
#     # Sort the pairs in descending order of similarity
#     sorted_pairs = sorted(similarity_context_pairs, key=lambda x: x[0], reverse=True)
    
#     # Extract the sorted contexts
#     sorted_contexts = [context for _, context in sorted_pairs]
    
#     # Print all contexts in order of relevancy
#     for i, context in enumerate(sorted_contexts, 1):
#         print(f"{i}. {context}")
    
#     return sorted_contexts


# def get_topk_reviews(query, contexts, reviews):
#     query_embedding = get_embeddings([query], model='text-embedding-3-small')[0]
#     context_embeddings = get_embeddings(contexts, model='text-embedding-3-small')

#     similarities = [cosine_similarity(query_embedding, context_embedding) for context_embedding in context_embeddings]

#     # Get the indices of the sorted array (from highest to lowest)
#     sorted_indices = np.argsort(similarities)[::-1]

#     # Convert numpy array back to a list (optional)
#     sorted_indices = sorted_indices.tolist()

#     # Reorder the reviews based on the sorted indices
#     reranked_reviews = [reviews[i] for i in sorted_indices]
    
#     return reranked_reviews

import os
import time
import urllib.parse

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from pymongo import MongoClient
from collections.abc import MutableMapping
import certifi


def fetch_restaurant_info():
    username = urllib.parse.quote_plus(os.environ['MONGODB_USERNAME'])
    password = urllib.parse.quote_plus(os.environ['MONGODB_PASSWORD'])
    uri = f"mongodb+srv://{username}:{password}@cluster0.61sar.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    client = MongoClient(uri, server_api=ServerApi('1'), tlsCAFile=certifi.where())
    db = client.restaurant_db
    collection = db.restaurant_info

    restaurants_info = list(collection.find({}, {'_id': False}))
    return restaurants_info