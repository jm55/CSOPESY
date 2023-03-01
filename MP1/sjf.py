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
            #print(t.pid, t.arrival, t.burst, t.end, t.end-t.arrival, t.end-t.arrival-t.burst)
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

    ongoing = None
    process.sort(key=getBurst)
    while processesNotUsed(process) > 0 or len(queue) or ongoing != None:
        #Queue process from process list
        for idx, p in enumerate(process):
            if p.arrival <= timer and not p.used:
                process[idx].used = True
                queue.append(copy.deepcopy(p))
                queue.sort(key=getBurst)

        #Get ongoing if queue has something that is arrived and lowest burst
        if len(queue) > 0:
            if queue[0].arrival <= timer and ongoing == None:
                ongoing = queue[0]
                queue.pop(0)

        #Add process or idle depending on the contents of queue
        if ongoing != None: #Decrement burst of first process in queue and add process to gantt chart if applicable
            ongoing.burst -= 1
            if ongoing.burst == 0:
                ganttslot = proc(ongoing.pid, ongoing.arrival, getBurstByPID(process, ongoing.pid),timer+1,True, actualArrival)
                ganttTable.append(ganttslot)
                ongoing = None
        else:
            ganttTable.append(idleProc(timer, actualArrival))
            actualArrival = timer
        timer += 1 #Step time
        actualArrival = timer
    return {"ganttTable": ganttTable, "AveTT":getAveTT(ganttTable), "AveWT":getAveWT(ganttTable)}