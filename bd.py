import json
import logging
import psycopg2
from psycopg2 import extensions, extras

class Db:
    def __init__(self):
        self.conn = psycopg2.connect(dbname='postgres', user='postgres',
                        password='11111', host='localhost')

        self.cursor = self.conn.cursor()
        logging.basicConfig(filename='logs.log', level=logging.INFO, format='%(asctime)s %(message)s')

    def create_tabel(self):
        logging.info(f'создание таблицы')
        self.cursor.execute(
            '''CREATE TABLE VACANCYS(
                VACANCY JSON
                )''')
        self.conn.commit()

    def update_tabel(self, data):
        insert_query = '''INSERT INTO VACANCYS (VACANCY)
                    VALUES (%s)'''
        extensions.register_adapter(dict, extras.Json)
        self.cursor.execute(insert_query, [data])
        self.conn.commit()

    def clear_tabel(self):
        logging.info(f'очищение таблицы')
        self.cursor.execute('''DELETE FROM VACANCYS''')
        self.conn.commit()

    def del_tabel(self):
        logging.info(f'удаление таблицы')
        self.cursor.execute('''DROP TABLE VACANCYS''')
        self.conn.commit()


    def check_tabel_exist(self):
        self.cursor.execute('''SELECT EXISTS(SELECT 1 FROM VACANCYS)''')
        return self.cursor.fetchall()

    def check_tabel_void(self):
        logging.info(f'проверка на пустоту')

        self.cursor.execute('''SELECT COUNT(*) FROM VACANCYS''')
        return self.cursor.fetchall()


    def get_tabel(self):
        logging.info(f'получение таблицы')
        self.cursor.execute('''SELECT * FROM VACANCYS''')

        vacancys = self.cursor.fetchall()

        vacancyslist = []

        for row in vacancys:
            vacancyslist.append(row[0])

        return vacancyslist

