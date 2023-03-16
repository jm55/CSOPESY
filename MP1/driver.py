'''
CSOPESY - CPU Scheduling

Escalona, de Veyra, Naval

Algorithms implemented: FCFS, SJF, SRTF, RR
'''

import copy

from proc import proc
import fcfs
import sjf
import srtf
import rr
import utils

'''
Compresses the consecutive IDLEs into one

Only affects how the GanttTable is 
displayed and does not affect its computations.
'''
def compressGanttTable(ganttTable:list): 
    if ganttTable == None:
        return None
    newGanttTable = []
    startIdleIdx = -1
    endIdleIdx = -1

    for idx, g in enumerate(ganttTable):
        if g.pid == "IDLE" and startIdleIdx == -1:
            startIdleIdx = g.arrival
        if g.pid == "IDLE" and startIdleIdx != -1:
            endIdleIdx = g.end
        if g.pid != "IDLE" and startIdleIdx != -1 and endIdleIdx != -1:
            #print(startIdleIdx, "->", endIdleIdx)
            newGanttTable.append(proc("IDLE", startIdleIdx, endIdleIdx-startIdleIdx, endIdleIdx, actualArrival=startIdleIdx))
            startIdleIdx = -1
            endIdleIdx = -1
        if g.pid != "IDLE" and startIdleIdx == -1 and endIdleIdx == -1:
            newGanttTable.append(copy.deepcopy(ganttTable[idx]))
    ganttTable = None
    return newGanttTable

'''
Consolidate similar procs items on list (by same PID) into a single line for printing
'''
def consolidateProcs(ganttTable:list):
    output = [] #List of string to be printed
    ganttTable.sort(key=utils.getPIDInt) #DON'T CHANGE
   
    '''
    Function assumes that ganttTable does not have IDLEs

    Input ganttTable look:
    1 start time: 9 end Time: 13 | Waiting time: 0
    1 start time: 21 end Time: 42 | Waiting time: 8
    1 start time: 137 end Time: 183 | Waiting time: 95
    2 start time: 13 end Time: 21 | Waiting time: 0
    3 start time: 948 end Time: 1045 | Waiting time: 934

    Actual Output from Sample IO look/Target output[] list of str of ganttTable:
    1 start time: 9 end time: 13 | start time: 21 end time: 42 | start time: 137 end time: 183 | Waiting time: 103
    2 start time: 13 end time: 21 | Waiting time: 0
    3 start time: 948 end time: 1045 | Waiting time: 934

    Consider the goal convert proc objects in Input ganttTable into single line string list[] for every PID sorted by PID. 
    '''

    prevPID = None
    out_str = ""
    out_wait = 0
    for g in ganttTable:
        if prevPID == None:
            #Set the PID and start&end for output string and add wait to output_wait for the first item
            #e.g.: "<pid> start time: <start> end time: <end> | "
            prevPID = g.pid
            out_str += g.procPID() + g.procStartEnd()
            out_wait += g.wait
        elif g.pid == prevPID: 
            #Append the next 'start time ## end time: ## |' and add wait to the output_wait for the same pids
            #e.g.: "<pid> start time: <start> end time: <end> | start time: <start> end time: <end> | "
            out_str += g.procStartEnd()
            out_wait += g.wait
        elif g.pid != prevPID:
            #Build the final output string by adding the total waiting time as 'Waiting time: #' and append it into the output[]
            #e.g.: "<pid> start time: <start> end time: <end> | start time: <start> end time: <end> | Waiting time: <wait>"
            output.append(out_str+g.procWait(out_wait))
            
            #Reset the output string and output wait for use of next ganttTable item
            out_str = ""
            out_wait = 0

            #Similar thing for the first item
            #e.g.: "<pid> start time: <start> end time: <end> | "
            prevPID = g.pid
            out_str += g.procPID() + g.procStartEnd()
            out_wait += g.wait

    return output

'''
Drops IDLE processes from ganttTable as per sample IO files on Canvas.
'''
def dropIDLE(ganttTable:list):
    if ganttTable == None:
        return None
    newGanttTable = []
    for g in ganttTable:
        if g.pid != "IDLE":
            newGanttTable.append(g)
    return newGanttTable

'''
Parses input from terminal using specified
xyz and abc pattern
Recommended command: py driver.py < [filename.txt]
'''
def parseInput():
    input_processes = []
    xyz = list(map(int, input().rstrip().split())) #Get XYZ values as array/list.
    #Retrieve ABCs from input
    for _ in range(xyz[1]): 
        abc = list(map(int, input().strip().split()))
        input_processes.append(proc(abc[0],abc[1], abc[2]))
    return xyz, input_processes

def main():
    #Parse input
    xyz, input_processes = parseInput()
    
    #Get mode and execute
    if xyz[0] == 0:
        output = fcfs.FCFS(input_processes)
    elif xyz[0] == 1:
        output = sjf.SJF(input_processes)
    elif xyz[0] == 2:
        output = srtf.SRTF(input_processes)
    elif xyz[0] == 3:
        output = rr.RR(input_processes, xyz[2])
    else:
        print("Invalid mode!")
        exit(1)

    #Error occured
    if output == None:
        print("ERROR: No Output Found!")
        exit(1)

    #Compress Gantt Table for better display
    output["ganttTable"] = compressGanttTable(output["ganttTable"])

    #Drop IDLEs
    output["ganttTable"] = dropIDLE(output["ganttTable"])

    #Consolidate Processes
    output["ganttTable"] = consolidateProcs(output["ganttTable"])

    #Display output
    utils.printGanttTable(output)

if __name__ == "__main__":
    main()