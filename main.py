from bs4 import BeautifulSoup
import requests
from random import randint
from time import sleep

def write_text_in_file(text: str) -> None:
    file = open("ru_text.txt", "a")
    file.write(text)
    file.close()


def get_html(url):
    response = requests.get(url)
    return response.text


def clean_p_from_a(p_with_a: str) -> str:
    if "<a href=" in p_with_a:
        print("<a href=")
        p_without_a_begin: str = p_with_a.partition('<a href="')[0]
        p_without_a_middle: str = p_with_a.partition('_blank">')[2].partition('</a>')[0]
        p_without_a_end: str = p_with_a.partition('</a>')[2]
        p_without_a: str = p_without_a_begin + p_without_a_middle + p_without_a_end
        print("p_without_a:", p_without_a)
    else:
        p_without_a: str = p_with_a

    return p_without_a


def parse_page(url: list) -> str:
    print("=====================================================================================\n\n")
    print("Ссылка:", url)
    html = get_html(url)
    soup = BeautifulSoup(html)
    div = soup.find('div', class_='inread-content')
    # print("DIV:", div)
    div_str: str = str(div)
    count_p: int = div_str.count('<p>')
    print("count_p:", str(count_p))

    p: str = div_str.partition('<p>')[2].partition('</p>')[0]
    print("p:", p)

    rest_of_text: str = div_str.partition('<p>')[2].partition('</p>')[2]
    # print("rest:", rest_of_text)

    p = clean_p_from_a(p)

    result_text: str = p

    for i in range(count_p - 1):
        p = rest_of_text.partition('<p>')[2].partition('</p>')[0]
        print("px2:", p)

        p = clean_p_from_a(p)

        if "<strong>" in p:
            print("Find strong -> BREAK")
            break

        if "<blockquote" in p:
            print("Find <blockquote -> BREAK")
            break

        if "incut incut--photostory" in p:
            print("Find: incut incut--photostory -> BREAK")
            break

        if "<img alt=" in p:
            print("Find: <img alt= -> BREAK")
            break

        if "<div>" in p:
            print("Find: <div> -> BREAK")
            break

        if "article__incut" in p:
            print("Find: article__incut -> BREAK")
            break

        result_text += p

        if i + 1 != count_p - 1:
            rest_of_text = rest_of_text.partition('<p>')[2].partition('</p>')[2]

            # print("restx2:", rest_of_text)

    return result_text + "\n"


def parse_main(html) -> None:
    soup = BeautifulSoup(html)
    ul = soup.find('ul', class_='news_list news_list_big')
    a_list: list = ul.find_all_next('a')
    # print(a_list)

    all_link: list = []
    for i in a_list:
        str_a = str(i)
        a = str_a.partition('f="')[2].partition('">')[0]

        if "/news/" in a:
            break

        if "#" in a:
            break

        all_link.append(a)

    print("all_link:" , all_link)

    for i in all_link:
        text_of_page: str = parse_page(i)
        write_text_in_file(text_of_page)

    rand:int = randint(10, 100)
    print("Пауза на: ", rand)
    sleep(rand)


def main():
    year: int = 2020
    month_: int = 2
    day_in_month: int = 27
    for m in range(month_):
        for day in range(day_in_month):
            site_url = "https://www.mk.ru/news/" + str(year) + "/" + str(m+1) + "/" + str(day + 1) + "/"
            html = get_html(site_url)
            # print(html)
            parse_main(html)


if __name__ == "__main__":
    main()
