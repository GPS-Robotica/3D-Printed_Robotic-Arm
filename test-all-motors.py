#!/usr/bin/python

# IMPORTS
from time import sleep
import RPi.GPIO as GPIO
from gpiozero import AngularServo
from gpiozero import Device
from gpiozero.pins.pigpio import PiGPIOFactory

Device.pin_factory = PiGPIOFactory('127.0.0.1')

# VARIABILI
# MOTORE STEP - NEMA 17
DIR = 20  # pin per la direzione
STEP = 21  # pin per lo step
SPR = 200  # 360 / 1.8 -> 1.8 gradi per step.
StepDelay = .0005  # 1/200 -> più basso = più veloce

# SERVO MOTORI - 1 x MG996R
Mot_Spalla = 5

# SERVO MOTORI - 3 x SG90
Mot_Gomito = 6
Mot_Polso = 13
Mot_Mano = 19

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# MOTORE STEP - SETUP
GPIO.setup(DIR, GPIO.OUT)  # Imposta il pin DIR in output
GPIO.setup(STEP, GPIO.OUT)  # Imposta il pin STEP in output
GPIO.output(DIR, GPIO.HIGH)  # Assegna il valore true al pin di uscita DIR.

# SERVO MOTORI - SETUP
GPIO.setup(Mot_Spalla, GPIO.OUT)
GPIO.setup(Mot_Gomito, GPIO.OUT)
GPIO.setup(Mot_Polso, GPIO.OUT)
GPIO.setup(Mot_Mano, GPIO.OUT)

# MAIN CODE
def main():
    print('Programma per testare i motori.')
    sleep(3)

    print('Test stepper.')
    demoStepper(DIR, STEP, SPR, StepDelay)
    sleep(2)

    print('Test servo Spalla.')
    demoServo(Mot_Spalla, "MG996R")
    sleep(2)

    print('Test servo Gomito.')
    demoServo(Mot_Gomito, "SG90")
    sleep(2)
    
    print('Test servo Polso.')
    demoServo(Mot_Polso, "SG90")
    sleep(2)
    
    print('Test servo Mano.')
    demoServo(Mot_Mano, "SG90")

def demoStepper(directionPin, stepPin, stepPerRevolution, stepDelay):
    GPIO.output(directionPin, GPIO.HIGH)
    for x in range(int(stepPerRevolution)):
        GPIO.output(stepPin, GPIO.HIGH)
        sleep(stepDelay)
        GPIO.output(stepPin, GPIO.LOW)
        sleep(stepDelay)

    sleep(1)
    GPIO.output(directionPin, GPIO.LOW)
    for x in range(int(stepPerRevolution)):
        GPIO.output(stepPin, GPIO.HIGH)
        sleep(stepDelay)
        GPIO.output(stepPin, GPIO.LOW)
        sleep(stepDelay)

def demoServo(servoPin, servoModel):
    if servoModel == "SG90":
        servo = AngularServo(servoPin, min_angle=0, max_angle=180, min_pulse_width=0.0006, max_pulse_width=0.0023)
    elif servoModel == "MG996R":
        servo = AngularServo(servoPin, min_angle=0, max_angle=180, min_pulse_width=0.0005, max_pulse_width=0.0025)
    else:
        return

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
        print("GPIO Cleanup!") 
        GPIO.cleanup() # cleanup all GPIO 
