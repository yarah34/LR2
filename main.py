from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs

users: dict = {}


# Слушатель http запросов
class HTTPHandler(BaseHTTPRequestHandler):

    def set_headers(self, status_code: int, content_type="text/html"):
        self.send_response(status_code)
        self.send_header('Content-type', content_type)
        self.end_headers()

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        data = self.rfile.read(content_length).decode('UTF-8')

        if self.path == "/signin.html":
            params: dict = parse_qs(data)

            login = params.get('name')
            password = params.get('pass')

            # Получены ли все параметры?
            if login is None or password is None:
                self.set_headers(403)
                self.wfile.write(b"Username or password incorrect!")
                return

            login = login.pop()
            password = password.pop()

            # Найдена ли запись в users?
            found_password = users.get(login)
            if found_password is None:
                self.set_headers(403)
                self.wfile.write(b"Username or password incorrect!")
            # Правильный ли пароль?
            elif found_password == password:
                self.set_headers(200)
                self.wfile.write(f"<p>Username: <b>{login}</b></p><br>- Mornin'<br>- Nice day for fishing, ain't it?<br>- Huh-ha!".encode("UTF-8"))
            else:
                self.set_headers(403)
                self.wfile.write(b"Username or password incorrect!")
        else:
            self.set_headers(404)

    def do_GET(self):
        path = "." + self.path

        try:
            f = open(path, "rb")
            self.set_headers(200)
            self.wfile.write(f.read())
            f.close()
        except Exception as e:
            self.set_headers(404)
            print(e)


def main():
    global users

    # Чтение БД с пользователями
    with open("users.txt", "r") as file:
        for line in file:
            login, password = line.strip().split(";")
            users[login] = password

    # Создаём объект http-сервера
    http_server = HTTPServer(("192.168.1.133", 44444), HTTPHandler)
    http_server.serve_forever()


if __name__ == '__main__':
    main()
