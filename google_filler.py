from __future__ import print_function
import datetime
import googleapiclient
from google.oauth2 import service_account
from googleapiclient.discovery import build
from schedule_parser import event

SCOPES = ['https://www.googleapis.com/auth/calendar']

calendarId = '2eeo0n10e1oqgfh42ul503bvc4@group.calendar.google.com'  # in calendar settings
SERVICE_ACCOUNT_FILE = 'spheric-hawk-340206-19cc1befa5b4.json'  # in service acc by creating key

tz = datetime.timezone(offset=datetime.timedelta(hours=3), name='Almaty')
time = datetime.datetime.now(tz=tz)
print(time.weekday())
print(time)


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
        print('Event created: %s' % (e.get('id')))

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
        calendars = self.service.calendars()
        self.service.calendars().clear('proimary').execute()


calendar = GoogleCalendar()
calendar.clear_cal()
# print("+ - create event\n? - print event list\n")
# c = input()
#
# if c == '+':
#     cal_event = event
#     calendar.create_event(cal_event)
# elif c == '?':
#     calendar.get_events_list()
# else:
#     pass
