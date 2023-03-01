from proc import proc

def idleProc(timer:int, actualArrival:int):
    return proc("IDLE", timer, 1, timer+1, True, actualArrival)

def unusedProcess(process:list):
    for p in process:
        if p.used == False:
            return True
    return False

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
            #print(t.pid, t.arrival, t.burst, t.end, t.end-t.arrival, t.end-t.arrival-t.burst)
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

def getPID(p:proc):
    return p.pid