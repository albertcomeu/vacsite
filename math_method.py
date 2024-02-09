from bd import Db
db = Db()
from textanalysis import Analyse
a = Analyse()

class Math_method:
    def __init__(self, resumestr):
        self.resumestr = a.prepare(resumestr)
        self.vacancyslist = db.get_tabel()

    def procent_count_for_marks(self):

        vacancys = self.vacancyslist

        for i in range(len(vacancys)):
            requirement = vacancys[i]['requirements']
            count = 0
            if len(requirement) == 0:
                vacancys[i]['label'] = 0
                continue

            for j in requirement:
                for word in self.resumestr:
                    if j == word:
                        count += 1

            procent = (count / (len(requirement))) * 100

            if procent >= 70:
                vacancys[i]['label'] = 1

            else:
                vacancys[i]['label'] = 0

        return vacancys


    def procent_count(self):
        vacancys = self.vacancyslist

        reslist = []

        for i in range(len(vacancys)):
            requirement = vacancys[i]['requirements']
            count = 0
            if len(requirement) == 0: continue
            for j in requirement:
                for word in self.resumestr:
                    if j == word:
                        count += 1

            procent = (count / (len(requirement))) * 100

            if procent >= 70:

                reslist.append((vacancys[i]['vacancy_name'], vacancys[i]['requirements'],
                                vacancys[i]['salary'], vacancys[i]['url']))
        return reslist
