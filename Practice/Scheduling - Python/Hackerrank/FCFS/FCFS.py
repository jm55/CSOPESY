'''
IO based from Hackerrank Problem (https://www.hackerrank.com/challenges/minimum-average-waiting-time/problem)

Algorithm: FCFS

Note: Not working on cases with idles.
'''
#!/bin/python3

import copy

def processesNotUsed(process:list):
    notUsed = 0
    for p in process:
        if p[3] == False:
            notUsed += 1
    return notUsed

def burstTimeRemaining(process:list):
    burstTimes = 0
    for c in process:
        burstTimes += c[2]
    return burstTimes
    
def getAveWT(ganttTable:list):
    total = 0
    size = 0
    for t in ganttTable:
        if t["PID"] != "IDLE":
            print(t, t["Et"]-t["At"]-t["Bt"])
            total += t["Et"]-t["At"]-t["Bt"] #WaitTime=(EndTime-ArrivalTime)-BurstTime
            size += 1
    print("WT Total: ", total)
    return total/size

def getAveTT(ganttTable:list):
    total = 0
    size = 0
    for t in ganttTable:
        if t["PID"] != "IDLE":
            print(t, t["Et"]-t["At"])
            total += t["Et"]-t["At"] #TurnaroundTime=EndTime-ArrivalTime
            size += 1
    print("TT Total: ", total)
    return total/size

def getBurst(c:list):
    return c[2]

def getBurstByPID(processes:list, pid:str):
    for p in processes:
        if str(p[0]) == pid:
            return p[2]

def getArrival(c):
    return c[1]

def FCFS(process):
    queue = []
    ganttTable = []
    timer = 0

    process.sort(key=getArrival) #Initially sort by arrival time

    for idx, c in enumerate(process): #To prevent process reuse
        process[idx].append(False)
    
    while processesNotUsed(process)>0 or burstTimeRemaining(queue):
        #queue.sort(key=getArrival) #Sort by lowest arrival time
        for idx, c in enumerate(process): #Add proc on process queue that arrive within the updated time.
            if c[1] <= timer and not c[3]:
                queue.append(copy.deepcopy(c))
                process[idx][3] = True
        if len(queue) > 0:
            queue[0][2] -= 1
            if queue[0][2] == 0:
                ganttTable.append({"PID":queue[0][0], "At":queue[0][1], "Bt": getBurstByPID(process, str(queue[0][0])), "Et":timer+1}) #Formatted as PID, At, Bt, Ct/Et
                queue.pop(0)
        else:
            ganttTable.append({"PID":"IDLE", "At":timer, "Bt": 1, "Et":timer+1}) #Formatted as PID, At, Bt, Ct/Et
        timer += 1
    return {"AveTT:":getAveTT(ganttTable), "AveWT":getAveWT(ganttTable)}


if __name__ == '__main__':
    n = int(input().strip())
    process = []
    for _ in range(n):
        p = [_+1] + list(map(int, input().rstrip().split()))
        process.append(p)
    result = FCFS(process)
    print(result)