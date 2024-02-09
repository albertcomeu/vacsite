from flask import Flask, request, render_template
from werkzeug.utils import secure_filename
import os
import logging
from PyPDF2 import PdfReader
import docx
from textanalysis import Analyse
from pars import Pars
from ner_alg import Ner_skills
from salary_counting import Count

app = Flask(__name__)

logging.basicConfig(filename='logs.log', level=logging.INFO, format='%(asctime)s %(message)s')

# Initialize the skills analysis object
n = Ner_skills()

# Resume processing function
def processing_resume(resumestr):
    from math_method import Math_method
    logging.info('Анализ резюме')
    analyse = Analyse()
    mm = Math_method(resumestr)
    reslist = mm.procent_count()
    return reslist

# Named Entity Recognition (NER) processing function
def ner_process(resume, vacancy):
    if vacancy:
        skill_vector = list(n.find_words(vacancy) - resume)
        if skill_vector:
            return skill_vector
        return []
    else:
        return []

# File upload handler
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part'

    file = request.files['file']

    if file.filename == '':
        return 'No selected file'

    if file:
        filename = secure_filename(file.filename)
        extension = os.path.splitext(filename)[1].lower()
        if extension in ('.txt', '.docx', '.pdf'):
            file_path = os.path.join('uploads', filename)
            file.save(file_path)

            # Processing the uploaded file
            resumestr = ""
            if extension == '.txt':
                with open(file_path, 'r') as f:
                    resumestr = f.read()
            elif extension == '.docx':
                doc = docx.Document(file_path)
                for paragraph in doc.paragraphs:
                    resumestr += paragraph.text
            elif extension == '.pdf':
                reader = PdfReader(file_path)
                for page in reader.pages:
                    resumestr += page.extract_text()

            print(resumestr)

            # Resume processing
            res = processing_resume(resumestr)
            resume_skill_vector = n.find_words(resumestr)

            vacancies_method1 = []
            for i in range(min(len(res), 15)):
                vacancy_info = {'Название вакансии': res[i][0], 'Зарплата': 0, 'Ссылка': res[i][3]}
                if isinstance(res[i][2], dict):
                    max_salary = res[i][2].get('to')
                    min_salary = res[i][2].get('from')
                    if max_salary is None and min_salary is None:
                        vacancy_info['Зарплата'] = 'Не указана'
                    elif max_salary is None:
                        vacancy_info['Зарплата'] = min_salary
                    elif min_salary is None:
                        vacancy_info['Зарплата'] = max_salary
                    else:
                        vacancy_info['Зарплата'] = (max_salary + min_salary) // 2
                else:
                    vacancy_info['Зарплата'] = 'Не указана'

                skill_vector = ner_process(resume_skill_vector, res[i][1])
                if skill_vector:
                    vacancy_info['Рекомендации по скиллам'] = ', '.join(skill_vector[:5])

                vacancies_method1.append(vacancy_info)

            print('Ожидание 2-ого метода...(может занять несколько минут)')

            c = Count(resumestr)
            c.fill_req()
            final_vacancies, salary = c.get_rec_v_and_salary()
            vacancies_method2 = []
            for vacancy in final_vacancies:
                print(final_vacancies)
                vacancy_info = {'Название вакансии': vacancy['Название вакансии: '],
                                'Ссылка': vacancy['Ссылка на вкансию: ']}
                skill_vector = ner_process(resume_skill_vector, vacancy['требования'])
                if skill_vector:
                    vacancy_info['Рекомендации по скиллам'] = ', '.join(skill_vector[:5])
                vacancies_method2.append(vacancy_info)

            return render_template('result.html', vacancies_method1=vacancies_method1,
                                   vacancies_method2=vacancies_method2, estimated_salary=salary)

        else:
            return 'Unsupported file type'
    return 'Something went wrong'

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
    app.run(debug=True)
