#!/usr/bin/python

# IMPORTS
from time import sleep
import os

from xbox360controller import Xbox360Controller

import RPi.GPIO as GPIO
from gpiozero import AngularServo
from gpiozero import Device
from gpiozero.pins.pigpio import PiGPIOFactory

Device.pin_factory = PiGPIOFactory('127.0.0.1')

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

DIR_PIN = 20  # pin per la direzione
STEP_PIN = 21  # pin per lo step
STEP_PER_REVOLUTION = 200  # 360 / 1.8 -> 1.8 gradi per step.
STEP_DELAY = .0005  # 1/200 -> più basso = più veloce

MOT_SPALLA_PIN = 5
MOT_GOMITO_PIN = 6
MOT_POLSO_PIN = 13
MOT_MANO_PIN = 19

# MOTORE STEP - SETUP
GPIO.setup(DIR_PIN, GPIO.OUT)
GPIO.setup(STEP_PIN, GPIO.OUT)
GPIO.output(DIR_PIN, GPIO.HIGH)

# SERVO MOTORI - SETUP
GPIO.setup(MOT_SPALLA_PIN, GPIO.OUT)
GPIO.setup(MOT_GOMITO_PIN, GPIO.OUT)
GPIO.setup(MOT_POLSO_PIN, GPIO.OUT)
GPIO.setup(MOT_MANO_PIN, GPIO.OUT)

ServoSpallaAngle = 20
ServoGomitoAngle = 170
ServoPolsoAngle = 90
ServoManoAngle = 90

ControllerEnabled = False
LoopMenuController = False
LoopMenuConsole = False
IndexMenu = 1
Menu = 1

def SpostaServo(ServoMotore, ServoAngle, Text, angle = -1):
    if angle == -1:
        angle = int(input(Text))

    step = angle - ServoAngle
    if step < 0: step *= -1
    for i in range(step):
        if (angle > ServoAngle):
            ServoAngle += 1
            ServoMotore.angle = ServoAngle
            sleep(.01)
        elif (angle < ServoAngle):
            ServoAngle -= 1
            ServoMotore.angle = ServoAngle
            sleep(.01)

    return ServoAngle

ServoSpalla = AngularServo(MOT_SPALLA_PIN, min_angle=0, max_angle=180, min_pulse_width=0.0005, max_pulse_width=0.0025)
ServoSpalla.angle = 90
SpostaServo(ServoSpalla, 90, '', ServoSpallaAngle)
ServoGomito = AngularServo(MOT_GOMITO_PIN, min_angle=0, max_angle=180, min_pulse_width=0.0005, max_pulse_width=0.0025)
ServoGomito.angle = 90
SpostaServo(ServoGomito, 90, '', ServoGomitoAngle)
ServoPolso = AngularServo(MOT_POLSO_PIN, min_angle=0, max_angle=180, min_pulse_width=0.0005, max_pulse_width=0.0025)
ServoPolso.angle = 90
SpostaServo(ServoPolso, 90, '', ServoPolsoAngle)
ServoMano = AngularServo(MOT_MANO_PIN, min_angle=0, max_angle=180, min_pulse_width=0.0005, max_pulse_width=0.0025)
ServoMano.angle = 90
SpostaServo(ServoMano, 90, '', ServoManoAngle)

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

def on_button_pressed(button):
    global ControllerEnabled
    global IndexMenu
    global Menu

    if Menu == 1:
        if IndexMenu == 1:
            Menu = 2
            MenuController()
        elif IndexMenu == 2:
            ControllerEnabled = not ControllerEnabled
            StampaMenu()
    elif Menu == 2:
        if IndexMenu == 5:
            Menu = 1
            IndexMenu = 1
            MenuController()

def on_axis_moved(axis):
    global IndexMenu
    
    global ServoSpallaAngle
    global ServoGomitoAngle
    global ServoPolsoAngle
    global ServoManoAngle

    global ServoSpalla
    global ServoGomito
    global ServoPolso
    global ServoMano

    if axis.y == 1:
        if IndexMenu > 1:
            IndexMenu -= 1
            MenuController()
    elif axis.y == -1:
        if (Menu == 1 and IndexMenu < 2) or (Menu == 2 and IndexMenu < 5):
            IndexMenu += 1
            MenuController()
    if axis.x == 1:
        if Menu == 2:
            if IndexMenu == 1 and ServoSpallaAngle < 180:
                ServoSpallaAngle = SpostaServo(ServoSpalla, ServoSpallaAngle, '', (ServoSpallaAngle + 5))
                MenuController()
            elif IndexMenu == 2 and ServoGomitoAngle < 180:
                ServoGomitoAngle = SpostaServo(ServoGomito, ServoGomitoAngle, '', ServoGomitoAngle + 5)
                MenuController()
            elif IndexMenu == 3 and ServoPolsoAngle < 180:
                ServoPolsoAngle = SpostaServo(ServoPolso, ServoPolsoAngle, '', ServoPolsoAngle + 5)
                MenuController()
            elif IndexMenu == 4 and ServoManoAngle < 180:
                ServoManoAngle = SpostaServo(ServoMano, ServoManoAngle, '', ServoManoAngle + 5)
                MenuController()
    elif axis.x == -1:
        if Menu == 2:
            if IndexMenu == 1 and ServoSpallaAngle >= 5:
                ServoSpallaAngle = SpostaServo(ServoSpalla, ServoSpallaAngle, '', (ServoSpallaAngle - 5))
                MenuController()
            elif IndexMenu == 2 and ServoGomitoAngle >= 5:
                ServoGomitoAngle = SpostaServo(ServoGomito, ServoGomitoAngle, '', ServoGomitoAngle - 5)
                MenuController()
            elif IndexMenu == 3 and ServoPolsoAngle >= 5:
                ServoPolsoAngle = SpostaServo(ServoPolso, ServoPolsoAngle, '', ServoPolsoAngle - 5)
                MenuController()
            elif IndexMenu == 4 and ServoManoAngle >= 5:
                ServoManoAngle = SpostaServo(ServoMano, ServoManoAngle, '', ServoManoAngle - 5)
                MenuController()

def LoadingBar(Numero):
    bar1 = int(Numero / 180 * 36)*'='
    bar2 = (36 - int(Numero / 180 * 36))*' '
    return '[' + bar1 + bar2 + ']'

def MenuController():
    global ControllerEnabled
    global IndexMenu
    global Menu
    global LoopMenuController

    if LoopMenuController: LoopMenuController = False

    with Xbox360Controller(0, axis_threshold=0.2) as controller:
        controller.button_a.when_pressed = on_button_pressed
        controller.hat.when_moved = on_axis_moved

        cls()
        if Menu == 1:
            print('Programma per la gestione del robot.')
            print('Opzioni disponibili:')
            print(('->' if IndexMenu == 1 else '') + 'Muovi il braccio.')
            print(('->' if IndexMenu == 2 else '') + 'Disabilita il controller.')
        elif Menu == 2:
            print('Controllando il braccio...')
            
            print(('->' if IndexMenu == 1 else '') + 'Spalla' + ('\t' if IndexMenu == 1 else '\t\t') + '[' + '{:03}'.format(ServoSpallaAngle) + ']\t' + LoadingBar(ServoSpallaAngle))
            print(('->' if IndexMenu == 2 else '') + 'Gomito' + ('\t' if IndexMenu == 2 else '\t\t') + '[' + '{:03}'.format(ServoGomitoAngle) + ']\t' + LoadingBar(ServoGomitoAngle))
            print(('->' if IndexMenu == 3 else '') + 'Polso\t\t[' + '{:03}'.format(ServoPolsoAngle) + ']\t' + LoadingBar(ServoPolsoAngle))
            print(('->' if IndexMenu == 4 else '') + 'Mano\t\t[' + '{:03}'.format(ServoManoAngle) + ']\t' + LoadingBar(ServoManoAngle))
            print(('->' if IndexMenu == 5 else '') + 'Torna indietro.')
        else:
            Menu = 1
            MenuController()

        LoopMenuController = True
        while LoopMenuController:
            sleep(.01)

def MenuConsole():
    global ControllerEnabled
    global LoopMenuConsole
    global IndexMenu
    global Menu

    global ServoSpallaAngle
    global ServoGomitoAngle
    global ServoPolsoAngle
    global ServoManoAngle

    global ServoSpalla
    global ServoGomito
    global ServoPolso
    global ServoMano

    LoopMenuConsole = True
    while LoopMenuConsole:
        cls()

        if Menu == 1:
            print('Programma per la gestione del robot.')
            print('Opzioni disponibili:')
            print('1. Muovi il braccio.')
            print('2. Abilita il controller.')
            print('3. Per chiudure il programma.')
        elif Menu == 2:
            print('Controllando il braccio...')
            print('1. Spalla\t[' + '{:03}'.format(ServoSpallaAngle) + ']\t' + LoadingBar(ServoSpallaAngle))
            print('2. Gomito\t[' + '{:03}'.format(ServoGomitoAngle) + ']\t' + LoadingBar(ServoGomitoAngle))
            print('3. Polso\t[' + '{:03}'.format(ServoPolsoAngle) + ']\t' + LoadingBar(ServoPolsoAngle))
            print('4. Mano\t\t[' + '{:03}'.format(ServoManoAngle) + ']\t' + LoadingBar(ServoManoAngle))
            print('5. Torna indietro.')
        else:
            Menu = 1
            MenuConsole()

        SceltaMenu = input('Seleziona un\'opzione: ')
        cls()

        if Menu == 1:
            if SceltaMenu == '1':
                Menu = 2
                if LoopMenuConsole: LoopMenuConsole = False
                MenuConsole()
            elif SceltaMenu == '2':
                IndexMenu = 1
                ControllerEnabled = not ControllerEnabled
                StampaMenu()
            elif SceltaMenu == '3':
                print('Sempre fiero di servirvi.')
                sleep(1)
                if LoopMenuConsole: LoopMenuConsole = False
            else:
                print('Opzione fuori menu.')
                input('Premere invio per tornare indietro.')
        if Menu == 2:
            if SceltaMenu == '1':
                print('Controllando la spalla...')
                ServoSpallaAngle = SpostaServo(ServoSpalla, ServoSpallaAngle, 'Inserire l\'angolo per la spalla: ')
            elif SceltaMenu == '2':
                print('Controllando il gomito...')
                ServoGomitoAngle = SpostaServo(ServoGomito, ServoGomitoAngle, 'Inserire l\'angolo per il gomito: ')
            elif SceltaMenu == '3':
                print('Controllando il polso...')
                ServoPolsoAngle = SpostaServo(ServoPolso, ServoPolsoAngle, 'Inserire l\'angolo per il polso: ')
            elif SceltaMenu == '4':
                print('Controllando la mano...')
                ServoManoAngle = SpostaServo(ServoMano, ServoManoAngle, 'Inserire l\'angolo per la mano: ')
            elif SceltaMenu == '5':
                Menu = 1
                if LoopMenuConsole: LoopMenuConsole = False
                MenuConsole()
                


def StampaMenu():
    global ControllerEnabled
    global LoopMenuConsole
    global LoopMenuController

    if LoopMenuConsole: LoopMenuConsole = False
    if LoopMenuController: LoopMenuController = False

    if ControllerEnabled:
        MenuController()
    else:
        MenuConsole()

if __name__ == "__main__":
    try:
        StampaMenu()

    except KeyboardInterrupt:
        cls()
        print("Keyboard interrupt")

    except Exception as e:
        print(e) 

    finally:
        GPIO.cleanup() # cleanup all GPIO 