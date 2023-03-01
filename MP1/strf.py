import copy

from proc import proc
import utils

def updateGanttTable(ganttTable:list, slot: proc):
    for idx in range(len(ganttTable)):
        if ganttTable[idx].pid == slot.pid:
            ganttTable[idx].end = slot.end
            ganttTable[idx].burst = slot.burst
            return ganttTable
    ganttTable.append(slot)
    return ganttTable

def STRF(processes:list):
    queue = [] #Process queue
    ganttTable = [] #Gantt table
    timer = 0 #'Clock'
    actualArrival = 0 #Process' ACTUAL arrival time on GanttTable

    processes.sort(key=utils.getArrival) #Initially sort by arrival time
    while utils.unusedProcess(processes) or len(queue):
        #Add proc on process queue that arrive within the updated time
        for idx, p in enumerate(processes): 
            if p.arrival <= timer and not p.used:
                processes[idx].used = True #To not be appended again
                queue.append(copy.deepcopy(p)) #REMEMBER copy.deepcopy()
        
        queue.sort(key=utils.getPID)
        queue.sort(key=utils.getArrival)
        queue.sort(key=utils.getBurst) #Re-sort by lowest burst time
        
        #Add process or idle depending on the contents of queue
        if len(queue) > 0: #Decrement burst of first process in queue and add process to gantt chart if applicable
            queue[0].burst -= 1
            ganttslot = proc(queue[0].pid, queue[0].arrival, utils.getBurstByPID(processes, queue[0].pid),timer+1,True, actualArrival)
            ganttTable = updateGanttTable(ganttTable, ganttslot)
            if queue[0].burst == 0:
                queue.pop(0)
        else: #Add idle if nothing on queue
            ganttTable.append(utils.idleProc(timer, actualArrival))
            actualArrival = timer
        timer += 1 #Step time
        actualArrival = timer
    return {"ganttTable": ganttTable, "AveTT":utils.getAveTT(ganttTable), "AveWT":utils.getAveWT(ganttTable)}