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

    time_skip = 0 #Will be used for skipping time by whatever burst time queue[0] is.

    '''
    FURTHER EXPLANATION BEHIND TIME_SKIP:
    This is because of FCFS non-preemptive nature thus allowing us to use the burst time 
    as is to be the 'stepping-stone' for the timer to skip to the end of the burst time 
    instead of counting 1 time unit at a time.

    Do note that IDLEs remain counting 1 at a time.
    '''

    #Run until there are no processes unused or left in queue
    while utils.unusedProcess(processes) or len(queue):

        #Add proc on process queue that arrive within the updated time
        for idx, p in enumerate(processes): 
            if p.arrival <= timer and not p.used:
                processes[idx].used = True #To not be appended again
                queue.append(copy.deepcopy(p)) #REMEMBER copy.deepcopy()
        
        #Add process or idle depending on the contents of queue
        if len(queue) > 0: #Decrement burst of first process in queue and add process to gantt chart if applicable
            time_skip = queue[0].burst
            queue[0].burst = 0
            ganttslot = proc(queue[0].pid, queue[0].arrival, utils.getBurstByPID(processes, queue[0].pid), timer+time_skip, True, actualArrival)
            ganttTable = utils.updateGanttTable(ganttTable, ganttslot)
            queue.pop(0)
            actualArrival += time_skip #Replaces the timer+1 originally used
            timer += time_skip #Replaces timer += 1 below at the end of while loop
            time_skip = 0 #Rest time skip for next process
        else: #Add idle if nothing on queue
            ganttTable.append(utils.idleProc(timer, actualArrival))
            actualArrival = timer+1
            timer+=1
            time_skip = 0
        #timer += 1 #Step time

    return {"ganttTable": ganttTable, "AveTT":utils.getAveTT(ganttTable), "AveWT":utils.getAveWT(ganttTable)}