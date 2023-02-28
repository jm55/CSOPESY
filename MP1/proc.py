class proc:
    def __init__(self, pid:str, arrival:int, burst:int, end:int=0, used:bool=False, actualArrival:int=0):
        self.pid = pid
        self.arrival = arrival
        self.burst = burst
        self.used = used
        self.end = end
        self.wait = 0
        self.actualArrival = actualArrival
        self.turnaround = 0
    def printProc(self):
        print("{pid}: Start Time: {at} -> End Time: {et} | Waiting Time: {wt}".format(pid=self.pid, at=self.actualArrival, et=self.end, wt=self.wait))