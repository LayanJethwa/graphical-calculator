import pygame

import constants
import parser
import evaluator

constants.precedences_setup()

display_mode = "input"
current_texts = ['|']+['']*6
selected = 0
cursor_active = True

pygame.init()
screen = pygame.display.set_mode((constants.WIDTH, constants.HEIGHT))
running = True

import input_display
import graph_display

'''
label_font = pygame.font.Font('code/assets/universcondensed_medium.ttf', constants.AXIS_LABEL_LENGTH*3)

screen.fill(constants.WHITE)

pygame.draw.line(screen, constants.BLACK, (0,constants.Y0), (constants.WIDTH,constants.Y0))
pygame.draw.line(screen, constants.BLACK, (constants.X0,0), (constants.X0,constants.HEIGHT))

pygame.draw.line(screen, constants.BLACK, (0,constants.Y0-constants.AXIS_LABEL_LENGTH), (0,constants.Y0+constants.AXIS_LABEL_LENGTH))
pygame.draw.line(screen, constants.BLACK, (constants.WIDTH-1,constants.Y0-constants.AXIS_LABEL_LENGTH), (constants.WIDTH-1,constants.Y0+constants.AXIS_LABEL_LENGTH))
pygame.draw.line(screen, constants.BLACK, (constants.X0-constants.AXIS_LABEL_LENGTH,0), (constants.X0+constants.AXIS_LABEL_LENGTH,0))
pygame.draw.line(screen, constants.BLACK, (constants.X0-constants.AXIS_LABEL_LENGTH,constants.HEIGHT-1), (constants.X0+constants.AXIS_LABEL_LENGTH,constants.HEIGHT-1))

screen.blit(label_font.render(str(constants.XMIN), False, constants.BLACK), (constants.AXIS_LABEL_LENGTH,constants.Y0+constants.AXIS_LABEL_LENGTH))
screen.blit(label_font.render(str(constants.XMAX), False, constants.BLACK), (constants.WIDTH-label_font.size(str(constants.XMAX))[0]-constants.AXIS_LABEL_LENGTH,constants.Y0+constants.AXIS_LABEL_LENGTH))
screen.blit(label_font.render(str(constants.YMIN), False, constants.BLACK), (constants.X0+constants.AXIS_LABEL_LENGTH,constants.HEIGHT-label_font.size(str(constants.YMIN))[1]-constants.AXIS_LABEL_LENGTH))
screen.blit(label_font.render(str(constants.YMAX), False, constants.BLACK), (constants.X0+constants.AXIS_LABEL_LENGTH,constants.AXIS_LABEL_LENGTH))
'''

'''
infix = input("y=")
postfix = parser.parse(infix)
points = evaluator.evaluate(postfix)



previous_point = ()
for point in points:
    current_point = ((point[0]*constants.SCALEX)-(constants.XMIN*constants.SCALEX),
               constants.HEIGHT - ((point[1]*constants.SCALEY)-(constants.YMIN*constants.SCALEY)))

    if previous_point:
        pygame.draw.line(screen, constants.RED, previous_point, current_point)

    previous_point = current_point
    
pygame.display.update()
'''
def render_graphs(graphs):
    for index in range(len(graphs)):
        graph = graphs[index]
        if graph != '':
            postfix = parser.parse(graph)
            points = evaluator.evaluate(postfix)
            graph_display.plot_graph(screen, points, constants.COLOURS[index])

input_display.update_screen(screen, current_texts, selected)
pygame.display.update()

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
                        current_texts[selected] = current_texts[selected].replace('|',constants.SHIFT_KEYS[event.key]+'|')

                    elif event.key in constants.IDENTICAL_KEYS:
                        current_texts[selected] = current_texts[selected].replace('|',chr(event.key)+'|')
                    elif key.isdigit():
                        current_texts[selected] = current_texts[selected].replace('|',key+'|')

                    elif key == 'x':
                        current_texts[selected] = current_texts[selected].replace('|','𝑥|')
                    elif event.key == ord('/'):
                        current_texts[selected] = current_texts[selected].replace('|','÷|')

                    elif key == 'q':
                        current_texts[selected] = current_texts[selected].replace('|','²|')
                    elif key == 'w':
                        current_texts[selected] = current_texts[selected].replace('|','³|')

                    elif key == 'backspace':
                        current_texts[selected] = current_texts[selected][0:-2]+'|'
                    elif key == 'return':
                        current_texts[selected] = current_texts[selected][0:-1]
                        cursor_active = False

                elif cursor_active == False:
                    if event.key == pygame.K_DOWN:
                        current_texts, selected, cursor_active = input_display.move('down', current_texts, selected, cursor_active)
                    elif event.key == pygame.K_UP:
                        current_texts, selected, cursor_active = input_display.move('up', current_texts, selected, cursor_active)
                    elif key == 'return':
                        display_mode = "graph"

                if display_mode == 'input':
                    input_display.update_screen(screen, current_texts, selected)
                    pygame.display.update()
                elif display_mode == 'graph':
                    graph_display.update_screen(screen)
                    render_graphs(current_texts)
                    pygame.display.update()

            elif display_mode == "graph":
                if key == 'return':
                    display_mode = 'input'
                    input_display.update_screen(screen, current_texts, selected)
                    pygame.display.update()