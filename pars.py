import requests  # для запроса к hh api
import json  # для обработки
import logging
from bd import Db
from textanalysis import Analyse

class Pars():
    def __init__(self):
        self.hh_url = 'https://api.hh.ru/'  # url hh для получения вакансий
        self.superjob_url = 'https://api.superjob.ru/2.0/'

        logging.basicConfig(filename='logs.log', level=logging.INFO, format='%(asctime)s %(message)s')

    def get_page(self, page):
        # формирование и отправка запроса
        params = {
            'area': 1,
            'page': page,
            'per_page': 100,
            'app_key': 'v3.r.137503460.fd89b87cab8626a226ed50a00b025a9e5ecbe1b9.6a576eab96e6323b2dd4ae40db5122f78a295c92'
        }
        superjob_req = requests.get(self.superjob_url + 'vacancies', params)
        hh_req = requests.get(self.hh_url + 'vacancies', params)

        hh_data = hh_req.content.decode()

        superjob_data = superjob_req.content.decode()

        superjob_req.close()
        hh_req.close()

        logging.info(f'получение вакансий с {page} страницы')

        return (hh_data, superjob_data)

    def get_vacancy(self):
        # обработка запроса добавляем информацию о вакансии в список каждый элемент которого является вакансией

        logging.info(f'получение вакансий')

        db = Db()
        db.clear_tabel()

        analyse = Analyse()

        for page in range(0, 20):
            js = self.get_page(page)
            hh_vacancys = json.loads(js[0])
            superjob_vacancys = json.loads(js[1])

            hh_db_add = []
            sj_db_add = []

            for i in hh_vacancys['items']:
                hh_db_add.append({'vacancy_name': str(i['name']),
                            'requirements': analyse.prepare(str(i['snippet']['requirement'])),
                            'salary': i['salary'],
                            'url': str(i['alternate_url']),
                            'employer': str(i['employer'])
                            })

            for i in superjob_vacancys['objects']:
                sj_db_add.append({'vacancy_name': str(i['profession']),
                                        'requirements': analyse.prepare(str(i['candidat'])),
                                        'salary': i['payment_from'],
                                        'url': str(i['link']),
                                        'employer': str(i['firm_name'])
                                         })

            for i in hh_db_add + sj_db_add:
                db.update_tabel(i)
