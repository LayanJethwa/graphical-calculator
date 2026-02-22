import re

import constants
import helpers


def process(infix):
    infix = infix.replace('x','*').replace('𝑥','x').replace('²','^2').replace('³','^3').replace('÷','/').replace('π',str(constants.PI)).replace('e',str(constants.E))

    implicit_multiplication = re.findall(r"(\d+)x", infix)
    processed_infix = infix
    for match in implicit_multiplication:
        processed_infix = processed_infix.replace(match+'x',match+'*x')

    logarithms = re.findall(fr"log(\d+|[{''.join(constants.OPERANDS)}])\((\d+|[{''.join(constants.OPERANDS)}])\)", processed_infix)
    for match in logarithms:
        processed_infix = processed_infix.replace(f'log{match[0]}({match[1]})',f'{match[0]}log{match[1]}')
    
    processed_infix = re.findall(fr"(?:^|[{''.join(constants.OPERATORS)}])(-(?:\d+(?:\.\d+)?|[{''.join(constants.OPERANDS)}]))|(\d+(?:\.\d+)?)|([{''.join(constants.OPERANDS)}])|([{''.join(constants.OPERATORS)}])|({'|'.join([f'(?:{i})' for i in constants.UNARY_FUNCTIONS + constants.BINARY_FUNCTIONS])})", processed_infix)
    processed_infix = [token for group in processed_infix for token in group if token]

    return processed_infix


def convert(processed_infix):
    out_queue = helpers.SafeList()
    operator_stack = helpers.SafeList()

    def send():
        out_queue.append(operator_stack.pop())

    for token in processed_infix:

        if token.lstrip('-').replace(".", "", 1).isdigit() or token.lstrip('-') in constants.OPERANDS:
            out_queue.append(token)

        elif token in constants.UNARY_FUNCTIONS:
            operator_stack.append(token)

        elif token == '(':
            operator_stack.append(token)

        elif token == ')':
            while operator_stack.get(-1) != '(':
                send()
            operator_stack.pop()
            if operator_stack.get(-1) in constants.UNARY_FUNCTIONS:
                send()

        else:
            while ((operator_stack.get(-1) != '(' and operator_stack.get(-1) not in constants.UNARY_FUNCTIONS
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