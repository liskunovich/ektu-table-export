from all_schedule_links_parser import get_general_links_list
from decorators import timer
from individual_schedule_parser import parse_table, get_group_name
from utilities import get_html


@timer
def main(url):
    html = get_html(url)
    if html.status_code == 200:
        parse_table(html.text, url)
    else:
        print('Site is not working')


# if __name__ == "__main__":
#     main(input("Введите ссылку на расписание группы:\n"))

if __name__ == "__main__":
    links_list = get_general_links_list()
    for element in links_list:
        for link in element:
            main(link)
