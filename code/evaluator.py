import constants


def create_function(postfix):
    stack = []
    for token in postfix:
        if token == 'x':
            stack.append(lambda x: x)

        elif token.isdigit():
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


def create_points(function, frequency=constants.DEFAULT_FREQUENCY):
    points = []
    for x in range(constants.XMIN*frequency, (constants.XMAX*frequency)+frequency, constants.XMAX-constants.XMIN):
        points.append((x/frequency, function(x/frequency)))
    return points

def evaluate(postfix, frequency=constants.DEFAULT_FREQUENCY):
    return create_points(create_function(postfix), frequency)