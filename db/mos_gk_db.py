import pymysql.cursors

from .db import get_database_connection

############# проверка наличия продукта по url ################
def checkProd (url):
    # Получить соединение с базой данных
    connection = get_database_connection()

    try:
        with connection.cursor() as cursor:
            # SQL
            sql = "SELECT `id` FROM `mos_gk` WHERE `url` = %s"
            # Выполнить команду запроса (Execute Query).
            # есть пользователь с этим ником в базе
            res = cursor.execute(sql, (url))
            return res
    except pymysql.Error as e:
        print("Error:", e)
        return None
    finally:
        # Закрыть соединение (Close connection).
        connection.close()

############# добавление нового продукта ################
def addNewProd(url, breadcrumbs_list, product_title, name_separation_1, name_separation_2):
    # Получить соединение с базой данных
    connection = get_database_connection()

    print ("connect successful addNewProd!")
    try:
        with connection.cursor() as cursor:
            # Проверка длины breadcrumbs_list
            if len(breadcrumbs_list) == 2:
                print("Попадаем в условие для длины 2")  # Отладочный вывод
                sql = "INSERT INTO `mos_gk` (`url`, `level_1`, `level_2`, `title_h1`, `name_separation_1`, `name_separation_2`) VALUES (%s, %s, %s, %s, %s, %s)"
                values = (url, breadcrumbs_list[0], breadcrumbs_list[1], product_title, name_separation_1, name_separation_2)
            elif len(breadcrumbs_list) == 3:
                sql = "INSERT INTO `mos_gk` (`url`, `level_1`, `level_2`, `level_3`, `title_h1`, `name_separation_1`, `name_separation_2`) VALUES (%s, %s, %s, %s, %s, %s)"
                values = (url, breadcrumbs_list[0], breadcrumbs_list[1], breadcrumbs_list[2], product_title, name_separation_1, name_separation_2)
            elif len(breadcrumbs_list) == 4:
                sql = "INSERT INTO `mos_gk` (`url`, `level_1`, `level_2`, `level_3`, `level_4`, `title_h1`, `name_separation_1`, `name_separation_2`) VALUES (%s, %s, %s, %s, %s, %s)"
                values = (url, breadcrumbs_list[0], breadcrumbs_list[1], breadcrumbs_list[2], breadcrumbs_list[3], product_title, name_separation_1, name_separation_2)
            elif len(breadcrumbs_list) == 5:
                sql = "INSERT INTO `mos_gk` (`url`, `level_1`, `level_2`, `level_3`, `level_4`, `level_5`, `title_h1`, `name_separation_1`, `name_separation_2`) VALUES (%s, %s, %s, %s, %s, %s)"
                values = (url, breadcrumbs_list[0], breadcrumbs_list[1], breadcrumbs_list[2], breadcrumbs_list[3], breadcrumbs_list[4], product_title, name_separation_1, name_separation_2)
            else:
                raise ValueError("breadcrumbs_list должен содержать от 2 до 5 элементов")
            res = cursor.execute(sql, values)
            connection.commit()
            inserted_id = cursor.lastrowid
            return inserted_id
    except pymysql.Error as e:
        print("Error:", e)
        return 0  # Верните значение, которое указывает на неудачу
    finally:
        # Закрыть соединение (Close connection).
        connection.close()