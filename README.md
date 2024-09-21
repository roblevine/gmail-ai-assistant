https://developers.google.com/gmail/api/quickstart/python

# Python quickstart

bookmark_border
Quickstarts explain how to set up and run an app that calls a Google Workspace API.

Google Workspace quickstarts use the API client libraries to handle some details of the authentication and authorization flow. We recommend that you use the client libraries for your own apps. This quickstart uses a simplified authentication approach that is appropriate for a testing environment. For a production environment, we recommend learning about authentication and authorization before choosing the access credentials that are appropriate for your app.

Create a Python command-line application that makes requests to the Gmail API.

## Objectives

Set up your environment.
Install the client library.
Set up the sample.
Run the sample.

## Prerequisites

To run this quickstart, you need the following prerequisites:

Python 3.10.7 or greater
The pip package management tool
A Google Cloud project.
A Google account with Gmail enabled.

## Set up your environment

To complete this quickstart, set up your environment.

## Enable the API

Before using Google APIs, you need to turn them on in a Google Cloud project. You can turn on one or more APIs in a single Google Cloud project.
In the Google Cloud console, enable the Gmail API.

Enable the API

## Configure the OAuth consent screen

If you're using a new Google Cloud project to complete this quickstart, configure the OAuth consent screen and add yourself as a test user. If you've already completed this step for your Cloud project, skip to the next section.

In the Google Cloud console, go to Menu menu > APIs & Services > OAuth consent screen.
Go to OAuth consent screen

For User type select Internal, then click Create.
Complete the app registration form, then click Save and Continue.
For now, you can skip adding scopes and click Save and Continue. In the future, when you create an app for use outside of your Google Workspace organization, you must change the User type to External, and then, add the authorization scopes that your app requires.

Review your app registration summary. To make changes, click Edit. If the app registration looks OK, click Back to Dashboard.

## Authorize credentials for a desktop application

To authenticate end users and access user data in your app, you need to create one or more OAuth 2.0 Client IDs. A client ID is used to identify a single app to Google's OAuth servers. If your app runs on multiple platforms, you must create a separate client ID for each platform.
In the Google Cloud console, go to Menu menu > APIs & Services > Credentials.
Go to Credentials

1. Click Create Credentials > OAuth client ID.
2. Click Application type > Desktop app.
3. In the Name field, type a name for the credential. This name is only shown in the Google Cloud console.
4. Click Create. The OAuth client created screen appears, showing your new Client ID and Client secret.
5. Click OK. The newly created credential appears under OAuth 2.0 Client IDs.
6. Save the downloaded JSON file as credentials.json, and move the file to your working directory.

## Install the Google client library

- Install the Google client library for Python:

````bash
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
````

## Configure the sample

1. In your working directory, create a file named quickstart.py.
2. Include the following code in quickstart.py:

gmail/quickstart/quickstart.pyView on GitHub

````python
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]


def main():
  """Shows basic usage of the Gmail API.
  Lists the user's Gmail labels.
  """
  creds = None
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "credentials.json", SCOPES
      )
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("token.json", "w") as token:
      token.write(creds.to_json())

  try:
    # Call the Gmail API
    service = build("gmail", "v1", credentials=creds)
    results = service.users().labels().list(userId="me").execute()
    labels = results.get("labels", [])

    if not labels:
      print("No labels found.")
      return
    print("Labels:")
    for label in labels:
      print(label["name"])

  except HttpError as error:
    # TODO(developer) - Handle errors from gmail API.
    print(f"An error occurred: {error}")


````
