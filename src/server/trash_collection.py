import json
import os
import datetime
import pickle
import os.path
from google.oauth2 import service_account
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these SCOPES, delete the file token.pickle.
SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]
CREDENTIALS_FILE = "credentials/google_credentials.json"
CONFIG_FILE = "credentials/calendar_config.json"
with open(CONFIG_FILE, "r") as f:
    CONFIG = json.load(f)


class GoogleCalendarClient:
    token_path = "token.pickle"
    config = CONFIG

    def authenticate_google_calendar(self):
        creds = None
        if os.path.exists(self.token_path):
            with open(self.token_path, "rb") as token:
                creds = pickle.load(token)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    CREDENTIALS_FILE, SCOPES
                )
                creds = flow.run_local_server(port=0)
            with open(self.token_path, "wb") as token:
                pickle.dump(creds, token)
        return creds

    def get_next_trash_collection(self):
        creds = self.authenticate_google_calendar()
        service = build("calendar", "v3", credentials=creds)

        now = datetime.datetime.utcnow().isoformat() + "Z"
        events_result = (
            service.events()
            .list(
                calendarId=CONFIG["id"],
                timeMin=now,
                maxResults=10,
                singleEvents=True,
                orderBy="startTime",
            )
            .execute()
        )
        events = events_result.get("items", [])
        # return events
        trash_events = {}
        for event in events:
            summary = event["summary"]
            start = event["start"].get("dateTime", event["start"].get("date"))
            trash_type = summary.split()[
                0
            ]  # Assuming trash type is the first word in summary
            if trash_type not in trash_events:
                trash_events[trash_type] = start

        return trash_events
