import constants


def create_function(postfix):
    stack = []
    for token in postfix:
        if token == 'x':
            stack.append(lambda x: x)
        elif token == '-x':
            stack.append(lambda x: -x)

        elif token.lstrip('-').replace(".", "", 1).isdigit():
            stack.append(lambda x, v=float(token): v)

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
    
    return stack[0]


def frange(start, stop, step):
    res, n = start, 1

    while res < stop:
        yield res
        res = start + n * step
        n += 1


def create_points(function, frequency=constants.DEFAULT_FREQUENCY):
    points = []
    for x in frange(constants.XMIN*frequency, (constants.XMAX*frequency)+frequency, constants.XDIFF):
        points.append((x/frequency, function(x/frequency)))
    return points

def evaluate(postfix, frequency=constants.DEFAULT_FREQUENCY):
    return create_points(create_function(postfix), frequency)