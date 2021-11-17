from datetime import datetime
from io import StringIO
from pathlib import Path
import psycopg2
from hashlib import sha256

psql = {
    "dbname": 'db_name1',
    "user": 'postgres',
    "password": 'P@ssw0rd',
    # "user": 'db_user1',
    # "password": 'P@ssw0rd',
    "host": 'localhost',
    "port": 5432
}

def get_connection():
    return psycopg2.connect(
        dbname=psql['dbname'],
        user=psql['user'],
        password=psql['password'],
        host=psql['host'],
        port=psql['port']
    )


def try_login(login: list, password: list) -> (int, bytes):
    # Получены ли все параметры?
    if login is None or password is None:
        return 403, b"Username or password incorrect!"

    login: str = login.pop()
    password: str = password.pop()

    # Запрос на получение пары name, pass
    conn = get_connection()
    cursor = conn.cursor()

    password_hash = sha256(password.encode("UTF-8")).hexdigest()

    cursor.execute("SELECT name FROM users WHERE name = %s AND pass = %s LIMIT 1", (login, password_hash) )
    records: list = cursor.fetchall()
    # [(admin, pass), (user, pass), ...]

    cursor.close()
    conn.close()

    # Если запись найдена, отправляем положительный результат
    if len(records) != 0:
        username_from_db: str = records[0][0]
        with open("pages/profile.html", 'r') as f:
            text = f.read().replace("{login}", username_from_db)
            return 200, text.encode("UTF-8")
    else:
        return 403, b"Username or password incorrect!"


def get_page(path: str) -> (int, bytes):
    # ... /index.html
    path = "./pages" + path

    while "../" in path or "//" in path:
        path = path.replace("../", "").replace("//", "/")

    file_name = Path(path).name

    if file_name.endswith(".html") or file_name.endswith(".ico"):
        try:
            f = open(path, "rb")
            answer = f.read()
            f.close()
            return 200, answer
        except Exception as e:
            print(e)
            return 404, None
    else:
        return 403, None


def view_db(value: list) -> (int, bytes):
    '''
    Формирует html страницу на основе переданном параметре.
    :param value: передаётся из запроса на стр. profile.html и принимает значения authors или books
    :return: (код, html для показа пользователю)
    '''

    # Получены ли все параметры?
    if value is None:
        return 404, None

    value: str = value.pop()

    if value == "authors":
        return get_authors()
    elif value == "books":
        return get_books()
    else:
        return 404, None


def get_authors() -> (int, bytes):
    conn = psycopg2.connect(
        dbname=psql['dbname'],
        user=psql['user'],
        password=psql['password'],
        host=psql['host'],
        port=psql['port']
    )
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM authors")
    records: list = cursor.fetchall()
    cursor.close()
    conn.close()

    sb = StringIO()
    sb.write("<ul>")
    for record in records:
        sb.write(f"<li>{record[0]}, \t {record[1]}</li>")
    sb.write("</ul>")

    return 200, sb.getvalue().encode("UTF-8")


def get_books() -> (int, bytes):
    conn = psycopg2.connect(
        dbname=psql['dbname'],
        user=psql['user'],
        password=psql['password'],
        host=psql['host'],
        port=psql['port']
    )
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM books ORDER BY id")
    records: list = cursor.fetchall()

    cursor.close()
    conn.close()

    sb = StringIO()
    sb.write("<ul>")
    for record in records:
        dt: datetime = record[2]
        sb.write(f"<li>{record[0]}, \t {record[1]}, \t {dt.year}</li>")
    sb.write("</ul>")

    return 200, sb.getvalue().encode("UTF-8")
