# Здесь мы делаем пост запросы для извлечения всех преподов.
# Затем извлекаем факты и записываем в таблицу excel.
import json
import logging
import os
import time

import pandas as pd
import requests as requests
from bs4 import BeautifulSoup

# from ontologyExtender.scripts.parser import FactsParser
from parser import FactsParser

# from ontologyExtender.scripts.parser import FactsParser

# create logger
logger = logging.getLogger('logger')
logger.setLevel(logging.DEBUG)

# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# add formatter to ch
ch.setFormatter(formatter)

# add ch to logger
logger.addHandler(ch)


class ParsingException(Exception):
    pass


def import_teachers_sstu(local=False):
    start_time = time.time()

    # Получаем список преподов
    teachers = get_teachers_local() if local else get_teachers_remote()

    logger.info("Got {} raws".format(len(teachers)))

    duration = time.time() - start_time

    with open('hand_filled.json', encoding='utf-8') as json_file:
        standart = json.load(json_file)[2]['data']

    if not local:
        tp = 0  # correct matching
        fp = 0  # wrong matching
        fn = 0  # miss matching

        for teacher in teachers:
            for std in standart:
                if std['url'] == teacher[0]:
                    comparing = [
                        [std['name'], teacher[1]],
                        [std['department'], teacher[2]],
                        [std['thesis_1'], teacher[3].get('thesis_1', "")],
                        [std['thesis_2'], teacher[3].get('thesis_2', "")],
                        [std['speciality_1'], teacher[3].get('speciality_1', "")],
                        [std['speciality_2'], teacher[3].get('speciality_2', "")],
                        [std['degree_1'], teacher[3].get('degree_1', "")],
                        [std['degree_2'], teacher[3].get('degree_2', "")],
                        [std['branch_1'], teacher[3].get('branch_1', "")],
                        [std['branch_2'], teacher[3].get('branch_2', "")],
                    ]
                    for cmr in comparing:
                        if cmr[0] != "" and cmr[1] != "":
                            if cmr[0] == cmr[1]:
                                tp += 1
                            else:
                                fp += 1
                        elif cmr[0] == "" and cmr[1] != "":
                            fn += 1

        precision = tp / (tp + fp)
        recall = tp / (tp + fn)
        f = 2 * (precision * recall) / (precision + recall)

        print("Precision: " + str(precision))
        print("Recall: " + str(recall))
        print("F: " + str(f))
    print("Time: " + str(duration))

    # Записываем в файл
    write_teachers(teachers)


def get_teachers_remote():
    parser = FactsParser()
    # Получаем количество страниц с помощью пост запроса
    # Перебираем все страницы и получаем список преподов
    url = "https://www.sstu.ru/local/components/sstu/teachers.filter/ajax/list.php"

    logger.info("Извлекаю список преподавателей.")
    response = post_request(url)
    # Получаем количество страниц с помощью BeautifulSoup #filter_page.a.text
    soup = BeautifulSoup(response.text, 'html.parser')

    last_a = soup.select_one('#filter_page > li:last-child > a')

    # select href attribute
    page_count = int(last_a['href'])

    # Получаем список преподов
    teachers = []
    teachers_limit = 100

    for i in range(1, page_count + 1):
        logger.info("Страница {} из {}".format(i, page_count))
        payload = "abc=&page=" + str(i)
        response = post_request(url, payload)
        soup = BeautifulSoup(response.text, 'html.parser')
        teacher_urls = [teacher['href'] for teacher in soup.select('div.name>a')]

        for teacher_url in teacher_urls:
            try:
                logger.info("URL: " + teacher_url)
                response = get_request("https://www.sstu.ru/" + teacher_url)
                logger.info("Парсинг.")
                soup = BeautifulSoup(response.text, 'html.parser')
                raw_text = soup.select_one('body > div.boot > div.page > div > div.row.row-content > div > div').text

                stop = raw_text.find("Научно-исследовательская работа")
                if stop == -1:
                    stop = raw_text.find("Организационно-методическая деятельность")
                if stop == -1:
                    stop = raw_text.find("Повышение квалификации")
                if stop == -1:
                    stop = raw_text.find("Основные публикации")
                if stop == -1:
                    stop = raw_text.find("Сведения из научно-технической библиотеки")

                raw_text = raw_text[:stop]

                if len(raw_text) > 7000:
                    logger.warning("Too much text (%d). Stop at %d." % (len(raw_text), stop))
                    # print(raw_text)
                    # exit()

                try:
                    teacher = get_facts(raw_text, teacher_url, parser)
                except ParsingException as e:
                    logger.error(e)
                    continue

                teachers.append(teacher)

                if len(teachers) > teachers_limit:
                    return teachers
            except Exception as e:
                logger.error(e)

    return teachers


def get_teachers_local():
    logger.info("Loading local")
    parser = FactsParser()
    teachers = []

    # go throw each file in tomita-docker/tomita-parser/input
    for filename in os.listdir('tomita-docker/tomita-parser/input'):
        with open('tomita-docker/tomita-parser/input/' + filename, encoding='utf-8') as raw_text:
            try:
                teacher = get_facts(raw_text.read(), filename, parser)
                teachers.append(teacher)
            except ParsingException as e:
                logger.error(e)
                continue

    return teachers


def get_facts(raw_text, teacher_url, parser):
    logger.info("Извлечение фактов {}".format(teacher_url))
    try:
        facts = parser.get_facts(raw_text).as_array()
    except Exception as e:
        raise ParsingException("Ошибка при извлечении фактов: " + str(e))

    payload = {}
    for f in facts:
        if f[0] not in ['Scientist', 'Department']:
            attributes = {
                'Thesis': 'thesis_',
                'Speciality': 'speciality_',
                'AcademicDegree': 'degree_',
                'BranchOfScience': 'branch_'
            }
            key = attributes[f[0]] + "1"
            if key in payload:
                key = attributes[f[0]] + "2"

            payload[key] = f[1]

    teacher = ["https://sstu.ru" + teacher_url]
    scientist = [f[1] for f in facts if f[0] == 'Scientist']
    department = [f[1] for f in facts if f[0] == 'Department']
    if len(scientist) > 0:
        teacher.append(scientist[0])
    else:
        teacher.append("")
    if len(department) > 0:
        teacher.append(department[0])
    else:
        teacher.append("")
    teacher.append(payload)
    return teacher


def post_request(url, payload=None):
    s = requests.Session()

    # s.proxies = {
    #     "http": "http://user:qwerty@1.1.1.1:3104",
    #     "https": "http://user:qwerty@1.1.1.1:3104"
    # }

    return s.post(
        url,
        data=payload,
        headers={
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
        },
        timeout=5
    )


def get_request(url):
    s = requests.Session()

    # s.proxies = {
    #     "http": "http://user:qwerty@1.1.1.1:3104",
    #     "https": "http://user:qwerty@1.1.1.1:3104"
    # }

    return s.get(
        url,
        timeout=5,
    )


def write_teachers(teachers):
    logger.info("Запись в excel.")
    # Create a DataFrame
    df = pd.DataFrame(teachers, columns=['Url', 'Name', 'Department', 'Payload'])

    # Export the DataFrame to Excel
    df.to_excel('teachers.xlsx', index=False)


def main():
    import_teachers_sstu(local=True)
    logger.info("Данные сохранены.")


if __name__ == '__main__':
    main()