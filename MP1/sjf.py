from proc import proc

import copy

def processesNotUsed(process:list):
    notUsed = 0
    for p in process:
        if p.used == False:
            notUsed += 1
    return notUsed

def burstTimeRemaining(process:list):
    burstTimes = 0
    for p in process:
        burstTimes += p.burst
    return burstTimes
    
def getAveWT(ganttTable:list):
    total = 0
    size = 0
    for idx, t in enumerate(ganttTable):
        if t.pid != "IDLE":
            #print(t.getString(), t.end-t.arrival-t.burst)
            total += t.end-t.arrival-t.burst #WaitTime=(EndTime-ArrivalTime)-BurstTime
            ganttTable[idx].wait = t.end-t.arrival-t.burst
            size += 1
    #print("WT Total: ", total)
    return total/size

def getAveTT(ganttTable:list):
    total = 0
    size = 0
    for idx, t in enumerate(ganttTable):
        if t.pid != "IDLE":
            #print(t.getString(), t.end-t.arrival)
            total += t.end-t.arrival #WaitTime=(EndTime-ArrivalTime)-BurstTime
            ganttTable[idx].turnaround = t.end-t.arrival
            size += 1
    #print("TT Total: ", total)
    return total/size

def getBurst(p:proc):
    return p.burst

def getBurstByPID(processes:list, pid:str):
    for p in processes:
        if str(p.pid) == pid:
            return p.burst

def getArrival(p:proc):
    return p.arrival

def idleProc(timer:int, actualArrival:int):
    return proc("IDLE", timer, 1, timer+1, True, actualArrival)

def SJF(process:list):
    queue = [] #For process queue
    ganttTable = [] #Gantt table containing proc objects
    timer = 0 #Equivalent to the ticking 'clock'
    actualArrival = 0 #Place holder for process' real ACTUAL arrival time

    process.sort(key=getArrival)
    process.sort(key=getBurst)
    while processesNotUsed(process)>0 or burstTimeRemaining(queue):
        #Add proc on process queue that arrive within the updated time
        for idx, p in enumerate(process): 
            if p.arrival <= timer and not p.used:
                queue.append(copy.deepcopy(p))
                process[idx].used = True
        
         #Add process or idle depending on the contents of queue
        if len(queue) > 0: #Decrement burst of first process in queue and add process to gantt chart if applicable
            queue[0].burst -= 1
            if queue[0].burst == 0:
                ganttslot = proc(queue[0].pid, queue[0].arrival, getBurstByPID(process, queue[0].pid),timer+1,True, actualArrival)
                actualArrival = timer+1
                ganttTable.append(ganttslot)
                queue.pop(0)
        else:
            ganttTable.append(idleProc(timer, actualArrival))
        
        timer += 1 #Step time
    return {"ganttTable": ganttTable, "AveTT":getAveTT(ganttTable), "AveWT":getAveWT(ganttTable)}