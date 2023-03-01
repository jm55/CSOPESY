import copy

from proc import proc
import utils

def SJF(processes:list):
    queue = [] #Process queue
    ganttTable = [] #Gantt table
    timer = 0 #'Clock'
    actualArrival = 0 #Process' ACTUAL arrival time on GanttTable
    ongoing = None #'Follows wait until finish'

    #Re-sort by least to most important factor
    processes.sort(key=utils.getPID)
    processes.sort(key=utils.getArrival)
    processes.sort(key=utils.getBurst)
    while utils.unusedProcess(processes) or len(queue) or ongoing != None:
        #Queue process from process list
        for idx, p in enumerate(processes):
            if p.arrival <= timer and not p.used:
                processes[idx].used = True #To not be appended again
                queue.append(copy.deepcopy(p)) #REMEMBER copy.deepcopy()
                queue.sort(key=utils.getBurst)

        #Get ongoing if queue has something that is arrived and lowest burst
        if len(queue) > 0:
            if queue[0].arrival <= timer and ongoing == None:
                ongoing = queue[0]
                queue.pop(0)

        #Add process or idle depending on the contents of queue
        if ongoing: #Decrement burst of first process in queue and add process to gantt chart if applicable
            ongoing.burst -= 1
            if ongoing.burst == 0:
                ganttslot = proc(ongoing.pid, ongoing.arrival, utils.getBurstByPID(processes, ongoing.pid),timer+1,True, actualArrival)
                ganttTable.append(ganttslot)
                ongoing = None
        else: #Add idle if nothing ongoing
            ganttTable.append(utils.idleProc(timer, actualArrival))
            actualArrival = timer
        timer += 1 #Step time
        actualArrival = timer
    return {"ganttTable": ganttTable, "AveTT":utils.getAveTT(ganttTable), "AveWT":utils.getAveWT(ganttTable)}