from collections import defaultdict

RIGHT_ASSOCIATIVE = ['NEG']

PRECEDENCES_LIST = [['NEG'],['/','*'],['+','-']]
PRECEDENCES = {None:100000}

def precedences_setup():
    for index in range(len(PRECEDENCES_LIST)):
        for operator in PRECEDENCES_LIST[index]:
            PRECEDENCES[operator] = index


DEFAULT_FREQUENCY = 300

WIDTH = 480
HEIGHT = 320

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
BLUE = (0,120,215) #talk about accessibility for colours here
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


# for robust mapping between computer and hardware, key.name:what key is treated as
KEY_MAP = {'r': ['EXPONENT','RADICAL'], 'f': 'FRACTION', 's': ['SQRT', 'CBRT'],
           '0': '0', '1': '1', '2': '2', '3': '3', '4': '4', '5': '5', '6': '6', '7': '7', '8': '8', '9': '9', '.': '.',
           '=': '+', '-': '-', '#': '*', '/': '/',
           'x': 'x',
           'left': 'LEFT', 'right': 'RIGHT', 'up': 'UP', 'down': 'DOWN',
           'backspace': 'DEL', 'return': 'EXE', 'left shift': 'SHIFT', 'right shift': 'ANGLE', 'a': ['AC', 'OFF'],
           'n': 'ZOOM_IN', 'm': 'ZOOM_OUT',
           'p': ['PI', 'E'],
           'q': ['SIN', 'CSC'],
           'w': ['COS', 'SEC'],
           'e': ['TAN', 'COT'],
           'l': ['LN', 'LOG10'],
           'k': 'LOG',
           'j': ['SQUARED', 'CUBED'],
           '[': '(', ']': ')'}

KEY_MAP = defaultdict(str, KEY_MAP)


BINARY_OPERATORS = ['RADICAL', 'FRACTION', 'LOG', 'EXPONENT']
UNARY_OPERATORS = ['SQRT', 'CBRT', 'SIN', 'COS', 'TAN', 'CSC', 'SEC', 'COT', 'LN', 'LOG10', 'SQUARED', 'CUBED']
NUMBERS = '0123456789.'
SYMBOLS = "+-*/"
VARIABLES = ['x', 'PI', 'E']
ARROWS = ['LEFT', 'RIGHT', 'UP', 'DOWN']
ZOOM = ['ZOOM_IN', 'ZOOM_OUT']
TRIG = ['SIN', 'COS', 'TAN', 'CSC', 'SEC', 'COT']
BRACKETS = ['(', ')']