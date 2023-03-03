'''
CSOPESY - CPU Scheduling

Escalona, De Veyra, Kaye

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
    def printProc(self):
        out = "{pid}".format(pid=self.pid).ljust(6," ") + "Start Time: {at}".format(at=self.actualArrival).ljust(16, " ")
        out += "->".ljust(4," ") + "End Time: {et}".format(et=self.end).ljust(16, " ") + "| Wait Time: {wt}".format(wt=self.wait).ljust(16," ")
        print(out)