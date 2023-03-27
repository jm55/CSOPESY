'''
CSOPESY - CPU Scheduling

de Veyra, Escalona, Naval, Villavicencio

Algorithms implemented: FCFS, SJF, SRTF, RR
'''

import time
import math

from proc import proc
import fcfs
import sjf
import srtf
import rr

def parseInput(file):
    input_processes = []
    xyz = list(map(int, file.readline().rstrip().split())) #Get XYZ values as array/list.
    #Retrieve ABCs from input
    for _ in range(xyz[1]): 
        abc = list(map(int, file.readline().strip().split()))
        input_processes.append(proc(str(abc[0]),abc[1], abc[2]))
    return xyz, input_processes

def loop_files(mode:int, directory:str, files:list):
    out = []
    passing = 0
    for f in files:
        output = None
        mode = parseInput(open(directory+f[0], "r"))[0][0]
        print("Testing: {filename:}...".format(filename=f[0]))
        if mode == 0:
            output = fcfs.FCFS(parseInput(open(directory+f[0], "r"))[1])
        elif mode == 1:
            output = sjf.SJF(parseInput(open(directory+f[0], "r"))[1])
        elif mode == 2:
            output = srtf.SRTF(parseInput(open(directory+f[0], "r"))[1])
        elif mode == 3:
            input = parseInput(open(directory+f[0], "r"))
            output = rr.RR(input[1], input[0][2])
        else: 
            print("Invalid Mode")
        if output != None:
            #print(output["AveWT"], math.floor(output["AveWT"]), f[1], math.floor(f[1]),  math.floor(output["AveWT"]) == math.floor(f[1]))
            if math.floor(output["AveWT"]) == math.floor(f[1]): # and output["AveTT"] == f[2]:
                out.append(f[0] + " PASS (EWT/AWT:{ewt:.1f}/{awt:.1f})".format(ewt=f[1], ett=f[2], awt=output["AveWT"], tt=output["AveTT"]))
                passing += 1
            else:
                out.append(f[0] + " FAIL (EWT/AWT:{ewt:.1f}/{awt:.1f})".format(ewt=f[1], ett=f[2], awt=output["AveWT"], tt=output["AveTT"]))
    print("")
    return [out, (passing/len(files))*100]

def test_fcfs():
    print("Testing FCFS...")
    directory = "test_files\\fcfs\\"
    #Format as [filename, Expected WT, Expected TT]
    files = [
                ["1.txt", 2.6, 6.8],
                ["2.txt", 13.75, 24.25],
                ["3.txt", 5.5, 13.5],
                ["4.txt", 6.8, 12.8],
                ["5.txt", 11.25, 22],
                ["6.txt", 7.75, 13.25],
                ["7.txt", 3, 6],
                ["8.txt", 17, 27],
                ["9.txt", 26, 40]
            ]
    return loop_files(0, directory, files)

def test_sjf():
    print("Testing SJF...")
    directory = "test_files\\sjf\\"
    #Format as [filename, Expected WT, Expected TT]
    files = [
                ["1.txt", 2.4, 6.6],
                ["2.txt", 13.75, 24.25],
                ["3.txt", 3.5, 11.5],
                ["4.txt", 5.2, 11.2],
                ["5.txt", 9, 19.5],
                ["6.txt", 7, 13],
                ["7.txt", 25, 39]
            ]
    return loop_files(1, directory, files)

def test_srtf():
    print("Testing SRTF...")
    directory = "test_files\\srtf\\"
    #Format as [filename, Expected WT, Expected TT]
    files = [
                ["1.txt", 2.4, 6.6],
                ["2.txt", 6.25, 16.75],
                ["3.txt", 7.2, 16.2],
                ["4.txt", 3.5, 11.5],
                ["5.txt", 5.2, 11.2],
                ["6.txt", 6.5, 13],
                ["7.txt", 16.8, 30.8]
            ]
    return loop_files(2, directory, files)
        
def test_rr():
    print("Testing RR...")
    directory = "test_files\\rr\\"
    #Format as [filename, Expected WT, Expected TT]
    files = [
                ["1.txt", 66.25, 104.5],
                ["2.txt", 34.8, 48.8],
                ["3.txt", 10.6, 16.6],
                ["4.txt", 4.4, 8.6]
            ]
    return loop_files(3, directory, files)

def sample_io():
    print("Testing SampleIO...")
    directory = "test_files\\sample_io\\"
    files = [
                ["input05.txt", 438.4, 0],
                ["input08.txt", 5170.0, 0],
                ["input11.txt", 55831.0, 0],
                ["input13.txt", 144131.2, 0],
            ]
    return loop_files(-1, directory, files)


#<<< EXECUTION ZONE >>>
start = time.time()

scores = [
            ["FCFS", 0],
            ["SJF", 0],
            ["STRF", 0],
            ["RR", 0],
            ["SampleIO",0]
        ]
scores[0][1] = test_fcfs()
scores[1][1] = test_sjf()
scores[2][1] = test_srtf()
scores[3][1] = test_rr()
scores[4][1] = sample_io()

end = time.time()

print("MP1 Test Result Summary:")
print("Format: Expected/Actual\n")
for s in scores:
    print(s[0].ljust(4," "), "{:.2f}% PASSED".format(s[1][1]))
    for out in s[1][0]:
        print(out)
    print("")

for s in scores:
    print(s[0].ljust(4," "), "{:.2f}% PASSED".format(s[1][1]))
print("Test Time: {:.4f}s".format(end-start))