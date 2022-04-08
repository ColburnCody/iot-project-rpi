from gpiozero import Motor, LED
from time import sleep
from signal import pause
import evdev
from evdev import InputDevice, categorize, ecodes
import constant
import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("./serviceAccount.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

doc_treats = db.collection(constant.COLLECTION_NAME).document(constant.DOCUMENT_TREATS)
led = LED(17)
motor = Motor(4, 14)
d = InputDevice('/dev/input/event0')


def on_treat_snapshot(doc_snapshot, change, read_time):
    for doc in doc_snapshot:
        response = doc.to_dict()["approval"]
        if response == "approved":
            led.off()
            print("Treat request approved!")
            doc_treats.update({u'approval': ""})
            dispense_treat()
        elif response == "denied":
            led.off()
            print("Treat request denied!")
            doc_treats.update({u'approval': ""})

def dispense_treat():
    print("Dispensing treat")
    motor.forward()
    sleep(5)
    motor.backward()
    sleep(5)
    print("Enjoy your treat, Remi!")
    

doc_treat_watch = doc_treats.on_snapshot(on_treat_snapshot)



for event in d.read_loop():
    if event.type == ecodes.EV_KEY:
        if event.type == 1:
            print("Treat requested")
            led.on()
            doc_treats.update({u'request': True})
        sleep(1)
