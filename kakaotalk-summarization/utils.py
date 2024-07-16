import os
import pickle
import time

import anthropic
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
from openai import OpenAI


ANTHROPIC_API_KEY = os.environ['ANTHROPIC_API_KEY']
GOOGLE_API_KEY = os.environ['GOOGLE_API_KEY']
OPENAI_API_KEY = os.environ['OPENAI_API_KEY']
MAX_LEN = 3000


def shorten_conv(conversation):
    shortened_len = len(conversation)
    lst = conversation.split('\n')
    for i, l in enumerate(lst):
        utterance_len = len(l)
        shortened_len -= utterance_len
        if shortened_len <= MAX_LEN:
            break

    lst_shortened = lst[i+1:]
    conv_shortened = '\n'.join(lst_shortened)
    return conv_shortened


def summarize(conversation, prompt, temperature=0.0, model='gpt-3.5-turbo-0125'):
    if len(conversation) > MAX_LEN:
        conversation = shorten_conv(conversation)

    prompt = prompt + '\n\n' + conversation

    if 'gpt' in model:
        client = OpenAI(api_key=OPENAI_API_KEY)
        completion = client.chat.completions.create(
            model=model,
            messages=[{'role': 'user', 'content': prompt}],
            temperature=temperature
        )

        return completion.choices[0].message.content
    elif 'gemini' in model:
        genai.configure(api_key=GOOGLE_API_KEY)
        client = genai.GenerativeModel(model)
        response = client.generate_content(
            contents=prompt,
            safety_settings={
                HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE
            }
        )
        time.sleep(1)

        return response.text
    elif 'claude' in model:
        client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
        message = client.messages.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
            max_tokens=1024
        )

        return message.content[0].text


def get_train_data():
    with open('./res/train_data.pickle', 'rb') as f:
        train_data = pickle.load(f)

    return train_data


def get_prompt():
    conv_train = get_train_data()[18]

    prompt = f"""당신은 요약 전문가입니다. 사용자 대화들이 주어졌을 때 요약하는 것이 당신의 목표입니다. 대화를 요약할 때는 다음 단계를 따라주세요:

1. 대화 참여자 파악: 대화에 참여하는 사람들의 수와 관계를 파악합니다.
2. 주제 식별: 대화의 주요 주제와 부차적인 주제들을 식별합니다.
3. 핵심 내용 추출: 각 주제에 대한 중요한 정보나 의견을 추출합니다.
4. 감정과 태도 분석: 대화 참여자들의 감정이나 태도를 파악합니다.
5. 맥락 이해: 대화의 전반적인 맥락과 배경을 이해합니다.
6. 특이사항 기록: 대화 중 특별히 눈에 띄는 점이나 중요한 사건을 기록합니다.
7. 요약문 작성: 위의 단계에서 얻은 정보를 바탕으로 간결하고 명확한 요약문을 작성합니다.
각 단계를 수행한 후, 최종적으로 전체 대화를 200자 내외로 요약해주세요.

아래는 예시 대화와 예시 요약 과정 및 결과 입니다.

예시 대화:
{conv_train}

예시 요약 과정
1. "우리 대학교 졸업 여행 간 거 기억나?"라는 언급과 전반적으로 친밀한 대화 톤을 사용하고 있는 것을 보았을 떄 두 사용자는 오랜 친구 사이로 보입니다.
대화의 시작 부분에서 "코로나가 좀 잠잠해지면 해외여행 중에 가고 싶은 곳 있어?"라고 묻고 있는 것을 보았을 때 코로나 이후 가고 싶은 해외 여행지에 대해 논의하고 있습니다.
따라서 다음과 같이 요약 할 수 있습니다:
최소 대학 생활부터 함께 한 매우 친밀한 사이의 두 사용자가 코로나가 잠잠해졌을 때 방문하고 싶은 해외 여행지에 대해 일상적이고 가벼운 톤으로 대화하고 있습니다.

2. 대화 중 호주, 일본, 하와이, 괌, 베트남 다낭, 스위스, 유럽들이 언급하고 있습니다.
남편의 첫 직장 워크샵, 대학교 졸업 여행, 호주 워킹홀리데이 등의 경험을 이야기하면서 과거 여행 경험을 공유하며 추억을 회상하고 있습니다.
따라서 다음과 같이 요약 할 수 있습니다:
여행지로는 하와이, 괌, 스위스, 호주, 베트남 다낭 등을 언급하며 남편과의 연락 관련 다툼이나 졸업여행 관련 추억을 회상합니다.

3. 소매치기, 여권 분실, 인도에서의 여성 여행자 위험 등을 언급하며 해외 여행의 위험성에 대해 우려를 표현하고 있습니다.
"해외 여행 가면 가이드 안 끼고 가면 영어 실력 엄청 좋은 사람이랑 가는 거 아닐 땐 소통 문제도 좀 곤란할 때가 있는 거 같아"라는 언급과 "왜 영어 공부를 열심히 안 했을까... 후회"라는 표현이 있는 것을 보았을 때 언어 장벽의 어려움을 인식하고 영어 실력 향상에 대한 욕구를 표현합니다.
따라서 다음과 같이 요약 할 수 있습니다:
또한 여행 중 발생하는 위험에 대한 우려도 표하고 있으며, 해외여행 시 언어 장벽의 어려움을 인식하고 영어 실력을 향상시키고 싶다는 마음을 가볍게 표현합니다.

예시 요약 결과
최소 대학 생활부터 함께 한 매우 친밀한 사이의 두 사용자가 코로나가 잠잠해졌을 때 방문하고 싶은 해외 여행지에 대해 일상적이고 가벼운 톤으로 대화하고 있습니다.
여행지로는 하와이, 괌, 스위스, 호주, 베트남 다낭 등을 언급하며 남편과의 연락 관련 다툼이나 졸업여행 관련 추억을 회상합니다.
또한 여행 중 발생하는 위험에 대한 우려도 표하고 있으며, 해외여행 시 언어 장벽의 어려움을 인식하고 영어 실력을 향상시키고 싶다는 마음을 가볍게 표현합니다.
    
아래 사용자 대화에 대해 3문장 내로 요약해주세요:"""
    return prompt