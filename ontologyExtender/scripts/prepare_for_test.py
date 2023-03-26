# подключение к бд mysql
import mysql.connector
import time
import logging
from bs4 import BeautifulSoup
from requests import get, post
from dotenv import load_dotenv
import os

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

# use .env file
load_dotenv()


def retrieve_from_origin():
    # подключение к бд
    mydb = mysql.connector.connect(
        host=os.getenv("MYSQL_HOST"),
        user=os.getenv("MYSQL_USER"),
        passwd=os.getenv("MYSQL_PASSWORD"),
        database=os.getenv("MYSQL_DATABASE"),
        auth_plugin='mysql_native_password'
    )

    # получение курсора
    mycursor = mydb.cursor()

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

            # save to db
            teacher = {
                "url": teacher_url,
                "text": raw_text
            }

            sql = "INSERT INTO teachers_raw (url, text) VALUES (%s, %s)"
            val = (teacher_url, raw_text)
            mycursor.execute(sql, val)
            mydb.commit()

            teachers.append(url)

            if len(teachers) > teachers_limit:
                return teachers

    # закрытие соединения
    mydb.close()


def retrieve_from_db():
    # подключение к бд
    mydb = mysql.connector.connect(
        host=os.getenv("MYSQL_HOST"),
        user=os.getenv("MYSQL_USER"),
        passwd=os.getenv("MYSQL_PASSWORD"),
        database=os.getenv("MYSQL_DATABASE"),
        auth_plugin='mysql_native_password'
    )

    # получение курсора
    mycursor = mydb.cursor()

    # записать каждого препода в отдельный файл
    mycursor.execute("SELECT text FROM teachers_raw")
    myresult = mycursor.fetchall()
    i = 0

    for x in myresult:
        i += 1
        # записать в файле ./tomita-parser/input/raw_{number}.txt
        with open("./tomita-docker/tomita-parser/input/raw_" + str(i) + ".txt", "w", encoding="utf-8") as f:
            f.write(x[0].decode("utf-8"))

    # закрытие соединения
    mydb.close()

    logger.info("Записано {} файлов.".format(i))


def post_request(url, payload=""):
    response = post(url, data=payload)
    if response.status_code != 200:
        raise Exception("POST request failed: " + str(response.status_code))
    return response


def get_request(url):
    response = get(url)
    if response.status_code != 200:
        raise Exception("GET request failed: " + str(response.status_code))
    return response


if __name__ == "__main__":
    start_time = time.time()

    # retrieve_from_origin()
    retrieve_from_db()

    logger.info("Время выполнения: %s секунд" % (time.time() - start_time))
