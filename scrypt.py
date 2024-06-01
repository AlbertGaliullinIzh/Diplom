import time
import json
import datetime
import shutil

print("Starting update index.html")

# Исходный файл
src_file = 'default-index.html'

# Путь для копии файла
dst_file = 'index.html'

# Копирование файла
shutil.copy(src_file, dst_file)

with open('result.json', 'r') as file:
    current_position = file.tell()
    while True:
        file.seek(current_position)
        
        print(file.readlines())
        file.seek(current_position)
        
        json_list = list(json.loads(elem) for elem in file.readlines() if elem != '\n')
        current_position = file.tell()

        file_r_text = ""
        with open('index.html', 'r+') as file_r:
            file_r_text = file_r.read()
            file_r.seek(0)
            for elem in json_list:
                file_r_text = file_r_text.replace(f'waiting for a message from the {elem["name"]}...', f'<div class="message"><h4>{elem["trigger"]}</h4><p>{datetime.datetime.now()}</p><p>{elem["IP"]}</p></div>'+f"waiting for a message from the {elem["name"]}..."+f"{'<br>' if len(json_list) != 0 else ""}")
            file_r.write(file_r_text)
        time.sleep(5)