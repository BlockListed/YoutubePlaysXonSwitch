import pytchat
import time
from multiprocessing import Process, Queue
from switchcon import Switchc
import json

# Getting variables from json file with the variables
with open("vars.json", "r") as f:
    data = json.load(f.read)

# Setting up connection to switch
s = Switchc(data["ip"])

# Defining funtions for use with dict
def up():
    print("Up")
    s.sendLstick("up")
def left():
    print("left")
    s.sendLstick("left")
def down():
    print("down")
    s.sendLstick("down")
def right():
    print("right")
    s.sendLstick("right")
def a():
    print("a")
    s.sendCommand("click A")
def b():
    print("b")
    s.sendCommand("click B")
def y():
    print("y")
    s.sendCommand("click Y")
def x():
    print("x")
    s.sendCommand("click X")
def plus():
    print("+")
    s.sendCommand("click PLUS")
def l():
    print("l")
    s.sendCommand("click L")

# Setting up dict for case statement which is more efficient
commanddict = {"!up": up, "!left": left, "!down": down, "!right": right, "!a": a, "!b": b, "!y": y, "!x": x, "!+": plus, "!l": l}

# Adding list for queing and dict to save when last message was sent
timemessage = {}

# Setting up queue for everything to work
q = Queue()

# Defining function to complete go through command queue
def CmdQueue():
    while True:
            if q.empty() == False:
                command = q.get()
                with open("messages.log", "a") as f:
                    f.write(f"{command} \n")
                commanddict[command]()

            else:
                time.sleep(0.25)

# Starting the CmdQueue as Process so the chat getting shit can do its job.
p = Process(target=CmdQueue)
p.start()

# Getting chat shit
chat = pytchat.create(video_id=data["id"])
while chat.is_alive():
    for c in chat.get().sync_items():
        if commanddict.get(c.message, "nocmd") != "nocmd":
            if timemessage.get(c.author.name, 1) == 1:
                #print(f"New user {c.author.name}")
                #print(f"{c.message} from {c.author.name}. \n")
                q.put(c.message)
                timemessage.update({c.author.name: int(time.time())})

            elif (int(time.time()) - timemessage.get(c.author.name, 1)) < 5:
                print(f"{c.author.name} - Timeout")
            
            elif (int(time.time()) - timemessage.get(c.author.name, 1)) >= 5:
                print(f"{c.author.name} - {c.message}")
                q.put(c.message)
                timemessage.update({c.author.name: int(time.time())})
