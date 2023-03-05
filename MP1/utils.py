'''
CSOPESY - CPU Scheduling

Escalona, De Veyra, Naval

Algorithms implemented: FCFS, SJF, SRTF, RR
'''

from proc import proc

'''
Prints the GanttTable as specified.
'''
def printGanttTable(output):
    #Get ganttable and sort by PID
    ganttTable = output["ganttTable"]
    ganttTable.sort(key=getPID)

    #Print headers (formalities)
    header = "PID".ljust(6," ") + "Start Time".upper().ljust(16, " ")
    header += "->".ljust(4," ") + "End Time".upper().ljust(16, " ") + "| Wait Time".upper().ljust(16," ")
    print(header)
    print("".ljust(len(header),"="))
    
    #Print every item on GanttTable and the aveWT
    for p in ganttTable:
        p.printProc()
    print("\nAverage Wait Time: ".upper(), output["AveWT"])
    #print("Average Turnaround Time: ", output["AveTT"])
    print("")

'''
Returns an IDLE process if 1 time unit.
'''
def idleProc(timer:int, actualArrival:int):
    return proc("IDLE", timer, 1, timer+1, True, actualArrival)

'''
True if list of process has unused process,
false if otherwise.
'''
def unusedProcess(process:list):
    for p in process:
        if p.used == False:
            return True
    return False

'''
Returns the sum of burstTimes 
of processes on a process list.
Useful for checking queue. 
'''
def burstTimeRemaining(process:list):
    burstTimes = 0
    for p in process:
        burstTimes += p.burst
    return burstTimes
    
'''
Find an item that matches the given process (via slot) 
and update end time of the given process. If no process
is found, then append to ganttTable
'''
def updateGanttTable(ganttTable:list, process: proc):
    for idx in range(len(ganttTable)):
        if ganttTable[idx].pid == process.pid:
            ganttTable[idx].end = process.end
            return ganttTable
    ganttTable.append(process)
    return ganttTable

'''
Returns the average waiting time.
'''
def getAveWT(ganttTable:list):
    total = 0
    size = 0
    for idx, t in enumerate(ganttTable):
        if t.pid != "IDLE": #Only consider those actual processes
            total += t.end-t.arrival-t.burst #WaitTime=(EndTime-ArrivalTime)-BurstTime
            ganttTable[idx].wait = t.end-t.arrival-t.burst
            size += 1
    return total/size

'''
Returns the average turnaround time.
'''
def getAveTT(ganttTable:list):
    total = 0
    size = 0
    for idx, t in enumerate(ganttTable):
        if t.pid != "IDLE": #Only consider those actual processes
            total += t.end-t.arrival #WaitTime=(EndTime-ArrivalTime)-BurstTime
            ganttTable[idx].turnaround = t.end-t.arrival
            size += 1
    return total/size

def getBurst(p:proc):
    return p.burst

def getBurstByPID(processes:list, pid:str):
    for p in processes:
        if str(p.pid) == pid:
            return p.burst

def getArrival(p:proc):
    return p.arrival

def getPID(p:proc):
    return p.pid