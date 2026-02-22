import math

import constants
import helpers


def create_function(postfix):
    stack = []
    for token in postfix:
        if token == 'x':
            stack.append(lambda x: x)
        elif token == '-x':
            stack.append(lambda x: -x)

        elif token.lstrip('-').replace(".", "", 1).isdigit():
            stack.append(lambda x, v=float(token): v)

        elif token in constants.UNARY_FUNCTIONS:
            a = stack.pop()
            if token == 'sin':
                stack.append(lambda x, a=a: math.sin(a(x)))
            elif token == 'cos':
                stack.append(lambda x, a=a: math.cos(a(x)))
            elif token == 'tan':
                stack.append(lambda x, a=a: math.tan(a(x)))
            elif token == 'csc':
                stack.append(lambda x, a=a: 1/math.sin(a(x)))
            elif token == 'sec':
                stack.append(lambda x, a=a: 1/math.cos(a(x)))
            elif token == 'cot':
                stack.append(lambda x, a=a: 1/math.tan(a(x)))
        
        else:
            b = stack.pop()
            a = stack.pop()
            if token == '+':
                stack.append(lambda x, a=a, b=b: a(x) + b(x))
            elif token == '-':
                stack.append(lambda x, a=a, b=b: a(x) - b(x))
            elif token == '*':
                stack.append(lambda x, a=a, b=b: a(x) * b(x))
            elif token == '/':
                stack.append(lambda x, a=a, b=b: a(x) / b(x))
            elif token == '^':
                stack.append(lambda x, a=a, b=b: a(x) ** b(x))
            elif token == 'log':
                stack.append(lambda x, a=a, b=b: math.log(b(x), a(x)))
    
    return stack[0]


def create_points(function, frequency=constants.DEFAULT_FREQUENCY):
    points = []
    for x in helpers.frange(constants.XMIN*frequency, (constants.XMAX*frequency)+frequency, constants.XDIFF):
        try:
            points.append((x/frequency, function(x/frequency)))
        except:
            points.append((x/frequency, None))
    return points


def evaluate(postfix, frequency=constants.DEFAULT_FREQUENCY):
    return create_points(create_function(postfix), frequency)