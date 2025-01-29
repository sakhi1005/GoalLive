import datetime
import os.path
from datetime import time, datetime

from future.backports.datetime import datetime, timedelta
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from utils.GoogleCalendarUtils import format_calendar_event, get_path_to_user_account, find_free_slots_from_calendar

# If modifying these scopes, delete the file credentials.json.
SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]

def get_user_calendar(email_id: str, date: datetime):
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = get_user_token(email_id)
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first time.

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("./resources/credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        persist_user_token(email_id, creds)

    try:
        service = build("calendar", "v3", credentials=creds)

        # Call the Calendar API
        # now = datetime.utcnow().isoformat() + "Z"  # 'Z' indicates UTC time
        start_of_day = datetime.combine(date, time.min).isoformat() + "Z"  # Start of the day
        end_of_day = datetime.combine(date, time.max).isoformat() + "Z"  # End of the day
        events_result = service.events().list(
            calendarId="primary", timeMin=start_of_day, timeMax=end_of_day,
            maxResults=50, singleEvents=True,
            orderBy="startTime").execute()
        events = events_result.get("items", [])
        # return events

        # Prints the start and name of the next 10 events
        formatted_events = []
        for event in events:
            formatted_event = format_calendar_event(event)
            formatted_events.append(formatted_event)

        return formatted_events

    except HttpError as error:
        print(f"An error occurred: {error}")

def get_user_token(email_id):
    # returns the parsed credentials of the user if he has already logged in
    path_to_user_creds = get_path_to_user_account(email_id)
    if os.path.exists(path_to_user_creds):
        return Credentials.from_authorized_user_file(path_to_user_creds, SCOPES)

def persist_user_token(email_id, creds):
    path_to_user_creds = get_path_to_user_account(email_id)
    with open(path_to_user_creds, "w+") as token:
        token.write(creds.to_json())


if __name__ == "__main__":
    # pass
    email_id = input("Enter your email id: ")
    events = get_user_calendar(email_id)
    today = datetime.today().date()

    # Create a datetime object for 12 AM today
    datetime_12am = datetime.combine(today, time(0))
    datetime_tom_12am = datetime_12am + timedelta(days=1)
    user_slots = find_free_slots_from_calendar(datetime_12am, datetime_tom_12am, events)
    print(str(user_slots))
