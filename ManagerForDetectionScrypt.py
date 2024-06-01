import DetectionAnomaliesTraffic
import time
import requests
import json

class ManagerForDosDetection():

    countMachineKnown = 10
    machineIp = []

    def __init__(self, numberParticipants):
        self.countMachineKnown = numberParticipants
        self.machineList = list()
        self.json_list = list()
        self.current_position = 0

        self.itMachineIp = ['192.168.31.116']

    def sendmessage(self, ip, assumption):
        try:
            data = {"name": "VPN", "trigger": "DOS-attack"}
            json_data = json.dumps(data)
            url = "http://10.0.2.7:5000/sendnotificate"
            response = requests.post(url, data=json_data, headers={"Content-Type": "application/json"})
        except:
            print("Error send")
    def SendRegularNotification(self, ip, assumption):
        try:
            data = {"name": "VPN"}
            json_data = json.dumps(data)
            url = "http://10.0.2.7:5000/RegularNotification"
            response = requests.post(url, data=json_data, headers={"Content-Type": "application/json"})
        except:
            print("Error send")
    def start(self):
        while True:
            try:
                self.ReadingFile()
                unicationIP = set([elem["id.orig_h"] for elem in self.json_list if elem['id.orig_h'] not in self.itMachineIp])
                for elem in unicationIP:
                    self.UpploadMachine(elem, [item for item in self.json_list if item["id.orig_h"] == elem])
    
                for elem in self.machineList:
                    if elem.MachineIsNotActive():
                        self.machineList.remove(elem)
                for elem in self.machineList:
                    if elem.IsMachineScanning():
                        self.sendmessage(elem.GetIp(), "Сканирование портов")
                        continue
                    if elem.IsMachineAttacking() > 0.9:
                        self.sendmessage(elem.GetIp(), "DoS-атака")
            except: 
                print("error start")
            time.sleep(10)



    def UpploadMachine(self, ip, input_traffic):
        try:
            index = self.GetIdMachineForList(ip)
            if index == -1:            
                self.machineList.append(
                    machine.Machine(ip, input_traffic, False if len(self.machineList) < self.countMachineKnown else True))
            else:
                self.machineList[index].AddTraffic(input_traffic)
        except: 
            print("error UpploadMachine")
    def GetIdMachineForList(self,ip):
        i = 0
        for elem in self.machineList:
            if elem.GetIp() == ip:
                return i
            i+=1
        return -1
    
    def ReadingFile(self):# считывание с файла, с ранее указаной позиции
        try:
            with open('/opt/zeek/logs/current/conn.log', 'r') as file:
                file.seek(self.current_position)
                self.json_list = file.readlines()
                self.current_position = file.tell()
                i = 0
                while i < len(self.json_list):
                    self.json_list[i] = eval(self.json_list[i].replace("true","True").replace("false","False"))
                    i+=1
        except:
            print("error ReadingFile")


manager = ManagerForDosDetection(8)
manager.start()

