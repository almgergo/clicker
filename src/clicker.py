from pynput import mouse
from pynput import keyboard

import time
import threading
import random

from click import Click

clicks = []

previous_click = None
last_click = None

paused = False
stop = False

mouse_controller = mouse.Controller()

long_sleep_secs = 5


# A thread that does the clicking
class ClickingThread(threading.Thread):
    def __init__(self, i):
        threading.Thread.__init__(self)
        self.h = i

    def run(self):
        do_clicks()


# on click.py we add the position of the click.py to our click.py list
def on_click(x, y, button, pressed):
    if pressed:
        global last_click, previous_click

        last_click = time.time()
        if previous_click is None:
            previous_click = last_click
            clicks.append(Click(x, y, 0.8))
        else:
            clicks.append(Click(x, y, last_click - previous_click))

        previous_click = last_click


# if backspace is pressed, stop the recording of clicks and start repeating them
# if insert is pressed, pause / resume clicking
# if home is pressed, stop the program
def on_press(key):
    global paused, stop

    if key == keyboard.Key.backspace:
        mouse_listener.stop()
        clicking_thread = ClickingThread(1)
        clicking_thread.start()
    elif key == keyboard.Key.insert:
        paused = not paused
        print("pause toggle")
    elif key == keyboard.Key.home:
        stop = True
        return False
        print("STOP")


# preforms a mouse button press and release with a random delay between
def click_mouse(controller):
    # press mouse button
    controller.press(mouse.Button.left)

    # sleep a random time between press and release
    time.sleep(0.08 + (random.random() - 0.5) / 50)

    # release mouse button
    controller.release(mouse.Button.left)


# moves the mouse to the give position
def move_mouse(controller, click):
    # move the cursor to the position
    controller.position = (click.x, click.y)
    time.sleep(random.random() / 40 + 0.01)


# repeat the clicks until 'stop' is called
def do_clicks():
    global paused, stop, clicks, mouse_controller
    i = 0

    # if no clicks are recorded, there is no point in repeating them :)
    if len(clicks) == 0:
        stop = True

    while not stop:
        if paused:
            time.sleep(1)
        else:
            time.sleep(clicks[i].delay + (random.random() - 0.5) / 5)

            move_mouse(mouse_controller, clicks[i])

            click_mouse(mouse_controller)

            i += 1
            if i >= len(clicks):
                i %= len(clicks)
                # if we've completed a cycle, sleep a longer amount
                long_sleep = long_sleep_secs + random.random() * 3
                print("sleeping for: " + str(long_sleep))
                time.sleep(long_sleep)


mouse_listener = mouse.Listener(on_click=on_click)
mouse_listener.start()

with keyboard.Listener(on_press=on_press) as keyboard_listener:
    keyboard_listener.join()
