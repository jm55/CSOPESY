'''
CSOPESY - CPU Scheduling

Escalona, de Veyra, Naval

Algorithms implemented: FCFS, SJF, SRTF, RR
'''

from proc import proc

'''
Prints the GanttTable as specified.
'''
def printGanttTable(output):
    #Get ganttable
    ganttTable = output["ganttTable"]
    #ganttTable.sort(key=getPID)
    
    #Lists for stringified ver. of ganttTable processes.
    printable = [] #Will contain individual process to be printed later 'Stringified processes'
    wait_times = [] #Will contain sum of all wait times per pid (contains tuple of [pid,wait,added(t/f)])
    
    #Build printable and wait_times
    for p in ganttTable:
        #Discard IDLEs
        if "IDLE" in p.pid:  
            continue

        #For valid PIDs
        if len(printable) == 0: #Printable no contents, append first available value
            printable.append((p.printPID() + p.printStart() + p.printEnd()))
            wait_times.append([p.pid, p.wait, False])
        elif len(printable) > 0: #Printable has at least 1
            printable_found = False #For if the same printable is found (process already in printables) or not
            
            #Iterate for every available printable already saved
            for idx, i in enumerate(printable): 
                printable_pid = int(str(i).split(' ')[0]) #Extract pid from string ("<{pid}> start time: {st} | ")
                if int(p.pid) == printable_pid:
                    printable[idx] += p.printStart() + p.printEnd()
                    printable_found = True
            if not printable_found:
                printable.append((p.printPID() + p.printStart() + p.printEnd()))
            
            #Build sum of wait_times based on what the current PID
            if len(wait_times) == 0: #Wait Times has no contents, append first available value
                wait_times.append([p.pid, p.wait, False])
            else:
                wait_found = False #For if the same wait_time is found (wait of process in wait_times) or not
                for idx, t in enumerate(wait_times):
                    time_pid = int(str(t[0]).split(' ')[0]) #Extract pid from string ("<{pid}> start time: {st} | ")
                    if int(p.pid) == time_pid:
                        wait_times[idx][1] += p.wait
                        wait_found = True
                if not wait_found:
                    wait_times.append([p.pid, p.wait, False])

    #Append summation of wait_times to printable
    for idx1, p in enumerate(printable):
        for idx2, w in enumerate(wait_times):
            if int(w[0]) == int(str(p).split(' ')[0]) and not w[2]:
                printable[idx1] += "Waiting time: {wt:.0f}".format(wt=w[1])
                wait_times[idx2][2] = True
    
    #Finally, print the finished table
    for p in printable:
        print(p)

    #Print average times
    print("Average wait time: ", round(output["AveWT"],1))
    #print("Average Turnaround Time: ", output["AveTT"])

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