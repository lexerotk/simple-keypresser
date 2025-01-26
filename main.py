import time
import keyboard as kb
from colorama import Fore, Back, Style
import argparse
import threading

# VARIABLES

parser = argparse.ArgumentParser(description="You can use optional args.")
key = ""
keyPressDelay = ""
startStopKey = ""
isStopped = threading.Event()
keylist = [
    # LETTER KEYS
    "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m",
    "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z",

    # NUMBER KEYS
    "0", "1", "2", "3", "4", "5", "6", "7", "8", "9",

    # FUNCTION KEYS
    "f1", "f2", "f3", "f4", "f5", "f6", "f7", "f8", "f9", "f10", "f11", "f12",

    # NUMPAD KEYS
    "num_0", "num_1", "num_2", "num_3", "num_4", "num_5", "num_6", "num_7", "num_8", "num_9",
    "num_lock", "num_divide", "num_multiply", "num_subtract", "num_add",

    # ARROW KEYS
    "up", "down", "left", "right",

    # SPECIAL KEYS
    "enter", "esc", "backspace", "tab", "caps_lock", "shift", "ctrl", "alt", "alt_gr",
    "space", "print_screen", "scroll_lock", "pause", "insert", "delete", "home", "end",
    "page_up", "page_down",

    # PUNCTUATION MARKS
    "`", "-", "=", "[", "]", "\\", ";", "'", ",", ".", "/",

    # SHIFT CHARACTERS
    "~", "!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "_", "+", "{", "}",
    "|", ":", "\"", "<", ">", "?",

    # OS KEYS
    "win", "menu"
]

# ARGS

parser.add_argument("--keylist", help="Shows a list of keys you can use.", dest="show_keylist", action="store_true")
args = parser.parse_args()

# SCRIPT

def printKeyList():
    keylist_r = ""
    print(Fore.YELLOW + "Here's the all keys you can use" + Style.RESET_ALL)
    for i in keylist:
        keylist_r += i + "    "
    print(keylist_r)
    
def setKey():
    keyAvailable = False
    global key
    key = str(input("Please specify the key you want (US LAYOUT): "))
    for i in keylist:
        if key.lower() == i:
            keyAvailable = True
    if keyAvailable:
        setDelay()
    else:
        print(Fore.RED + "The key is invalid. Please check the keylist." + Style.RESET_ALL)
        setKey()
            
def setDelay():
    global keyPressDelay
    try:
        keyPressDelay = int(input("Please specify the delay between key presses (miliseconds): "))
    except:
        print(Fore.RED + "You can only specify an integer value." + Style.RESET_ALL)
    if keyPressDelay < 1:
        print(Fore.RED + "The min delay you can set is 1ms." + Style.RESET_ALL)
        setDelay()
    else:
        setStartStop()

def setStartStop(): 
    keyAvailable = False
    global startStopKey
    startStopKey = str(input("Please specify a key for stopping the process (US LAYOUT): "))
    for i in keylist:
        if startStopKey.lower() == i:
            keyAvailable = True
    if keyAvailable:
        startKeyPress()
    else:
        print(Fore.RED + "The key is invalid. Please check the keylist." + Style.RESET_ALL)
        setKey()

def startKeyPress():
    print("Starting in 3 seconds...")
    time.sleep(1)
    print("Starting in 2 seconds...")
    time.sleep(1)
    print("Starting in 1 seconds...")
    time.sleep(1)
    press_thread = threading.Thread(target=startPressing)
    monitor_thread = threading.Thread(target=startStop)
    press_thread.start()  
    monitor_thread.start()  
    press_thread.join()  
    monitor_thread.join()  

def startPressing():
    global key
    global keyPressDelay
    while not isStopped.is_set():
        kb.send(key)
        time.sleep(keyPressDelay / 1000)
        
def startStop():
    time.sleep(0.5)
    is_pressed = False  
    while True:
        if kb.is_pressed(startStopKey):
            if not is_pressed:  
                print(Fore.RED + f"{startStopKey} is pressed. Process has been paused." + Style.RESET_ALL)
                isStopped.set()  
                break
        else:
            is_pressed = False  
        time.sleep(0.05)  
    time.sleep(0.5)
    is_pressed = False
    while True:
        if kb.is_pressed(startStopKey):
            is_pressed = False
            restartProcess()
            break

def restartProcess():
    print(Fore.GREEN + "Continuing..." + Style.RESET_ALL)
    time.sleep(0.7)
    isStopped.clear()  
    press_thread = threading.Thread(target=startPressing)  
    press_thread.start()
    monitor_thread = threading.Thread(target=startStop)
    monitor_thread.start()
    press_thread.join()  
    monitor_thread.join()

if args.show_keylist:
    printKeyList()
else:
    print("------------------------------------------")
    print("| " + Fore.YELLOW + "Simple Key Presser Script v0.1 By @lexerotk" + Style.RESET_ALL)
    print("| " + Fore.RED + "THIS IS AN ALPHA VERSION. MIGHT BE UNSTABLE AND CAUSE ISSUES." + Style.RESET_ALL)
    print("| " + Fore.YELLOW + "Check source code at my Github profile!" + Style.RESET_ALL)
    print("------------------------------------------")
    setKey()