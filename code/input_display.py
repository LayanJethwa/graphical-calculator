import pygame

import constants


font = pygame.font.Font('./assets/STIXTwoMath-Regular.ttf', 30)


def update_screen(screen, current_texts, selected, view_window):
    screen.fill(constants.WHITE)
    pygame.draw.rect(screen, constants.BLACK, pygame.Rect(0,0,constants.WIDTH, 40),2)


    colour = constants.BLACK
    screen.blit(font.render('𝑥:', False, constants.BLACK), (5,5))
    if selected == 7:
        colour = constants.BLUE
    pygame.draw.rect(screen, colour, pygame.Rect(35,5,80,30),2)
    screen.blit(font.render(view_window[0], False, constants.BLACK), (40,6))

    colour = constants.BLACK
    screen.blit(font.render('-', False, constants.BLACK), (125,5))
    if selected == 8:
        colour = constants.BLUE
    pygame.draw.rect(screen, colour, pygame.Rect(145,5,80,30),2)
    screen.blit(font.render(view_window[1], False, constants.BLACK), (150,6))

    colour = constants.BLACK
    screen.blit(font.render('𝑦:', False, constants.BLACK), (245,5))
    if selected == 9:
        colour = constants.BLUE
    pygame.draw.rect(screen, colour, pygame.Rect(275,5,80,30),2)
    screen.blit(font.render(view_window[2], False, constants.BLACK), (280,6))

    colour = constants.BLACK
    screen.blit(font.render('-', False, constants.BLACK), (365,5))
    if selected == 10:
        colour = constants.BLUE
    pygame.draw.rect(screen, colour, pygame.Rect(385,5,80,30),2)
    screen.blit(font.render(view_window[3], False, constants.BLACK), (390,6))


    for line in range(7):
        screen.blit(font.render(f'{line+1}:  𝑦 =', False, constants.BLACK), (35,45+line*40))
        if selected == line:
            screen.blit(font.render('>', False, constants.BLUE), (5,45+line*40))
            screen.blit(font.render(current_texts[selected], False, constants.BLACK), (125,45+line*40))
        elif current_texts[line] == '':
            screen.blit(font.render('...', False, constants.BLACK), (125,45+line*40))
        else:
            screen.blit(font.render(current_texts[line], False, constants.BLACK), (125,45+line*40))
        pygame.draw.rect(screen, constants.COLOURS[line], pygame.Rect(440,55+line*40,30,15))


def move(direction, current_texts, selected, cursor_active, view_window):
    if direction == 'up':
        if selected == 0:
            selected = 7
            view_window[selected-7] += '|'
            cursor_active = True

        elif selected > 0:
            selected -= 1
            current_texts[selected] += '|'
            cursor_active = True

    elif direction == 'down':
        if selected < 7:
            selected += 1
            current_texts[selected] += '|'
            cursor_active = True
        
        elif selected >= 7:
            selected = 0
            current_texts[selected] += '|'
            cursor_active = True

    elif direction == 'left':
        if selected > 7:
            selected -= 1
            view_window[selected-7] += '|'
            cursor_active = True

    elif direction == 'right':
        if selected < 10:
            selected += 1
            view_window[selected-7] += '|'
            cursor_active = True

    return current_texts, selected, cursor_active, view_window