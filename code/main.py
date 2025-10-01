import pygame
import asyncio

import constants
import parser
import evaluator
import helpers


constants.precedences_setup()

display_mode = "input"
current_texts = ['|']+['']*6
view_window = [str(i) for i in [constants.XMIN, constants.XMAX, constants.YMIN, constants.YMAX]]
selected = 0
cursor_active = True


pygame.init()
screen = pygame.display.set_mode((constants.WIDTH, constants.HEIGHT))
running = True

import input_display
import graph_display

def render_graphs(graphs):
    for index in range(len(graphs)):
        graph = graphs[index]
        if graph != '':
            postfix = parser.parse(graph)
            points = evaluator.evaluate(postfix)
            graph_display.plot_graph(screen, points, constants.COLOURS[index])


input_display.update_screen(screen, current_texts, selected, view_window)
pygame.display.update()


async def main():
    global running, display_mode, cursor_active, selected, current_texts, view_window
    while running:
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()

            elif event.type == pygame.KEYDOWN:
                key = pygame.key.name(event.key)

                if display_mode == "input":
                    if cursor_active == True:
                        if event.key in constants.SHIFT_KEYS and (event.mod & pygame.KMOD_SHIFT):
                            if selected < 7:
                                current_texts[selected] = current_texts[selected].replace('|',constants.SHIFT_KEYS[event.key]+'|')

                        elif event.key in constants.IDENTICAL_KEYS or key.isdigit():
                            if selected < 7:
                                current_texts[selected] = current_texts[selected].replace('|',chr(event.key)+'|')
                            else:
                                view_window[selected-7] = view_window[selected-7].replace('|',chr(event.key)+'|')

                        elif helpers.safe_chr(event.key) in constants.PLACEHOLDER_KEYS:
                            if selected < 7:
                                current_texts[selected] = current_texts[selected].replace('|',f'{constants.PLACEHOLDER_KEYS[chr(event.key)]}|')

                        elif key == 'backspace':
                            if selected < 7:
                                current_texts[selected] = current_texts[selected][0:-2]+'|'
                            else:
                                view_window[selected-7] = view_window[selected-7][0:-2]+'|'

                        elif key == 'return':
                            if selected < 7:
                                current_texts[selected] = current_texts[selected][0:-1]
                            else:
                                view_window[selected-7] = view_window[selected-7][0:-1]
                                constants.XMIN, constants.XMAX, constants.YMIN, constants.YMAX = [float(i) for i in view_window]
                                constants.update_bounds()
                            cursor_active = False

                    elif cursor_active == False:
                        if event.key == pygame.K_DOWN:
                            current_texts, selected, cursor_active, view_window = input_display.move('down', current_texts, selected, cursor_active, view_window)
                        elif event.key == pygame.K_UP:
                            current_texts, selected, cursor_active, view_window = input_display.move('up', current_texts, selected, cursor_active, view_window)
                        elif event.key == pygame.K_LEFT:
                            current_texts, selected, cursor_active, view_window = input_display.move('left', current_texts, selected, cursor_active, view_window)
                        elif event.key == pygame.K_RIGHT:
                            current_texts, selected, cursor_active, view_window = input_display.move('right', current_texts, selected, cursor_active, view_window)
                        elif key == 'return':
                            display_mode = "graph"

                    if display_mode == 'input':
                        input_display.update_screen(screen, current_texts, selected, view_window)
                        pygame.display.update()
                    elif display_mode == 'graph':
                        graph_display.update_screen(screen)
                        render_graphs(current_texts)
                        pygame.display.update()

                elif display_mode == "graph":
                    if key == 'return':
                        display_mode = 'input'
                        input_display.update_screen(screen, current_texts, selected, view_window)
                        pygame.display.update()

                    elif event.key in [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_n, pygame.K_m]:
                        if event.key == pygame.K_UP:
                            graph_display.move('up')
                        elif event.key == pygame.K_DOWN:
                            graph_display.move('down')
                        elif event.key == pygame.K_LEFT:
                            graph_display.move('left')
                        elif event.key == pygame.K_RIGHT:
                            graph_display.move('right')
                        elif event.key == pygame.K_n:
                            graph_display.zoom('in')
                        elif event.key == pygame.K_m:
                            graph_display.zoom('out')

                        graph_display.update_screen(screen)
                        render_graphs(current_texts)
                        pygame.display.update()

        await asyncio.sleep(0)

asyncio.run(main())