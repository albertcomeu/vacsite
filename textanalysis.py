from nltk.corpus import stopwords  #спсиок слов которые нужно удалить
from pymorphy2 import MorphAnalyzer  #для анализа слов
import string  #для доп.фильтрации

class Analyse():
    def __init__(self):
        self.stopwords = stopwords.words('russian')
        self.morph = MorphAnalyzer()
        self.stopwords.extend(['аналогичный', 'навык', 'знание', 'соответствующий', 'высокий', 'работа', 'задача', 'курс', 'опыт',
                               'образование', 'год', 'месяц', 'пользователь', 'владение', 'готовый', 'понимание', 'проект', 'принцип'
                               , 'основа', 'готовый', 'рассматривать', 'кандидат', 'график', 'полный', 'день', 'рабочий',
                               'специализация', 'сменный', 'согласно', 'самый', 'который', 'система', 'зарплата', 'согласно',
                               'руб', 'москва', 'россия', 'должность', 'язык', 'частный', 'обучение', 'время', 'организация',
                               'область', 'мочь', 'также', 'необходимый', 'российский', 'помогать', 'полностью', 'помощь',
                               'квалификация', 'получить', 'дополнительно', 'иметь', 'грамотный', 'личный', 'связь', 'ещё',
                               '\n', ' ', ';'])
                               #расширяем список стоп слов


    def prepare(self, text):
        rtext = ''.join(filter(lambda w: w not in string.punctuation, text))#удаляем из текста знаки пунктуации

        rtext = ''.join(map(lambda w: w.replace('\n', ' '), rtext))#удаляем символ '\n'

        sptext = rtext.split(' ')#превращаем строку в список

        lower = list(map(lambda i: i.lower(), sptext))#переводим элементы списка в нижний регистр

        for i in range(len(lower)):
            lower[i] = self.morph.normal_forms(lower[i])[0]#приводим слово к нормальной форме ед.числ им.падеж

        filtred = list(filter(lambda w: w not in self.stopwords and w != '', lower))#удаляем стоп-слова

        nonum = list(filter(lambda el: el.isalpha(), filtred))#удаляем числа и цифры

        return nonum