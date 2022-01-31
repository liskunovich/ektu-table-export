import requests
from fake_headers import Headers
from bs4 import BeautifulSoup
import re

URL = "https://www.do.ektu.kz/PReports/Schedule/ScheduleGroup.asp?page=3&GroupID=12072"
headers = Headers(headers=True)


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
    data = []
    soup = BeautifulSoup(html, 'lxml')
    table = soup.find_all('table', {'id': 'tblSchedule'})
    get_group_name(html)
    # print(html)


def get_cell_info(html):
    row_data = []
    soup = BeautifulSoup(html, 'lxml')
    table = soup.find_all('td')
    for row in table:
        row_data.append(row)
    row_data = row_data[15::]
    # rows = soup.find_all("tr")
    #
    # for row in rows:
    #     element = row.find_all("th")
    #     row_data.append(element)
    # row_data = [cell for cell in row_data if len(cell) > 0]
    print(row_data)


