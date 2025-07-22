import re


class safelist(list):
    def get(self, index, default=None):
        try:
            return self[index]
        except IndexError:
            return default


def process(infix):
    matches = re.findall(r"(\d+)x", infix)
    processed_infix = infix
    for match in matches:
        processed_infix = processed_infix.replace(match+'x',f"({match}*x)")
    
    processed_infix = re.findall(r"\d+|\D", processed_infix)

    return processed_infix


def convert(processed_infix):
    precedences_list = [('^'),('/','*'),('+','-')]
    precedences_dict = {None:100000}
    for index in range(len(precedences_list)):
        for operator in precedences_list[index]:
            precedences_dict[operator] = index

    right_associative = ['^']
    functions = []
    operands = ['x']

    out_queue = safelist()
    operator_stack = safelist()

    def send():
        out_queue.append(operator_stack.pop())

    for token in processed_infix:

        if token.isdigit() or token in operands:
            out_queue.append(token)

        elif token in functions:
            operator_stack.append(token)

        elif token == '(':
            operator_stack.append(token)

        elif token == ')':
            while operator_stack.get(-1) != '(':
                send()
            operator_stack.pop()
            if operator_stack.get(-1) in functions:
                send()

        else:
            while ((operator_stack.get(-1) != '(' and operator_stack.get(-1) not in functions
                   and operator_stack.get(-1) != None) and 
                   ((precedences_dict[operator_stack.get(-1)] < precedences_dict[token])
                    or (precedences_dict[operator_stack.get(-1)] == precedences_dict[token]
                        and token not in right_associative))):
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