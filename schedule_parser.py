import datetime

import requests
from fake_headers import Headers
from bs4 import BeautifulSoup
import re
from google_filler import GoogleCalendar

# URL = "https://www.do.ektu.kz/PReports/Schedule/ScheduleGroup.asp?page=3&GroupID=12072"  # BT
URL = "https://www.do.ektu.kz/PReports/Schedule/ScheduleGroup.asp?page=3&GroupID=12265"  # ПН

headers = Headers(headers=True)
data = []
current_status = 0
current_day = " "
week = {
    "1": "Понедельник",
    "2": "Вторник",
    "3": "Среда",
    "4": "Четверг",
    "5": "Пятница",
    "6": "Суббота"
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




def get_group_name(html):
    soup = BeautifulSoup(html, 'lxml')
    group_name_element = soup.find("div", {"class": "PageTitle"})
    group_name = re.search(r"Расписание группы:\s(.*)", group_name_element.text).group(1)
    return group_name


def get_html(url, params=None):
    r = requests.get(url, headers=headers.generate(), params=params)
    r.encoding = 'utf8'
    return r


def get_table(html):
    soup = BeautifulSoup(re.sub(r'<br/>', "|", html), 'lxml')
    table = soup.find('table', {'id': 'tblSchedule'})
    rows = table.find_all('tr', recursive=False)
    rows = rows[1:]
    for row in rows:
        cols = row.find_all('td', {'class': 'td1'})
        cols = [re.sub(r'\s+', " ", ele.text).strip() for ele in cols]
        data.append([list(map(lambda x: x.strip(), ele.split("|"))) for ele in cols])
    # get_group_name(html)
    # print(data[0])
    get_cell_info(data)


def get_cell_info(data_table):
    calendar = GoogleCalendar()
    currently_time_count = 0
    # for i in range(len(data_table)):
    for i in range(1):
        day_count = 0
        for cell in data_table[i]:
            day_count += 1
            if cell == [""]:
                pass
            else:
                subject_day = week[f'{day_count}']
                subject_time = re.search(r'\d{2}:\d{2}\s-\s\d{2}:\d{2}', cell[0]).group(0) if check_time_exist(
                    cell[0]) else time_dict[
                    f'{currently_time_count}']
                auditory = re.search(r'\[.*?\]', cell[0]).group(0) if check_time_exist(cell[0]) else cell[0]
                # tz = datetime.timezone(offset=datetime.timedelta(hours=3), name='Almaty')
                # time = datetime.datetime.now(tz=tz)
                # print(time.weekday())
                # print(time)
                # start_date =
                # end_date =
                start_time = re.search(r'[^-\s.]*', subject_time).group(0)
                end_time = re.search(r'[^^\d][^\-\s]{4}\d', subject_time).group(0).strip()
                event = {
                    'summary': f'{auditory}{cell[3]}',
                    'description': f'{cell[4]}', # Teacher or Type or What? Solve it
                    'start': {
                        'dateTime': f'2022-02-09T{start_time}:00+00:00',
                        'timeZone': 'Asia/Almaty'
                    },
                    'end': {
                        'dateTime': f'2022-02-10T{end_time}:00+00:00',
                        'timeZone': 'Asia/Almaty'
                    },
                    'recurrence': [
                        'RRULE:FREQ=WEEKLY;UNTIL=20220601T170000Z',
                    ]
                }
                # print(subject_time, subject_day)
                print(event)
        currently_time_count += 1


def check_time_exist(string):
    if re.match(r'\d{2}:\d{2}\s-\s\d{2}:\d{2}', string):
        return True
    else:
        return False
