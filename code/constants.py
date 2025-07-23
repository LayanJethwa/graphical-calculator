RIGHT_ASSOCIATIVE = ['^']
FUNCTIONS = []
OPERANDS = ['x']

PRECEDENCES_LIST = [('^'),('/','*'),('+','-')]
PRECEDENCES = {None:100000}

def precedences_setup():
    for index in range(len(PRECEDENCES_LIST)):
        for operator in PRECEDENCES_LIST[index]:
            PRECEDENCES[operator] = index

XMIN = -15
XMAX = 15
YMIN = -10
YMAX = 10

DEFAULT_FREQUENCY = 300

WIDTH = 480
HEIGHT = 320

SCALEX = WIDTH/(XMAX-XMIN)
SCALEY = HEIGHT/(YMAX-YMIN)

X0 = -(XMIN*SCALEX)
Y0 = HEIGHT + (YMIN*SCALEY)

AXIS_LABEL_LENGTH = 3