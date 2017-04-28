#Program asks for user input to determine color to shine.

import time, sys
import RPi.GPIO as GPIO

redPin = 11   #Set to appropriate GPIO
greenPin = 13 #Should be set in the 
bluePin = 15  #GPIO.BOARD format

def blink(pin):
    GPIO.setmode(GPIO.BOARD)
    
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.HIGH)
    
def turnOff(pin):
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)
    
def redOn():
    blink(redPin)

def redOff():
    turnOff(redPin)

def greenOn():
    blink(greenPin)

def greenOff():
    turnOff(greenPin)

def blueOn():
    blink(bluePin)

def blueOff():
    turnOff(bluePin)

def yellowOn():
    blink(redPin)
    blink(greenPin)

def yellowOff():
    turnOff(redPin)
    turnOff(greenPin)

def cyanOn():
    blink(greenPin)
    blink(bluePin)

def cyanOff():
    turnOff(greenPin)
    turnOff(bluePin)

def magentaOn():
    blink(redPin)
    blink(bluePin)

def magentaOff():
    turnOff(redPin)
    turnOff(bluePin)

def whiteOn():
    blink(redPin)
    blink(greenPin)
    blink(bluePin)

def whiteOff():
    turnOff(redPin)
    turnOff(greenPin)
    turnOff(bluePin)


def main():
    while True:
        cmd = raw_input("-->")


        if cmd == "red off":
            redOn()
        elif cmd == "red on":
            redOff()
        elif cmd == "green off":
            greenOn()
        elif cmd == "green on":
            greenOff()
        elif cmd == "blue off":
            blueOn()
        elif cmd == "blue on":
            blueOff()
        elif cmd == "yellow off":
            yellowOn()
        elif cmd == "yellow on":
            yellowOff()
        elif cmd == "cyan off":
            cyanOn()
        elif cmd == "cyan on":
            cyanOff()
        elif cmd == "magenta off":
            magentaOn()
        elif cmd == "magenta on":
            magentaOff()
        elif cmd == "white off":
            whiteOn()
        elif cmd == "white on":
            whiteOff()
        else:
            print("Not a valid command")
        
        
    return
    

