from http.server import HTTPServer, BaseHTTPRequestHandler
from io import StringIO
from pathlib import Path
from urllib.parse import urlparse, parse_qs
import psycopg2


client = psycopg2.connect(
    dbname='db_name1',
    user='postgres',
    password='P@ssw0rd',
    host='localhost',
    port=5432
)


# Слушатель http запросов
class HTTPHandler(BaseHTTPRequestHandler):

    def redirect(self, location):
        self.send_response(301)
        self.send_header("Location", location)
        self.end_headers()

    def send(self, status_code, content=None, content_type="text/html;charset=UTF-8"):
        self.send_response(status_code)
        self.send_header('Content-type', content_type)
        self.end_headers()
        if content is not None:
            self.wfile.write(content.encode("UTF-8"))

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        url = urlparse(self.path)
        params = parse_qs(self.rfile.read(content_length).decode('UTF-8'))

        if url.path == "/signin":
            login = params.get('name').pop()
            password = params.get('pass').pop()

            cursor = client.cursor()
            cursor.execute(
                "SELECT name as result FROM users WHERE name = %s AND pass = md5(%s)",
                (login, password)
            )

            data: set = cursor.fetchone()

            cursor.close()

            if data is None:
                self.send(403, "Username or password incorrect!")
            else:
                self.redirect("/books")
        else:
            self.send(404, f"Page {self.path} not found!")

    def do_GET(self):
        url = urlparse(self.path)
        params = parse_qs(url.query)

        if url.path == "/books":
            bookname = params.get("name")

            sql = "select ba.id, a.name as author, b.name as book from books_by_authors ba \
                              left join author a on a.id = ba.aid \
                              left join book b on b.id = ba.bid"

            if bookname:
                sql += f"\rwhere b.name like '{bookname.pop()}'"

            try:
                cursor = client.cursor()
                cursor.execute(sql)

                data: list = cursor.fetchall()
                cursor.close()

                content = StringIO()
                for row in data:
                    id = row[0]
                    author = row[1]
                    book = row[2]
                    content.write(f"<tr><td>{id}</td><td>{author}</td><td>{book}</td></tr>")

                with open("views/booklist.html", "r", encoding="UTF-8") as f:
                    self.send(200, f.read().replace("{data}", content.getvalue()))
            except Exception as e:
                print(e)
                self.send(500, f"Error {e}. <br/> SQL: {sql}")
        elif url.path == "/":
            self.redirect("/login.html")
        else:
            path = "./static" + self.path

            # Fix Path Traversal
            while "../" in path or "//" in path:
                path = path.replace("../", "").replace("//", "/")

            file_name = Path(path).name

            # Extension filter
            if file_name.endswith(".html") or file_name.endswith(".ico"):
                try:
                    with open(path, "r", encoding="UTF-8") as f:
                        answer = f.read()
                        self.send(200, answer)
                except Exception as e:
                    print(e)
                    self.send(404)
            else:
                self.send(403)



def main():
    # Создаём объект http-сервера
    http_server = HTTPServer(("192.168.1.133", 44444), HTTPHandler)
    http_server.serve_forever()


if __name__ == '__main__':
    main()
