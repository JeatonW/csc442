from pynput.keyboard import Key, Controller
from time import sleep
keyboard = Controller()

#input
passwordArray = ['T', 'h', 'i', 's', ' ', 'i', 's', ' ', 'a', 'n', ' ', 'i', 'n', 'c', 'o', 'r', 'r', 'e', 'c', 't', ' ', 'p', 'a', 's', 's', 'w', 'o', 'r', 'd', '.', 'Th', 'hi', 'is', 's ', ' i', 'is', 's ', ' a', 'an', 'n ', ' i', 'in', 'nc', 'co', 'or', 'rr', 're', 'ec', 'ct', 't ', ' p', 'pa', 'as', 'ss', 'sw', 'wo', 'or', 'rd', 'd.']
timings = ['0.73', '0.84', '0.15', '0.57', '0.97', '0.65', '0.85', '0.23', '0.18', '0.96', '0.21', '0.66', '0.98', '0.44', '0.36', '0.39', '0.77', '0.11', '0.20', '0.86', '0.72', '0.13', '0.69', '0.40', '0.97', '0.19', '0.27', '0.76', '0.73', '0.11', '0.77', '0.34', '0.72', '0.32', '0.77', '0.82', '0.57', '0.27', '0.30', '0.68', '0.77', '0.24', '0.70', '0.81', '0.64', '0.52', '0.25', '0.36', '0.59', '0.89', '0.90', '0.27', '0.80', '0.98', '0.31', '0.66', '0.11', '0.42', '0.97']

#convert password array to a string
password = ""
i = 0
for c in passwordArray:
    password += c
    i += 1
    if(i >= len(passwordArray) // 2 + 1):
        break

#split timings array into two arrays; one for KHTs and another for KITs
split = int(len(timings)/2)
keypress = timings[0:split+1]
keyinterval = timings[split+1:]

#print all information
print("Features = {}".format(password))
print("Timings = {}".format(timings))
print("KHTs = {}".format(keypress))
print("KITs = {}".format(keyinterval))

#give enough time to bring command window into focus
sleep(5)

#evoke beginning using enter press
keyboard.press(Key.enter)
keyboard.release(Key.enter)

#give enough time for tk window to appear
sleep(5)

#type out password using KHTs and KITs
i = 0
length = len(password)
while(i < length):
    keyboard.press(password[i])
    sleep(float(keypress[i]))
    keyboard.release(password[i])
    if(i != length-1):
        sleep(float(keyinterval[i]))
    else:
        keyboard.press(Key.enter)
        keyboard.release(Key.enter)
    i += 1

#prompt when finished
print("\nFinished.")
