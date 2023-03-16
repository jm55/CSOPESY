'''
CSOPESY - CPU Scheduling

Escalona, de Veyra, Naval

Algorithms implemented: FCFS, SJF, SRTF, RR
'''

'''
Process (proc for short) object.

Contains all of the necessary data for the process which is primarily 
based on how one would draw a process table.

A list of this object can be either a process table, a process queue, or ganttTable 
depending on how its data is appended, modified and shown.
'''
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
    
    def procWait(self, wait_time:int=None):
        if wait_time == None:
            return " Waiting time: {wt}".format(wt=self.wait)
        else:
            return " Waiting time: {wt}".format(wt=wait_time)

    def procStartEnd(self):
        return "start time: {at} end Time: {et} |".format(at=self.actualArrival, et=self.end)

    def procPID(self):
        return "{pid} ".format(pid=self.pid)

    def procAsString(self):
        return self.procPID() + self.procStartEnd() + self.procWait()
    
    def printProc(self): # print process (name, start time, end time, and wait time) for gantt chart
        print(self.procAsString())