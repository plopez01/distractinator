import pyttsx3
import time
import random
import win32gui
import win32con  

# Init TTS
engine = pyttsx3.init()
engine.setProperty('rate', 180)

# Load brain
agressivelvl = 0

banid = 0

Threats = ["dontdistractme.py", "administrador de tareas"]

phrases = []

banresponses = {
    "youtube": [],
    "reddit": [],
    "twitter": [],
    "discord": [],
    "steam": [],
    "dontdistractme": [],
    "administrador de tareas": []
}

bannedThings = list(banresponses.keys())

brain = open("brain.txt", "r")
for memory in brain:
    phrases.append(memory.split('\n')[0])
brain.close();

notWorkingFile = open("notworking.txt", "r")
for memory in notWorkingFile:
    if("**" in memory):
        banid += 1
        continue
    if("#" in memory):
        continue
    banresponses[bannedThings[banid]].append(memory.split('\n')[0])
notWorkingFile.close();


# Introduction
engine.say(phrases[0])
engine.runAndWait()

def isWorking():
    global agressivelvl
    mainWindow = win32gui.GetWindowText(win32gui.GetForegroundWindow()).lower()
    #print(mainWindow)
    for ban in bannedThings:
        if(ban in mainWindow):
            agressivelvl += 1
            return 1, ban
    if(agressivelvl > 0):
        agressivelvl -= 1
    return 0, mainWindow

# Main loop
while True:
    print(agressivelvl)
    time.sleep(random.uniform(60-agressivelvl*15, 120-agressivelvl*15))
    
    working, mainWindow = isWorking()
    
    if(working == 0):
        engine.say(phrases[int(random.uniform(1, len(phrases)))])
        engine.runAndWait()
    elif(working == 1):
        if(agressivelvl >= 3):
            agressivelvl = 0
            engine.say("A TOMAR POR CULO")
            engine.runAndWait()
            win32gui.PostMessage(win32gui.GetForegroundWindow(),win32con.WM_CLOSE,0,0)
        else: 
            engine.say(banresponses[mainWindow][int(random.uniform(0, len(banresponses[mainWindow])))])
            engine.runAndWait()


    
