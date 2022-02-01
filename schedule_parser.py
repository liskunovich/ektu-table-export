import requests
from fake_headers import Headers
from bs4 import BeautifulSoup
import re

URL = "https://www.do.ektu.kz/PReports/Schedule/ScheduleGroup.asp?page=3&GroupID=12072"
headers = Headers(headers=True)
data = []
week = {"1": "Понедельник",
        "2": "Вторник",
        "3": "Среда",
        "4": "Четверг",
        "5": "Пятница",
        "6": "Суббота"}


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
    soup = BeautifulSoup(html, 'lxml')
    table = soup.find('table', {'id': 'tblSchedule'})
    rows = table.find_all('tr', recursive=False)
    rows = rows[1:]
    for row in rows:
        cols = row.find_all('td')
        # cols = [re.sub(r'\n+', " ", ele.text).strip() for ele in cols]
        data.append([ele for ele in cols if ele])
    # print(data[0])
    # get_group_name(html)
    # print(data[0])
    get_cell_info(data)


def get_cell_info(data_table):
    for i in range(1):
        day_count = 0
        for ele in data_table[i]:
            day_count += 1
            if ele.text == " ":
                print("Free Time")
            else:
                print(ele.text)
                # print(week[f'{day_count}'])
