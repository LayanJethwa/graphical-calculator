import pygame

import parser
import constants
import evaluator

constants.precedences_setup()

pygame.init()
screen = pygame.display.set_mode((constants.WIDTH, constants.HEIGHT))
running = True
screen.fill((255,255,255))

pygame.draw.line(screen, (0,0,0), (0,constants.Y0), (constants.WIDTH,constants.Y0))
pygame.draw.line(screen, (0,0,0), (constants.X0,0), (constants.X0,constants.HEIGHT))

infix = input("y=")
postfix = parser.parse(infix)
points = evaluator.evaluate(postfix)

previous_point = ()
for point in points:
    current_point = ((point[0]*constants.SCALEX)-(constants.XMIN*constants.SCALEX),
               constants.HEIGHT - ((point[1]*constants.SCALEY)-(constants.YMIN*constants.SCALEY)))

    if previous_point:
        pygame.draw.line(screen, (255,0,0), previous_point, current_point)

    previous_point = current_point
    
pygame.display.update()

while running:
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()