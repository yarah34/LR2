from http.server import HTTPServer, BaseHTTPRequestHandler


# Слушатель http запросов
class HTTP_handler(BaseHTTPRequestHandler):

    def do_POST(self):
        self.send_response(200)

    def do_GET(self):

        print(self.headers)
        print(self.path)

        if self.path == "/":
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            with open("index.html", "rb") as f:
                self.wfile.write(f.read())


def main():

    # Создаём объект http-сервера
    http_server = HTTPServer(("192.168.1.133", 44444), HTTP_handler)

    http_server.serve_forever()


if __name__ == '__main__':
    main()
