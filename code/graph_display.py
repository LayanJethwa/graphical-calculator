import pygame

import constants

label_font = pygame.font.Font('code/assets/universcondensed_medium.ttf', constants.AXIS_LABEL_LENGTH*3)

def update_screen(screen):
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

def plot_graph(screen, points, colour):
    previous_point = ()
    for point in points:
        current_point = ((point[0]*constants.SCALEX)-(constants.XMIN*constants.SCALEX),
                constants.HEIGHT - ((point[1]*constants.SCALEY)-(constants.YMIN*constants.SCALEY)))

        if previous_point:
            pygame.draw.line(screen, colour, previous_point, current_point)

        previous_point = current_point
