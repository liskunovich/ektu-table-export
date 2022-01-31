from bs4 import BeautifulSoup
from fake_headers import Headers
import time
import requests
import urllib3
import re

URL = "https://www.do.ektu.kz/PReports/Schedule/ScheduleGroup.asp?page=3&GroupID=12072"
headers = Headers(headers=True)


def get_html(url, params=None):
    r = requests.get(url, headers=headers.generate(), params=params)
    r.encoding = 'utf8'
    return r


def get_group(html):
    soup = BeautifulSoup(html, 'lxml')
    group_name_element = soup.find("div", {"class": "PageTitle"})
    group_name = re.search(r"Расписание группы:\s(.*)", group_name_element.text).group(1)
    return group_name


def get_content(html):
    data = []
    soup = BeautifulSoup(html, 'lxml')
    table = soup.find_all('table', attrs={'class': 'lineItemsTable'})
    get_group(html)
    # print(html)


def parse():
    html = get_html(URL)
    if html.status_code == 200:
        print("Site is working")
        get_content(html.text)
    else:
        print("Site is not working")


parse()
