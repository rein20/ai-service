# ai-service

패스트캠퍼스 "[9개 프로젝트로 챗봇부터 AI 에이전트까지](https://fastcampus.co.kr/data_online_llmservice?utm_source=linkedin&utm_medium=viral&utm_campaign=prd^240415^237192&utm_content=teacher^kms^237192)" 강의 실습 코드 모음입니다.

## 해당 코드의 목표
실서비스 출시된 AI 서비스들을 직접 따라 만들어보면서 Prompt Engineering, RAG 등의 기술을 익히고 \
데이터 확보, 모델 평가 기준 설정 및 고도화, 기술 데모 제작, 실서비스 고려 등의 프레임워크를 갖추는 것입니다. \
이론 설명도 있지만 깊은 이론보다는 실서비스 적용을 위한 실습에 초점을 두었습니다.

## 구성
아래 주제에 대한 실습 코드로 구성되어 있습니다. 실습 완료 기준으로 실서비스에 준하는 수준의 기능 결과물을 확인하실 수 있습니다.
- Prompt Engineering 이론 및 실습
- 프로젝트 1. 야놀자 높은/낮은 리뷰 요약
- 프로젝트 5. 카카오톡 대화 요약
- Retrieval Augmented Generation (RAG) 이론 및 실습
- 프로젝트 6. 사내 업무 지원 슬랙 챗봇
- 프로젝트 9. 배달의민족 리뷰 기반 메뉴/맛집 추천

## 공통 내용
### 개발 프로세스 개발 절차
본 프로젝트에서 진행하는 AI 서비스 개발 실습은 아래의 공통된 개발 프로세스를 따라 진행합니다.

1. **문제(Task) 조건 확인**
    - 어떤 서비스에서 무엇을 목표로 하는 지에 따라 필요한 기술이 달라 질 수 있습니다.
    - 실제 서비스 화면을 같이 확인하면서 어떤 조건들이 있는 지 꼼꼼하게 확인합니다.
    - 예를 들어, 야놀자 리뷰 요약에는 "후기가 3개 이상 있고, 후기 글의 90자 이상이어야 함"라는 조건이 있습니다.
        - 따라서 이 조건에 부합하지 않은 숙소 요약은 제외해야 합니다.
2. **평가 기준 설정**
    - 객관적인 정량적인 평가 기준을 설정합니다.
    - 예를 들어, 사람이 평가하는 방식과 유사한 Strong LLM이 평가하는 방식이 적합하다면 검토해 볼 수 있습니다.
3. **모델 선정**
    - 2024년 4월 기준으로는 Claude 3, GPT4가 가장 강력한 LLM들이며 여기서 모델 선정을 시작합니다.
    - RAG가 필요한 경우 임베딩 모델 선정도 같이 진행합니다.
4. **Baseline 모델 개발**
    - Naive한 방법으로 가장 빠르게 기본이 되는 Baseline 모델을 개발하고 초기 평가를 진행합니다.
5. **모델 고도화 및 평가 진행**
    - 2번에서 설정한 평가 기준을 지표로 삼아 Baseline 모델에서 시작하여 모델 고도화 및 평가를 진행합니다.
6. **데모 제작**
    - 어느 정도 품질이 되는 모델이 개발되었으면, Gradio 프레임워크 기반으로 데모를 제작합니다.
    - 2번 평가 기준을 활용한 정량 평가, 데모를 활용한 정성 평가를 기준으로 실서비스 가능성을 고려하고 런칭 여부 등을 결정합니다.
7. **실서비스 여부 검토**
    - 비용, 라이센스 이슈, 악용 가능성을 고려한 가드레일 필요성 등을 전부 검토합니다.
    - 예를 들어, 트래픽이 높아 ChatGPT API를 호출 횟수가 너무 빈번할 경우 비용적으로 부담이 될 수 있어 구체적인 해결 방법론을 모색합니다.

위 개발 프로세스 순서는 필요에 따라 조금씩 바뀔 수 있습니다. \
다만, 문제 조건을 확인하지 않는다거나, 정량적인 평가 기준을 설정하지 않으면 모델 고도화 방향이 최적이 아닐 수 있습니다.

## 프로젝트 별 내용
1) 각 프로젝트 별 주된 내용은 무엇인가요? 어떤 기능들을 개발하나요? (개발 요구사항/Task 를 작성해주세요)
2) 각 프로젝트 별로 주요하게 사용되는 기술(프롬프트 엔지니어링 기법, OpenAI 기능 등)을 작성해주세요.

### Prompt Engineering 이론 및 실습
- 학습 내용
    - 프롬프트 품질에 대한 평가 기준을 설정하고, 각 프롬프트 엔지니어링 기법들을 직접 사용해보고 효과를 체감해봅니다.
    - 다른 방법론(ex. 파인튜닝) 대비 장단점을 이해하고, 수많은 방법론 중 선택 할 수 있는 방법론임을 인식합니다.
- 사용 기술
    - OpenAI API, Google Colaboratory, LLM 평가 지표(ex. LLM-as-a-judge, ROUGE), Prompt Engineering 기법들

### 프로젝트 1. 야놀자 높은/낮은 리뷰 요약
<p float="left">
  <img src="https://drive.google.com/uc?export=view&id=1TF5y4AMXwrXPPBSD6HTal9rSXmxg4Iaz" width="300" />
  <img src="https://drive.google.com/uc?export=view&id=1bf6FFF6jI4OTYee09-G-1hq5iKU3STau" width="300" /><br>
</p>

- 학습 내용
    - 야놀자 후기 요약 기능을 그대로 구현해봅니다.
    - 첫 프로젝트인만큼 데이터 확보, 모델 개발, 데모 제작 과정 등을 최대한 상세하게 진행합니다.
- Task 조건
    - 각 숙소 별로 높은 리뷰, 낮은 리뷰를 요약해야 함 (여기서 높은/낮은의 기준은 공개 X)
    - 모텔은 최근 3개월, 호텔/펜션/게하는 최근 6개월 후기 요약
    - 후기가 3개 이상 있고, 후기 글의 90자 이상이어야 함
    - 후기가 많을 수록 최근 작성 후기 위주로 요약
- 사용 기술
    - OpenAI API, BeautifulSoup4, Selenium, Gradio, Prompt Engineering 기법들

### 프로젝트 5. 카카오톡 대화 요약
<p float="left">
  <img src="https://drive.google.com/uc?export=view&id=1YDHH75artK3U4jVtMGrnpeH71OyJIqdD" width="300" />
  <img src="https://drive.google.com/uc?export=view&id=1PNHQ2WrSrshm6MO3-NqdCPv1sG5gW-NY" width="300" /><br>
</p>

- 학습 내용
    - 카카오톡 대화 요약 기능을 그대로 구현해봅니다.
- Task 조건
    - 한글 기준 3천 자 초과 시, 가장 최신 메시지부터 3천 자까지만 요약합니다.
- 사용 기술
    - OpenAI API, Gradio, AI Hub, Huggingface Hub, Prompt Engineering 기법들

### Retrieval Augmented Generation (RAG) 이론 및 실습
- 학습 내용
    - RAG 개념을 이해하고 언제 어떤 방법을 사용하는지 파악합니다.
- 사용 기술
    - OpenAI API (LLM + Embedding), Google Colaboratory, RAG 평가 방법론 (ex. RAGAS)

### 프로젝트 6. 사내 업무 지원 슬랙 챗봇
- 학습 내용
    - 이전 강의인 RAG 기술을 추가로 활용하여 ChatGPT API만으로는 해결이 어려운 태스크를 해결합니다.
- 사용 기술
    - OpenAI API (LLM + Embedding), Slack Client, Prompt Engineering/RAG 기법들

### 프로젝트 9. 배달의민족 리뷰 기반 메뉴/맛집 추천
<p float="left">
  <img src="https://drive.google.com/uc?export=view&id=17TXHEhTvO9GfAGR12J0D1VyBGzyRexZv" width="300" />
  <img src="https://drive.google.com/uc?export=view&id=1ktsDPqEAqMa6o0M4aEKD4xvYSWX_2TtL" width="300" /><br>
</p>

- 학습 내용
    - 배달의민족 리뷰 기반 메뉴/맛집 추천 기능을 그대로 구현해봅니다.
    - 최종 프로젝트인만큼 엄밀한 구현보다는 지금까지 배운 기법들을 복습하고 잘 활용하는데 초점을 둡니다.
- Task 조건
    - GPT-4를 활용하고, 최근 3개월 리뷰 일부를 활용합니다.
    - 고객 리뷰 및 가게 정보를 안전하게 관리합니다.
    - 오픈리스트 및 배민1 광고 상품 일부 매장들 정보만 활용합니다.
- 사용 기술: OpenAI API (LLM + Embedding + Assistant), Claude API, BeautifulSoup4, Selenium, Gradio
