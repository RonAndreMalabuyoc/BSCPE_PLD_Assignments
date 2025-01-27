import speech_recognition as sr
import pyautogui
import keyboard
import pyttsx3

engine = pyttsx3.init()
r = sr.Recognizer()
mic = sr.Microphone(0, sample_rate=48000)
sending = False
mouseLeft = False
mouseRight = False
dict = {  
    "forward": {
        "key": "w",
        "held": False
    },
    "left": {
        "key": "a",
        "held": False
    },
    "backward": {
        "key": "s",
        "held": False
    },
    "right": {
        "key": "d",
        "held": False
    },
    "inventory": {
        "key": "e",
        "held": False
    },
    "jump": {
        "key": "space",
        "held": False
    },
    "sprint": {
        "key": "ctrlleft",
        "held": False
    },
    "sneak": {
        "key": "shiftleft",
        "held": False
    },
}

def is_valid_command(command):
    valid_keywords = list(dict.keys()) + [
        "look", "up", "down", "left", "right", 
        "mouse", "wheel", "once", "stop"
    ]
    
    return any(keyword in command.lower() for keyword in valid_keywords)

def parse_command(command):
    print("Command: " + command)
    global mouseLeft
    global mouseRight
    if "look" in command:
        if "up" in command:
            print("Going Up")
            engine.say("Looking up")
            engine.runAndWait()
            pyautogui.move(0, -5, 2)
        if "right" in command:
            print("Going Right")
            engine.say("Looking right")
            engine.runAndWait()
            pyautogui.move(5, 0, 2)
        if "down" in command:
            print("Going Down")
            engine.say("Looking down")
            engine.runAndWait()
            pyautogui.move(0, 5, 2)
        if "left" in command:
            print("Going Left")
            engine.say("Looking left")
            engine.runAndWait()
            pyautogui.move(-5, 0, 2)
        return
    if "mouse" in command:
        if "wheel" in command:
            print("Scrolling Mouse Wheel")
            engine.say("Scrolling hotbar")
            engine.runAndWait()
            pyautogui.scroll(1)
            return
        if "left" in command:
            if "once" in command:
                print("Clicking Left Mouse")
                engine.say("Punch")
                engine.runAndWait()
                pyautogui.mouseDown(button='left')
            elif "stop" in command:
                print("Stopping Left Mouse")
                engine.say("No more violence")
                engine.runAndWait()
                mouseLeft = False
            else:
                print("Holding Left Mouse")
                engine.say("Punching")
                engine.runAndWait()
                mouseLeft = True
                return
        if "right" in command:
            if "once" in command:
                print("Clicking Right Mouse")
                engine.say("Interact")
                engine.runAndWait()
                pyautogui.mouseDown(button='right')
            elif "stop" in command:
                print("Stopping Right Mouse")
                engine.say("No more touching")
                engine.runAndWait()
                mouseRight = False
            else:
                print("Holding Right Mouse")
                engine.say("Interacting")
                engine.runAndWait()
                mouseRight = True
            return
       
    for k in dict.keys():
        if k in command:
            if "once" in command:
                print(f"Going {k.capitalize()}")
                engine.say(f"{k}")
                engine.runAndWait()
                pyautogui.press(dict[k]["key"])
            elif "stop" in command:
                print(f"Stopping {k.capitalize()}")
                engine.say(f"Stopping {k}")
                engine.runAndWait()
                dict[k]["held"] = False
                pyautogui.keyUp(dict[k]["key"])
            else:
                print(f"Holding {k.capitalize()}")
                engine.say(f"Holding {k}")
                engine.runAndWait()
                dict[k]["held"] = True
            return
       
def listen_command():
    global sending
    try:
        sending = True
        with mic as source:
            print("Listening for a command...")
            engine.say("My ears are active")
            engine.runAndWait()
            audio = r.listen(source)
        try:
            command = r.recognize_google(audio)
            
            if is_valid_command(command):
                print("✅ Valid command received!")
                parse_command(command)
            else:
                print("❌ Invalid command. Try again.")
                engine.say("Invalid command. Try again.")
                engine.runAndWait()
                print("Tip: Try commands like 'forward', 'look up', 'mouse left', etc.")
                listen_command()  
        except sr.UnknownValueError:
            print("❌ Could not understand audio. Please try again.")
            engine.say("Could not understand. Try again.")
            engine.runAndWait()
            listen_command()  
        
        sending = False
    
    except Exception as e:
        print(f"An error occurred: {e}")
        sending = False

while True:
    if mouseLeft:
        pyautogui.mouseDown(button='left')
    if mouseRight:
        pyautogui.mouseDown(button='right')
    if not sending:
        listen_command()
    if keyboard.is_pressed('f10'):
        exit()
    for k in dict.keys():
        if dict[k]["held"]:
            pyautogui.keyDown(dict[k]["key"])

        