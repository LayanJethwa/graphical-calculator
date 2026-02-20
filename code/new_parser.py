import re

import constants
import helpers


def convert(processed_infix):
    out_queue = helpers.SafeList()
    operator_stack = helpers.SafeList()

    def send():
        out_queue.append(operator_stack.pop())

    for token in processed_infix:

        if token[1] == "operand":
            out_queue.append(token)

        else:
            while ((operator_stack.get(-1) != '(' and operator_stack.get(-1) not in constants.UNARY_FUNCTIONS
                   and operator_stack.get(-1) != None) and 
                   ((constants.PRECEDENCES[operator_stack.get(-1)] < constants.PRECEDENCES[token[0]])
                    or (constants.PRECEDENCES[operator_stack.get(-1)] == constants.PRECEDENCES[token[0]]
                        and token[0] not in constants.RIGHT_ASSOCIATIVE))):
                        send()
            operator_stack.append(token)

    while len(operator_stack) != 0:
        if operator_stack[-1] == '(':
            raise Exception("Mismatched parentheses")
        else:
            send()

    return out_queue