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
    
    def printProc(self): # print process (name, start time, end time, and wait time) for gantt chart
        mod_pid = self.pid
        if "P" in mod_pid:
            mod_pid = mod_pid[1:len(mod_pid)] 
        out = "{pid} start time: {at} end Time: {et} | Waiting time: {wt}".format(pid=mod_pid, at=self.actualArrival, et=self.end, wt=self.wait)
        print(out)

    def printPID(self):
        mod_pid = self.pid
        if "P" in mod_pid:
            mod_pid = mod_pid[1:len(mod_pid)]
        return mod_pid + " "

    def printStart(self):
        return "start time: {at} ".format(at=self.actualArrival)
    
    def printEnd(self):
        return "end Time: {et} | ".format(et=self.end)