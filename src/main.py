import time
from machine import Pin

import mount_sd
from managed_mic import record_from_mic_until

global button_pressed
button_pressed=False

button = Pin(16, Pin.IN, Pin.PULL_DOWN)

def button_handler(pin):
    global button_pressed
    if not button_pressed:
        button_pressed=True
button.irq(trigger=Pin.IRQ_RISING, handler=button_handler)

event_callback = lambda :button_pressed

recording_count = 0

with mount_sd.sd_mounted():
    while True:
        print("Press to start")
        # Waiting for button
        button_pressed = False
        while not button_pressed:
            time.sleep(0.01)
        # wait for release
        while button.value():
            time.sleep(0.01)
        button_pressed = False

        record_from_mic_until(f"/sd/recording{recording_count}.wav",
                            event_callback)
        # wait for release
        while button.value():
            time.sleep(0.01)
        print("Cycle complete")
        recording_count += 1
