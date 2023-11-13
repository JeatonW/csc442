from ftplib import FTP

# FTP server details
IP = "10.0.0.125"
PORT = 21
USER = "velociraptor"
PASSWORD = "henryosborn"
FOLDER = "/"
USE_PASSIVE = True # set to False if the connection times out
METHOD = False #true=7bit, false=10bit

# connect and login to the FTP server
ftp = FTP()
ftp.connect(IP, PORT)
ftp.login(USER, PASSWORD)
ftp.set_pasv(USE_PASSIVE)

# navigate to the specified directory and list files
ftp.cwd(FOLDER)
files = []
ftp.dir(files.append)

# exit the FTP server
ftp.quit()

#sift through all rows in the ftp
#throw away rows that contain true permissions in first 3 slots
#(only if METHOD is true) i.e. '***---------' -> throw away
#trim each row so that only the last 7 (or 10) characters of permissions are visible
#i.e. '---x----wx 1 0 0 0 Mar 28 2022 a5hh76' -> 'x----wx' 
count = 0
trimmedStrings = []
for f in files:
    if(f[0] == '-' and f[1] == '-' and f[2] == '-' and METHOD):
        trimmedStrings.append(f[3:10])
    if(not METHOD):
        trimmedStrings.append(f[:10])
    count += 1

#convert permissions to a binary number
#i.e. 'x----wx' -> '1000011'
permToBytes = []
count = 0
byteLength = 0
permToBytes.append("")
for s in trimmedStrings:
    for i in s:
        if(i == '-'):
            permToBytes[count] += "0"
        else:
            permToBytes[count] += "1"
        byteLength += 1
        if(byteLength >= 7):
            byteLength = 0
            count += 1
            permToBytes.append("")

#convert binary numbers to decimal, and decimal to chars
result = ""
count = 0
for i in permToBytes:
    if(permToBytes[count] != ''):
        result += chr(int(permToBytes[count], 2))
    count += 1

#print hidden message result
print(result)
