import pygame

import constants

font = pygame.font.Font('code/assets/STIXTwoMath-Regular.ttf', 30)

def update_screen(screen, current_texts, selected):
    screen.fill(constants.WHITE)
    pygame.draw.rect(screen, constants.BLACK, pygame.Rect(0,0,constants.WIDTH, 40),2)
    screen.blit(font.render('𝑥:', False, constants.BLACK), (5,5))
    pygame.draw.rect(screen, constants.BLACK, pygame.Rect(35,7.5,80,25),2)
    screen.blit(font.render('-', False, constants.BLACK), (125,5))
    pygame.draw.rect(screen, constants.BLACK, pygame.Rect(145,7.5,80,25),2)
    screen.blit(font.render('𝑦:', False, constants.BLACK), (245,5))
    pygame.draw.rect(screen, constants.BLACK, pygame.Rect(275,7.5,80,25),2)
    screen.blit(font.render('-', False, constants.BLACK), (365,5))
    pygame.draw.rect(screen, constants.BLACK, pygame.Rect(385,7.5,80,25),2)

    for line in range(7):
        screen.blit(font.render(f'{line+1}:  𝑦 =', False, constants.BLACK), (35,45+line*40))
        if selected == line:
            screen.blit(font.render('>', False, constants.BLACK), (5,45+line*40))
            screen.blit(font.render(current_texts[selected], False, constants.BLACK), (125,45+line*40))
        elif current_texts[line] == '':
            screen.blit(font.render('...', False, constants.BLACK), (125,45+line*40))
        else:
            screen.blit(font.render(current_texts[line], False, constants.BLACK), (125,45+line*40))
        pygame.draw.rect(screen, constants.COLOURS[line], pygame.Rect(440,55+line*40,30,15))

def move(direction, current_texts, selected, cursor_active):
    if direction == 'up':
        if selected > 0:
            selected -= 1
            current_texts[selected] += '|'
            cursor_active = True

    elif direction == 'down':
        if selected < 7:
            selected += 1
            current_texts[selected] += '|'
            cursor_active = True

    return current_texts, selected, cursor_active