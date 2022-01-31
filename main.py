from bs4 import BeautifulSoup
from fake_headers import Headers
from schedule_parser import get_html, get_group_name, get_cell_info
from schedule_parser import get_table
import time
import requests
import urllib3

URL = "https://www.do.ektu.kz/PReports/Schedule/ScheduleGroup.asp?page=3&GroupID=12072"
headers = Headers(headers=True)


def parse():
    html = get_html(URL)
    if html.status_code == 200:
        print("Site is working")
        get_table(html.text)
        get_group_name(html.text)
        get_cell_info(html.text)
    else:
        print("Site is not working")


parse()
