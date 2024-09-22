import base64
from datetime import datetime
import os.path
import logging

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
            logging.info("No labels found.")
            return []

        logging.info(f"Labels count: {len(labels)}")

        if logging.getLogger().isEnabledFor(logging.DEBUG):
            logging.debug("Labels:")
            for label in labels:
                logging.debug(f"{label['id']}: {label['name']}")

        return labels
    except HttpError as error:
        print(f"An error occurred: {error}")
        return []


def query_emails_by_label(service, user_id, label_id, max_results=5):
    try:
        response = (
            service.users()
            .messages()
            .list(userId=user_id, labelIds=[label_id], maxResults=max_results)
            .execute()
        )
        messages = response.get("messages", [])

        if not messages:
            logging.info("No messages found.")
            return []
        else:
            logging.info(f"Messages count: {len(messages)}")
            if logging.getLogger().isEnabledFor(logging.DEBUG):
                logging.debug("Messages:")

            emails = []
            for message in messages:
                msg_id = message["id"]

                msg = (
                    service.users().messages().get(userId=user_id, id=msg_id).execute()
                )
                internal_date = msg["internalDate"]
                internal_date_as_string = datetime.fromtimestamp(
                    int(internal_date) / 1000
                ).strftime("%Y-%m-%d %H:%M:%S")
                headers = msg["payload"]["headers"]
                subject = next(
                    (header["value"] for header in headers if header["name"] == "Subject"),
                    "No Subject"
                )

                bodyData = "(no content)"
                for part in msg["payload"]["parts"]:
                  if part["mimeType"] == "text/plain":
                    bodyDataBase64 = part["body"]["data"]
                    bodyData = base64.urlsafe_b64decode(bodyDataBase64).decode("utf-8")

                emails.append({
                    "id": msg_id,
                    "internal_date": internal_date_as_string,
                    "subject": subject,
                    "body": bodyData
                })

            return emails
    except HttpError as error:
        print(f"An error occurred: {error}")
        return []

def main():
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
    )
    creds = get_credentials()
    service = build("gmail", "v1", credentials=creds)
    fetch_labels(service)

    emails = query_emails_by_label(service, "me", "Label_15")
    for email in emails:
        logging.info(f"Email ID: {email['id']}, Internal Date: {email['internal_date']}, Subject: {email['subject']}")
        if (logging.getLogger().isEnabledFor(logging.DEBUG)):
          logging.debug(f"Body: {email['body']}")
          logging.debug("----------------------------------------------------")

if __name__ == "__main__":
    main()
