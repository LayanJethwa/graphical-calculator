import constants
import helpers


def create_function(postfix):
    stack = []
    for token in postfix:
        if token[0] == 'x':
            stack.append(lambda x: x)

        elif str(token[0]).isdigit():
            stack.append(lambda x, v=float(token[0]): v)
        
        elif token[1] == "operand":
            stack.append(token[0])
        
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