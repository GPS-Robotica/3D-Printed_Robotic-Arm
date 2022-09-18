#!/usr/bin/python

# IMPORTS
import RPi.GPIO as GPIO
import time
from piservo import Servo
#from piservo import Drive

# VARIABILI
# MOTORE STEP - NEMA 17
DIR = 20 # pin per la direzione
STEP = 21 # pin per lo step
SPR = 200 # 360 / 1.8 -> 1.8 gradi per step.
step_delay = .005 #1/200

# SERVO MOTORI - 2 x MG996R
Mot_Spalla1 = 16
Mot_Spalla2 = 19

# SERVO MOTORI - 4 x SG90
Mot_Gomito1 = 5
Mot_Gomito2 = 6
Mot_Polso2 = 24
Mot_Mano = 26

GPIO.setmode(GPIO.BCM) # BOH
# MOTORE STEP - SETUP
GPIO.setup(DIR, GPIO.OUT) # Imposta il pin DIR in output
GPIO.setup(STEP, GPIO.OUT) # Imposta il pin STEP in output
GPIO.output(DIR, GPIO.HIGH) # Assegna il valore true al pin di uscita DIR.

# SERVO MOTORI - SETUP
GPIO.setup(Mot_Spalla1, GPIO.OUT)
GPIO.setup(Mot_Spalla2, GPIO.OUT)
GPIO.setup(Mot_Gomito1, GPIO.OUT)
GPIO.setup(Mot_Gomito2, GPIO.OUT)
GPIO.setup(Mot_Polso2, GPIO.OUT)
GPIO.setup(Mot_Mano, GPIO.OUT)



# MAIN CODE
def main():
    print('Hello world!')
    for x in range(SPR):
        GPIO.output(STEP, GPIO.HIGH)
        
# funzione per stepper

def demoStepper():
    GPIO.output(DIR, GPIO.HIGH)
    for x in range(SPR/2):
        GPIO.output(STEP, GPIO.HIGH)
        sleep(step_delay)
        GPIO.output(STEP, GPIO.LOW)
        sleep(step_delay)
    GPIO.output(DIR, GPIO.LOW)
    for x in range(SPR/2):
        GPIO.output(STEP, GPIO.HIGH)
        sleep(step_delay)
        GPIO.output(STEP, GPIO.LOW)
        sleep(step_delay)
        
# funzione per spalla

def demoServoSpalla():
    spalla2 = Servo(Mot_Spalla2)
    spalla1 = Servo(Mot_Spalla1)
    
    spalla2.write(-30)
    spalla1.write(30)
    time.sleep(3)
    spalla2.write(30)
    spalla1.write(-30)
    time.sleep(3)
    spalla2.stop()
    spalla1.stop()


if __name__ == "__main__":
    main()