import datetime
from collections import Counter
class Machine:
    def __init__(self, ip, traffic, suspicious):
        self.ip = ip
        self.countTraffic = [len(traffic)]
        self.lastActiveTime = datetime.datetime.now()
        self.traffic = traffic
        self.suspiciousTraffic = self.AnalysForSuspiciousTraffic()
        self.suspicious = suspicious
        self.suspiciousTrafficCount = 0


    def GetIp(self):
        return self.ip
    def GetTraffic(self):
        return self.traffic
    def AddTraffic(self, input_traffic): # Добавляяем трафик
        if len(self.countTraffic) < 10:
            self.countTraffic.append(len(input_traffic))
        else:
            self.countTraffic.pop(0)
            self.countTraffic.append(len(input_traffic))
        self.traffic = input_traffic
        self.suspiciousTraffic = self.AnalysForSuspiciousTraffic()
        self.analyzCountTraffic()
        self.lastActiveTime = datetime.datetime.now()
    def analyzCountTraffic(self): # анализ на количество трафика
        i = 0
        flowGrowth = list()
        while i!=len(self.countTraffic)-1:
            flowGrowth.append(self.countTraffic[i+1]/self.countTraffic[i])
            i+=1
        grad = (sum(flowGrowth)/len(flowGrowth))/max(flowGrowth)
        self.suspiciousTrafficCount = grad if grad >=0 else 0
        return
    def MachineIsNotActive(self): # если машина неактивка
        return datetime.datetime.now()-self.lastActiveTime >= datetime.timedelta(minutes=3)
    def AnalysForSuspiciousTraffic(self):# проверка на подозрительность трафика
        recordsForIp = [elem for elem in self.traffic if (elem["conn_state"] in ['S0','SHR', 'OTH', 'RSTRH', 'RSTO','REJ'])]
        return len(recordsForIp) / len(self.traffic)
    def IsMachineScanning(self):
        recordsForIp = [elem for elem in self.traffic if (elem.get("conn_state") == "S0" or elem.get("conn_state") == "REJ")]
        if len(recordsForIp) > 10:                 
            unique_values = set()
            for d in recordsForIp:
                unique_values.add(d["id.orig_p"])
            if len(unique_values) > 10:
                return True
            else:
                return False
    def IsMachineAttacking(self):
        res = self.suspiciousTraffic * 0.5 + self.suspicious * 0.1 + self.suspiciousTrafficCount * 0.4
        if self.suspiciousTraffic * 0.5 + self.suspicious * 0.1 + self.suspiciousTrafficCount * 0.4 > 0.1:
            print(f"IP - {self.GetIp()} --- {self.suspiciousTraffic * 0.5 + self.suspicious * 0.1 + self.suspiciousTrafficCount * 0.4}")
            print(f"self.suspiciousTraffic - {self.suspiciousTraffic}    self.suspicious - {self.suspicious}     self.suspiciousTrafficCount - {self.suspiciousTrafficCount}")
            print("___")
        self.suspiciousTraffic = 0
        self.suspicious = 0
        self.suspiciousTrafficCount = 0
        return res
