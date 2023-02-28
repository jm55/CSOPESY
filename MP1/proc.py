class proc:
    def __init__(self, pid:str, arrival:int, burst:int, end:int=0, used:bool=False):
        self.pid = pid
        self.arrival = arrival
        self.burst = burst
        self.used = used
        self.end = end
    def setUsed(self, used:bool):
        self.used = used
    def getString(self):
        return self.pid + ": " + str(self.arrival) + "/" + str(self.burst) + "/" + str(self.end) + " (" + str(self.used) + ")"
    def printString(self):
        print(self.getString())