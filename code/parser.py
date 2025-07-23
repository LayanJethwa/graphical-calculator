import re

import constants


class SafeList(list):
    def get(self, index, default=None):
        try:
            return self[index]
        except IndexError:
            return default


def process(infix):
    infix = infix.replace('x','*').replace('𝑥','x').replace('²','^2').replace('³','^3').replace('÷','/')
    matches = re.findall(r"(\d+)x", infix)
    processed_infix = infix
    for match in matches:
        processed_infix = processed_infix.replace(match+'x',match+'*x')
    
    processed_infix = re.findall(r"\d+|\D", processed_infix)

    return processed_infix


def convert(processed_infix):
    out_queue = SafeList()
    operator_stack = SafeList()

    def send():
        out_queue.append(operator_stack.pop())

    for token in processed_infix:

        if token.isdigit() or token in constants.OPERANDS:
            out_queue.append(token)

        elif token in constants.FUNCTIONS:
            operator_stack.append(token)

        elif token == '(':
            operator_stack.append(token)

        elif token == ')':
            while operator_stack.get(-1) != '(':
                send()
            operator_stack.pop()
            if operator_stack.get(-1) in constants.FUNCTIONS:
                send()

        else:
            while ((operator_stack.get(-1) != '(' and operator_stack.get(-1) not in constants.FUNCTIONS
                   and operator_stack.get(-1) != None) and 
                   ((constants.PRECEDENCES[operator_stack.get(-1)] < constants.PRECEDENCES[token])
                    or (constants.PRECEDENCES[operator_stack.get(-1)] == constants.PRECEDENCES[token]
                        and token not in constants.RIGHT_ASSOCIATIVE))):
                        send()
            operator_stack.append(token)

    while len(operator_stack) != 0:
        if operator_stack[-1] == '(':
            raise Exception("Mismatched parentheses")
        else:
            send()

    return out_queue


def parse(infix):
    return convert(process(infix))