from gpiozero import Motor, LED
from time import sleep
import evdev
from evdev import InputDevice, categorize, ecodes

led = LED(17)

d = InputDevice('/dev/input/event0')
for event in d.read_loop():
    if event.type == ecodes.EV_KEY:
        print(event)
        if event.type == 1:
            led.on()
            sleep(1)
            led.off()
        sleep(1)
