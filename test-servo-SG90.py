#!/usr/bin/python

# IMPORTS
import RPi.GPIO as GPIO
from gpiozero import AngularServo
from time import sleep
from gpiozero import Device
from gpiozero.pins.pigpio import PiGPIOFactory

Device.pin_factory = PiGPIOFactory('127.0.0.1')

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
# VARIABILI
# SERVO MOTORI - 4 x SG90
Mot_Gomito1 = 5

# SERVO MOTORI - SETUP
GPIO.setup(Mot_Gomito1, GPIO.OUT)

# MAIN CODE
def main():
    print('Test servo motore SG90.')
    demoServo()

# funzione per spalla
def demoServo():
    servo = AngularServo(18, min_angle=0, max_angle=180, min_pulse_width=0.0006, max_pulse_width=0.0023)
    servo.angle = 0
    sleep(2)
    servo.angle = 90
    sleep(2)
    servo.angle = 180
    sleep(2)

    for i in range(180):
        servo.angle = i
        sleep(0.01)

    for i in range(180):
        servo.angle = 180 - i
        sleep(0.01)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt: # If CTRL+C is pressed, exit cleanly:
        print("Keyboard interrupt")

    except Exception as e:
        print(e)

    finally:
        print("clean up")
        GPIO.cleanup() # cleanup all GPIO
