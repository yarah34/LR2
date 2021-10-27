from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs


import controller


# Слушатель http запросов
class HTTPHandler(BaseHTTPRequestHandler):

    def set_headers(self, status_code: int, content_type="text/html;charset=UTF-8"):
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

            status_code, answer = controller.try_login(login, password)

            self.set_headers(status_code)
            self.wfile.write(answer)
        elif self.path == "/view_db":
            params: dict = parse_qs(data)
            value = params.get('view_db')

            status_code, answer = controller.view_db(value)

            self.set_headers(status_code)
            self.wfile.write(answer)
        else:
            self.set_headers(404)

    def do_GET(self):
        status_code, answer = controller.get_page(self.path)

        self.set_headers(status_code)
        if answer is not None:
            self.wfile.write(answer)


def main():
    # Чтение БД с пользователями
    with open("users.txt", "r") as file:
        for line in file:
            login, password = line.strip().split(";")
            controller.users[login] = password

    # Создаём объект http-сервера
    http_server = HTTPServer(("192.168.1.133", 44444), HTTPHandler)
    http_server.serve_forever()


if __name__ == '__main__':
    main()
