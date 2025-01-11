import requests
from bs4 import BeautifulSoup
import re

# # импорты из моих модулей
# from db.gofroeuropack_db import checkProd, addNewProd

def mos_gk_main_parse(url):
    response = requests.get(url=url)
    soup = BeautifulSoup(response.text, 'lxml')
    all_categories = soup.find_all('a', class_="catalog-section-list-item-title intec-cl-text-hover")
    for category in all_categories:
        category_url = category.get('href')
        category_url = f"https://mos-gk.ru{category_url}"
        mos_gk_category_parse(category_url)

def mos_gk_category_parse(url):
    response = requests.get(url=url)
    soup = BeautifulSoup(response.text, 'lxml')
    pagi_container = soup.find('div', class_='system-pagenavigation-items-wrapper')
    if pagi_container:
        last_page = int(pagi_container.find_all('div', class_='system-pagenavigation-item')[-2].text.strip())
        for page in range(1, last_page + 1):
            page_url = f'{url}?PAGEN_1={page}'
            response_2 = requests.get(url=page_url)
            soup_2 = BeautifulSoup(response_2.text, 'lxml')
            all_products = soup_2.find_all('div', class_='catalog-section-item-name')
            for product in all_products:
                product_url = product.find('a').get('href')
                product_url = f"https://mos-gk.ru{product_url}"
                go_to_one_product(product_url)
    else:
        all_products = soup.find_all('div', class_='catalog-section-item-name')
        for product in all_products:
            product_url = product.find('a').get('href')
            product_url = f"https://mos-gk.ru{product_url}"
            go_to_one_product(product_url)

def go_to_one_product(url):
    checking_prod = checkProd(url)
    if checking_prod:
        print(f'Продукт {url} уже есть в базе данных')
    else:
        print('no')
        print(url)



def main(url):
    mos_gk_main_parse(url)

if __name__ == "__main__":
    main('https://mos-gk.ru/catalog/')