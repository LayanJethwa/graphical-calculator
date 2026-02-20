import math

def create_function(postfix):
    stack = []
    for token in postfix:
        if token == 'x':
            stack.append(lambda x: x)

        elif token.isdigit():
            stack.append(lambda x, v=float(token): v)

        elif token in ['sin', 'cos', 'tan']: #Unary functions
            a = stack.pop()
            if token == 'sin':
                stack.append(lambda x, a=a: math.sin(a(x)))
            elif token == 'cos':
                stack.append(lambda x, a=a: math.cos(a(x)))
            elif token == 'tan':
                stack.append(lambda x, a=a: math.tan(a(x)))
        
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

f = create_function(postfix=["x","2","="])
f(2) # returns 4
f(7) # returns 9
[f(x) for x in range(1,4)] # returns [3,4,5] (evaluates for each in range, i.e. [1,2,3])