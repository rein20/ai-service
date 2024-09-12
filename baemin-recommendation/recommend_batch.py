import os
import urllib.parse

import certifi
import numpy as np
from pymongo import MongoClient
from pymongo.server_api import ServerApi

from utils import get_embeddings, cosine_similarity, call_openai


COMBINATIONS = {
    "해장": ["수박주스", "토마토주스", "미숫가루", "와플", "해장파스타", "아메리카노"],
    "다이어트": ["샐러드파스타", "샐러트", "그릭요거트", "포케", "샌드위치"]
}


KEYWORDS_BLACKLIST = ['리뷰', 'zㅣ쀼', 'ZI쀼', 'Zl쀼', '찜', '이벤트', '추가', '소스']
KEYWORDS_CONTEXT = [
    '해장', '숙취',
    '다이어트'
]


def is_valid_menu(menu_name):
    return True if not any(keyword in menu_name for keyword in KEYWORDS_BLACKLIST) else False


def extract_keywords(review_text):
    keywords = []

    for word in review_text.split():
        if any(keyword in word for keyword in KEYWORDS_CONTEXT):
            keywords.append(word)
    return keywords


def fetch_restaurant_info():
    username = urllib.parse.quote_plus(os.environ['MONGODB_USERNAME'])
    password = urllib.parse.quote_plus(os.environ['MONGODB_PASSWORD'])
    uri = f"mongodb+srv://{username}:{password}@cluster0.61sar.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    client = MongoClient(uri, server_api=ServerApi('1'), tlsCAFile=certifi.where())
    db = client.restaurant_db
    collection = db.restaurant_info

    restaurants_info = list(collection.find({}))
    return restaurants_info


def create_candidates(restaurants_infos):
    candidates = []
    for index, info in enumerate(restaurants_infos):
        for reviews in info["reviews"]:
            menus = reviews["menus"].split(',')
            review_text = reviews["review_text"]

            # 리뷰에 컨텍스트/카테고리 관련 키워드 있는 지 확인
            keywords = extract_keywords(review_text)
            if keywords == []:
                continue

            for menu in menus:
                menu_name = menu.split('/')[0]
                if is_valid_menu(menu_name):
                    candidates.append(
                        {
                            "restaurant": info["restaurant"],
                            "menu": menu_name,
                            "keywords": " ".join([menu_name] + keywords)
                        }
                    )

    return candidates


def create_recommendations(query, candidates):
    contexts = [cand["keywords"] for cand in candidates]
    query_embedding = get_embeddings([query], model='text-embedding-3-large')[0]
    context_embeddings = get_embeddings(contexts, model='text-embedding-3-large')
    similarities = [cosine_similarity(query_embedding, context_embedding) for context_embedding in context_embeddings]

    sorted_indices = np.argsort(similarities)[::-1]
    recommendations = [candidates[i] for i in sorted_indices]

    recommendations_filtered = []
    unique_menus = set()
    for rec in recommendations:
        # 컨텍스트/카테고리-메뉴 조합 중 지정 조합만 사용
        menus_allowed = COMBINATIONS[query]
        if any(menu in rec['menu'] for menu in menus_allowed):
            menu_name = rec['menu'].split('/')[0]
            # 중복 메뉴 제거
            if menu_name not in unique_menus:
                rec['menu'] = menu_name
                recommendations_filtered.append(rec)
                unique_menus.add(menu_name)

    final_recommendations = {}
    for rec in recommendations_filtered:
        menu_name = rec['menu'].split('/')[0]
        if rec['restaurant'] not in final_recommendations:
            final_recommendations[rec['restaurant']] = [menu_name]
        else:
            final_recommendations[rec['restaurant']].append(menu_name)

    return final_recommendations


def create_recommmendation_text(query, recommendations):
    prompt = f"""당신은 배달의민족이라는 음식 주문 모바일 어플에서 리뷰 텍스트 기반으로 메뉴를 추천해주는 메뉴뚝딱AI입니다.
아래 목록은 {query}와 관련된 메뉴들을 연관성 높은 순서로 나열한 목록입니다.
당신의 목표는 특정 키워드와 연관된 메뉴들을 추천하는 것입니다. 총 2개의 키워드가 있으며 다이어트, 해장으로 구성되어 있습니다.

당신이 생성해야 할 문구 예시는 다음과 같습니다:
{query}에 좋은 메뉴들로 토마토주스, 미숫가루를 골라봤어요! 좋은 선택이 될 거에요.

주의사항
1. 메뉴를 추천 할 때 메뉴명만 적어야 합니다. 메뉴 목록에 수박주스x3이 있는 경우 수박주스, [숙취해소] 생토마토주스의 경우 토마토주스만 작성합니다.
2. 메뉴에 중복이 있는 경우 제외해주세요. 예시로 수박주스x3, 수박주스, [SUMMER NEW]수박주스는 전부 중복입니다.

메뉴 목록
{str(recommendations)}
"""
    recommendation_message = call_openai(prompt)
    return recommendation_message


def insert_to_mongo(query, recommendations, text):
    username = urllib.parse.quote_plus(os.environ['MONGODB_USERNAME'])
    password = urllib.parse.quote_plus(os.environ['MONGODB_PASSWORD'])
    uri = f"mongodb+srv://{username}:{password}@cluster0.61sar.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    client = MongoClient(uri, server_api=ServerApi('1'), tlsCAFile=certifi.where())
    db = client.recommendations_db
    collection = db.recommendations

    insertion = {
        "recommend_text": "",
        "recommend_reason": text,
        "recommendations": [
            {"restaurant": key, "menus": value} for key, value in recommendations.items()
        ]
    }
    result = collection.update_one({"_id": query}, {"$set": insertion}, upsert=True)
    return result


def recommend_batch():
    infos = fetch_restaurant_info()
    candidates = create_candidates(infos)
    queries = COMBINATIONS.keys()
    for query in queries:
        recommendations = create_recommendations(query, candidates)
        text = create_recommmendation_text(query, recommendations)
        result = insert_to_mongo(query, recommendations, text)
        print(result)


if __name__ == '__main__':
    recommend_batch()