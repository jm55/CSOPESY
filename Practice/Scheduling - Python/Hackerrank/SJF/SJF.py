'''
IO based from Hackerrank Problem (https://www.hackerrank.com/challenges/minimum-average-waiting-time/problem)

Algorithm: SJF and FCFS

Note: Not working on cases with idles.
'''
#!/bin/python3

def burstTimeRemaining(process):
    burstTimes = 0
    for c in process:
        burstTimes += c[1]
    return burstTimes
    
def getAveWT(ganttTable):
    total = 0
    for t in ganttTable:
        total += t["Et"]-t["At"]-t["Bt"] #WaitTime=(EndTime-ArrivalTime)-BurstTime
    return total/len(ganttTable)

def getAveTT(ganttTable):
    total = 0
    for t in ganttTable:
        total += t["Et"]-t["At"] #TurnaroundTime=EndTime-ArrivalTime
    return total/len(ganttTable)

def getBurst(c):
    return c[1]

def getArrival(c):
    return c[0]

def SJF(process):
    queue = []
    ganttTable = []
    timer = 0

    process.sort(key=getArrival) #Initially sort by arrival time

    for idx, c in enumerate(process): #To prevent process reuse
        process[idx].append(False)
    
    queue.append(process[0])
    process[0][2] = True
    #print(timer, queue, ganttTable)
    while burstTimeRemaining(queue):
        queue.sort(key=getBurst) #Sort by lowest burst time remaining
        timer += queue[0][1]
        ganttTable.append({"At":queue[0][0], "Bt":queue[0][1], "Et":timer}) #Formatted as At, Bt, Ct/Et
        queue[0][1] = 0
        queue.pop(0)
        for idx, c in enumerate(process): #Add proc on process queue that arrive within the updated time.
            if c[0] <= timer and not c[2]:
                queue.append(c)
                process[idx][2] = True
        #print(timer, queue, ganttTable)
    return {"AveTT:":getAveTT(ganttTable), "AveWT":getAveWT(ganttTable)}


if __name__ == '__main__':
    n = int(input().strip())
    process = []
    for _ in range(n):
        process.append(list(map(int, input().rstrip().split())))
    result = SJF(process)
    print(result)