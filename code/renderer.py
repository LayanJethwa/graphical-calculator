import constants

import pygame
pygame.init()
screen = pygame.display.set_mode((constants.WIDTH, constants.HEIGHT))
font = pygame.font.Font('./assets/STIXTwoMath-Regular.ttf', 30)

line = 0
screen.fill(constants.WHITE)
screen.blit(font.render(f'{line+1}:  𝑦 =', False, constants.BLACK), (35,45+line*40))
screen.blit(font.render('>', False, constants.BLUE), (5,45+line*40))
pygame.display.update()

import math

import new_evaluator
import new_parser
import graph_display


class Object:
    def __init__(self):
        self.parent = None
        self.type = None

    def render(self, scale=1):
        pass

    def evaluate(self):
        pass


class Cursor(Object):
    def __init__(self, parent):
        super().__init__()
        self.expression = parent
        self.position = 0
        self.character = "|"

    def render(self, scale=1):
        surface = font.render(self.character, True, constants.BLUE)
        return pygame.transform.smoothscale(surface, tuple(i*scale for i in surface.get_size()))


class Expression(Object):
    def __init__(self, parent=None):
        super().__init__()
        self.objects = []
        self.parent = parent
        self.left = None
        self.right = None
        self.type = "expression"

    def update(self, arg, pos=-1):
        if arg == "del":
            self.objects.pop(pos)
        else:
            self.objects.insert(pos, arg)
            arg.parent = self

    def index(self, object):
        return self.objects.index(object)
    
    def render(self, scale=1, offset=0):
        global cursor
        surface = pygame.Surface((0,0), pygame.SRCALPHA)
        render_objects = self.objects.copy()
        if cursor.expression == self:
            render_objects.insert(cursor.position, cursor)
        for object in render_objects:
            rendered = object.render(scale=scale)
            new_surface = pygame.Surface((surface.get_width() + rendered.get_width(), max(surface.get_height(), rendered.get_height())), pygame.SRCALPHA)
            new_surface.blit(surface, (0,0))
            if object.type == "number" or object.type == "symbol":
                shift = offset
            else:
                shift = 0
            new_surface.blit(rendered, (surface.get_width(),shift+(new_surface.get_height()-rendered.get_height())/2))
            surface = new_surface
        if surface.get_size() == (0,0):
            surface = pygame.Surface((15,30), pygame.SRCALPHA)
        return pygame.transform.smoothscale(surface, tuple(i*scale for i in surface.get_size()))
    
    def evaluate(self): #handle unary minus (neg), brackets, decimal point
        tokens = []
        token = ""
        for object in self.objects:
            if object.type == "number":
                token += object.value
            elif object.type == "symbol":
                if token != "":
                    tokens.append((token, "operand"))
                tokens.append((object.value, "operator"))
                token = ""
            elif object.type == "variable": #assuming variable only comes after operator - handle implicit multiplication
                tokens.append((object.value, "operand"))
            else:
                tokens.append((object.evaluate(), "operand"))
        if token != "":
            tokens.append((token, "operand"))

        postfix = new_parser.convert(tokens)
        return new_evaluator.create_function(postfix)


class BinaryOperator(Object):
    def __init__(self):
        super().__init__()
        self.left = Expression(parent=self)
        self.right = Expression(parent=self)
        self.type = "binary_operator"

class Exponent(BinaryOperator):
    def __init__(self):
        super().__init__()

class Fraction(BinaryOperator):
    def __init__(self):
        super().__init__()

    def render(self, scale=1):
        numerator = self.left.render(scale=0.7)
        denominator = self.right.render(scale=0.7)
        surface = pygame.Surface((max(numerator.get_width(), denominator.get_width())+5, numerator.get_height()+5+denominator.get_height()), pygame.SRCALPHA)
        pygame.draw.line(surface, constants.BLACK, (0, surface.get_height()/2), (surface.get_width(), surface.get_height()/2))
        surface.blit(numerator, (2.5, 0))
        surface.blit(denominator, (2.5, 2.5+surface.get_height()/2))
        return pygame.transform.smoothscale(surface, tuple(i*scale for i in surface.get_size()))
    
    def evaluate(self):
        return lambda x, a=self.left.evaluate(), b=self.right.evaluate(): a(x) / b(x)

class Radical(BinaryOperator):
    def __init__(self):
        super().__init__()

    def render(self, scale=1):
        operator = self.left.render(scale=0.7)
        operand = self.right.render(scale=0.9)
        surface = pygame.Surface((operand.get_width()+10+operator.get_width(), operand.get_height()+10), pygame.SRCALPHA)
        pygame.draw.lines(surface, constants.BLACK, False, [(operator.get_width()-5, surface.get_height()-10), (operator.get_width(), surface.get_height()), (operator.get_width()+5, 5), (surface.get_width(), 5)], width=2)
        surface.blit(operand, (operator.get_width()+5, 10))
        surface.blit(operator, (0, 0))
        return pygame.transform.smoothscale(surface, tuple(i*scale for i in surface.get_size()))
    
    def evaluate(self):
        return lambda x, a=self.left.evaluate(), b=self.right.evaluate(): math.copysign(abs(b(x)) ** (1/int(a(x))), b(x)) #comment in design about principal root problem with complex numbers


class UnaryOperator(Object):
    def __init__(self):
        super().__init__()
        self.operand = Expression(parent=self)
        self.left = None
        self.right = None
        self.type = "unary_operator"

class SquareRoot(UnaryOperator):
    def __init__(self):
        super().__init__()

    def render(self, scale=1):
        operand = self.operand.render(scale=0.9)
        surface = pygame.Surface((operand.get_width()+15, operand.get_height()+5), pygame.SRCALPHA)
        pygame.draw.lines(surface, constants.BLACK, False, [(0, surface.get_height()-10), (5, surface.get_height()), (10, 0), (surface.get_width(), 0)], width=2)
        surface.blit(operand, (10, 5))
        return pygame.transform.smoothscale(surface, tuple(i*scale for i in surface.get_size()))
    
    def evaluate(self):
        return lambda x, a=self.operand.evaluate(): math.sqrt(a(x))


class Operand(Object):
    def __init__(self):
        super().__init__()
        self.value = None
        self.rendered_value = None

    def render(self, scale=1):
        surface = font.render(self.rendered_value, True, constants.BLACK)
        return pygame.transform.smoothscale(surface, tuple(i*scale for i in surface.get_size()))

class Number(Operand):
    def __init__(self, value):
        super().__init__()
        self.value = str(value)
        self.rendered_value = self.value
        self.type = "number"

class Symbol(Operand):
    def __init__(self, value):
        super().__init__()
        self.value = str(value)
        self.rendered_value = self.value
        self.type = "symbol"

        if self.value == "*":
            self.rendered_value = "x"
        elif self.value == "/":
            self.rendered_value = "÷"

class Variable(Operand):
    def __init__(self, value):
        super().__init__()
        self.value = str(value)
        self.rendered_value = self.value
        self.type = "variable"

        if self.value == "x":
            self.rendered_value = "𝑥"


function = Expression()
function.parent = function
global cursor
cursor = Cursor(function)

BINARY_OPERATORS = "EFR"
UNARY_OPERATORS = "S"
NUMBERS = "0123456789"
SYMBOLS = "+-*/"
VARIABLES = "x"
ARROWS = "<>"

running = True
while True:
    while running:
        token = str(input())
        if token in BINARY_OPERATORS:
            if token == "R":
                operator = Radical()
            elif token == "F":
                operator = Fraction()
            cursor.expression.update(operator, cursor.position)
            cursor.expression = operator.left
            cursor.position = 0
        elif token in UNARY_OPERATORS:
            if token == "S":
                operator = SquareRoot()
            cursor.expression.update(operator, cursor.position)
            cursor.expression = operator.operand
            cursor.position = 0
        elif token in NUMBERS:
            cursor.expression.update(Number(token), cursor.position)
            cursor.position += 1
        elif token in SYMBOLS:
            cursor.expression.update(Symbol(token), cursor.position)
            cursor.position += 1
        elif token in VARIABLES:
            cursor.expression.update(Variable(token), cursor.position)
            cursor.position += 1
        elif token in ARROWS:
            if token == "<":
                if cursor.position > 0:
                    cursor.position -= 1
                elif cursor.expression == cursor.expression.parent.right:
                    cursor.expression = cursor.expression.parent.left
                else:
                    cursor.position = cursor.expression.parent.parent.index(cursor.expression.parent)
                    cursor.expression = cursor.expression.parent.parent
            elif token == ">":
                if cursor.position < len(cursor.expression.objects):
                    cursor.position += 1
                elif cursor.expression == cursor.expression.parent.left:
                    cursor.expression = cursor.expression.parent.right
                else:
                    cursor.position = cursor.expression.parent.parent.index(cursor.expression.parent) + 1
                    cursor.expression = cursor.expression.parent.parent
        elif token == "Q":
            running = False
        
        surface = function.render(offset=5)
        white = pygame.Surface((200,40), pygame.SRCALPHA)
        white.fill(constants.WHITE)
        screen.blit(white, ((125,45)))
        screen.blit(surface, ((125,45)))
        pygame.display.update()
    
    evaluated = function.evaluate()
    points = new_evaluator.create_points(evaluated)

    screen.fill(constants.WHITE)
    graph_display.plot_graph(screen, points, constants.COLOURS[0])
    pygame.display.update()