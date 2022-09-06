import os
from fake_headers import Headers
from bs4 import BeautifulSoup
import re
from icalendar import *
import datetime
from datetime import datetime
from datetime import timedelta
from dateutil.relativedelta import relativedelta
from utilities import get_html

from decorators import timer

headers = Headers(headers=True)
data = []
current_status = 0
current_day = " "

week = {
    "0": "monday",
    "1": "tuesday",
    "2": "wednesday",
    "3": "thursday",
    "4": "friday",
    "5": "saturday"
}

time_dict = {
    "0": "08:00 - 08:50",
    "1": "08:55 - 09:45",
    "2": "10:10 - 11:00",
    "3": "11:05 - 11:55",
    "4": "12:55 - 13:45",
    "5": "13:50 - 14:40",
    "6": "15:05 - 15:55",
    "7": "16:00 - 16:50",
    "8": "17:05 - 17:55",
    "9": "18:05 - 18:55"
}


@timer
def get_group_name(html):
    soup = BeautifulSoup(html, 'lxml')
    group_name_element = soup.find("div", {"class": "PageTitle"})
    group_name = re.search(r"Расписание группы:\s(.*)", group_name_element.text).group(1)
    return group_name


@timer
@timer
def parse_table(html, url):
    soup = BeautifulSoup(re.sub(r'<br/>', "|", html), 'lxml')
    table = soup.find('table', {'id': 'tblSchedule'})
    rows = table.find_all('tr', recursive=False)
    rows = rows[1:]
    data.clear()
    for row in rows:
        cols = row.find_all('td', {'class': 'td1'})
        cols = [re.sub(r'\s+', " ", ele.text).strip() for ele in cols]
        data.append([list(map(lambda x: x.strip(), ele.split("|"))) for ele in cols])
    get_cell_info(data, url)


def next_closest_day(from_date, search_day):
    weekdays = ('monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday')
    if isinstance(search_day, str):
        search_day = weekdays.index(search_day.lower())
    from_day = from_date.weekday()
    different_days = search_day - from_day if from_day < search_day else 7 - from_day + search_day
    correct_format = from_date + timedelta(days=different_days)
    return correct_format.strftime("%Y-%m-%d")


@timer
def get_cell_info(data_table, url):
    calendar = Calendar()
    calendar.name = 'VCALENDAR'
    currently_time_count = 0
    for i in range(len(data_table)):
        day_count = 0
        for cell in data_table[i]:
            day_count += 1
            if cell == [""]:
                pass
            else:
                subject_info = get_subject_info(day_count, cell, currently_time_count, url)
                event_start_time = datetime.strptime(f'{subject_info[2]} {subject_info[5]}:00', '%Y-%m-%d %H:%M:%S')
                event_end_time = datetime.strptime(f'{subject_info[2]} {subject_info[6]}:00', '%Y-%m-%d %H:%M:%S')
                calendar.add_component(
                    event_filler(subject_info[4], event_start_time, event_end_time, subject_info[7],
                                 subject_info[8]))
        currently_time_count += 1
    save_to_ics(calendar, url)


def event_filler(auditory, event_start_time, event_end_time, subject_name, subject_description):
    event = Event()
    recurrence_end = event_start_time + relativedelta(months=5)
    event.add('summary', f'{auditory}{subject_name}')
    event.add('description', f'{subject_description}')
    event.add('tzid', 'Asia/Almaty')
    event.add('dtstart', event_start_time)
    event.add('dtend', event_end_time)
    event.add('rrule', {'freq': 'weekly', 'byweek': 1, 'until': recurrence_end})
    return event


def check_time_exist(string):
    if re.match(r'\d{2}:\d{2}\s-\s\d{2}:\d{2}', string):
        return True
    else:
        return False


def save_to_ics(calendar, url):
    directory = os.getcwd() + "/data/"
    f = open(os.path.join(directory, f'{get_group_name(get_html(url).text)}.ics'), 'wb')
    f.write(calendar.to_ical())
    f.close()


def get_subject_info(day_count, cell, currently_time_count, url):
    subject_day = week[f'{day_count - 1}']
    subject_time = re.search(r'\d{2}:\d{2}\s-\s\d{2}:\d{2}', cell[0]).group(0) if check_time_exist(
        cell[0]) else time_dict[f'{currently_time_count}']
    auditory = re.search(r'\[.*?\]', cell[0]).group(0) if check_time_exist(cell[0]) else cell[0]
    subject_name = cell[3] if cell[1] != '-' else cell[2]
    subject_description = cell[4].capitalize() if cell[1] != '-' else cell[3].capitalize()
    current_time = datetime.now(tz=None)
    subject_date = next_closest_day(current_time, subject_day)
    subject_start_time = re.search(r'[^-\s.]*', subject_time).group(0)
    subject_end_time = re.search(r'[^^\d][^\-\s]{4}\d', subject_time).group(0).strip()
    return [subject_day, subject_time, subject_date, current_time, auditory, subject_start_time, subject_end_time,
            subject_name, subject_description]
