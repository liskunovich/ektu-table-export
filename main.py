from schedule_parser import get_html
from schedule_parser import get_table, URL


def parse():
    html = get_html(URL)
    if html.status_code == 200:
        print("Site is working")
        get_table(html.text)
        # group_name = get_group_name(html.text)
    else:
        print("Site is not working")


parse()
