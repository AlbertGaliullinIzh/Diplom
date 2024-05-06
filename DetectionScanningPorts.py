import time
import requests
import json


machineIp = []
json_list= list()

print("Detection scaning ports start...")

with open('current/conn.log', 'r') as file:
    current_position = file.tell()
    while True:
        file.seek(current_position)
        json_list += file.readlines()
        current_position = file.tell()
        i = 0
        while i < len(json_list):
            if type(json_list[i]) == dict:
                i+=1
                continue
            json_list[i] = eval(json_list[i].replace("true","True").replace("false","False"))
            i+=1

        json_list_for_analiz = [elem for elem in json_list if elem.get("id.orig_h") != elem.get("id.resp_h") and elem.get("id.orig_h") not in machineIp]
        unicationIP = set([elem["id.orig_h"] for elem in json_list])

        for ip in unicationIP:
            recordsForIp = [elem for elem in json_list_for_analiz if elem.get("id.orig_h") == ip and (elem.get("conn_state") == "S0" or elem.get("conn_state") == "REJ")]
            if len(recordsForIp) > 10:
                try:
                    print(f"Обнаружена подозрительная активность. Предположение: сканирование портов. Адрес: {recordsForIp[0]['id.orig_h']}")
                    data = {"name": "VPN", "trigger": "Scanning ports"}#, "IP":str( recordsForIp['id.orig_h'])}
                    json_data = json.dumps(data)
                    url = "http://10.0.2.7:5000"
                    print(data)
                    response = requests.post(url, data=json_data, headers={"Content-Type": "application/json"})
                    if response.status_code == 200:
                        print("Данные успешно отправлены!")
                    else:
                        print(f"Ошибка при отправке данных: {response.status_code} - {response.text}")
                except:
                    print("Connection error")
        if len(json_list) <= 9:
            pass
        else:
            json_list = json_list[-9:]
        time.sleep(5)
