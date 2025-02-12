from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from datetime import datetime, timedelta

# The scope for managing Google Calendar events
SCOPES = ['https://www.googleapis.com/auth/calendar']

def authenticate_user():
    # Run local server to obtain user authorization
    flow = InstalledAppFlow.from_client_secrets_file(
        r'D:\New folder (3)\client_secret_17091883499-qv76lpge1u8egqijtdpb039tqevnt9tb.apps.googleusercontent.com.json', SCOPES)  # Update with your OAuth 2.0 JSON file path
    creds = flow.run_local_server(port=0)
    return creds

def create_event(creds):
    service = build('calendar', 'v3', credentials=creds)

    # Define the event details
    event = {
        'summary': 'Test Event',
        'description': 'This is a test event.',
        'start': {
            'dateTime': (datetime.utcnow() + timedelta(days=1)).isoformat() + 'Z',  # Start time
            'timeZone': 'UTC',
        },
        'end': {
            'dateTime': (datetime.utcnow() + timedelta(days=1, hours=1)).isoformat() + 'Z',  # End time
            'timeZone': 'UTC',
        },
        'attendees': [
            {'email': 'sannidhay2004@gmail.com'}  # Replace with the recipient email
        ],
        'conferenceData': {
            'createRequest': {
                'conferenceSolutionKey': {'type': 'hangoutsMeet'},
                'requestId': 'sample123'
            }
        },
    }

    # Create the event
    event = service.events().insert(calendarId='primary', body=event, conferenceDataVersion=1).execute()
    print(f"Event created successfully: {event.get('htmlLink')}")

if __name__ == '__main__':
    creds = authenticate_user()
    create_event(creds)
