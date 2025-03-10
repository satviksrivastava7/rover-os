import os
from pathlib import Path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google import generativeai as genai
from email.mime.text import MIMEText
from dotenv import load_dotenv
import base64

load_dotenv()
GEM_API_KEY = os.getenv('GEM_API_KEY')

BASE_DIR = Path(__file__).resolve().parent.parent
SECRETS_DIR = BASE_DIR / "secrets"
TOKEN_PATH = SECRETS_DIR / "token.json"
CREDENTIALS_PATH = SECRETS_DIR / "credentials.json"

SCOPES = [
   "https://www.googleapis.com/auth/gmail.send",
   "https://www.googleapis.com/auth/gmail.modify"
]
creds = None


if TOKEN_PATH.exists():
    creds = Credentials.from_authorized_user_file(str(TOKEN_PATH), SCOPES)
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(str(CREDENTIALS_PATH), SCOPES)
        creds = flow.run_local_server(port=0)

    with open(TOKEN_PATH, "w") as token:
        token.write(creds.to_json())

service = build("gmail", "v1", credentials=creds)
model = genai.configure(api_key=GEM_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

def fetch_mail(params: str, count: int = 5):
    """Fetches emails based on search parameters."""
    try:
        query = f"{params}"
        results = service.users().messages().list(userId='me', q=query, maxResults=count).execute()
        messages = results.get('messages', [])
        
        mails = []
        for msg in messages:
            msg_data = service.users().messages().get(userId='me', id=msg['id']).execute()
            payload = msg_data['payload']
            headers = payload.get('headers', [])
            subject = next((h['value'] for h in headers if h['name'] == 'Subject'), 'No Subject')
            sender = next((h['value'] for h in headers if h['name'] == 'From'), 'Unknown Sender')
            snippet = msg_data.get('snippet', '')
            mails.append({'id': msg['id'], 'subject': subject, 'sender': sender, 'snippet': snippet})
        
        return mails
    except HttpError as error:
        print(f"An error occurred: {error}")
        return []

def gen_summary(mail: str):
    """Summarizes any mail using Gemini AI."""
    prompt = f"Summarize this email: {mail}"
    response = model.generate_content(prompt)
    return response.text

def gen_response(mail: str):
    """Generates replies for any mail using Gemini AI."""
    prompt = f"Generate a professional response for this email: {mail}"
    response = model.generate_content(prompt)
    return response.text

def compose_mail(recipient: str, response_text: str):
    """Composes and send mail to the recipients"""
    try:
        message = MIMEText(response_text)
        message["to"] = recipient
        message["subject"] = "Re: Your email"
        
        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

        send_message = {"raw": raw_message}
        service.users().messages().send(userId="me", body=send_message).execute()
        
        print("Reply sent successfully!")
    except HttpError as error:
        print(f"An error occurred: {error}")

def reply_mail(mail_id: str, recipient: str, response_text: str):
   """Replies to an email within the same thread."""
   try:
      message = MIMEText(response_text)
      message["to"] = recipient
      message["subject"] = "Re: Your email"
      message["In-Reply-To"] = mail_id  
      message["References"] = mail_id   

      raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

      send_message = {
         "raw": raw_message,
         "threadId": mail_id
      }
      service.users().messages().send(userId="me", body=send_message).execute()
      
      print("Reply sent successfully in the same thread!")
   except HttpError as error:
      print(f"An error occurred: {error}")

def search_mail(sender_name: str, content: str, time: str):
    """Searches for emails based on sender, content, and time."""
    query = f"from:{sender_name} {content} after:{time}"
    return fetch_mail(query, count=10)

if __name__ == '__main__':
   """Main block"""
   
   mail = fetch_mail('from: ashutosh', 1)[0]
   print(mail)
   
   summary = gen_summary(mail["snippet"])
   response = gen_response(mail["snippet"])

   reply_mail(mail["id"], mail["sender"], response)