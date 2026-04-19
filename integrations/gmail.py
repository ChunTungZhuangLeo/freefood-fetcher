"""
Gmail Integration for Night Shift Agent
Fetches and analyzes emails from Gmail.

Setup:
1. Go to Google Cloud Console
2. Create a project and enable Gmail API
3. Create OAuth 2.0 credentials
4. Download credentials.json to this directory
"""

import os
import base64
from typing import List, Dict, Optional
from datetime import datetime, timedelta

# Note: These imports require: pip install google-auth-oauthlib google-api-python-client
try:
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.auth.transport.requests import Request
    from googleapiclient.discovery import build
    GMAIL_AVAILABLE = True
except ImportError:
    GMAIL_AVAILABLE = False
    print("Gmail integration not available. Install with: pip install google-auth-oauthlib google-api-python-client")


SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']


class GmailClient:
    """Gmail API client for fetching emails."""

    def __init__(self, credentials_path: str = "credentials.json"):
        self.credentials_path = credentials_path
        self.token_path = "token.json"
        self.service = None

        if GMAIL_AVAILABLE:
            self._authenticate()

    def _authenticate(self):
        """Authenticate with Gmail API."""
        creds = None

        # Load existing token
        if os.path.exists(self.token_path):
            creds = Credentials.from_authorized_user_file(self.token_path, SCOPES)

        # Refresh or get new credentials
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                if not os.path.exists(self.credentials_path):
                    print(f"Missing {self.credentials_path}. Download from Google Cloud Console.")
                    return

                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_path, SCOPES
                )
                creds = flow.run_local_server(port=0)

            # Save credentials
            with open(self.token_path, 'w') as token:
                token.write(creds.to_json())

        self.service = build('gmail', 'v1', credentials=creds)

    def get_recent_emails(self, max_results: int = 20, hours_back: int = 24) -> List[Dict]:
        """Fetch recent emails from inbox."""
        if not self.service:
            return self._get_mock_emails()

        try:
            # Calculate time filter
            after_time = datetime.now() - timedelta(hours=hours_back)
            query = f"after:{after_time.strftime('%Y/%m/%d')}"

            results = self.service.users().messages().list(
                userId='me',
                q=query,
                maxResults=max_results
            ).execute()

            messages = results.get('messages', [])
            emails = []

            for msg in messages:
                email_data = self.service.users().messages().get(
                    userId='me',
                    id=msg['id'],
                    format='metadata',
                    metadataHeaders=['From', 'Subject', 'Date']
                ).execute()

                headers = {h['name']: h['value'] for h in email_data.get('payload', {}).get('headers', [])}

                emails.append({
                    'id': msg['id'],
                    'from': headers.get('From', 'Unknown'),
                    'subject': headers.get('Subject', 'No subject'),
                    'date': headers.get('Date', ''),
                    'snippet': email_data.get('snippet', ''),
                    'labels': email_data.get('labelIds', [])
                })

            return emails

        except Exception as e:
            print(f"Error fetching emails: {e}")
            return self._get_mock_emails()

    def get_unread_count(self) -> int:
        """Get count of unread emails."""
        if not self.service:
            return 5  # Mock data

        try:
            results = self.service.users().messages().list(
                userId='me',
                q='is:unread',
                maxResults=1
            ).execute()
            return results.get('resultSizeEstimate', 0)
        except Exception:
            return 0

    def _get_mock_emails(self) -> List[Dict]:
        """Return mock emails for testing without Gmail API."""
        return [
            {
                'id': '1',
                'from': 'boss@company.com',
                'subject': 'URGENT: Quarterly Review Tomorrow',
                'date': datetime.now().isoformat(),
                'snippet': 'Please prepare the quarterly numbers for tomorrow\'s 10am meeting with the board.',
                'labels': ['UNREAD', 'IMPORTANT']
            },
            {
                'id': '2',
                'from': 'hackathon@ara.so',
                'subject': 'Ara x JHU Hackathon - Final Reminder',
                'date': datetime.now().isoformat(),
                'snippet': 'The hackathon starts tomorrow at 12pm. Don\'t forget to bring your laptop!',
                'labels': ['UNREAD']
            },
            {
                'id': '3',
                'from': 'team@github.com',
                'subject': 'New pull request in your repository',
                'date': datetime.now().isoformat(),
                'snippet': 'A new pull request has been opened in your repository...',
                'labels': []
            },
            {
                'id': '4',
                'from': 'newsletter@substack.com',
                'subject': 'The AI Agent Revolution',
                'date': datetime.now().isoformat(),
                'snippet': 'This week in AI: autonomous agents are changing everything...',
                'labels': []
            },
            {
                'id': '5',
                'from': 'support@amazon.com',
                'subject': 'Your order has shipped',
                'date': datetime.now().isoformat(),
                'snippet': 'Your package is on the way and will arrive by Friday.',
                'labels': []
            }
        ]


if __name__ == "__main__":
    # Test the client
    client = GmailClient()
    emails = client.get_recent_emails()

    print(f"\nFound {len(emails)} recent emails:\n")
    for email in emails:
        print(f"From: {email['from']}")
        print(f"Subject: {email['subject']}")
        print(f"Preview: {email['snippet'][:100]}...")
        print("-" * 50)
