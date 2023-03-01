import copy

from proc import proc
import fcfs
import sjf
import strf
import rr

def getPID(p:proc):
    return p.pid

def compressGanttTable(ganttTable:list): #Only affects how ganttTable is displayed and not on its computations
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

def parseInput():
    input_processes = []
    xyz = list(map(int, input().rstrip().split())) #Get XYZ values as array/list.
    #Retrieve ABCs from input
    for _ in range(xyz[1]): 
        abc = list(map(int, input().strip().split()))
        input_processes.append(proc("P"+str(abc[0]),abc[1], abc[2]))
    return xyz, input_processes

def main():
    xyz, input_processes = parseInput()
    
    #Get mode and execute
    if xyz[0] == 0:
        output = fcfs.FCFS(input_processes)
    elif xyz[0] == 1:
        output = sjf.SJF(input_processes)
    elif xyz[0] == 2:
        output = strf.STRF(input_processes)
    elif xyz[0] == 3:
        output = rr.RR(input_processes, xyz[2])
    else:
        print("Invalid mode!")
        exit(1)

    if output == None:
        print("ERROR: No Output Found!")
        exit(1)

    #Compress Gantt Table
    output["ganttTable"] = compressGanttTable(output["ganttTable"])

    #Print output
    printGanttTable(output["ganttTable"])
    print("\nAverage Wait Time: ".upper(), output["AveWT"])
    #print("Average Turnaround Time: ", output["AveTT"])
    print("")

def printGanttTable(ganttTable):
    header = "PID".ljust(6," ") + "Start Time".upper().ljust(16, " ")
    header += "->".ljust(4," ") + "End Time".upper().ljust(16, " ") + "| Wait Time".upper().ljust(16," ")
    print(header)
    print("".ljust(len(header),"="))
    for p in ganttTable:
        p.printProc()

if __name__ == "__main__":
    main()