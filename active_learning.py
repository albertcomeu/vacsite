from sklearn.metrics import precision_score, recall_score, f1_score
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from random import sample
from bd import Db
db = Db()


class Active:
    def __init__(self):
        self.data = db.get_tabel()
        self.labels = [0, 0, 0, 0, 0,
                  0, 1, 1, 0, 0,
                  1, 0, 1, 0, 0,
                  0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0,
                  0, 0, 1, 0, 0,
                  0, 0, 0, 0, 0,
                  0, 1, 0, 0, 1,
                  0, 0, 0, 0, 0,
                  0, 0, 0, 0, 1,
                  1, 0, 0, 0, 0,
                  0, 0, 1, 0, 0,
                  1, 0, 0, 1, 0,
                  0, 0, 0, 0, 1,
                  0, 0, 0, 0, 0,
                  1, 0, 1, 1, 0,
                  1, 0, 1, 0, 1,
                  0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0,
                  1, 0, 1, 0, 0, #105
                  1, 1, 0, 1, 0,
                  0, 0, 0, 1, 0,
                  0, 1, 1, 0, 0,
                  0, 0, 0, 0, 0,
                  0, 0, 1, 0, 1,
                  0, 1, 0, 0, 0,
                  0, 0, 0, 0, 0,
                  0, 0, 0, 1, 0,
                  1, 0, 0, 0, 0,
                  0, 1, 0, 0, 1,
                  0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0,
                  0, 0, 0, 1, 0,
                  0, 0, 0, 0, 0,
                  0, 1, 0, 0, 0,
                  0, 0, 1, 0, 0,
                  0, 0, 0, 0, 0,
                  0, 0, 1, 1, 0,
                  0, 1, 0, 0, 0 #200
                #201
                  ]

        self.labeled_data = []
        for l in range(len(self.labels)):
            self.data[l]['label'] = self.labels[l]
            self.labeled_data.append(self.data[l])

    def train_model(self):
        unlabeled_data = self.data[len(self.labels):]

        model = SVC()
        vectorizer = TfidfVectorizer()
        labeled_requirements = [''.join(example['requirements']) for example in self.labeled_data]
        labeled_labels = [example['label'] for example in self.labeled_data]
        unlabeled_requirements = [''.join(example['requirements']) for example in unlabeled_data]

        # Предварительная обработка данных
        labeled_features = vectorizer.fit_transform(labeled_requirements)
        unlabeled_features = vectorizer.transform(unlabeled_requirements)


        # Обучение модели на размеченных данных
        model.fit(labeled_features, labeled_labels)

        # Предсказание меток для неразмеченных данных
        predictions = model.predict(unlabeled_features)

        # Присвоение предсказанных меток неразмеченным данным
        for index, example in enumerate(unlabeled_data):
            example['label'] = predictions[index]

        return unlabeled_data

    def get_v(self):
        res_v = []

        unlabeled_data = self.train_model()

        # Вывод результатов
        for vacancy in unlabeled_data:
            res_v.append({'Название вакансии: ': vacancy['vacancy_name'],
                 'Ссылка на вкансию: ': vacancy['url'],
                 'Работодатель ': vacancy['employer'],
                 'требования': vacancy['requirements'],
                 'label': vacancy['label']
                 })

        return self.labeled_data + res_v

A = Active()
