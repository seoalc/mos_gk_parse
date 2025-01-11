import pymysql.cursors
from dotenv import load_dotenv
import os

# Загружаем переменные из .env
load_dotenv()

def get_database_connection():
    connection = pymysql.connect(host=os.getenv('DB_HOST'),
                                 user=os.getenv('DB_USER'),
                                 password=os.getenv('DB_PASSWORD', ''),
                                 db=os.getenv('DB_NAME'),
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    return connection