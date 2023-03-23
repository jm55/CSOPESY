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
    
    def printSTET(self): # Print start time and end time
        mod_pid = self.pid
        if "P" in mod_pid:
            mod_pid = mod_pid[1:len(mod_pid)] 
        return "start time: {at} end Time: {et} ".format(at=self.actualArrival, et=self.end)

    def printID(self): # print ID
        mod_pid = self.pid
        if "P" in mod_pid:
            mod_pid = mod_pid[1:len(mod_pid)]
        return mod_pid + " "