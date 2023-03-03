'''
CSOPESY - CPU Scheduling

Escalona, De Veyra, Kaye

Algorithms implemented: FCFS, SJF, SRTF, RR
'''

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
        input_processes.append(proc("P"+str(abc[0]),abc[1], abc[2]))
    return xyz, input_processes

def loop_files(mode:int, directory:str, files:list):
    print("Format: Expected/Actual")
    passing = 0
    for f in files:
        output = None
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
            if output["AveWT"] == f[1] and output["AveTT"] == f[2]:
                print(f[0] + " PASS (WT:{ewt:.2f}/{wt:.2f} TT:{ett:.2f}/{tt:.2f})".format(ewt=f[1], ett=f[2], wt=output["AveWT"], tt=output["AveTT"]))
                passing += 1
            else:
                print(f[0] + " FAIL (WT:{ewt:.2f}/{wt:.2f} TT:{ett:.2f}/{tt:.2f})".format(ewt=f[1], ett=f[2], wt=output["AveWT"], tt=output["AveTT"]))
    print("Score: {:.2f}".format((passing/len(files)*100))+"%")
    print("")
    return (passing/len(files))*100

def test_fcfs():
    print("FCFS Test")
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
    print("SJF Test")
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
    print("SRTF Test")
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
    print("RR Test")
    directory = "test_files\\rr\\"
    #Format as [filename, Expected WT, Expected TT]
    files = [
                ["1.txt", 66.25, 104.5]
            ]
    return loop_files(3, directory, files)

scores = [
            ["FCFS", 0],
            ["SJF", 0],
            ["STRF", 0],
            ["RR", 0]
        ]
scores[0][1] = test_fcfs()
scores[1][1] = test_sjf()
scores[2][1] = test_srtf()
scores[3][1] = test_rr()

print("MP1 Test Result Summary:")
for s in scores:
    print(s[0].ljust(6," "), "{:.2f}%".format(s[1]))