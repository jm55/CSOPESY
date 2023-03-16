'''
CSOPESY - CPU Scheduling

Escalona, de Veyra, Naval

Algorithms implemented: FCFS, SJF, SRTF, RR
'''

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
    
    time_skip = 0 #Will be used for skipping time by whatever burst time queue[0] is.

    '''
    FURTHER EXPLANATION BEHIND TIME_SKIP:
    This is because of SJF non-preemptive nature thus allowing us to use the burst time 
    as is to be the 'stepping-stone' for the timer to skip to the end of the burst time 
    instead of counting 1 time unit at a time.

    Do note that IDLEs remain counting 1 at a time.
    '''

    #Run until no process unused or is left on queue
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
            time_skip = ongoing.burst
            ganttslot = proc(ongoing.pid, ongoing.arrival, utils.getBurstByPID(processes, ongoing.pid), timer+time_skip,True, actualArrival)
            ganttTable = utils.updateGanttTable(ganttTable, ganttslot)
            actualArrival += time_skip #Replaces the timer+1 originally used
            timer += time_skip #Replaces timer += 1 below at the end of while loop
            time_skip = 0 #Rest time skip for next process
            ongoing = None
        else: #Add idle if nothing ongoing
            ganttTable.append(utils.idleProc(timer, actualArrival))
            actualArrival = timer+1
            timer+=1
            time_skip = 0
        #timer += 1 #Step time
    return {"ganttTable": ganttTable, "AveTT":utils.getAveTT(ganttTable), "AveWT":utils.getAveWT(ganttTable)}