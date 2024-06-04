import DetectionAnomaliesTraffic
import time
import requests
import json

class ManagerForDosDetection():

    countMachineKnown = 10
    machineIp = ['192.168.31.144']

    def __init__(self, numberParticipants):
        self.countMachineKnown = numberParticipants
        self.machineList = list()
        self.json_list = list()
        self.current_position = 0
        self.itMachineIp = ['192.168.31.144']

    def Sendmessage(self, ip, assumption):
        try:
            data = {"name": "nameMachine", "trigger": assumption, "IP":f"{ip}"}
            json_data = json.dumps(data)
            url = "http://IP-Server-monitoring:5000/sendnotificate"
            response = requests.post(url, data=json_data, headers={"Content-Type": "application/json"})
        except:
            print("Error send")
    def SendRegularNotification(self):
        try:
            data = {"name": "vpnsrv"}
            json_data = json.dumps(data)
            url = "http://192.168.31.244:5000/RegularNotification"
            response = requests.post(url, data=json_data, headers={"Content-Type": "application/json"})
        except:
            print("Error send")
    def start(self):
        while True:
            try:
                self.SendRegularNotification()
                self.ReadingFile()
                unicationIP = set([elem["id.orig_h"] for elem in self.json_list if elem['id.orig_h'] not in self.itMachineIp])
                for elem in unicationIP:
                    self.UpploadMachine(elem, [item for item in self.json_list if item["id.orig_h"] == elem])    
                for elem in self.machineList:
                    if elem.MachineIsNotActive():
                        self.machineList.remove(elem)
                for elem in self.machineList:
                    if elem.IsMachineScanning() == True:
                        self.Sendmessage(elem.GetIp(), "Сканирование портов")
                        continue
                    if elem.IsMachineAttacking() >= 0.8:
                        self.Sendmessage(elem.GetIp(), "DoS-атака")
            except: 
                print("error start")
            time.sleep(20)



    def UpploadMachine(self, ip, input_traffic):
        try:
            index = self.GetIdMachineForList(ip)
            if index == -1:            
                self.machineList.append(
                    DetectionAnomaliesTraffic.Machine(ip, input_traffic, False if len(self.machineList) < self.countMachineKnown else True))
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
    
    def ReadingFile(self):
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

