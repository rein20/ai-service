# ai-service
[프롬프트 엔지니어링으로
시작하는 AI/LLM 서비스 개발: 9개 프로젝트로 챗봇부터 AI 에이전트까지](https://fastcampus.co.kr/data_online_llmservice?utm_source=linkedin&utm_medium=viral&utm_campaign=prd^240415^237192&utm_content=teacher^kms^237192) 강의 실습 코드 모음입니다.

## 해당 코드의 목표
실서비스 출시된 AI 서비스들을 직접 따라 만들어보면서 Prompt Engineering, RAG 등의 기술을 익히고 \
데이터 확보, 모델 평가 기준 설정 및 고도화, 기술 데모 제작, 실서비스 고려 등의 프레임워크를 갖추는 것입니다. \
이론 설명도 있지만 깊은 이론보다는 실서비스 적용을 위한 실습에 초점을 두었습니다.

## 구성
아래 주제에 대한 실습 코드로 구성되어 있습니다. 실습 완료 기준으로 실서비스에 준하는 수준의 기능 결과물을 확인하실 수 있습니다.
- [Part 3. Prompt Engineering 이론 및 실습](https://github.com/rein20/ai-service/tree/main/prompt-engineering)
- [Part 4. 야놀자 리뷰 요약](https://github.com/rein20/ai-service/tree/main/yanolja-summarization)
- [Part 5. 카카오 대화 요약](https://github.com/rein20/ai-service/tree/main/kakaotalk-summarization)
- [Part 8. 실전 RAG](https://github.com/rein20/ai-service/tree/main/retrieval-augmented-generation)
- [Part 12. 사내 업무 에이전트](https://github.com/rein20/ai-service/tree/main/assistant-question-answering)
- [Part 14. 배달의민족 리뷰 기반 메뉴/맛집 추천](https://github.com/rein20/ai-service/tree/main/baemin-recommendation)

## 강의에서 다루는 기술들
- LLM API
  - OpenAI ChatGPT API, Anthropic Claude API, Google Gemini API
- LLM 
  - LLM Evaluation
  - Prompt Engineering
  - Function Calling / Tool Use
  - Retrieval Augmented Generation (RAG)
  - VectorDB
- Frameworks
  - Beautifulsoup4, Selenium (Data Crawling)
  - Gradio (Demo)
  - Slackbot (Chatbot UI)
  - Google Calendar API (Function Calling)
  - Huggingface Hub (Data Download)
  - MongoDB (VectorDB, Meta DB)
  - FastAPI (LLM, Recommendation API)
  - NumPy, Pandas (RAG)

## FAQ
Q. 크롤링 이슈: IndexError: list index out of range
- 원인 : 야놀자 웹페이지의 태그의 클래스명 변경 또는 상속의 변화로 발생하는 이슈입니다.
- 해결 방법 :
  1. 야놀자 웹페이지에 접속하여 개발자 도구를 킵니다.
  2. 개발자 도구를 보면 맨 왼쪽 측에 있는 이미지와 같은 아이콘 <img width="30" alt="스크린샷 2024-08-17 18 03 22" src="https://github.com/user-attachments/assets/17d0bb9c-7532-46c5-9abb-40936ec56491"> 을 클릭합니다. 
  3. 아이콘을 클릭한 상태에서 날짜가 표기된 부분을 클릭합니다.<img width="771" alt="스크린샷 2024-08-17 18 04 50" src="https://github.com/user-attachments/assets/a0d6d4f3-d8e5-4828-a6f6-1fc0757cf54a">
  4. 그러면 개발자 도구에 날짜 태그가 잡힐 것입니다. 그 태그에 마우스 오른쪽을 클릭하여 copy > copy selector를 클릭합니다. 그러면 자동으로 날짜 태그의 위치가 복사되어집니다.
  5. 에디터로 돌아가 review_date의 select 인수에 붙여넣기 해줍니다. 그러면 처음에는 <img width="1354" alt="스크린샷 2024-08-17 18 15 45" src="https://github.com/user-attachments/assets/9c8106e9-4170-4fd2-805e-78b1f1cfcfcc"> 이미지와 같이 붙여넣어졌을텐데 여기서 :nth-child(n) 부분들은 다 지워줍니다. 그러면 이렇게 코드가 변경됩니다. <img width="1036" alt="스크린샷 2024-08-17 18 16 59" src="https://github.com/user-attachments/assets/360a57b2-5d58-4673-91db-f6b04a7f4486">
  6. 이제 저장하고 실행하면 이슈가 해결됩니다.
 
Q. 크롤링 이슈: 리뷰들의 별점이 전부 5점으로 나옵니다.
- 원인: 위와 동일합니다.
- 해결 방법:
  - 최근 리뷰 별점을 웹사이트에 그리는 방식에 변화가 있었는데, 다음 커밋 참고해서 수정해주시면 정상 작동합니다. [commit](https://github.com/rein20/ai-service/commit/fb6ab0fe5c8ef9f794e423b1497d70a755cf76cf)
