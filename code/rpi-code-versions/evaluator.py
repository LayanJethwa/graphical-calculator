import constants
import helpers

import math


def create_function(postfix):
    stack = []
    for token in postfix:
        value, tag = token

        if tag == "operand":
            if value == 'x':
                stack.append(lambda x: x)
            elif value == "PI":
                stack.append(lambda x: math.pi)
            elif value == "E":
                stack.append(lambda x: math.e)
            elif callable(value):
                stack.append(value)
            else:
                try:
                    stack.append(lambda x, v=float(value): v)
                except:
                    raise Exception("Invalid string for a number")
        
        elif value == "NEG":
            a = stack.pop()
            stack.append(lambda x, a=a: -a(x))
        
        else:
            b = stack.pop()
            a = stack.pop()
            if token[0] == '+':
                stack.append(lambda x, a=a, b=b: a(x) + b(x))
            elif token[0] == '-':
                stack.append(lambda x, a=a, b=b: a(x) - b(x))
            elif token[0] == '*':
                stack.append(lambda x, a=a, b=b: a(x) * b(x))
            elif token[0] == '/':
                stack.append(lambda x, a=a, b=b: a(x) / b(x))
    
    return stack[0]


def create_points(function, frequency=constants.DEFAULT_FREQUENCY):
    points = []
    for x in helpers.frange(constants.XMIN*frequency, (constants.XMAX*frequency)+frequency, constants.XDIFF):
        try:
            if isinstance(function(x/frequency), complex):
                points.append((x/frequency, None))
            else:
                points.append((x/frequency, function(x/frequency)))
        except:
            points.append((x/frequency, None))
    return points


def evaluate(postfix, frequency=constants.DEFAULT_FREQUENCY):
    return create_points(create_function(postfix), frequency)