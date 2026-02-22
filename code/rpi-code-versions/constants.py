RIGHT_ASSOCIATIVE = ['NEG']

PRECEDENCES_LIST = [['NEG'],['/','*'],['+','-']]
PRECEDENCES = {None:100000}

def precedences_setup():
    for index in range(len(PRECEDENCES_LIST)):
        for operator in PRECEDENCES_LIST[index]:
            PRECEDENCES[operator] = index


DEFAULT_FREQUENCY = 300

WIDTH = 800
HEIGHT = 480

WSCALE = 5/3 #multipliers from 480x320, specifically for hardware scaling - screen bigger than expected
HSCALE = 3/2

XMIN = -15
XMAX = 15
YMIN = -10
YMAX = 10

XDIFF = XMAX-XMIN
YDIFF = YMAX-YMIN

SCALEX = WIDTH/(XDIFF)
SCALEY = HEIGHT/(YDIFF)

X0 = -(XMIN*SCALEX)
Y0 = HEIGHT + (YMIN*SCALEY)

def update_bounds():
    global XDIFF, YDIFF, SCALEX, SCALEY, X0, Y0

    XDIFF = XMAX-XMIN
    YDIFF = YMAX-YMIN

    SCALEX = WIDTH/(XDIFF)
    SCALEY = HEIGHT/(YDIFF)

    X0 = -(XMIN*SCALEX)
    Y0 = HEIGHT + (YMIN*SCALEY)

AXIS_LABEL_LENGTH = 3

ZOOM_SCALE_FACTOR = 2


BLACK = (0,0,0)
WHITE = (255,255,255)
BLUE = (0,120,215)
COLOURS = [(255,20,60), #red
           (255,140,0), #orange
           (34,139,34), #green
           (0,0,255), #blue
           (128,0,128), #purple
           (255,0,255), #magenta
           (160,82,45)] #brown


EDIT_TEXT = ['...','|']


E = 2.718281828459045235360287471352
PI = 3.141592653589793238462643383279

R1 = 2
R2 = 3
R3 = 4
R4 = 5
R5 = 6
R6 = 7
R7 = 8
R8 = 9

ROWS = [R1,R2,R3,R4,R5,R6,R7,R8]

C1 = 15
C2 = 16
C3 = 17
C4 = 18
C5 = 19

COLS = [C1,C2,C3,C4,C5]

KEY_MATRIX = [["UP", "RIGHT", "DOWN", "LEFT", "SHIFT"], #caps is implemented
["deg/rad", "ZOOM_IN", "ZOOM_OUT", "integral", "x"],
["FRACTION", "SQRT", ["²", "³"], ["power(exponent)", "RADICAL"], "log("],
["ln", ["π", "e"], ["sin(", "csc("], ["cos(", "sec("], ["tan(", "cot("]],
["(", ")", ["AC", "OFF"], "DEL", "."],
["+", "-", "*", "/", "EXE"],
['1','2','3','4','5'],
['6','7','8','9','0']]


BINARY_OPERATORS = ['RADICAL', 'FRACTION']
UNARY_OPERATORS = ['SQRT']
NUMBERS = '0123456789.'
SYMBOLS = "+-*/"
VARIABLES = "x"
ARROWS = ['LEFT', 'RIGHT', 'UP', 'DOWN']
ZOOM = ['ZOOM_IN', 'ZOOM_OUT']