from bs4 import BeautifulSoup
import time
import requests
import urllib3

URL = "https://www.do.ektu.kz/PReports/Schedule/ScheduleGroup.asp?page=3&GroupID=12072"
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36',
    'accept': '*/*'}


def get_html(url, params=None):
    r = requests.get(url, headers=headers, params=params)
    r.encoding = 'utf8'
    return r


def get_content(html):
    data = []
    soup = BeautifulSoup(html, 'html.parser')
    group_name = soup.find_all(text=re.compile('\[(.*\d?)\]'))
    table = soup.find_all('table', attrs={'class': 'lineItemsTable'})
    # print(html)
    print(group_name)


def parse():
    html = get_html(URL)
    if html.status_code == 200:
        print("Site is working")
        get_content(html.text)
    else:
        print("Site is not working")


parse()
