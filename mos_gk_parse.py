import requests
from bs4 import BeautifulSoup
import re

# # импорты из моих модулей
# from db.gofroeuropack_db import checkProd, addNewProd

def mos_gk_main_parse(url):
    response = requests.get(url=url)
    soup = BeautifulSoup(response.text, 'lxml')
    print(response)


def main(url):
    mos_gk_main_parse(url)

if __name__ == "__main__":
    main('https://mos-gk.ru/catalog/')