"""
Google Calendar Integration for Night Shift Agent
Fetches and analyzes calendar events.
"""

import os
from typing import List, Dict
from datetime import datetime, timedelta

try:
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.auth.transport.requests import Request
    from googleapiclient.discovery import build
    CALENDAR_AVAILABLE = True
except ImportError:
    CALENDAR_AVAILABLE = False


SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']


class CalendarClient:
    """Google Calendar API client."""

    def __init__(self, credentials_path: str = "credentials.json"):
        self.credentials_path = credentials_path
        self.token_path = "calendar_token.json"
        self.service = None

        if CALENDAR_AVAILABLE:
            self._authenticate()

    def _authenticate(self):
        """Authenticate with Google Calendar API."""
        creds = None

        if os.path.exists(self.token_path):
            creds = Credentials.from_authorized_user_file(self.token_path, SCOPES)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                if not os.path.exists(self.credentials_path):
                    return

                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_path, SCOPES
                )
                creds = flow.run_local_server(port=0)

            with open(self.token_path, 'w') as token:
                token.write(creds.to_json())

        self.service = build('calendar', 'v3', credentials=creds)

    def get_todays_events(self) -> List[Dict]:
        """Fetch today's calendar events."""
        if not self.service:
            return self._get_mock_events()

        try:
            now = datetime.utcnow()
            start_of_day = now.replace(hour=0, minute=0, second=0, microsecond=0)
            end_of_day = start_of_day + timedelta(days=1)

            events_result = self.service.events().list(
                calendarId='primary',
                timeMin=start_of_day.isoformat() + 'Z',
                timeMax=end_of_day.isoformat() + 'Z',
                singleEvents=True,
                orderBy='startTime'
            ).execute()

            events = events_result.get('items', [])

            return [{
                'id': e.get('id'),
                'title': e.get('summary', 'Untitled'),
                'time': self._format_time(e.get('start', {})),
                'end_time': self._format_time(e.get('end', {})),
                'duration': self._calculate_duration(e.get('start', {}), e.get('end', {})),
                'location': e.get('location', ''),
                'attendees': [a.get('email') for a in e.get('attendees', [])],
                'description': e.get('description', '')
            } for e in events]

        except Exception as e:
            print(f"Error fetching calendar: {e}")
            return self._get_mock_events()

    def _format_time(self, time_obj: Dict) -> str:
        """Format calendar time object."""
        if 'dateTime' in time_obj:
            dt = datetime.fromisoformat(time_obj['dateTime'].replace('Z', '+00:00'))
            return dt.strftime('%I:%M %p')
        elif 'date' in time_obj:
            return 'All day'
        return 'TBD'

    def _calculate_duration(self, start: Dict, end: Dict) -> str:
        """Calculate event duration."""
        try:
            if 'dateTime' in start and 'dateTime' in end:
                start_dt = datetime.fromisoformat(start['dateTime'].replace('Z', '+00:00'))
                end_dt = datetime.fromisoformat(end['dateTime'].replace('Z', '+00:00'))
                duration = end_dt - start_dt
                hours = duration.seconds // 3600
                minutes = (duration.seconds % 3600) // 60
                if hours > 0:
                    return f"{hours}h {minutes}m" if minutes else f"{hours}h"
                return f"{minutes}m"
        except Exception:
            pass
        return "Unknown"

    def _get_mock_events(self) -> List[Dict]:
        """Return mock events for testing."""
        return [
            {
                'id': '1',
                'title': 'Morning Standup',
                'time': '9:00 AM',
                'end_time': '9:30 AM',
                'duration': '30m',
                'location': 'Zoom',
                'attendees': ['team@company.com'],
                'description': 'Daily team sync'
            },
            {
                'id': '2',
                'title': 'Product Review',
                'time': '10:00 AM',
                'end_time': '11:00 AM',
                'duration': '1h',
                'location': 'Conference Room A',
                'attendees': ['pm@company.com', 'designer@company.com'],
                'description': 'Review Q2 roadmap'
            },
            {
                'id': '3',
                'title': 'Lunch with Mentor',
                'time': '12:30 PM',
                'end_time': '1:30 PM',
                'duration': '1h',
                'location': 'Cafe Luna',
                'attendees': [],
                'description': ''
            },
            {
                'id': '4',
                'title': 'Deep Work Block',
                'time': '2:00 PM',
                'end_time': '4:00 PM',
                'duration': '2h',
                'location': '',
                'attendees': [],
                'description': 'Focus time - no meetings'
            },
            {
                'id': '5',
                'title': 'Hackathon Prep',
                'time': '4:30 PM',
                'end_time': '5:30 PM',
                'duration': '1h',
                'location': 'Home',
                'attendees': [],
                'description': 'Prepare for Ara hackathon'
            }
        ]


if __name__ == "__main__":
    client = CalendarClient()
    events = client.get_todays_events()

    print(f"\nToday's events ({len(events)}):\n")
    for event in events:
        print(f"{event['time']} - {event['title']} ({event['duration']})")
        if event['location']:
            print(f"  📍 {event['location']}")
        print()
