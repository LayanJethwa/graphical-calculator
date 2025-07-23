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

BLACK = (0,0,0)
WHITE = (255,255,255)
COLOURS = [(255,0,0),(0,255,0),(0,0,255),(255,0,255),(0,255,255),(128,0,128),(255,165,0)]

EDIT_TEXT = ['...','|']

IDENTICAL_KEYS = [ord(i) for i in ['-']]
SHIFT_KEYS = {ord(i[0]):i[1] for i in [('=','+'),('9','('),('0',')'),('8','x')]}
PLACEHOLDER_KEYS = {'q':'²', 'w':'³'}