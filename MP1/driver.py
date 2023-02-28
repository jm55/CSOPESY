import copy

from proc import proc
import fcfs
import sjf
import strf

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
    for _ in range(xyz[1]): 
        abc = list(map(int, input().strip().split()))
        input_processes.append(proc("P"+str(abc[0]),abc[1], abc[2]))
    
    #Get mode and execute
    if xyz[0] == 0:
        output = fcfs.FCFS(input_processes)
    elif xyz[0] == 1:
        output = sjf.SJF(input_processes)
    elif xyz[0] == 2:
        output = strf.STRF(input_processes)
    elif xyz[0] == 3:
        print("RR")
    else:
        print("Invalid mode!")
        exit(1)

    #Compress Gantt Table
    output = compressGanttTable(copy.deepcopy(output))

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