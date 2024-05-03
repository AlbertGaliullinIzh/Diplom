import time

machineIp = [""]
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
                print(f"Обнаружена подозрительная активность. Предположение: сканирование портов. Адрес: {recordsForIp[0]['id.orig_h']}")
        
        if len(json_list) <= 9:
            pass
        else:
            json_list = json_list[-9:]
        time.sleep(5)
