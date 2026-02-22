import constants

import pygame
pygame.init()
fonts = {30: pygame.font.Font('./assets/STIXTwoMath-Regular.ttf', 30)}

def get_font(size): #dynamic font
    size = int(size)
    if fonts.get(size):
        return fonts.get(size)
    else:
        fonts[size] = pygame.font.Font('./assets/STIXTwoMath-Regular.ttf', size)
        return fonts[size]

import math

import evaluator
import parser


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

    def render(self, scale=1, cursor=None):
        pixel_size = 30*scale
        surface = get_font(pixel_size).render(self.character, True, constants.BLUE)
        return pygame.transform.smoothscale(surface, tuple(i*scale for i in surface.get_size()))
    
    def move_left(self):
        if self.position > 0:
                self.position -= 1
        elif self.expression == self.expression.parent.right:
            self.expression = self.expression.parent.left
        else:
            self.position = self.expression.parent.parent.index(self.expression.parent)
            self.expression = self.expression.parent.parent

    def move_right(self):
        if self.position < len(self.expression.objects):
            self.position += 1
        elif self.expression == self.expression.parent.left:
            self.expression = self.expression.parent.right
        else:
            self.position = self.expression.parent.parent.index(self.expression.parent) + 1
            self.expression = self.expression.parent.parent


class Expression(Object):
    def __init__(self, parent=None):
        super().__init__()
        self.objects = []
        self.parent = parent
        self.left = None
        self.right = None
        self.type = "expression"

    def update(self, arg, pos=-1):
        if arg == "DEL":
            if pos != 0:
                self.objects.pop(pos-1)
        else:
            self.objects.insert(pos, arg)
            arg.parent = self

    def index(self, object):
        return self.objects.index(object)
    
    def render(self, scale=1, offset=0, cursor=Cursor(None)): #talk in design about problems with too small nested - choosing not to fix, same with smoothscale and resolution
        surface = pygame.Surface((0,0), pygame.SRCALPHA)
        render_objects = self.objects.copy()
        if cursor.expression == self:
            render_objects.insert(cursor.position, cursor)
        for object in render_objects:
            rendered = object.render(scale=scale, cursor=cursor)
            new_surface = pygame.Surface((surface.get_width() + rendered.get_width(), max(surface.get_height(), rendered.get_height())), pygame.SRCALPHA)
            new_surface.blit(surface, (0,0))
            if object.type == "number" or object.type == "symbol" or object.type == "variable":
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

        postfix = parser.convert(tokens)
        return evaluator.create_function(postfix)


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

    def render(self, scale=1, cursor=Cursor(None)):
        numerator = self.left.render(scale=0.7, cursor=cursor)
        denominator = self.right.render(scale=0.7, cursor=cursor)
        width = max(numerator.get_width(), denominator.get_width())+5
        surface = pygame.Surface((width, numerator.get_height()+5+denominator.get_height()), pygame.SRCALPHA)
        pygame.draw.line(surface, constants.BLACK, (0, surface.get_height()/2), (surface.get_width(), surface.get_height()/2))
        surface.blit(numerator, (2.5+((width-numerator.get_width())/2), 0))
        surface.blit(denominator, (2.5+((width-denominator.get_width())/2), 2.5+surface.get_height()/2))
        return pygame.transform.smoothscale(surface, tuple(i*scale for i in surface.get_size()))
    
    def evaluate(self):
        return lambda x, a=self.left.evaluate(), b=self.right.evaluate(): a(x) / b(x)

class Radical(BinaryOperator):
    def __init__(self):
        super().__init__()

    def render(self, scale=1, cursor=Cursor(None)):
        operator = self.left.render(scale=0.7, cursor=cursor)
        operand = self.right.render(scale=0.9, cursor=cursor)
        surface = pygame.Surface((operand.get_width()+10+operator.get_width(), operand.get_height()+10), pygame.SRCALPHA)
        pygame.draw.lines(surface, constants.BLACK, False, [(operator.get_width()-5, surface.get_height()-10), (operator.get_width(), surface.get_height()), (operator.get_width()+5, 5), (surface.get_width(), 5)], width=2)
        surface.blit(operand, (operator.get_width()+5, 10))
        surface.blit(operator, (0, 0))
        return pygame.transform.smoothscale(surface, tuple(i*scale for i in surface.get_size()))
    
    def evaluate(self):
        return lambda x, a=self.left.evaluate(), b=self.right.evaluate(): math.copysign(abs(b(x)) ** (1/a(x)), b(x)) #comment in design about principal root problem with complex numbers, had to change for non integer powers


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

    def render(self, scale=1, cursor=Cursor(None)):
        operand = self.operand.render(scale=0.9, cursor=cursor)
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

    def render(self, scale=1, cursor=Cursor(None)): #cursor default arg so that it can be passed through all the render operations without distinguishing type
        pixel_size = 30*scale #dynamic font size instead of smoothscale after
        font = get_font(pixel_size)
        surface = font.render(self.rendered_value, True, constants.BLACK)
        return surface

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