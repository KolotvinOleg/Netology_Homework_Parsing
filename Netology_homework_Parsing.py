import requests
from fake_headers import Headers
from bs4 import BeautifulSoup
import re
import json

def get_headers():
    return Headers(browser='chrom', os='win').generate()

def find_word_django_flask(text):
    pattern = 'Django|Flask'
    result = re.search(pattern, text)
    return result

def save_info_in_list(HOST) -> list:
    result_list = []
    response = requests.get(HOST, headers=get_headers())
    all_html_data = response.text
    soup = BeautifulSoup(all_html_data, 'lxml')
    vacancy_list_tag = soup.find_all('div', class_='vacancy-serp-item__layout')
    vacancys = list(vacancy_list_tag)
    for vacancy in vacancys:
        link = vacancy.find('a', class_='serp-item__title')['href']
        salary_tag = vacancy.find('span', class_='bloko-header-section-2')
        if salary_tag:
            salary = salary_tag.text.replace(u"\u202F", " ")
        else:
            salary = None
        company_tag = vacancy.find('a', class_="bloko-link bloko-link_kind-tertiary")
        company = company_tag.text
        city_tag = vacancy.find('div', class_="vacancy-serp-item-company")
        city_tag = city_tag.find_all(class_="bloko-text")
        city = city_tag[1].text.split(',')[0]
        response = requests.get(link, headers=get_headers())
        text = response.text
        if find_word_django_flask(text):
            mini_dict = {
                'link': link,
                'salary': salary,
                'company': company,
                'city': city
            }
            result_list.append(mini_dict)
    return result_list

if __name__ == '__main__':

    HOST = "https://spb.hh.ru/search/vacancy?area=1&area=2&order_by=publication_time&ored_clusters=true&text" \
    "=python&search_period=1"
    result_list = save_info_in_list(HOST)
    with open('result_list.json', 'w', encoding='utf-8') as file:
        json.dump(result_list, file, indent=2, ensure_ascii=False)