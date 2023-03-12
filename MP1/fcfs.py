'''
CSOPESY - CPU Scheduling

Escalona, de Veyra, Naval

Algorithms implemented: FCFS, SJF, SRTF, RR
'''

import copy

from proc import proc
import utils

def FCFS(processes:list):
    queue = [] #Process queue
    ganttTable = [] #Gantt table
    timer = 0 #'Clock'
    actualArrival = 0 #Process' ACTUAL arrival time on GanttTable

    #Re-sort by least to most important factor
    processes.sort(key=utils.getPID)
    processes.sort(key=utils.getArrival)

    #Run until there are no processes unused or left in queue
    while utils.unusedProcess(processes) or len(queue):
        
        #Add proc on process queue that arrive within the updated time
        for idx, p in enumerate(processes): 
            if p.arrival <= timer and not p.used:
                processes[idx].used = True #To not be appended again
                queue.append(copy.deepcopy(p)) #REMEMBER copy.deepcopy()
        
        #Add process or idle depending on the contents of queue
        if len(queue) > 0: #Decrement burst of first process in queue and add process to gantt chart if applicable
            queue[0].burst -= 1
            if queue[0].burst == 0: #Save to ganttchart and remove from queue
                ganttslot = proc(queue[0].pid, queue[0].arrival, utils.getBurstByPID(processes, queue[0].pid), timer+1, True, actualArrival)
                ganttTable = utils.updateGanttTable(ganttTable, ganttslot)
                queue.pop(0)
                actualArrival = timer+1
        else: #Add idle if nothing on queue
            ganttTable.append(utils.idleProc(timer, actualArrival))
            actualArrival = timer+1
        
        #Update timers and arrival markers for next iteration.
        timer += 1
    return {"ganttTable": ganttTable, "AveTT":utils.getAveTT(ganttTable), "AveWT":utils.getAveWT(ganttTable)}