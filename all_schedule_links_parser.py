import requests
from fake_headers import Headers
from bs4 import BeautifulSoup
import re

from decorators import timer
from utilities import get_html

URL = 'https://www.do.ektu.kz/PReports/Schedule/ScheduleGroup.asp?lang=kz'

HTML = get_html(URL)


def parse_table(html):
    soup = BeautifulSoup(html, 'lxml')
    table = soup.findAll('table', {'class': 'date'})
    # if len(table) == 0:
    #     print(soup.prettify())
    return table[1]


def get_links(table):
    links = table.findAll('a', {"class": 'main'}, text=re.compile(r'[0-9]+'))
    # print(len(links))
    # print('\n'.join(list(map(lambda x: x.attrs['href'], links))))
    return list(map(lambda x: 'https://www.do.ektu.kz/PReports/Schedule/ScheduleGroup.asp' + x.attrs['href'], links))


@timer
def get_general_links_list():
    links_list = []
    for link in get_links(parse_table(HTML.text)):
        links_list.append((get_links(parse_table(get_html(link).text))))
    return links_list
