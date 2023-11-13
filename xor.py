import sys

#display how the program should be used, then exit
def displayUsage():
    print("\n   py xor.py -k[keyFile] -i[inputFile] > [outputFile]")
    print("   -k[keyFile] set the key used to be the text inside of [keyFile]")
    print("   -i[inputFile] set the input file to [inputFile]\n")
    print("   py xor.py -k[keyFile] -i[inputFile]")
    print("   Printing to an output file is optional; you can print to the command line.")
    exit()

#read file byte by byte and convert to an array of decimal values (stdin)
def readFileBinarySTDIN():

    #read stdin as a byte array
    BA = sys.stdin.buffer.read()
    
    #convert byte array to an array of decimal values
    bytes = []
    for byte in BA:
        bytes.append(byte)
    return bytes

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

#perform xor decryption using 2 different arrays of binary strings:
#an encrypted text and a key. outputs array of decrypted binary strings
def xor(text, key):

    #convert text and key to byte array
    textBytes = bytearray(text)
    keyBytes = bytearray(key)

    #xor result will be stored in decimal array
    xorBytes = []

    #keep track of position in key
    keyLength = len(key)
    k = 0

    #for every byte, perform xor
    for i in textBytes:
        xorBytes.append(int(i ^ keyBytes[k]))

        #if key reaches the end, start from beginning of key
        k += 1
        if(k >= keyLength):
            k = 0
    
    #return result as a byte array
    return bytearray(xorBytes)

#collect system args
keyFile = ""
inputFile = ""
for arg in range(len(sys.argv)):
    if sys.argv[arg] == "--help":
        displayUsage()
    elif sys.argv[arg][:2] == "-k":
        keyFile = sys.argv[arg][2:]
    elif sys.argv[arg][:2] == "-i":
        inputFile = sys.argv[arg][2:]

if(keyFile == ""):
    print("\nMUST SPECIFY KEY FILE. Usage:")
    displayUsage()
if(inputFile == ""):
    print("\nMUST SPECIFY INPUT FILE. Usage:")
    displayUsage()

inputBytes = readFileBinary(sys.path[0] + "/" + inputFile)
keyBytes = readFileBinary(sys.path[0] + "/" + keyFile)

#perform xor 
code = xor(inputBytes, keyBytes)

#print out final code
sys.stdout.buffer.write(code)
