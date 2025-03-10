import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
creds = None

if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "D:/Projects/rover/secrets/credentials.json", SCOPES
      )
      creds = flow.run_local_server(port=0)
    with open("token.json", "w") as token:
      token.write(creds.to_json())

service = build("gmail", "v1", credentials=creds)
results = service.users().labels().list(userId="me").execute()
labels = results.get("labels", [])

def fetch_mail(params: str):
   """Method to fetch mail script"""

def gen_summary(mail: str):
   '''Summarises any mail using gemini AI'''

def gen_response(mail: str):
   """Generates replies for any mail using gemini API"""

def reply_mail(mail: str):
   """Replies to the required mail"""

def search_mail(sender_name: str, content: str, time: str):
   """Searches the mail based on the provided arguments"""
   

if __name__ == '__main__':
    """Main block"""
    print('Agent is working properly')
   