import os

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


SCOPES = ['https://www.googleapis.com/auth/calendar']

# 1. 함수 생성
def intialize_service():
    if os.path.exists('./res/token.json'):
        creds = Credentials.from_authorized_user_file('./res/token.json', SCOPES)
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            './res/credentials.json', SCOPES
        )
        creds = flow.run_local_server(port=0)
        with open('./res/token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('calendar', 'v3', credentials=creds)
    return service


def create_event(summary, start, end):
    service = intialize_service()

    event = {
        'summary': summary,
        'start': {
            'dateTime': start,
            'timeZone': 'Asia/Seoul',
        },
        'end': {
            'dateTime': end,
            'timeZone': 'Asia/Seoul',
        }
    }
    event = service.events().insert(calendarId='primary', body=event).execute()
    print('Event created: %s' % (event.get('htmlLink')))
    return event


def check_event(start, end):
    service = intialize_service()

    events_result = service.events().list(
        calendarId='primary',
        timeMin=start,
        timeMax=end,
        maxResults=5,
        singleEvents=True,
        orderBy='startTime'
    ).execute()

    return events_result


def delete_event(id):
    service = intialize_service()

    event = service.events().delete(calendarId='primary', eventId=id).execute()
    print('Event deleted')
    return event
