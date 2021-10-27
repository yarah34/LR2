from datetime import datetime
from io import StringIO
from pathlib import Path
import psycopg2

users: dict = {}


def try_login(login: list, password: list) -> (int, bytes):
    # Получены ли все параметры?
    if login is None or password is None:
        return 403, b"Username or password incorrect!"

    login: str = login.pop()
    password: str = password.pop()

    # Найдена ли запись в users?
    found_password = users.get(login)

    if found_password is None:
        return 403, b"Username or password incorrect!"

    # Правильный ли пароль?
    elif found_password == password:
        with open("pages/profile.html", 'r') as f:
            text = f.read().replace("{login}", login)
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
    conn = psycopg2.connect(dbname='db_name1', user='postgres', password='P@ssw0rd', host='localhost', port=5432)
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
    conn = psycopg2.connect(dbname='db_name1', user='postgres', password='P@ssw0rd', host='localhost', port=5432)
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
