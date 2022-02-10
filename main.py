
from bs4 import BeautifulSoup
from fake_headers import Headers
from schedule_parser import get_html, get_group_name, get_cell_info
from schedule_parser import get_table, URL, headers
from calendar_exporter import export
import time
from google_filler import GoogleCalendar
import requests
import urllib3


def parse():
    html = get_html(URL)
    if html.status_code == 200:
        print("Site is working")
        get_table(html.text)
        # group_name = get_group_name(html.text)
    else:
        print("Site is not working")


parse()
