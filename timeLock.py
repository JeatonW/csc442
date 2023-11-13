import sys
import time
import datetime
import hashlib

#display how the program should be used, then exit
def displayUsage():
    print("\n   py timeLock.py < [inputFile]\n")
    print("   py timeLock.py")
    print("   Using an input file is optional. Without it, program will prompt you for epoch time.")
    exit()

#get epoch time
def getEpoch():
    ed = input("\nGive the epoch time using the following format:\nYYYY MM DD hh mm ss\n")
    #d = "1999 12 31 23 59 59" #epoch time test (from assignment pdf)
    print("\n  Epoch Time: " + ed)
    ep = '%Y %m %d %H %M %S'

    try:
        e = int(time.mktime(time.strptime(ed,ep)))
    except:
        print("\nIncorrect format used for epoch time, or date & time do not exist.")
        exit()

    return e

#get current time
def getNow():
    cp = '%Y-%m-%d %H:%M:%S.%f'


    
    #cd = "2023-11-09 05:57:08"
    



    cd = str(datetime.datetime.now()) #actual current time
    #cd = '2013-05-06 07:43:25.0' #cur time test (from assignment pdf)
    print("Current Time: " + cd)
    return int(time.mktime(time.strptime(cd,cp)))

#using epoch and current time, generate a code
def genCode():

    #subtract epoch from current time to get time difference
    timeDiff = now - epoch

    #set time difference to beginning of current 60s interval
    #and convert to string
    timeDiff = str(timeDiff - timeDiff % 60)

    #perform MD5 compound hash twice
    ch1 = hashlib.md5(timeDiff.encode()).hexdigest()
    ch2 = hashlib.md5(ch1.encode()).hexdigest()

    #extract timelock code from compound hash
    code = ""

    #retrieve first two letters left>right
    alpCount = 0
    for i in ch2:
        if(97 <= ord(i) <= 102):
            code += i
            alpCount += 1
        if(alpCount == 2):
            break

    #retrieve first two numbers right>left
    numCount = 0
    i = len(ch2) - 1
    while(i >= 0):
        if(48 <= ord(ch2[i]) <= 57):
            code += ch2[i]
            numCount += 1
        if(numCount == 2):
            break
        i -= 1

    mid = int(len(ch2)/2 - 1)
    
    code += ch2[15]
    code += ch2[16]

    print(ch2)
    print(len(ch2))

    return code

#collect system args
for arg in range(len(sys.argv)):
    if sys.argv[arg] == "--help":
        displayUsage()

#get epoch and current times, print them both
epoch = getEpoch()
now = getNow()

#print result
sys.stdout.write("\nFinal Code: cyberstorm" + genCode() + "\n")
