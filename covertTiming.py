# use Python 3
import socket
from sys import stdout
from time import time

# enables debugging output
DEBUG = False

#halfway point of timings
#timings less than median represent 0,
#while timings greater than median represent 1
timingMedian = 0.15

# set the server's IP address and port
ip = "10.0.0.125"
port = 12321

# create the socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# connect to the server
s.connect((ip, port))

# create output for timings between characters
timings = []

# receive data until EOF
data = s.recv(4096).decode()
while (data.rstrip("\n") != "EOF"):
	# output the data
	stdout.write(data)
	stdout.flush()
	# start the "timer", get more data, and end the "timer"
	t0 = time()
	data = s.recv(4096).decode()
	t1 = time()
	# calculate the time delta (and output if debugging)
	delta = round(t1 - t0, 3)
	timings.append(delta)
	if (DEBUG):
		stdout.write(" {}\n".format(delta))
		stdout.flush()

print()
#display timings
print(timings)
print()

#create output for binary code
binaryCode = ""

#determine binary code of timings
for i in timings:
	if(i < 0.14):
		binaryCode += "0"
	if(i > 0.14 and i < 0.16):
		binaryCode += "1"
	if(i > 0.16):
		binaryCode += "2"

#print binary code
print(binaryCode)
print()
for i in binaryCode:
	if(i == "0"):
		print("1", end="")
	if(i == "1"):
		print("0", end="")

exit()

#convert binary to readable text and print
def convert(byteLength, text):

	#divide the string by 8, contain each 8 in one position of array
	fileBytes = []
	bitCount = 0
	curByte = ""
	for i in text:
		curByte += str(i)
		bitCount += 1
		if(bitCount > byteLength-1):
			fileBytes.append(curByte)
			bitCount = 0
			curByte = ""

	#convert binary to decimal
	decVals = []
	for i in fileBytes:
		curBitVal = 0
		curDigit = 0
		for j in range(byteLength):
			if(i[byteLength-1-j] == "1"):
				curBitVal += pow(2,curDigit)
			curDigit += 1
		decVals.append(curBitVal)

	#convert decimal values to characters via ascii codes
	charVals = ""
	for i in decVals:
		charVals += chr(i)

	#return result
	return charVals

#convert the full covert message using both 7 bit and 8 bit binary
sevenBitFull = convert(7, binaryCode)
eightBitFull = convert(8, binaryCode)

#recognize EOF and extract covert message from the repeating string
i = 0
length = len(sevenBitFull)
sevenBit = ""
while(i < length):
	if(i > length-1):
		break
	if(sevenBitFull[i] == 'E' and sevenBitFull[i+1] == 'O' and sevenBitFull[i+2] == 'F'):
		break
	sevenBit += sevenBitFull[i]
	i += 1
i = 0
length = len(eightBitFull)
eightBit = ""
while(i < length):
	if(i > length-1):
		break
	if(eightBitFull[i] == 'E' and eightBitFull[i+1] == 'O' and eightBitFull[i+2] == 'F'):
		break
	eightBit += eightBitFull[i]
	i += 1


#close the connection to the server
s.close()

#perform binary to text
stdout.write("\nCovert message:")
stdout.write("\n   Byte length 7: " + sevenBit)
stdout.write("\n   Byte length 8: " + eightBit + "\n")
stdout.flush()
