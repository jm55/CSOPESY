'''
IO based from Hackerrank Problem (https://www.hackerrank.com/challenges/minimum-average-waiting-time/problem)

Algorithm: SJF and FCFS
'''
#!/bin/python3

import math
import os
import random
import re
import sys

def burstTimeRemaining(customers):
    burstTimes = 0
    for c in customers:
        burstTimes += c[1]
    return burstTimes
    
def getAveWT(ganttTable):
    total = 0
    for t in ganttTable:
        total += t["Et"]-t["At"]-t["Bt"]
    return total/len(ganttTable)

def getAveTT(ganttTable):
    total = 0
    for t in ganttTable:
        total += t["Et"]-t["At"]
    return total/len(ganttTable)

def getBurst(c):
    return c[1]

def getArrival(c):
    return c[0]
    
def SJF(customers):
    #print("FCFS Min. Average")
    queue = []
    ganttTable = []
    timer = 0
    queue = [] #Contains idx of customers in line

    customers.sort(key=getArrival)

    for idx, c in enumerate(customers): #To prevent process reuse
        customers[idx].append(False)
    
    queue.append(customers[0])
    customers[0][2] = True
    #print(timer, queue, ganttTable)
    while burstTimeRemaining(queue):
        queue.sort(key=getBurst) #Sort by lowest burst time remaining
        timer += queue[0][1]
        ganttTable.append({"At":queue[0][0], "Bt":queue[0][1], "Et":timer}) #Formatted as At, Bt, Ct/Et
        queue[0][1] = 0
        queue.pop(0)
        for idx, c in enumerate(customers): #Add proc on process queue that arrive within the updated time.
            if c[0] <= timer and not c[2]:
                queue.append(c)
                customers[idx][2] = True
        #print(timer, queue, ganttTable)
    return {"AveTT:":getAveTT(ganttTable), "AveWT":getAveWT(ganttTable)}


if __name__ == '__main__':
    #fptr = open(os.environ['OUTPUT_PATH'], 'w')

    n = int(input().strip())

    customers = []

    for _ in range(n):
        customers.append(list(map(int, input().rstrip().split())))

    result = SJF(customers)

    print(n)
    for c in customers:
        print(c[0], c[1])
    print(result)

    #fptr.write(str(result) + '\n')

    #fptr.close()
