import pygame
import RPi.GPIO as GPIO # type: ignore
import time
import os
import traceback

import constants
import evaluator
import expression_tree


constants.precedences_setup()

GPIO.cleanup()
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

for r in constants.ROWS:
    GPIO.setup(r, GPIO.OUT)
    GPIO.output(r, GPIO.LOW)

for c in constants.COLS:
    GPIO.setup(c, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def reset(): # handles exceptions on hardware so it doesnt just shut down
    global display_mode, functions, cursors, view_window, selected, cursor_active, shift_mode
    
    display_mode = "input"
    functions = [expression_tree.Expression() for _ in range(7)]
    for function in functions:
        function.parent = function
    cursors = [expression_tree.Cursor(functions[_]) for _ in range(7)]
    view_window = [str(i) for i in [constants.XMIN, constants.XMAX, constants.YMIN, constants.YMAX]]
    selected = 0
    cursor_active = True
    shift_mode = False

    for r in constants.ROWS:
        GPIO.output(r, GPIO.LOW)
        
reset()


pygame.init()
screen = pygame.display.set_mode((constants.WIDTH, constants.HEIGHT), pygame.FULLSCREEN) #fullscreen for hardware
running = True
clock = pygame.time.Clock()

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
    try: #handle exceptions
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_TAB): #keyboard override for testing
                running = False
                pygame.quit()
                        
                        
        for r in range(len(constants.ROWS)):
            GPIO.output(constants.ROWS[r], GPIO.HIGH)

            for c in range(len(constants.COLS)):
                if GPIO.input(constants.COLS[c]) == GPIO.HIGH:
                    key = constants.KEY_MATRIX[r][c]
                    if type(key) == list:
                        key = key[shift_mode]
                    if key != "SHIFT":
                        shift_mode = False
                    
                    if display_mode == "input":
                        if cursor_active == True:
                            if selected < 7:
                                if key in constants.BINARY_OPERATORS:
                                    if key == "RADICAL":
                                        operator = expression_tree.Radical()
                                    elif key == "FRACTION":
                                        operator = expression_tree.Fraction()
                                    cursors[selected].expression.update(operator, cursors[selected].position)
                                    cursors[selected].expression = operator.left
                                    cursors[selected].position = 0
                                elif key in constants.UNARY_OPERATORS:
                                    if key == "SQRT":
                                        operator = expression_tree.SquareRoot()
                                    cursors[selected].expression.update(operator, cursors[selected].position)
                                    cursors[selected].expression = operator.operand
                                    cursors[selected].position = 0
                                elif key in constants.NUMBERS:
                                    cursors[selected].expression.update(expression_tree.Number(key), cursors[selected].position)
                                    cursors[selected].position += 1
                                elif key in constants.SYMBOLS:
                                    cursors[selected].expression.update(expression_tree.Symbol(key), cursors[selected].position)
                                    cursors[selected].position += 1
                                elif key in constants.VARIABLES:
                                    cursors[selected].expression.update(expression_tree.Variable(key), cursors[selected].position)
                                    cursors[selected].position += 1
                                elif key in constants.ARROWS:
                                    if key == "LEFT":
                                        cursors[selected].move_left()
                                    elif key == "RIGHT":
                                        cursors[selected].move_right()
                                elif key == "DEL":
                                    if cursors[selected].position > 0:
                                        cursors[selected].expression.update("DEL", cursors[selected].position)
                                        cursors[selected].position -= 1
                                elif key == "EXE":
                                    cursor_active = False
                                elif key == "AC":
                                    function = expression_tree.Expression()
                                    function.parent = function
                                    functions[selected] = function
                                    cursors[selected] = expression_tree.Cursor(function)

                            else:
                                if key in constants.NUMBERS:
                                    view_window[selected-7] = view_window[selected-7].replace('|',key+'|')
                                elif key == "DEL":
                                    view_window[selected-7] = view_window[selected-7][0:-2]+'|'
                                elif key == "EXE":
                                    view_window[selected-7] = view_window[selected-7][0:-1]
                                    constants.XMIN, constants.XMAX, constants.YMIN, constants.YMAX = [float(i) for i in view_window]
                                    constants.update_bounds()
                                    cursor_active = False
                                elif key == "AC":
                                    view_window[selected-7] = '|'
                                

                        elif cursor_active == False:
                            if key in constants.ARROWS:
                                selected, cursor_active, view_window = input_display.move(key, functions, cursors, selected, cursor_active, view_window)
                            elif key == 'EXE':
                                display_mode = "graph"
                                
                        if key == 'SHIFT':
                            shift_mode = not shift_mode

                        if display_mode == 'input':
                            input_display.update_screen(screen, functions, selected, view_window, cursors, cursor_active, shift_mode)
                            pygame.display.update()
                        elif display_mode == 'graph':
                            graph_display.update_screen(screen)
                            render_graphs(functions)
                            pygame.display.update()

                    elif display_mode == "graph":
                        if key == 'EXE':
                            display_mode = 'input'
                            input_display.update_screen(screen, functions, selected, view_window, cursors, cursor_active, shift_mode)
                            pygame.display.update()
                            
                        elif key in constants.ARROWS or key in constants.ZOOM:
                            if key in constants.ARROWS:
                                graph_display.move(key)
                            elif key == "ZOOM_IN":
                                graph_display.zoom('IN')
                            elif key == "ZOOM_OUT":
                                graph_display.zoom('OUT')

                            graph_display.update_screen(screen)
                            render_graphs(functions)
                            pygame.display.update()
                            
                            
                    if key == "OFF": # end program for hardware
                        os.system("sudo shutdown -h now")
                        GPIO.cleanup()
                        running = False
                        pygame.quit()
                    
                
                    time.sleep(0.2) #so key matrix doesn't put heavy stress on CPU    
            GPIO.output(constants.ROWS[r], GPIO.LOW)
            
            
    except Exception as e: #handle exceptions with logfile as can't see terminal output on hardware
        error_text = traceback.format_exc()
        print(error_text)
        with open("logs.txt", "a") as logfile:
            logfile.write(error_text)
            logfile.write("\n")
            logfile.close()
        reset()
        input_display.update_screen(screen, functions, selected, view_window, cursors, cursor_active, shift_mode)
        pygame.display.update()

    clock.tick(60)
