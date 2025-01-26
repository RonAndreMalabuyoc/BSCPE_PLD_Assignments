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

def is_valid_command(command):
    """
    Check if the command is valid by verifying it contains recognizable keywords.
    
    Valid commands include:
    - Movement commands (forward, backward, left, right)
    - Look commands (look up, look down, look left, look right)
    - Mouse commands (mouse left, mouse right, mouse wheel)
    - Action commands (jump, sprint, sneak, inventory)
    - Modifiers like 'once' or 'stop'
    """
    valid_keywords = list(dict.keys()) + [
        "look", "up", "down", "left", "right", 
        "mouse", "wheel", "once", "stop"
    ]
    
    # Check if any valid keyword is in the command
    return any(keyword in command.lower() for keyword in valid_keywords)

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
            print("Listening for a command...")
            audio = r.listen(source)
        
        # Recognize the speech
        try:
            command = r.recognize_google(audio)
            
            # Validate the command
            if is_valid_command(command):
                print("✅ Valid command received!")
                parse_command(command)
            else:
                print("❌ Invalid command. Please try again.")
                print("Tip: Try commands like 'forward', 'look up', 'mouse left', etc.")
                listen_command()  # Recursively call to get a valid command
        
        except sr.UnknownValueError:
            print("❌ Could not understand audio. Please try again.")
            listen_command()  # Recursively call to get a valid command
        
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