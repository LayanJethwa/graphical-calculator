import constants
import helpers


def convert(processed_infix):
    out_queue = helpers.SafeList()
    operator_stack = helpers.SafeList()

    def send():
        out_queue.append(operator_stack.pop())

    for token in processed_infix:
        value, tag = token

        if tag == "operand":
            out_queue.append(token)
        
        elif value == "(":
            operator_stack.append(token)

        elif value == ")":
            while operator_stack.get(-1)[0] != "(":
                send()
            operator_stack.pop()

        else:
            while True:
                top = operator_stack.get(-1)
                if top is None:
                    break
                elif top[0] == "(":
                    break
                top_prec = constants.PRECEDENCES.get(top[0], 0)
                cur_prec = constants.PRECEDENCES.get(value, 0)

                if (top_prec < cur_prec) or (top_prec == cur_prec and value not in constants.RIGHT_ASSOCIATIVE):
                    send()
                else:
                    break
            operator_stack.append(token)
            

    while len(operator_stack) != 0:
        if operator_stack[-1][0] == '(':
            raise Exception("Mismatched parentheses")
        else:
            send()

    return out_queue