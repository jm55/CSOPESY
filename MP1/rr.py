'''
CSOPESY - CPU Scheduling

Escalona, De Veyra, Kaye

Algorithms implemented: FCFS, SJF, SRTF, RR
'''

import copy

from proc import proc
import utils

def RR(processes:list, q:int):
    queue = [] #Process queue
    ganttTable = [] #Gantt table
    timer = 0 #'Clock'
    actualArrival = 0 #Process' ACTUAL arrival time on GanttTable
    timeJump = 0 #used for dynamically adding timer's count since RR tends to have dynamic time increments (q or process' burst; whichever is lower)

    #Re-sort by least to most important factor
    processes.sort(key=utils.getPID)
    processes.sort(key=utils.getArrival)
    
    #Run until no process unused or is left on queue
    while utils.unusedProcess(processes) or len(queue):
        
        #Add proc on process queue that arrive within the updated time
        for idx, p in enumerate(processes): 
            if p.arrival <= timer and not p.used:
                processes[idx].used = True #To not be appended again
                queue.append(copy.deepcopy(p)) #REMEMBER copy.deepcopy()
        
        #Add process or idle depending on the contents of queue
        if len(queue) > 0: #Decrement burst of first process in queue and add process to gantt chart if applicable
            timeJump = 0

            #Decrement by q or itself (whichever is lower)            
            if queue[0].burst < q:
                timeJump = queue[0].burst
                queue[0].burst -= queue[0].burst
            else:
                timeJump = q
                queue[0].burst -= q

            #Update ganttTable with latest values from process in queue[0]
            ganttslot = proc(queue[0].pid, queue[0].arrival, utils.getBurstByPID(processes, queue[0].pid), timer+timeJump, True, actualArrival)
            ganttTable = utils.updateGanttTable(ganttTable, ganttslot)
            
            #Check if reached 0
            if queue[0].burst == 0: #Remove from queue
                queue.pop(0)
            else: #Switch queue[0] position to end.
                temp = copy.deepcopy(queue[0])
                queue.pop(0)
                queue.append(temp)

            #Update timers
            actualArrival = timer+timeJump
            timer += timeJump
            
        else: #Add idle if nothing on queue
            ganttTable.append(utils.idleProc(timer, actualArrival))
            actualArrival = timer+1
            timer += 1
    return {"ganttTable": ganttTable, "AveTT":utils.getAveTT(ganttTable), "AveWT":utils.getAveWT(ganttTable)}