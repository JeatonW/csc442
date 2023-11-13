#take in file name and set file text to a string
import sys

#display how the program should be used, then exit
def displayUsage():
	print("\n   py binaryDecoder.py -7 -8 -s -i[inputFile]")
	print("   -7   perform decryption using byte length 7")
	print("   -8   perform decryption using byte length 8")
	print("   -s   perform decryption swapping from 7 to 8 bits, starting at 7")
	print("   -i[inputFile] set input file to [inputFile]")
	exit()

#read from a file and return the text
def readFile(inFile):
	with open(inFile, 'r') as i:
		text = ""
		for l in i.readlines():
			text += l.replace("\n", "").replace(" ", "")
		return text

#convert file's binary to readable text and print
def convert(byteLength):

	#divide the string by 8, contain each 8 in one position of array
	fileBytes = []
	bitCount = 0
	curByte = ""
	for i in fileText:
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

		#if ascii value doesnt exist, this means we used
		#the incorrect bit length (can happen if the length
		#of the information is divisible by both 7 and 8, i.e.
		#56. in this case we only want only one to conversion 
		#of the correct length, not both.
		#if(curBitVal > 127):
			#return

	#convert decimal values to characters via ascii codes
	charVals = ""
	for i in decVals:
		charVals += chr(i)

	#print result
	return charVals

#convert file's binary to readable text and print
def convertSwap():

	#divide the string by 8, contain each 8 in one position of array
	fileBytes = []
	bitCount = 0
	curByte = ""
	s = False
	byteLength = 7
	for i in fileText:
		curByte += str(i)
		bitCount += 1


		if(bitCount > byteLength-1):
			fileBytes.append(curByte)
			bitCount = 0
			curByte = ""
			if(not s):
				byteLength = 8
				s = True
			else:
				byteLength = 7
				s = False
			curByteLength = byteLength - 1

	#convert binary to decimal

	decVals = []
	for i in fileBytes:
		curBitVal = 0
		curDigit = 0

		for j in range(len(i)):
			byteLength = len(i)
			if(i[byteLength-1-j] == "1"):
				curBitVal += pow(2,curDigit)
			curDigit += 1
		decVals.append(curBitVal)

		#if ascii value doesnt exist, this means we used
		#the incorrect bit length (can happen if the length
		#of the information is divisible by both 7 and 8, i.e.
		#56. in this case we only want only one to conversion 
		#of the correct length, not both.
		#if(curBitVal > 127):
			#return

	#convert decimal values to characters via ascii codes
	charVals = ""
	for i in decVals:
		charVals += chr(i)

	#print result
	return charVals

#collect system args
seven = False
eight = False
swap = False
fileName = ""
for arg in range(len(sys.argv)):
	if sys.argv[arg] == "--help":
		displayUsage()
	elif sys.argv[arg] == "-7":
		seven = True
	elif sys.argv[arg] == "-8":
		eight = True
	elif sys.argv[arg] == "-s":
		swap = True
	elif sys.argv[arg][:2] == "-i":
		fileName = sys.argv[arg][2:]

#input validation
if(fileName == ""):
	print("\n*MUST SPECIFY INPUT FILE. Usage:")
	displayUsage()
if(not seven and not eight and not swap):
	print("\n*MUST SPECIFY BYTE LENGTH. Usage:")
	displayUsage()

#read file
fileText = readFile(fileName)

#display converted text
print()
if(seven):
	print(convert(7))
if(eight):
	print(convert(8))
if(swap):
	print(convertSwap())
