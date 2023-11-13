import sys
import os

#display how the program should be used, then exit
def displayUsage():
    sys.stdout.write("\n   python steg.py -(sr) -(bB) -o[val] -i[val] -w[inputFile] -h[inputFile] > [outputFile]\n")
    sys.stdout.write("   -s   store\n")
    sys.stdout.write("   -r   retrieve\n")
    sys.stdout.write("   -b   bit mode\n")
    sys.stdout.write("   -B   byte mode\n")
    sys.stdout.write("   -o[val] set offset to [val] (default is 0)\n")
    sys.stdout.write("   -i[val] set interval to [val] (default is 1)\n")
    sys.stdout.write("   -w[inputFile] set wrapper file to [inputFile]\n")
    sys.stdout.write("   -h[inputFile] set hidden file to [inputFile]\n\n")
    sys.stdout.write("   To try multiple offset and interval values at once:\n\n")
    sys.stdout.write("   python steg.py -r -(bB) -m -w[inputFile]\n")
    sys.stdout.write("   -m   prompt user to input an array of offset and interval values and try them all\n\n")
    sys.stdout.write("   std.out redirection is not used in this case, so do not include the \"> [outputFile]\" at the end.\n")
    sys.stdout.write("   You can use -i and -o here if you know one of those values for sure.\n")
    exit()

#sort an array of ints from least to greatest
def sortArray(arr):
    
    #continue sorting until a pass has been made without swapping
    arrSorted = False
    while(not arrSorted):
        arrSorted = True

        #for every element, if current element is greater than next, swap
        i = 0
        while(i < len(arr)-1):
            if(arr[i] > arr[i+1]):
                temp = arr[i]
                arr[i] = arr[i+1]
                arr[i+1] = temp
                arrSorted = False
            i += 1

    #return sorted array
    return arr

#read file byte by byte and convert to an array of decimal values
def readFileBinary(fileName):

    #read file as a byte array
    File = open(fileName, 'rb')
    BA = bytearray(File.read())

    #convert byte array to an array of decimal values
    bytes = []
    for byte in BA:
        bytes.append(byte)
    return bytes

#encrypt a hidden image into a wrapper image
def storage(W, H, curOffset, curInterval):
    
    #start at offset
    curPos = curOffset

    #byte method
    if(byte):

        #start at offset and replace each W bit with an H bit at each interval
        i = 0
        while(i < len(H)):
            W[curPos] = H[i]
            curPos += curInterval
            i += 1

        #continue at the same interval replacing W with sentinel bytes
        i = 0
        while(i < len(SENTINEL)):
            W[curPos] = SENTINEL[i]
            curPos += curInterval
            i += 1

        #return result
        return W
    
    #bit method
    if(bit):

        #convert wrapper to bytes
        baW = bytearray(W)
        baH = bytearray(H)
        
        #insert MSB of hidden file bytes into wrapper byte
        i = 0
        while(i < len(baH)):

            #do each bit of the hidden file byte and move to next wrapper byte when complete
            for j in range(8):
                baW[curPos] &= 0xfe
                baW[curPos] |= ((baH[i] & 0x80) >> 7)
                baH[i] <<= 1
                curPos += curInterval
            i += 1

        #same as above but sentinel bytes
        i = 0
        while(i < len(SENTINEL)):
            for j in range(8):
                baW[curPos] &= 0xfe
                baW[curPos] |= ((SENTINEL[i] & 0x80 >> 7))
                SENTINEL[i] <<= 1
                curPos += curInterval
            i += 1

#extract a hidden file from a wrapper file
def extract(W, H, curOffset, curInterval):

    #start at offset position
    curPos = curOffset
    senPos = 0

    #byte method
    if(byte):
        
        #check each byte
        while(True):

            #if current byte is not a sentinel byte, add it to hidden file bytes
            if(W[curPos] != SENTINEL[senPos]):
                H.append(W[curPos])
                senPos = 0

            #if current byte is a sentinel byte, continue checking for full sentinel
            else:
                H.append(W[curPos])
                senPos += 1

                #if full sentinel is found, hidden file is complete. break loop
                if(senPos >= len(SENTINEL)-1):
                    break
                    
            curPos += curInterval
            
        return H
    
    #bit method
    if(bit):

        #convert wrapper to bytes
        baW = bytearray(W)

        #check through entire wrapper text
        while(curPos < len(baW)):

            #build a byte       
            b = 0x0
            for j in range(8):
                
                #take LSB out of wrapper byte, place in byte being built, move to next wrapper byte
                b |= (baW[curPos] & 0x1)
                if(j < 7):
                    b <<= 1
                    curPos += curInterval
            
            #once byte is completed, check if it is a sentinel value
            #if it is, keep track of that (senPos). once all sentinel
            #values are found, break the loop
            if(b == SENTINEL[senPos]):
                senPos += 1
                if(senPos >= len(SENTINEL)-1):
                    break
            else:
                senPos = 0
            
            #move to next wrapper byte after current byte being built is complete        
            curPos += curInterval

            #add every completed byte to hidden byte array
            H.append(b)
   
        #return result as an array of decimals
        return H

# -s store
# -r retrieve
# -b bit
# -B byte
# -m array o/i
# -o<val> offset
# -i<val> interval
# -w<val> wrapper file
# -h<val> hidden file

#stegged-bit:  -b -o1024
#stegged-byte: -B -o1024 -i8 ... -B -o1025 -i2

#collect system args
store = retrieve = bit = byte = multiple = False
offset = 0
interval = 1
wrapperFile = hiddenFile = []
W = H = []
for arg in range(len(sys.argv)):
    if sys.argv[arg] == "--help":
        displayUsage()
    elif sys.argv[arg][:2] == "-s":
        store = True
    elif sys.argv[arg][:2] == "-r":
        retrieve = True
    elif sys.argv[arg][:2] == "-b":
        bit = True
    elif sys.argv[arg][:2] == "-B":
        byte = True
    elif sys.argv[arg] == "-m":
        multiple = True
    elif sys.argv[arg][:2] == "-o":
        offset = int(sys.argv[arg][2:])
    elif sys.argv[arg][:2] == "-i":
        interval = int(sys.argv[arg][2:])
    elif sys.argv[arg][:2] == "-w":
        wrapperFile = sys.argv[arg][2:]
    elif sys.argv[arg][:2] == "-h":
        hiddenFile = sys.argv[arg][2:]

#input validation
if(not store and not retrieve):
    sys.stdout.write("\nMUST SPECIFY STORAGE OR EXTRACTION. Usage:\n")
    displayUsage();
if(store and retrieve):
    sys.stdout.write("\nCANNOT PERFORM STORAGE AND EXTRACTION AT THE SAME TIME. Usage:\n")
    displayUsage();
if(not bit and not byte):
    sys.stdout.write("\nMUST SPECIFY BIT OR BYTE MODE. Usage:\n")
    displayUsage();
if(bit and byte):
    sys.stdout.write("\nCANNOT PERFORM BIT AND BYTE MODES AT THE SAME TIME. Usage:\n")
    displayUsage();
if((store and hiddenFile == []) or (store and wrapperFile != [])):
    sys.stdout.write("\nSTORAGE MODE REQUIRES HIDDEN FILE AND NOT WRAPPER FILE. Usage:\n")
    displayUsage();
if((extract and wrapperFile == []) or (extract and hiddenFile != [])):
    sys.stdout.write("\nEXTRACTION MODE REQUIRES WRAPPER FILE AND NOT HIDDEN FILE. Usage:\n")
    displayUsage();
if(multiple and not retrieve):
    sys.stdout.write("\nCANNOT STORE MULTIPLE HIDDEN FILES, MUST EXTRACT. Usage:\n")
    displayUsage();

#sentinel bytes
#   0x0:  0 decimal
#   0xff: 255 decimal
#   0, 255, 0, 0, 255, 0
SENTINEL = [0, 255, 0, 0, 255, 0]

if(len(wrapperFile) > 0):
    W = readFileBinary(sys.path[0] + "/" + wrapperFile)
if(len(hiddenFile) > 0):
    H = readFileBinary(sys.path[0] + "/" + hiddenFile)

#take in multiple values for offset and interval, attempt storage/extract for each
if(multiple):

    #offset was not given in command arguments
    if(offset == 0):

        #take in a list of values, convert them into an array of ints
        offsetString = input("\nInput offset values separated by commas (Enter nothing for all powers of 2.):\n")
        offsetString = offsetString.replace(" ", "")
        if(offsetString == ""):
            offsetArray = []
            o = 1
            offsetArray.append(0)
            while(o < 20):
                i = 1
                temp = 2
                while(i < o):
                    temp = temp * 2
                    i = i + 1
                offsetArray.append(temp)
                o = o + 1
        else:
            offsetArray = offsetString.split(",")
        offsetArray = list(map(int, offsetArray))

    #offset was given in command arguments, and we will use that offset
    else:
        offsetArray = [offset]

    #interval was not given in command arguments
    if(interval == 1):

        #take in a list of values, convert them into an array of ints
        intervalString = input("\nInput interval values separated by commas (Enter nothing for all powers of 2.):\n")
        print
        intervalString = intervalString.replace(" ", "")
        if(intervalString == ""):
            intervalArray = []
            o = 1
            while(o < 20):
                i = 1
                temp = 2
                while(i < o):
                    temp = temp * 2
                    i = i + 1
                intervalArray.append(temp)
                o = o + 1
        else:
            intervalArray = intervalString.split(",")
        intervalArray = list(map(int, intervalArray))

    #interval was given in command arguments, and we will use that interval
    else:
        intervalArray = [interval]

    

    #ensure that arrays are sorted least to greatest
    offsetArray = sortArray(offsetArray)
    intervalArray = sortArray(intervalArray)

    #we only want to keep the successful file with the highest offset value; lower offsets should be deleted
    #lastSuccessfulFile = None

    #try storage/extract for every single offset/interval value
    for o in offsetArray:
        for i in intervalArray:

            #extract
            if(retrieve):

                #open the file and attempt to extract it to an output file
                fileName = "output o=" + str(o) + " i=" + str(i)
                with open(fileName, 'w') as f:
                    try:
                        f.buffer.write(bytearray(extract(W, H, o, i)))
                        f.close()
                        print("Success for offset=" + str(o) + " interval=" + str(i))

                        #delete any files with a lower offset value (we only want highest offset)
                        #if(lastSuccessfulFile != None):
                        #    os.remove(lastSuccessfulFile)
                        #lastSuccessfulFile = fileName

                    #if the attempt failed, delete the output file
                    except:
                        f.close()
                        os.remove(fileName)
                        print("Failure for offset=" + str(o) + " interval=" + str(i))

#perform storage or extraction once (multiple = false) and print to output file
else:
    code = bytearray()
    if(store):
        encryptedFile = storage(W, H, offset, interval)
        code = bytearray(encryptedFile)
    if(retrieve):
        hiddenFile = extract(W, H, offset, interval)
        code = bytearray(hiddenFile)
    #output
    sys.stdout.buffer.write(code)
