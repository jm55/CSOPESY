import copy

from proc import proc
import fcfs
import sjf

def getPID(p:proc):
    return p.pid

def compressGanttTable(ganttTable:list):
    newGanttTable = []
    return ganttTable

def main():
    input_processes = []
    output = []
    xyz = list(map(int, input().rstrip().split())) #Get XYZ values as array/list.
    
    #Retrieve ABCs from input
    for i in range(xyz[1]): 
        abc = list(map(int, input().strip().split()))
        input_processes.append(proc("P"+str(abc[0]),abc[1], abc[2]))
    
    #Get mode and execute
    if xyz[0] == 0:
        output = fcfs.FCFS(input_processes)
    elif xyz[0] == 1:
        output = sjf.SJF(input_processes)
    elif xyz[0] == 2:
        print("STRF")
    elif xyz[0] == 3:
        print("RR")
    else:
        print("Invalid mode!")
        exit(1)

    #Compress Gantt Table
    output = compressGanttTable(copy.deepcopy(output))

    #Print output
    printGanttTable(output["ganttTable"])
    print("Average Wait Time: ", output["AveWT"])
    print("Average Turnaround Time: ", output["AveTT"])
    print("")

def printGanttTable(ganttTable):
    for p in ganttTable:
        p.printProc()

if __name__ == "__main__":
    main()