import http.server
import json
import socketserver

class RequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)

        data = json.loads(body.decode('utf-8'))

        if self.path == '/sendnotificate':
            with open('result.json', 'w') as f:
                json.dump(data, f)
        elif self.path == '/EqualsHash':
            with open('hash.json', 'r') as f1:
                dict1 = json.load(f1)

            # РЎСЂР°РІРЅРёРІР°РµРј Р·РЅР°С‡РµРЅРёСЏ РїРѕ РєР»СЋС‡Р°Рј
            print(dict1)
            print(data)
            for key in dict1:
                if key in data:
                    if dict1[key] != data[key]:
                         with open('result.json', 'w') as f:
                            json.dump({"name": "server", "trigger": "РќРµ СЃРѕРІРїР°РґР°РµС‚ HASH", "IP": "172.31.2.5"}, f)
            

        self.send_response(200)
        self.end_headers()

PORT = 5000
Handler = RequestHandler
with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"РЎРµСЂРІРµСЂ Р·Р°РїСѓС‰РµРЅ РЅР° РїРѕСЂС‚Рµ {PORT}.")
    httpd.serve_forever()
