import speech_recognition as sr
import pyautogui
import keyboard

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


def parse_command(command):
    print("Command: " + command)

    global mouseLeft
    global mouseRight

    if "look" in command:
        if "up" in command:
            pyautogui.move(0, -5, 2)
        if "right" in command:
            pyautogui.move(5, 0, 2)
        if "down" in command:
            pyautogui.move(0, 5, 2)
        if "left" in command:
            pyautogui.move(-5, 0, 2)
        return

    if "mouse" in command:
        if "wheel" in command:
            pyautogui.scroll(1)
            return
        if "left" in command:
            if "once" in command:
                pyautogui.mouseDown(button='left')
            elif "stop" in command:
                mouseLeft = False
            else:
                mouseLeft = True
                return
        if "right" in command:
            if "once" in command:
                pyautogui.mouseDown(button='right')
            elif "stop" in command:
                mouseRight = False
            else:
                mouseRight = True
            return
        
    for k in dict.keys():
        if k in command:
            if "once" in command:
                pyautogui.press(dict[k]["key"])
            elif "stop" in command:
                dict[k]["held"] = False
                pyautogui.keyUp(dict[k]["key"])
            else:
                dict[k]["held"] = True
            return
        

def listen_command():
    global sending
    try:
        sending = True
        with mic as source:
            audio = r.listen(source)

        sending = False
        parse_command(r.recognize_google(audio))
    except Exception as e:
        print(e)
        senidng = False


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

    