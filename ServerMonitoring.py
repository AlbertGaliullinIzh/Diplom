import http.server
import json
import socketserver


class RequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        data = json.loads(body.decode('utf-8'))
        with open('result.json', 'w') as f:
            json.dump(data, f)
        self.send_response(200)
        self.end_headers()


PORT = 5000
Handler = RequestHandler
with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"Сервер запущен на порте {PORT}.")
    httpd.serve_forever()
