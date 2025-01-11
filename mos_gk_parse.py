import requests
from bs4 import BeautifulSoup
import re

# импорты из моих модулей
from db.mos_gk_db import checkProd, addNewProd

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
        response = requests.get(
            url=url
        )
        soup = BeautifulSoup(response.text, 'lxml')

        # в список получаю элементы из хлебных крошек
        breadcrumbs_container = soup.find('div', class_='breadcrumb-wrapper-2 intec-content-wrapper')
        breadcrumbs_item = breadcrumbs_container.find_all('div', class_="breadcrumb-item")
        breadcrumbs_list = []
        for breadcrumb in breadcrumbs_item:
            breadcrumbs_list.append(breadcrumb.text.strip())
        # Удаляем \n и всё, что после него
        cleaned_breadcrumbs = [item.split('\n')[0] for item in breadcrumbs_list]
        
        product_title = soup.find('h1').text.strip()
        print(product_title)
        name_separation_1 = extract_product_name(product_title)
        if name_separation_1 is None:
            name_separation_1 = 'отсутствует'
        name_separation_2 = extract_dimensions(product_title)
        if name_separation_2 is None:
            name_separation_2 = 'отсутствует'

        # Инициализация переменных
        length = 'характеристика отсутствует'
        width = 'характеристика отсутствует'
        height = 'характеристика отсутствует'
        mark = 'характеристика отсутствует'
        profile = 'характеристика отсутствует'
        color = 'характеристика отсутствует'
        options_container = soup.find('div', class_='catalog-element-section-properties')
        options_items = options_container.find_all('div', class_='catalog-element-section-property')
        for option in options_items:
            option_name = option.find('div', class_='catalog-element-section-property-name').text.strip()
            if option_name == 'Длина, мм':
                length = option.find('div', class_='catalog-element-section-property-value').text.strip()
                length = length.replace(';', '') # Удаляем точку с запятой
            if option_name == 'Ширина, мм':
                width = option.find('div', class_='catalog-element-section-property-value').text.strip()
                width = width.replace(';', '') # Удаляем точку с запятой
            if option_name == 'Высота, мм':
                height = option.find('div', class_='catalog-element-section-property-value').text.strip()
                height = height.replace(';', '') # Удаляем точку с запятой
            if option_name == 'Марка':
                mark = option.find('div', class_='catalog-element-section-property-value').text.strip()
                mark = mark.replace(';', '') # Удаляем точку с запятой
            if option_name == 'Профиль':
                profile = option.find('div', class_='catalog-element-section-property-value').text.strip()
                profile = profile.replace(';', '') # Удаляем точку с запятой
            if option_name == 'Цвет':
                color = option.find('div', class_='catalog-element-section-property-value').text.strip()
                color = color.replace(';', '') # Удаляем точку с запятой

        normal_price = soup.find('div', class_='catalog-element-price-discount intec-grid-item-auto').text.strip()
        normal_price = normal_price.replace(' руб.', '')
        
        addNewProd(url, breadcrumbs_list, product_title, name_separation_1, name_separation_2, length, width, height, mark, profile, color, normal_price)

# функция для вырезания из названия того, что идет до размеров
def extract_product_name(product):
    # Регулярное выражение для поиска части до указания размеров
    pattern = r'^[^0-9]+(?=\s*\d)'
    match = re.match(pattern, product)
    if match:
        return match.group(0).strip()
    else:
        return None

def extract_dimensions(product):
    # Регулярное выражение для поиска размеров в формате "70*70*60"
    pattern = r'\d+[*х]\d+[*х]\d+'
    match = re.search(pattern, product)
    if match:
        return match.group(0)
    else:
        return None



def main(url):
    mos_gk_main_parse(url)

if __name__ == "__main__":
    main('https://mos-gk.ru/catalog/')