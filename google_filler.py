from __future__ import print_function
import datetime
import json

import googleapiclient
import requests
from google.oauth2 import service_account
from googleapiclient.discovery import build
from schedule_parser import event

SCOPES = ['https://www.googleapis.com/auth/calendar', 'https://www.googleapis.com/auth/calendar.events']

calendarId = 'onceuponatimeinektu@gmail.com'  # in calendar settings
SERVICE_ACCOUNT_FILE = 'spheric-hawk-340206-19cc1befa5b4.json'  # in service acc by creating key

tz = datetime.timezone(offset=datetime.timedelta(hours=3), name='Almaty')
time = datetime.datetime.now(tz=tz)
print(time.weekday())
print(time)

id_list = []


class GoogleCalendar(object):

    def __init__(self):
        credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
        self.service = googleapiclient.discovery.build('calendar', 'v3', credentials=credentials)

    # создание словаря с информацией о событии
    # def create_event_dict(self):
    #
    #     return event

    # создание события в календаре
    def create_event(self, event):
        e = self.service.events().insert(calendarId=calendarId,
                                         body=event).execute()
        self.save_to_json(e.get('id'))
        print('Event created: %s' % e.get('id'))

    # вывод списка из десяти предстоящих событий
    def get_events_list(self):
        now = datetime.datetime.utcnow().isoformat() + 'Z'
        print('Getting the upcoming 10 events')
        events_result = self.service.events().list(calendarId=calendarId,
                                                   timeMin=now,
                                                   maxResults=10, singleEvents=True,
                                                   orderBy='startTime').execute()
        events = events_result.get('items', [])

        if not events:
            print('No upcoming events found.')
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            print(start, event['summary'])

    def clear_cal(self):
        events_result = self.service.events().list(calendarId=calendarId,
                                                   timeMin='2022-01-01T07:00:00+03:00',
                                                   maxResults=2500, singleEvents=True,
                                                   orderBy='startTime').execute()
        for i in range(len(self.get_from_json())):
            self.service.events().delete(calendarId='onceuponatimeinektu@gmail.com',
                                         eventId=f'{self.get_from_json()[i]}').execute()
        self.clear_json()

    def save_to_json(self, id):
        content = None
        with open("id_database.json", "r") as file:
            content = file.read()
            content = json.loads(content) if content != '' else []
        with open("id_database.json", "w") as file:
            content.append(id)
            file.write(json.dumps(content))

    def get_from_json(self):
        content = None
        with open("id_database.json", "r") as file:
            content = file.read()
            content = json.loads(content) if content != '' else []
        return content

    def clear_json(self):
        with open("id_database.json", "w") as file:
            file.write(json.dumps([]))


calendar = GoogleCalendar()

print("+ - create event\n? - print event list\n")
c = input()

if c == '+':
    cal_event = event
    calendar.create_event(cal_event)
elif c == '?':
    calendar.get_events_list()
elif c == "clear":
    calendar.clear_cal()
else:
    pass

# 115113879910396707501
#
#
# https://support.sisense.com/kb/en/article/google-calendar-python-export-script
