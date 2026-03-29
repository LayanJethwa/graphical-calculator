import pygame

import constants


label_font = pygame.font.Font('/home/lrsje/graphical-calculator/assets/universcondensed_medium.ttf', constants.AXIS_LABEL_LENGTH*3)


def update_screen(screen):
    screen.fill(constants.WHITE)

    pygame.draw.line(screen, constants.BLACK, (0,constants.Y0), (constants.WIDTH,constants.Y0))
    pygame.draw.line(screen, constants.BLACK, (constants.X0,0), (constants.X0,constants.HEIGHT)) # draws axes

    pygame.draw.line(screen, constants.BLACK, (0,constants.Y0-constants.AXIS_LABEL_LENGTH), (0,constants.Y0+constants.AXIS_LABEL_LENGTH)) # draws axis label ticks
    pygame.draw.line(screen, constants.BLACK, (constants.WIDTH-1,constants.Y0-constants.AXIS_LABEL_LENGTH), (constants.WIDTH-1,constants.Y0+constants.AXIS_LABEL_LENGTH))
    pygame.draw.line(screen, constants.BLACK, (constants.X0-constants.AXIS_LABEL_LENGTH,0), (constants.X0+constants.AXIS_LABEL_LENGTH,0))
    pygame.draw.line(screen, constants.BLACK, (constants.X0-constants.AXIS_LABEL_LENGTH,constants.HEIGHT-1), (constants.X0+constants.AXIS_LABEL_LENGTH,constants.HEIGHT-1))

    screen.blit(label_font.render(str(constants.XMIN), False, constants.BLACK), (constants.AXIS_LABEL_LENGTH,constants.Y0+constants.AXIS_LABEL_LENGTH)) # draws axis label numbers
    screen.blit(label_font.render(str(constants.XMAX), False, constants.BLACK), (constants.WIDTH-label_font.size(str(constants.XMAX))[0]-constants.AXIS_LABEL_LENGTH,constants.Y0+constants.AXIS_LABEL_LENGTH))
    screen.blit(label_font.render(str(constants.YMIN), False, constants.BLACK), (constants.X0+constants.AXIS_LABEL_LENGTH,constants.HEIGHT-label_font.size(str(constants.YMIN))[1]-constants.AXIS_LABEL_LENGTH))
    screen.blit(label_font.render(str(constants.YMAX), False, constants.BLACK), (constants.X0+constants.AXIS_LABEL_LENGTH,constants.AXIS_LABEL_LENGTH))


def plot_graph(screen, points, colour): # plots points on screen and interpolates between them
    previous_point = ()
    for point in points:
        if point[1] == None:
            previous_point = None
        else: # maths coordinates vs computer coordinates - (0,0) is top left for the computer and y direction is reversed, but origin can be anywhere on the screen or off due to the moving and view window so the graph needs to be transformed appropriately
            current_point = ((point[0]*constants.SCALEX)-(constants.XMIN*constants.SCALEX),
                    constants.HEIGHT - ((point[1]*constants.SCALEY)-(constants.YMIN*constants.SCALEY)))

            if previous_point:
                pygame.draw.line(screen, colour, previous_point, current_point)

            previous_point = current_point


def move(direction): # allows panning around graph, points updated and re-rendered according to new bounds each time
    if direction == 'UP':
        constants.YMAX += (constants.YDIFF/5)
        constants.YMIN += (constants.YDIFF/5)
    elif direction == 'DOWN':
        constants.YMAX -= (constants.YDIFF/5)
        constants.YMIN -= (constants.YDIFF/5)
    elif direction == 'LEFT':
        constants.XMAX -= (constants.XDIFF/5)
        constants.XMIN -= (constants.XDIFF/5)
    elif direction == 'RIGHT':
        constants.XMAX += (constants.XDIFF/5)
        constants.XMIN += (constants.XDIFF/5)
    constants.update_bounds()

def zoom(direction): # allows zooming in and out of graph, centered on the center of the screen, points updated and re-rendered according to new bounds each time
    XCENTRE = (constants.XMAX+constants.XMIN)/2
    YCENTRE = (constants.YMAX+constants.YMIN)/2
    if direction == 'IN' and constants.XMAX > 0.001: # bounds so that calculations do not get too intensive on CPU (for zooming out, eventually we would reach significant floating point errors so the graph would not render accurately anyway)
        constants.XMIN = XCENTRE-((constants.XMAX-XCENTRE)/constants.ZOOM_SCALE_FACTOR)
        constants.XMAX = XCENTRE+((constants.XMAX-XCENTRE)/constants.ZOOM_SCALE_FACTOR)
        constants.YMIN = YCENTRE-((constants.YMAX-YCENTRE)/constants.ZOOM_SCALE_FACTOR)
        constants.YMAX = YCENTRE+((constants.YMAX-YCENTRE)/constants.ZOOM_SCALE_FACTOR)
    elif direction == 'OUT' and constants.XMAX < 1000000:
        constants.XMIN = XCENTRE-((constants.XMAX-XCENTRE)*constants.ZOOM_SCALE_FACTOR)
        constants.XMAX = XCENTRE+((constants.XMAX-XCENTRE)*constants.ZOOM_SCALE_FACTOR)
        constants.YMIN = YCENTRE-((constants.YMAX-YCENTRE)*constants.ZOOM_SCALE_FACTOR)
        constants.YMAX = YCENTRE+((constants.YMAX-YCENTRE)*constants.ZOOM_SCALE_FACTOR)
    constants.update_bounds()
