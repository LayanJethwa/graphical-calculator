from collections import defaultdict

RIGHT_ASSOCIATIVE = ['^','log'] #most can go (unary neg right-associative?)
OPERANDS = ['x']
OPERATORS = ['+',r"\-",'/','*','^','(',')']
UNARY_FUNCTIONS = ['sin','cos','tan','csc','sec','cot']
BINARY_FUNCTIONS = ['log']

PRECEDENCES_LIST = [['sin','cos','tan'],['^','log'],['/','*'],['+','-']] #can be trimmed to only basic operators
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
BLUE = (0,120,215)
COLOURS = [(255,0,0),(0,255,0),(0,0,255),(255,0,255),(0,255,255),(128,0,128),(255,165,0)]


EDIT_TEXT = ['...','|']


E = 2.718281828459045235360287471352
PI = 3.141592653589793238462643383279


IDENTICAL_KEYS = [ord(i) for i in '-.e'] #all can go
SHIFT_KEYS = {ord(i[0]):i[1] for i in [('=','+'),('9','('),('0',')'),('8','x')]}
PLACEHOLDER_KEYS = {'q':'²', 'w':'³', 'x':'𝑥', '/':'÷', 'p':'π', 'l':'log(', 's':'sin(', 'c':'cos(', 't':'tan(', 'r':'csc(', 'y':'sec(', 'u':'cot('}

KEY_MAP = {'r': ['power(exponent)','RADICAL'], 'f': 'FRACTION', 's': 'SQRT', # for robust mapping between computer and hardware, key.name:what key is treated as
           '0': '0', '1': '1', '2': '2', '3': '3', '4': '4', '5': '5', '6': '6', '7': '7', '8': '8', '9': '9', '.': '.',
           '=': '+', '-': '-', '#': '*', '/': '/',
           'x': 'x',
           'left': 'LEFT', 'right': 'RIGHT', 'up': 'UP', 'down': 'DOWN',
           'backspace': 'DEL', 'return': 'EXE', 'left shift': 'SHIFT', 'a': ['AC', 'OFF'],
           'n': 'ZOOM_IN', 'm': 'ZOOM_OUT'}

KEY_MAP = defaultdict(str, KEY_MAP)


BINARY_OPERATORS = ['RADICAL', 'FRACTION']
UNARY_OPERATORS = ['SQRT']
NUMBERS = '0123456789.'
SYMBOLS = "+-*/"
VARIABLES = "x"
ARROWS = ['LEFT', 'RIGHT', 'UP', 'DOWN']
ZOOM = ['ZOOM_IN', 'ZOOM_OUT']

#implemented: -,+,(,),x,𝑥,²,÷,π,sin,cos,tan,.,DEL,AC,EXE,up,right,down,left,z-in,z-out,SHIFT,³,csc,sec,cot,e