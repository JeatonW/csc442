import sys

#display how the program should be used, then exit
def displayUsage():
    print("\n   py vigenere.py -(ed) -k[key] -i[inputFile] > [outputFile]")
    print("   -e perform encryption")
    print("   -d perform decryption")
    print("   -k set the key used in encryption/decryption process")
    print("   -i[inputFile] set input file to [inputFile]\n")
    print("   Perform encryption/decryption without the use of a file:")
    print("   py vigenere.py -(ed) -k[key]")
    exit()

#read from a file and return the text
def readFile(inFile):
    with open(inFile, 'r') as i:
        text = ""
        for l in i.readlines():
            text += l
        return text

#use input text and the user-defined key to encrypt a message and return the result
def encrypt(inputVar) -> str:

    final = ""
    keyCount = 0

    #evaluate every character of the soon-to-be encrypted message
    for i in inputVar:

        #if character in key is not a letter, dont use to encrypt
        while(True):
            if(ord(key[keyCount]) < 65 or 90 < ord(key[keyCount]) < 97 or 122 < ord(key[keyCount])):
                keyCount += 1
                if(keyCount >= len(key)):
                    keyCount = 0
            else:
                break

        #if character in input text is not a letter, dont encrypt
        if(ord(i) < 65 or 90 < ord(i) < 97 or 122 < ord(i)):
            final += i
        else:

            #determine whether or not uppercase for current char
            #for both input and key. values 65-90 are uppercase,
            #values 97-122 are lowercase. 97-65 = 32, so the offset
            #of numerical values is 32.
            inputOffset = 0
            keyOffset = 0
            if(97 <= ord(i) <= 122):
                inputOffset = 32
            if(97 <= ord(key[keyCount]) <= 122):
                keyOffset = 32

            #collapse values down so that A/a=0, B/b=1, C/c=2 etc
            #combine input char and key char
            temp = ord(i)-65-inputOffset + ord(key[keyCount])-65-keyOffset

            #if combined value is of a greater value than there are
            #letters in the alphabet, cycle back through to the start
            #of the alphabet (x -> y -> z -> a -> b -> c), then
            #"undo the collapse" (return A back to its correct ascii
            # value, 0 (A) -> 65, 1 (B) -> 66 etc)
            if(temp >= 26):
                temp -= 26
            temp += 65+inputOffset
            keyCount += 1

            #if the contents of the key is spent, cycle back to the
            #beginning of the key
            if(keyCount >= len(key)):
                keyCount = 0

            #add completed character to the final encrypted message
            final += chr(temp)
    
    return final

#use input text and the user-defined key to decrypt a message and return the result
def decrypt(inputVar) -> str:

    final = ""
    keyCount = 0

    #evaluate every character of the soon-to-be decrypted message
    for i in inputVar:

        #if character in key is not a letter, dont use to decrypt
        while(True):
            if(ord(key[keyCount]) < 65 or 90 < ord(key[keyCount]) < 97 or 122 < ord(key[keyCount])):
                keyCount += 1
                if(keyCount >= len(key)):
                    keyCount = 0
            else:
                break

        #if character in input text is not a letter, dont decrypt
        if(ord(i) < 65 or 90 < ord(i) < 97 or 122 < ord(i)):
            final += i
        else:

            #determine whether or not uppercase for current char
            #for both input and key. values 65-90 are uppercase,
            #values 97-122 are lowercase. 97-65 = 32, so the offset
            #of numerical values is 32.
            inputOffset = 0
            keyOffset = 0
            if(97 <= ord(i) <= 122):
                inputOffset = 32
            if(97 <= ord(key[keyCount]) <= 122):
                keyOffset = 32

            #collapse values down so that A/a=0, B/b=1, C/c=2 etc
            #combine input char and key char
            temp = ord(i)-65-inputOffset - (ord(key[keyCount])-65-keyOffset)

            #if combined value is less than zero, cycle back through to the end
            #of the alphabet (c -> b -> a -> z -> y -> x), then
            #"undo the collapse" (return A back to its correct ascii
            # value, 0 (A) -> 65, 1 (B) -> 66 etc)
            if(temp < 0):
                temp += 26
            temp += 65+inputOffset
            keyCount += 1

            #if the contents of the key is spent, cycle back to the
            #beginning of the key
            if(keyCount >= len(key)):
                keyCount = 0

            #add completed character to the final encrypted message
            final += chr(temp)
        
    return final

#collect system args
e = False
d = False
key = ""
fileName = ""
fileText = ""
for arg in range(len(sys.argv)):
    if sys.argv[arg] == "--help":
        displayUsage()
    elif sys.argv[arg] == "-e":
        e = True
    elif sys.argv[arg] == "-d":
        d = True
    elif sys.argv[arg][:2] == "-k":
        key = sys.argv[arg][2:]
    elif sys.argv[arg][:2] == "-i":
        fileName = sys.argv[arg][2:]

#input validation
if(key == ""):
    print("\nMUST SPECIFY KEY. Usage:")
    displayUsage()
if(e and d):
    print("\nCANNOT PERFORM ENCRYPTION AND DECRYPTION AT THE SAME TIME. Usage:")
    displayUsage()
if((e and d) or (not e and not d)):
    print("\nMUST SPECIFY ENCRYPTION OR DECRYPTION. Usage:")
    displayUsage()

#if file name included, grab text from file
if(fileName != ""):
    fileText = readFile(fileName)

#otherwise display normal instructions
else:
    if(e):
        print("\nInput text to be encrypted, or type \"***\" to exit:\n")
    if(d):
        print("\nInput text to be decrypted, or type \"***\" to exit:\n")

#manage user input and perform encryption/decryption accordingly
while(True):

    #using file as input text
    if(fileText != ""):
        if(e):
            print()
            print(encrypt(fileText), end='')
            break
        elif(d):
            print()
            print(decrypt(fileText), end='')
            break

    #no file used
    if(fileText == ""):
        inputText = input()
        if(inputText == "***"):
            break
        if(e):
            print(encrypt(inputText))
        elif(d):
            print(decrypt(inputText))