import os

from schedule_parser import get_html, get_group_name
from schedule_parser import get_table, URL


def parse():
    html = get_html(URL)
    if html.status_code == 200:
        print("Site is working")
        group_name = get_group_name(html.text)
        if os.path.isfile(f'C:\\Users\\david\\PycharmProjects\\ektuTable\\timeTable\\data\\{group_name}.zip'):
            print("File Exist")
        else:
            get_table(html.text)
            os.rename('C:\\Users\\david\\PycharmProjects\\ektuTable\\timeTable\\data\\onceuponatimeinektu@gmail.com.ical.zip',
                  f'C:\\Users\\david\\PycharmProjects\\ektuTable\\timeTable\\data\\{group_name}.zip')
    else:
        print("Site is not working")


parse()
