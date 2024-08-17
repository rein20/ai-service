# 슬랙 셋업 방법
# 1. slack.com에서 계정 생성
# 2. 신규 슬랙 워크스페이스 생성
# 3. 신규 슬랙봇 생성 (https://api.slack.com/apps)
#   - 우측 상단 Create New App 버튼 클릭
#   - App 이름, 워크스페이스 지정 후 Create App 클릭
#   - Permissions > Scopes > Bot Token Scopes 밑에 Add an OAuth Scope 버튼
#   - 4개 선택 - app_mentions:read, channels:history, channels:read, chat:write
#   - 좌측 상단 Settings 메뉴 > Socket Mode > Enable Socket Mode
#   - Token 이름 지정 후 Generate 버튼 클릭
#     - 생성된 token을 복사 후 환경변수 SLACK_BOT_TOKEN으로 저장
#   - Basic Information > Add features and functionality > Event Subscriptions 활성화 후 저장
#     - Subscribe to bot events > Add Bot User Event 클릭 후 app_mention 추가 후 저장
#   - OAuth & Permssions > Install to <워크스페이스 이름> 클릭 > 허용

import os
import anthropic
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack import WebClient
from slack_bolt import App

# Event API & Web API
app = App(token=os.environ['SLACK_BOT_TOKEN']) 
slack_client = WebClient(os.environ['SLACK_BOT_TOKEN'])
anthropic_client = anthropic.Anthropic(api_key=os.environ['ANTHROPIC_API_KEY'])


# This gets activated when the bot is tagged in a channel    
@app.event("app_mention")
def handle_message_events(body, logger):
    # Log message
    print(str(body["event"]["text"]).split(">")[1])
    
    # Create prompt for ChatGPT
    prompt = str(body["event"]["text"]).split(">")[1]
    
    # Let the user know that we are busy with the request 
    response = slack_client.chat_postMessage(
        channel=body["event"]["channel"],
        thread_ts=body["event"]["event_ts"],
        text="안녕하세요, 개인 비서 슬랙봇입니다! :robot_face: \n곧 전달 주신 문의사항 처리하겠습니다!"
    )

    response = anthropic_client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.0
    )
    
    # Reply to thread 
    response = slack_client.chat_postMessage(
        channel=body["event"]["channel"], 
        thread_ts=body["event"]["event_ts"],
        text=f"{response.content[0].text}"
    )

if __name__ == "__main__":
    SocketModeHandler(app, os.environ['SLACK_APP_TOKEN']).start()