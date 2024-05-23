from gensim.models import Word2Vec
from sklearn.metrics.pairwise import cosine_similarity
from textanalysis import Analyse
import logging
from bd import Db
db = Db()
a = Analyse()


class Ner_skills:
    def __init__(self):

        self.vacancy_requirements = [v['requirements'] for v in db.get_tabel()]

        logging.info(f'инициализация ner')

    def train_model(self):
        req_for_train = self.vacancy_requirements

        model = Word2Vec(req_for_train, window=5, min_count=1, workers=4)

        model.save('modelgensim')

    def find_similar_tags(self, tag, threshold):
        model = Word2Vec.load('modelgensim')
        try:
            tag_vector = model.wv[tag]

        except KeyError as e:
            return ['1']

        tags = [tag for tag_list in self.vacancy_requirements for tag in tag_list]

        similarities = cosine_similarity([tag_vector], [model.wv[tag] for tag in tags])[0]

        similar_tags = [tag for i, sim in enumerate(similarities) if sim > threshold]

        return similar_tags

    def find_words(self, lst):
        sim_word = []

        for el in lst:

            try:

                #similar_tags = self.find_similar_tags(el, 0.85)

                sim_word.append(el)

            except KeyError:
                continue

        sim_word = set(sim_word)

        return sim_word