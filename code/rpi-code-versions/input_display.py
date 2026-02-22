import pygame

import constants


font = pygame.font.Font('/home/lrsje/graphical-calculator/assets/STIXTwoMath-Regular.ttf', 30)
small_font = pygame.font.Font('/home/lrsje/graphical-calculator/assets/STIXTwoMath-Regular.ttf', 10)


def update_screen(screen, functions, selected, view_window, cursors, cursor_active, shift_mode):
    screen.fill(constants.WHITE)
    pygame.draw.rect(screen, constants.BLACK, pygame.Rect(0,0,constants.WIDTH, 40),2)


    colour = constants.BLACK
    screen.blit(font.render('𝑥:', False, constants.BLACK), (5*constants.WSCALE,5))
    if selected == 7:
        colour = constants.BLUE
    pygame.draw.rect(screen, colour, pygame.Rect(35*constants.WSCALE,5,80,30),2)
    screen.blit(font.render(view_window[0], False, constants.BLACK), (40*constants.WSCALE,6))

    colour = constants.BLACK
    screen.blit(font.render('-', False, constants.BLACK), (35*constants.WSCALE+90,5))
    if selected == 8:
        colour = constants.BLUE
    pygame.draw.rect(screen, colour, pygame.Rect(35*constants.WSCALE+110,5,80,30),2)
    screen.blit(font.render(view_window[1], False, constants.BLACK), (35*constants.WSCALE+115,6))

    colour = constants.BLACK
    screen.blit(font.render('𝑦:', False, constants.BLACK), (245*constants.WSCALE,5))
    if selected == 9:
        colour = constants.BLUE
    pygame.draw.rect(screen, colour, pygame.Rect(275*constants.WSCALE,5,80,30),2)
    screen.blit(font.render(view_window[2], False, constants.BLACK), (280*constants.WSCALE,6))

    colour = constants.BLACK
    screen.blit(font.render('-', False, constants.BLACK), (275*constants.WSCALE+90,5))
    if selected == 10:
        colour = constants.BLUE
    pygame.draw.rect(screen, colour, pygame.Rect(275*constants.WSCALE+110,5,80,30),2)
    screen.blit(font.render(view_window[3], False, constants.BLACK), (275*constants.WSCALE+115,6))


    for line in range(7):
        screen.blit(font.render(f'{line+1}:  𝑦 =', False, constants.BLACK), (35*constants.WSCALE,45*constants.HSCALE+line*40*constants.HSCALE))
        if selected == line:
            screen.blit(font.render('>', False, constants.BLUE), (5*constants.WSCALE,45*constants.HSCALE+line*40*constants.HSCALE))
            if cursor_active:
                surface = functions[line].render(offset=5, cursor=cursors[selected])
            else:
                surface = functions[line].render(offset=5)
            surface = pygame.transform.smoothscale(surface, (surface.get_width()*constants.WSCALE, surface.get_height()*constants.HSCALE))
            screen.blit(surface, (35*constants.WSCALE+90,45*constants.HSCALE+line*40*constants.HSCALE))
        elif not functions[line].objects:
            screen.blit(font.render('...', False, constants.BLACK), (35*constants.WSCALE+90,45*constants.HSCALE+line*40*constants.HSCALE))
        else:
            surface = functions[line].render(offset=5)
            surface = pygame.transform.smoothscale(surface, (surface.get_width()*constants.WSCALE, surface.get_height()*constants.HSCALE))
            screen.blit(surface, (35*constants.WSCALE+90,45*constants.HSCALE+line*40*constants.HSCALE))
        
        pygame.draw.rect(screen, constants.COLOURS[line], pygame.Rect(440*constants.WSCALE,55*constants.HSCALE+line*40*constants.HSCALE,30,15))
        
        
    if shift_mode:
        screen.blit(small_font.render("SHIFT", False, constants.BLACK), (450*constants.WSCALE, 5))


def move(direction, functions, cursors, selected, cursor_active, view_window):
    if direction == 'UP':
        if selected == 0:
            selected = 7
            view_window[selected-7] += '|'
            cursor_active = True

        elif selected > 0:
            selected -= 1
            cursors[selected].expression = functions[selected]
            cursors[selected].position = len(functions[selected].objects)
            cursor_active = True

    elif direction == 'DOWN':
        if selected < 7:
            selected += 1
            cursors[selected].expression = functions[selected]
            cursors[selected].position = len(functions[selected].objects)
            cursor_active = True
        
        elif selected >= 7:
            selected = 0
            cursors[selected].expression = functions[selected]
            cursors[selected].position = len(functions[selected].objects)
            cursor_active = True

    elif direction == 'LEFT':
        if selected > 7:
            selected -= 1
            view_window[selected-7] += '|'
            cursor_active = True

    elif direction == 'RIGHT':
        if selected < 10:
            selected += 1
            view_window[selected-7] += '|'
            cursor_active = True

    return selected, cursor_active, view_window
