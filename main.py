import base64
from datetime import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from datetime import datetime

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

def get_credentials():
    creds = None
    # Load credentials from file if available
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    
    return creds

def fetch_labels(service):
    try:
        # Call the Gmail API
        results = service.users().labels().list(userId="me").execute()
        labels = results.get("labels", [])

        if not labels:
            print("No labels found.")
            return
        print("Labels:")
        for label in labels:
            print(label["id"] + ": " + label["name"])
    except HttpError as error:
        # TODO: Handle errors from Gmail API.
        print(f"An error occurred: {error}")

def query_emails_by_label(service, user_id, label_id):
    try:
        response = service.users().messages().list(userId=user_id, labelIds=[label_id]).execute()
        messages = response.get('messages', [])
        
        if not messages:
            print('No messages found.')
        else:
            print('Messages:')
            for message in messages:
                msg_id = message['id']

                msg = service.users().messages().get(userId=user_id, id=msg_id).execute()
                internal_date = msg['internalDate']
                internal_date_as_string = datetime.fromtimestamp(int(internal_date)/1000).strftime('%Y-%m-%d %H:%M:%S')
                print(f"Message ID: {msg_id}")
                print(f"Internal Date: {internal_date_as_string}")
                print(f"Snippet: {msg['snippet']}")
                print("--")
                # Print the email body
                for part in msg['payload']['parts']:
                    if part['mimeType'] == 'text/plain':
                        bodyDataBase64 = part['body']['data']
                        bodyData = base64.urlsafe_b64decode(bodyDataBase64).decode('utf-8')
                        print(f"Body: {bodyData}")
    except HttpError as error:
        # TODO: Handle errors from Gmail API.
        print(f"An error occurred: {error}")

def main():
    creds = get_credentials()
    service = build("gmail", "v1", credentials=creds)
    fetch_labels(service)
    query_emails_by_label(service, "me", "Label_15")

if __name__ == "__main__":
    main()