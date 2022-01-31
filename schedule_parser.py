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
    table = soup.find_all('table', attrs={'class': 'lineItemsTable'})
    get_group_name(html)
    print(html)

