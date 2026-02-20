import RPi.GPIO as GPIO
import time

R1 = 2
R2 = 3
R3 = 4
R4 = 5
R5 = 6
R6 = 7
R7 = 8
R8 = 9

rows = [R1,R2,R3,R4,R5,R6,R7,R8]

C1 = 15
C2 = 16
C3 = 17
C4 = 18
C5 = 19

cols = [C1,C2,C3,C4,C5]

DEG = 11
RAD = 12

GPIO.cleanup()

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

for r in rows:
    GPIO.setup(r, GPIO.OUT)
    GPIO.output(r, GPIO.LOW)

for c in cols:
    GPIO.setup(c, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

GPIO.setup(DEG, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(RAD, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def detectRow(row, chars):
    for r in rows:
        GPIO.output(r, GPIO.LOW)
    GPIO.output(row, GPIO.HIGH)
    time.sleep(0.01)

    for c in range(len(cols)):
        if GPIO.input(cols[c]) == GPIO.HIGH:
            print(chars[c])
            time.sleep(0.2)
    GPIO.output(row, GPIO.LOW)

'''
while True:
    detectRow(R1, ["up", "right", "down", "left", "shift"])
    detectRow(R2, ["on", "zoom in", "zoom out", "integral", "x"])
    detectRow(R3, ["fraction", "sqrt", "square", "power", "log"])
    detectRow(R4, ["ln", "pi", "sin", "cos", "tan"])
    detectRow(R5, ["(", ")", "AC", "DEL", "."])
    detectRow(R6, ["+", "-", "*", "/", "EXE"])
    detectRow(R7, [1,2,3,4,5])
    detectRow(R8, [6,7,8,9,0])
    if GPIO.input(DEG) == GPIO.LOW:
        print("degrees")
    elif GPIO.input(RAD) == GPIO.LOW:
        print("radians")
'''
while True:
    for r in rows:
        GPIO.output(r, GPIO.LOW)

    for r in rows:
        GPIO.output(r, GPIO.HIGH)
        time.sleep(0.01)
        for c in cols:
            if GPIO.input(c) == GPIO.HIGH:
                print(r, c)
                time.sleep(0.2)
        GPIO.output(r, GPIO.LOW)