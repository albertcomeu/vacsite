from PyPDF2 import PdfReader
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.cluster import AgglomerativeClustering
from sklearn.metrics import silhouette_score
import matplotlib.pyplot as plt
import pandas as pd
import logging


class Count:
    def __init__(self, resumestr_from_bot):
        from textanalysis import Analyse
        from bd import Db
        analyse = Analyse()
        bd = Db()
        self.vacancys = bd.get_tabel()
        self.vacancys_req = []

        resumestr = {'vacancy_name': 'resume', 'requirements': resumestr_from_bot}

        resumestr['requirements'] = analyse.prepare(resumestr_from_bot)

        self.vacancys.append(resumestr)

        logging.info(f'инициализация класса Count')

    def fill_req(self):
        for vacancy in range(len(self.vacancys)):
            self.vacancys_req.append(' '.join(self.vacancys[vacancy]['requirements']))
        logging.info(f'заполнение вакансий')

    def silhouette_method(self):
        from sklearn.feature_extraction.text import TfidfVectorizer
        from scipy.cluster.hierarchy import dendrogram, linkage
        import matplotlib.pyplot as plt

        tfidf = TfidfVectorizer().fit_transform(self.vacancys_req)
        linkage_matrix = linkage(tfidf.toarray(), method='ward')

        # Построение дендрограммы
        plt.figure(figsize=(20, 10))
        dendrogram(linkage_matrix, truncate_mode='lastp', p=60, show_leaf_counts=True)
        plt.xlabel('Samples')
        plt.ylabel('Distance')
        plt.title('Dendrogram')
        plt.xticks(rotation=90)
        plt.tight_layout()
        plt.show()

    def agglomerate_clastering_for_mark(self):

        logging.info(f'кластеризация')

        tfidf = TfidfVectorizer().fit_transform(self.vacancys_req)

        cluster = AgglomerativeClustering(n_clusters=166, affinity='euclidean', linkage='ward')

        cluster.fit_predict(tfidf.toarray())

        clusters = cluster.labels_

        res = []

        for vacancy in range(len(self.vacancys)):
            res.append({'Text: ': self.vacancys[vacancy], 'Cluster: ': clusters[vacancy]})

        resume_claster = -1
        recomend_vacancy = []

        for el in res:
            if 'resume' in el['Text: ']['vacancy_name']:
                resume_claster = el['Cluster: ']
                break

        if resume_claster == -1:
            return 'Подходящих вакансий не найдено :('

        for el in res:
            if el['Cluster: '] == resume_claster and el['Text: ']['vacancy_name'] != 'resume':
                el['label'] = 1

            else: el['label'] = 0

            if el['Text: ']['vacancy_name'] == 'resume':
                res.remove(el)

        return res

    def agglomerate_clastering(self):

        logging.info(f'кластеризация')

        tfidf = TfidfVectorizer().fit_transform(self.vacancys_req)

        cluster = AgglomerativeClustering(n_clusters=166, affinity='euclidean', linkage='ward')

        cluster.fit_predict(tfidf.toarray())

        clusters = cluster.labels_

        res = []

        for vacancy in range(len(self.vacancys)):
            res.append({'Text: ': self.vacancys[vacancy], 'Cluster: ': clusters[vacancy]})

        resume_claster = -1
        recomend_vacancy = []

        for el in res:
            if 'resume' in el['Text: ']['vacancy_name']:
                resume_claster = el['Cluster: ']
                break

        if resume_claster == -1:
            return 'Подходящих вакансий не найдено :('

        for el in res:
            if el['Cluster: '] == resume_claster and el['Text: ']['vacancy_name'] != 'resume':
                recomend_vacancy.append(el)

        return recomend_vacancy

    def get_rec_v_and_salary(self):

        logging.info(f'расчёт зп')

        recomend_vacancy = self.agglomerate_clastering()

        if recomend_vacancy == 'Подходящих вакансий не найдено :(': return recomend_vacancy

        salary = []

        final_vacancys = []

        for vacancy in recomend_vacancy:
            final_vacancys.append({'Название вакансии: ': vacancy['Text: ']['vacancy_name'],
                                   'Ссылка на вкансию: ': vacancy['Text: ']['url'],
                                   'требования': vacancy['Text: ']['requirements']
                                   })

            if type(vacancy['Text: ']['salary']) == dict:
                max_salary = vacancy['Text: ']['salary']['to']
                min_salary = vacancy['Text: ']['salary']['from']

                if max_salary and min_salary is None:
                    continue

                elif max_salary is None:
                    salary.append(min_salary)

                elif min_salary is None:
                    salary.append(max_salary)

                else:
                    salary.append((max_salary + min_salary) // 2)

            elif vacancy['Text: ']['salary'] is not None:
                salary.append(vacancy['Text: ']['salary'])


        salary = sum(salary) // len(salary)


        return final_vacancys, salary

