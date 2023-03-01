from proc import proc
import fcfs
import sjf
import strf
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
    for f in files:
        output = None
        if mode == 0:
            output = fcfs.FCFS(parseInput(open(directory+f[0], "r"))[1])
        elif mode == 1:
            output = sjf.SJF(parseInput(open(directory+f[0], "r"))[1])
        elif mode == 2:
            output = strf.STRF(parseInput(open(directory+f[0], "r"))[1])
        elif mode == 3:
            input = parseInput(open(directory+f[0], "r"))
            output = rr.RR(input[1], input[0][2])
        else: 
            print("Invalid Mode")
        if output != None:
            if output["AveWT"] == f[1] and output["AveTT"] == f[2]:
                print(f[0] + " PASS (WT:{ewt:.2f}/{wt:.2f} TT:{ett:.2f}/{tt:.2f})".format(ewt=f[1], ett=f[2], wt=output["AveWT"], tt=output["AveTT"]))
            else:
                print(f[0] + " FAIL (WT:{ewt:.2f}/{wt:.2f} TT:{ett:.2f}/{tt:.2f})".format(ewt=f[1], ett=f[2], wt=output["AveWT"], tt=output["AveTT"]))
    print("")

def test_fcfs():
    print("FCFS Test")
    directory = "test_files\\fcfs\\"
    #Format as [filename, Expected WT, Expected TT]
    files = [
                ["1.txt", 2.6, 6.8],
                ["2.txt", 13.75, 24.25],
                ["3.txt", 5.5, 13.5],
                ["4.txt", 6.8, 12.8],
                ["5.txt", 11.25, 22]
            ]
    loop_files(0, directory, files)

def test_sjf():
    print("SJF Test")
    directory = "test_files\\sjf\\"
    #Format as [filename, Expected WT, Expected TT]
    files = [
                ["1.txt", 2.4, 6.6],
                ["2.txt", 13.75, 24.25],
                ["3.txt", 3.5, 11.5],
                ["4.txt", 5.2, 11.2],
                ["5.txt", 9, 19.5]
            ]
    loop_files(1, directory, files)

def test_strf():
    print("STRF Test")
    directory = "test_files\\strf\\"
    #Format as [filename, Expected WT, Expected TT]
    files = [
                ["1.txt", 2.4, 6.6],
                ["2.txt", 6.25, 16.75],
                ["3.txt", 7.2, 16.2],
                ["4.txt", 3.5, 11.5],
                ["5.txt", 5.2, 11.2]
            ]
    loop_files(2, directory, files)
        
def test_rr():
    print("RR Test")
    directory = "test_files\\rr\\"
    #Format as [filename, Expected WT, Expected TT]
    files = [
                ["io_test.txt", 2.4, 6.6]
            ]
    loop_files(3, directory, files)

test_fcfs()
test_sjf()
test_strf()
test_rr()