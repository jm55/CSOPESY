'''
CSOPESY - CPU Scheduling

de Veyra, Escalona, Naval, Villavicencio

Algorithms implemented: FCFS, SJF, SRTF, RR
'''

from proc import proc

'''
Prints the GanttTable as specified.
'''
def printGanttTable(output):
    #Get ganttable
    ganttTable = output["ganttTable"]
    processes = [] #processes and their start + end times
    wt = [] # each processes wait time
    
    for p in ganttTable:
        
        if len(processes) > 0: # 2nd item in queue, check if same proc or new
            
            idx = len(processes)-1 # get index of current
            prev = processes[idx].split(' ')[0] # get process number
            
            if str(p.pid) == prev: # same process
                processes[idx] += p.printSTET() # add start and end time to index
                wt[idx][1] += p.wait
                
            else: # new process
                processes.append(p.printID() + p.printSTET())
                wt.append([p.pid, 0 + p.wait])
        
        else: # first process
            processes.append(p.printID() + p.printSTET())
            wt.append([p.pid, 0 + p.wait])
        
    #put corresponding total wait times then print    
    for idx, item in enumerate(processes): 
        for w in wt:
            if w[0] == item.split(' ')[0]:
                item += "Waiting time: {wt:.0f}".format(wt=w[1])        
        print(item)
    
    print("Average waiting time: {avewt:.1f}".format(avewt=round(output["AveWT"],1)))

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
    '''
    for idx in range(len(ganttTable)):
        if ganttTable[idx].pid == process.pid:
            ganttTable[idx].end = process.end
            return ganttTable
    '''
    if len(ganttTable) > 0 and ganttTable[-1].pid == process.pid: #Compresses the consecutive processes
        ganttTable[-1].end = process.end
        return ganttTable
    ganttTable.append(process)
    return ganttTable

'''
Computes the waiting time of each process in the Gantt Table
'''
def getWT(ganttTable:list):
    processIDS = []
    for idx in range(len(ganttTable)):
        if not any(ganttTable[idx].pid in sublist for sublist in processIDS): #first instance of process in Gantt table
            ganttTable[idx].wait = ganttTable[idx].actualArrival - ganttTable[idx].arrival
            idSlot = [ganttTable[idx].pid, ganttTable[idx].end]
            processIDS.append(idSlot)
        else:
            temp = [sublist for sublist in processIDS if ganttTable[idx].pid in sublist]
            index = processIDS.index(temp[0])
            ganttTable[idx].wait = ganttTable[idx].actualArrival - processIDS[index][1] #Actual arrival of current instance of process - End of previous instance of process
            processIDS[index][1] = ganttTable[idx].end
    return ganttTable

'''
Returns the average waiting time.
'''
def getAveWT(ganttTable:list):
    getWT(ganttTable)
    total = 0
    processIDS = []
    for idx, t in enumerate(ganttTable): #Compute the total waiting time
        if t.pid != "IDLE": # Ignore IDLE times
            total += t.wait
            if t.pid not in processIDS:
                processIDS.append(t.pid)
    return total/len(processIDS)

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

def getPIDInt(p:proc):
    if "IDLE" in p.pid:
        return -1
    else:
        return int(p.pid)