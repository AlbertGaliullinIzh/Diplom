import machine
import time
import requests
import json

class ManagerForDosDetection():

    countIpList = list() # список с количеством Ip
    countRequestList = list() # список с количеством трафика
    countControversiallList = list() # список с подозрительным трафиком
    countMachineKnown = 10 # Количество машин, которые долдны подключится для киберучений
    
    machineIp = []


    countIpCoef = 0
    countRequestCoef = 0

    def __init__(self, numberParticipants):
        self.countMachineKnown = numberParticipants
        self.machineList = list()
        self.json_list = list()
        self.current_position = 0

        self.itMachineIp = ['192.168.31.116']

    def sendmessage(self, ip): # отправка данных о обнаруженном dos
        print(f"Обнаружена подозрительная активность. Предположение: Dos-аткака. Адрес: {ip}")
        data = {"name": "VPN", "trigger": "DOS-attack"}
        json_data = json.dumps(data)
        url = "http://10.0.2.7:5000"
        print(data)
        response = requests.post(url, data=json_data, headers={"Content-Type": "application/json"})
        if response.status_code == 200:
            print("Данные успешно отправлены!")
        else:
            print(f"Ошибка при отправке данных: {response.status_code} - {response.text}")

    def start(self):
        while True:
            self.ReadingFile()
            unicationIP = set([elem["id.orig_h"] for elem in self.json_list if elem['id.orig_h'] not in self.itMachineIp])
            for elem in unicationIP:
                self.UpploadMachine(elem, [item for item in self.json_list if item["id.orig_h"] == elem])

            for elem in self.machineList:
                #if elem.MachineIsNotActive():
                #    self.machineList.remove(elem)
                print(elem.GetIp() + " - " + str(elem.IsMachineAttacking()))
            print("----")
            time.sleep(10)



    def UpploadMachine(self, ip, input_traffic):
        index = self.GetIdMachineForList(ip)
        if index == -1:            
            self.machineList.append(
                machine.Machine(ip, input_traffic, False if len(self.machineList) < self.countMachineKnown else True))
        else:
            self.machineList[index].AddTraffic(input_traffic)
    
    def GetIdMachineForList(self,ip):# получение id из списка машин
        i = 0
        for elem in self.machineList:
            if elem.GetIp() == ip:
                return i
            i+=1
        return -1
    
    def ReadingFile(self):# считывание с файла, с ранее указаной позиции
        with open('/opt/zeek/logs/current/conn.log', 'r') as file:
            file.seek(self.current_position)
            self.json_list = file.readlines()
            self.current_position = file.tell()
            i = 0
            while i < len(self.json_list):
                self.json_list[i] = eval(self.json_list[i].replace("true","True").replace("false","False"))
                i+=1


    # #def newIpAddresses():
    #     def plusCountIpCoef():
    #         if countIpCoef != 1:
    #             countIpCoef+=0.1
    #     def minusCountIpCoef():
    #         if countIpCoef != 0:
    #             countIpCoef-=0.1
    #     def resetCountIpCoef():
    #         if countIpCoef != 0:
    #             countIpCoef-=0.1
    #     unicationIP = set([elem["id.orig_h"] for elem in json_list])
    #     #добавляем количество ip в список
    #     if len(countIpList) < 10:
    #         countIpList.append(len(unicationIP))
    #     else:
    #         countIpList.pop(0)
    #         countIpList.append(len(unicationIP))
        
        # # Анализируем количество адресов
        # # проверка на максимальное количество подлючений
        # if max(countIpList) == countMachineKnown:
        #     resetCountIpCoef()
        #     return
        #
        # # если количетсво ip адресов одинакоевое
        # if len(set(countIpList)) == 1:
        #     resetCountIpCoef()
        #     return
        # # Если количетсво ip адресов варируется
        # i = 0
        # while i!=9:
        #     if countIpList[i] < countIpList[i+1]:
        #         plusCountIpCoef()
        #     if countIpList[i] > countIpList[i+1]:
        #         minusCountIpCoef()
        # return

manager = ManagerForDosDetection(8)
manager.start()

