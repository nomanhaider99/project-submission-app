from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TOKEN_PATH = os.path.join(BASE_DIR, "token.json")
CLIENT_SECRET_PATH = os.path.join(BASE_DIR, "client_secret.json")

SCOPES = ["https://www.googleapis.com/auth/drive.file"]

creds = None

if os.path.exists(TOKEN_PATH):
    creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
else:
    flow = InstalledAppFlow.from_client_secrets_file(
        CLIENT_SECRET_PATH,
        SCOPES
    )
    creds = flow.run_local_server(port=0)

    with open(TOKEN_PATH, "w") as token:
        token.write(creds.to_json())

build("drive", "v3", credentials=creds)

print("✅ token.json created in backend folder")
