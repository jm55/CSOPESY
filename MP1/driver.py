'''
CSOPESY - CPU Scheduling

de Veyra, Escalona, Naval, Villavicencio

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
        input_processes.append(proc(str(abc[0]),abc[1], abc[2]))
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

    output["ganttTable"].sort(key=utils.getPIDInt)

    #Display output
    utils.printGanttTable(output)

if __name__ == "__main__":
    main()