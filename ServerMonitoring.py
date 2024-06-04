import http.server
import json
import socketserver
import datetime
import threading
import time

machineDict = {"vpnsrv": datetime.datetime.now(), "server": datetime.datetime.now(), "server-attack": datetime.datetime.now(), "monitoring": datetime.datetime.now(), "router": datetime.datetime.now()}

def check_connection():
    global machineDict
    while True:
        now = datetime.datetime.now()
        for elem in machineDict.keys():            
            deltatime_for_machine = now - machineDict[elem]
            
            if deltatime_for_machine.total_seconds() / 60 >= 30:
                with open('result.json', 'a') as f:
                    json.dump({elem: "server", "trigger": "not connection", "IP": "-"}, f)
                    f.write('\n')
        time.sleep(1800)


class RequestHandler(http.server.SimpleHTTPRequestHandler):
    global machineDict
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        data = json.loads(body.decode('utf-8'))
        if self.path == '/sendnotificate':
            with open('result.json', 'a') as f:
                json.dump(data, f)
                f.write('\n')
        elif self.path == '/EqualsHash':
            with open('hash.json', 'r') as f1:
                dict1 = json.load(f1)
            for key in dict1:
                if key in data:
                    if dict1[key] != data[key]:
                         with open('result.json', 'a') as f:
                            json.dump({"name": "server", "trigger": "Uncorrected HASH", "IP": "172.31.2.5"}, f)
                            f.write('\n')
        elif self.path == '/RegularNotification':
            machineDict[data['name']] = datetime.datetime.now()          
        self.send_response(200)
        self.end_headers()

PORT = 5000
Handler = RequestHandler

thread = threading.Thread(target=check_connection)
thread.start()

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    httpd.serve_forever()
