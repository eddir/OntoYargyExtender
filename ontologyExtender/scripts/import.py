# Здесь мы делаем пост запросы для извлечения всех преподов.
# Затем извлекаем факты и записываем в таблицу excel.
import logging

import pandas as pd
import requests as requests
from bs4 import BeautifulSoup

from ontologyExtender.scripts.parser import FactsParser
# from parser import FactsParser

from requests.auth import HTTPProxyAuth

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


def import_teachers_sstu():
    # Получаем список преподов
    teachers = get_teachers()
    # Записываем в файл
    write_teachers(teachers)


def get_teachers():
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

                logger.info("Извлечение фактов.")
                try:
                    facts = parser.get_facts(raw_text).as_array()
                except Exception as e:
                    logger.warning(e)
                    logger.warning("Skipping")
                    continue

                payload = ""
                for f in facts:
                    if f[0] not in ['Scientist', 'Department']:
                        payload += "{}: {}, ".format(f[0], f[1])

                teacher = ["https://sstu.ru" + teacher_url]
                scientist = [f[1] for f in facts if f[0] == 'Scientist']
                department = [f[1] for f in facts if f[0] == 'Department']
                if len(scientist) > 0:
                    teacher.append(scientist[0])
                if len(department) > 0:
                    teacher.append(department[0])
                teacher.append(payload)
                teachers.append(teacher)
            except Exception as e:
                logger.error(e)

    return teachers


def post_request(url, payload=None):
    s = requests.Session()

    # s.proxies = {
    #     "http": "http://***REMOVED***:***REMOVED***@194.32.240.88:3104",
    #     "https": "https://***REMOVED***:***REMOVED***@194.32.240.88:3104"
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
    #     "http": "http://***REMOVED***:***REMOVED***@194.32.240.88:3104",
    #     "https": "https://***REMOVED***:***REMOVED***@194.32.240.88:3104"
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


def import_facts_sstu():
    ...


if __name__ == '__main__':
    import_teachers_sstu()
    # write_teachers([
    #     ['Иванов Иван Иванович', 'https://www.sstu.ru/teachers/ivanov-ivan-ivanovich/'],
    #     ['Петров Петр Петрович', 'https://www.sstu.ru/teachers/petrov-petr-petrovich/'],
    #     ['Сидоров Сидр Сидорович', 'https://www.sstu.ru/teachers/sidorov-sidr-sidorovich/']
    # ])
    logger.info("Данные сохранены.")
