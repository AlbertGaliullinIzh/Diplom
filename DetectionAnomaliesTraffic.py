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
    def MachineIsNotActive(self):
        return datetime.datetime.now()-self.lastActiveTime >= datetime.timedelta(minutes=3)
    def AddTraffic(self, input_traffic):
        if len(self.countTraffic) < 10:
            self.countTraffic.append(len(input_traffic))
        else:
            self.countTraffic.pop(0)
            self.countTraffic.append(len(input_traffic))
        self.traffic = input_traffic
        self.suspiciousTraffic = self.AnalysForSuspiciousTraffic()
        self.analyzCountTraffic()
        self.lastActiveTime = datetime.datetime.now()
    def analyzCountTraffic(self):
        c = 0
        i = 0
        t = 0
        while i < len(self.countTraffic)-2:
            i += 1
            if self.countTraffic[i-1] < self.countTraffic[i] and self.countTraffic[i] < self.countTraffic[i+1]:
                c += self.countTraffic[i]/self.countTraffic[i-1] - 1
                t+=1
            if self.countTraffic[i-1] < self.countTraffic[i] and self.countTraffic[i] > self.countTraffic[i+1] and self.countTraffic[i]/self.countTraffic[i-1] > self.countTraffic[i+1]/self.countTraffic[i]:
                c += self.countTraffic[i]/self.countTraffic[i-1] - 1
                t +=1
        if t == 0:
            self.suspiciousTrafficCount = 0
            return
        self.suspiciousTrafficCount = c/t if c/t < 1 else 1
    def AnalysForSuspiciousTraffic(self):
        recordsForIp = [elem for elem in self.traffic if (elem["conn_state"] in ['S0','SH','SHR', 'OTH', 'RSTRH', 'RSTO','REJ'])]
        return len(recordsForIp) / len(self.traffic)
    def IsMachineScanning(self):
        recordsForIp = [elem for elem in self.traffic if (elem.get("conn_state") == "S0" or elem.get("conn_state") == "REJ")]
        if len(recordsForIp) > 10:
            unique_values = set()
            for d in recordsForIp:
                unique_values.add(d["id.resp_p"])
            if len(unique_values) > 10:
                return True
            else:
                return False
    def IsMachineAttacking(self):
        res = self.suspiciousTraffic * 0.5 + self.suspicious * 0.1 + self.suspiciousTrafficCount * 0.4
        self.suspiciousTraffic = 0
        self.suspicious = 0
        self.suspiciousTrafficCount = 0
        return res
