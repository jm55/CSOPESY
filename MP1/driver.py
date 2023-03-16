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
        input_processes.append(proc("P"+str(abc[0]),abc[1], abc[2]))
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

    #Display output
    utils.printGanttTable(output)

if __name__ == "__main__":
    main()