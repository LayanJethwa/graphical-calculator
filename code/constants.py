RIGHT_ASSOCIATIVE = ['^','log']
OPERANDS = ['x']
OPERATORS = ['+','\-','/','*','^','(',')']
UNARY_FUNCTIONS = ['sin','cos','tan','csc','sec','cot']
BINARY_FUNCTIONS = ['log']

PRECEDENCES_LIST = [['sin','cos','tan'],['^','log'],['/','*'],['+','-']]
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


IDENTICAL_KEYS = [ord(i) for i in '-.e']
SHIFT_KEYS = {ord(i[0]):i[1] for i in [('=','+'),('9','('),('0',')'),('8','x')]}
PLACEHOLDER_KEYS = {'q':'²', 'w':'³', 'x':'𝑥', '/':'÷', 'p':'π', 'l':'log(', 's':'sin(', 'c':'cos(', 't':'tan(', 'r':'csc(', 'y':'sec(', 'u':'cot('}

E = 2.718281828459045235360287471352
PI = 3.141592653589793238462643383279