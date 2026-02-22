import pygame

import constants
import evaluator
import expression_tree


constants.precedences_setup()

display_mode = "input"
functions = [expression_tree.Expression() for _ in range(7)]
for function in functions:
    function.parent = function
cursors = [expression_tree.Cursor(functions[_]) for _ in range(7)]
view_window = [str(i) for i in [constants.XMIN, constants.XMAX, constants.YMIN, constants.YMAX]]
selected = 0
cursor_active = True
shift_mode = False


pygame.init()
screen = pygame.display.set_mode((constants.WIDTH, constants.HEIGHT))
running = True

import input_display
import graph_display

def render_graphs(graphs):
    for index in range(len(graphs)):
        graph = graphs[index]
        if graph.objects:
            evaluated = graph.evaluate()
            points = evaluator.create_points(evaluated)
            graph_display.plot_graph(screen, points, constants.COLOURS[index])


input_display.update_screen(screen, functions, selected, view_window, cursors, cursor_active, shift_mode)
pygame.display.update()


while running:
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()

        elif event.type == pygame.KEYDOWN:
            key = pygame.key.name(event.key)
            token = constants.KEY_MAP[key]
            if type(token) == list:
                token = token[shift_mode]
            if token != "SHIFT":
                shift_mode = False

            if display_mode == "input":
                if cursor_active == True:
                    if selected < 7:
                        if token in constants.BINARY_OPERATORS:
                            if token == "RADICAL":
                                operator = expression_tree.Radical()
                            elif token == "FRACTION":
                                operator = expression_tree.Fraction()
                            cursors[selected].expression.update(operator, cursors[selected].position)
                            cursors[selected].expression = operator.left
                            cursors[selected].position = 0
                        elif token in constants.UNARY_OPERATORS:
                            if token == "SQRT":
                                operator = expression_tree.SquareRoot()
                            cursors[selected].expression.update(operator, cursors[selected].position)
                            cursors[selected].expression = operator.operand
                            cursors[selected].position = 0
                        elif token in constants.NUMBERS:
                            cursors[selected].expression.update(expression_tree.Number(token), cursors[selected].position)
                            cursors[selected].position += 1
                        elif token in constants.SYMBOLS:
                            cursors[selected].expression.update(expression_tree.Symbol(token), cursors[selected].position)
                            cursors[selected].position += 1
                        elif token in constants.VARIABLES:
                            cursors[selected].expression.update(expression_tree.Variable(token), cursors[selected].position)
                            cursors[selected].position += 1
                        elif token in constants.ARROWS:
                            if token == "LEFT":
                                cursors[selected].move_left()
                            elif token == "RIGHT":
                                cursors[selected].move_right()
                        elif token == "DEL":
                            if cursors[selected].position > 0:
                                cursors[selected].expression.update("DEL", cursors[selected].position)
                                cursors[selected].position -= 1
                        elif token == "EXE":
                            cursor_active = False
                        elif token == "AC":
                            function = expression_tree.Expression()
                            function.parent = function
                            functions[selected] = function
                            cursors[selected] = expression_tree.Cursor(function)

                    else:
                        if token in constants.NUMBERS:
                            view_window[selected-7] = view_window[selected-7].replace('|',token+'|')
                        elif token == "DEL":
                            view_window[selected-7] = view_window[selected-7][0:-2]+'|'
                        elif token == "EXE":
                            view_window[selected-7] = view_window[selected-7][0:-1]
                            constants.XMIN, constants.XMAX, constants.YMIN, constants.YMAX = [float(i) for i in view_window]
                            constants.update_bounds()
                            cursor_active = False
                        elif token == "AC":
                            view_window[selected-7] = '|'


                elif cursor_active == False:
                    if token in constants.ARROWS:
                        selected, cursor_active, view_window = input_display.move(token, functions, cursors, selected, cursor_active, view_window)
                    elif token == "EXE":
                        display_mode = "graph"

                if token == "SHIFT":
                    shift_mode = not shift_mode

                if display_mode == 'input':
                    input_display.update_screen(screen, functions, selected, view_window, cursors, cursor_active, shift_mode)
                    pygame.display.update()
                elif display_mode == 'graph':
                    graph_display.update_screen(screen)
                    render_graphs(functions)
                    pygame.display.update()

            elif display_mode == "graph":
                if token == "EXE":
                    display_mode = 'input'
                    input_display.update_screen(screen, functions, selected, view_window, cursors, cursor_active, shift_mode)
                    pygame.display.update()

                elif token in constants.ARROWS or token in constants.ZOOM:
                    if token in constants.ARROWS:
                        graph_display.move(token)
                    elif token == "ZOOM_IN":
                        graph_display.zoom('IN')
                    elif token == "ZOOM_OUT":
                        graph_display.zoom('OUT')

                    graph_display.update_screen(screen)
                    render_graphs(functions)
                    pygame.display.update()

            
            if token == "OFF":
                running = False
                pygame.quit()


