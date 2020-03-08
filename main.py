from bs4 import BeautifulSoup
import requests


def get_html(url):
    response = requests.get(url)
    return response.text


def parse_page(url: list):
    print(url)
    html = get_html(url)
    soup = BeautifulSoup(html)
    div = soup.find('div', class_='inread-content')
    print("DIV:", div)
    div_str: str = str(div)
    count_p = div_str.count('<p>')
    print("count_p:", str(count_p))

    p: str = div_str.partition('<p>')[2].partition('</p>')[0]
    print("p:", p)
    for i in range(count_p-1):
        p: str = div_str.partition('<p>')[2].partition('</p>')[2]
        print("p:", p)
        p: str = p.partition('<p>')[2].partition('</p>')[0]
        print("p:", p)


def parse_main(html) -> None:
    soup = BeautifulSoup(html)
    ul = soup.find('ul', class_='news_list news_list_big')
    a_list: list = ul.find_all_next('a')
    # print(a_list)

    all_link: list = []
    for i in a_list:
        str_a = str(i)
        a = str_a.partition('f="')[2].partition('">')[0]
        all_link.append(a)

    for i in all_link:
        parse_page(i)
        break


def main():
    site_url = "https://www.mk.ru/news/"
    html = get_html(site_url)
    # print(html)
    parse_main(html)


if __name__ == ("__main__"):
    main()