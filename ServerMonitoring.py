import http.server
import json
import socketserver
import datetime
import threading
import time

machineDict = {"Vpnsrv": datetime.datetime.now, "Server": datetime.datetime.now, "Server-attack": datetime.datetime.now, "Monitoring": datetime.datetime.now, "Router": datetime.datetime.now}

def check_connection():
    global machineDict
    while True:
        now = datetime.datetime.now()
        for elem in machine.keys:            
            deltatime_for_machine = now - machineDict['elem']
            
            if (now - deltatime_for_machine).total_seconds() / 60 >= 30:
                with open('result.json', 'w') as f:
                            json.dump({elem: "server", "trigger": "not connection", "IP": "-"}, f)
            time.sleep(1800)


class RequestHandler(http.server.SimpleHTTPRequestHandler):
    global machineDict
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
            for key in dict1:
                if key in data:
                    if dict1[key] != data[key]:
                         with open('result.json', 'w') as f:
                            json.dump({"name": "server", "trigger": "Uncorrected HASH", "IP": "172.31.2.5"}, f)
        elif self.path == '/RegularNotification':
            machineDict[data['name']] = datetime.datetime.now
            

        self.send_response(200)
        self.end_headers()

PORT = 5000
Handler = RequestHandler

thread = threading.Thread(target=check_connection)
thread.start()

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    httpd.serve_forever()
