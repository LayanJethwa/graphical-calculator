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

import constants
import evaluator
import parser


class Object:
    def __init__(self):
        self.parent = None
        self.type = None

    def render(self, scale=1, cursor=None):
        pass

    def evaluate(self, angle_mode="RAD"):
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
            self.position = 0
        else:
            try:
                self.position = self.expression.parent.parent.index(self.expression.parent)
            except:
                self.position = 0 #literal edge case
            self.expression = self.expression.parent.parent

    def move_right(self):
        if self.position < len(self.expression.objects):
            self.position += 1
        elif self.expression == self.expression.parent.left:
            self.expression = self.expression.parent.right
            self.position = 0
        else:
            try:
                self.position = self.expression.parent.parent.index(self.expression.parent) + 1
            except:
                self.position = 0 #wrap cursor
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
    
    def render(self, scale=1, cursor=Cursor(None)): #talk in design about problems with too small nested - choosing not to fix, same with smoothscale and resolution, offset only for computer code [GONE], not needed for hardware screen - tweaks
        surface = pygame.Surface((0,0), pygame.SRCALPHA)
        render_objects = self.objects.copy()
        if cursor.expression == self:
            render_objects.insert(cursor.position, cursor)
        for object in render_objects:
            rendered = object.render(scale=scale, cursor=cursor)
            new_surface = pygame.Surface((surface.get_width() + rendered.get_width(), max(surface.get_height(), rendered.get_height())), pygame.SRCALPHA)
            new_surface.blit(surface, (0,0))
            new_surface.blit(rendered, (surface.get_width(),(new_surface.get_height()-rendered.get_height())/2))
            surface = new_surface
        if surface.get_size() == (0,0):
            surface = pygame.Surface((15,30), pygame.SRCALPHA)
            pygame.draw.rect(surface, constants.BLACK, pygame.Rect(0,0,15,30), 2)
        return pygame.transform.smoothscale(surface, tuple(i*scale for i in surface.get_size()))
    

    def evaluate(self, angle_mode="RAD"):
        tokens = []
        last_type = "operator"
        token = ""

        def add_token(value, tag): #handles implicit multiplication
            nonlocal last_type #references parent
            if last_type == "operand" and value == "(":
                tokens.append(("*", "operator"))
            elif last_type == "operand" and value in constants.VARIABLES:
                tokens.append(("*", "operator"))
            elif last_type == "operand" and callable(value):
                tokens.append(("*", "operator"))

            tokens.append((value, tag))

            if value == "(":
                last_type = "operator" #treats left bracket as operator, right as operand for unary neg
            elif value == ")":
                last_type = "operand"
            else:
                last_type = tag

        for object in self.objects:
            if object.type == "number":
                token += object.value

            elif object.type == "symbol" or object.type == "bracket":
                if token != "":
                    add_token(token, "operand")
                    token = ""

                if object.type == "symbol":
                    if object.value == "-" and last_type == "operator":
                        add_token("NEG", "operator")
                    else:
                        add_token(object.value, "operator")

                elif object.type == "bracket":
                    add_token(object.value, "bracket")

            elif object.type == "variable":
                if token != "":
                    add_token(token, "operand")
                    token = ""
                add_token(object.value, "operand")

            else:
                if token != "":
                    add_token(token, "operand")
                    token = ""
                add_token(object.evaluate(angle_mode), "operand")

        if token != "":
            add_token(token, "operand")
        
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
        surface.blit(numerator, (2.5+((width-numerator.get_width())/2), 0)) #centered innit
        surface.blit(denominator, (2.5+((width-denominator.get_width())/2), 2.5+surface.get_height()/2))
        return pygame.transform.smoothscale(surface, tuple(i*scale for i in surface.get_size()))
    
    def evaluate(self, angle_mode="RAD"):
        return lambda x, a=self.left.evaluate(angle_mode), b=self.right.evaluate(angle_mode): a(x) / b(x)

class Radical(BinaryOperator):
    def __init__(self):
        super().__init__()

    def render(self, scale=1, cursor=Cursor(None)):
        operator = self.left.render(scale=0.7, cursor=cursor)
        operand = self.right.render(scale=0.95, cursor=cursor)
        surface = pygame.Surface((operand.get_width()+10+operator.get_width(), operand.get_height()+10), pygame.SRCALPHA)
        pygame.draw.lines(surface, constants.BLACK, False, [(operator.get_width()-5, surface.get_height()-10), (operator.get_width(), surface.get_height()), (operator.get_width()+5, 5), (surface.get_width(), 5)], width=2)
        surface.blit(operand, (operator.get_width()+5, 10))
        surface.blit(operator, (0, 0))
        return pygame.transform.smoothscale(surface, tuple(i*scale for i in surface.get_size()))
    
    def evaluate(self, angle_mode="RAD"):
        return lambda x, a=self.left.evaluate(angle_mode), b=self.right.evaluate(angle_mode): math.copysign(abs(b(x)) ** (1/a(x)), b(x)) #comment in design about principal root problem with complex numbers, had to change for non integer powers
    
class Log(BinaryOperator):
    def __init__(self):
        super().__init__()

    def render(self, scale=1, cursor=Cursor(None)):
        base = self.left.render(scale=0.7, cursor=cursor)
        base = pygame.transform.smoothscale(base, tuple(i*scale for i in base.get_size()))
        operand = self.right.render(cursor=cursor)
        operand = pygame.transform.smoothscale(operand, tuple(i*scale for i in operand.get_size()))
        pixel_size = 30*scale
        font = get_font(pixel_size)
        text1 = font.render("log", True, constants.BLACK)
        text2 = font.render("(", True, constants.BLACK)
        text3 = font.render(")", True, constants.BLACK)
        surface = pygame.Surface((text1.get_width()+base.get_width()+text2.get_width()+operand.get_width()+text3.get_width()+5, text1.get_height()+base.get_height()), pygame.SRCALPHA)
        surface.blit(text1, (0, 0))
        surface.blit(base, (text1.get_width(), text1.get_height()))
        surface.blit(text2, (text1.get_width()+base.get_width(), 0))
        surface.blit(operand, (text1.get_width()+base.get_width()+text2.get_width()+2.5, 0))
        surface.blit(text3, (text1.get_width()+base.get_width()+text2.get_width()+operand.get_width()+5, 0))
        return surface
    
    def evaluate(self, angle_mode="RAD"):
        return lambda x, a=self.left.evaluate(angle_mode), b=self.right.evaluate(angle_mode): math.log(b(x), a(x))
    
class Exponent(BinaryOperator):
    def __init__(self):
        super().__init__()

    def render(self, scale=1, cursor=Cursor(None)):
        operand = self.left.render(cursor=cursor)
        operator = self.right.render(scale=0.7, cursor=cursor)
        surface = pygame.Surface((operand.get_width()+operator.get_width(), operand.get_height()), pygame.SRCALPHA)
        surface.blit(operand, (0, 2.5))
        surface.blit(operator, (operand.get_width(), 0))
        return pygame.transform.smoothscale(surface, tuple(i*scale for i in surface.get_size()))
    
    def evaluate(self, angle_mode="RAD"):
        return lambda x, a=self.left.evaluate(angle_mode), b=self.right.evaluate(angle_mode): a(x)**b(x)


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
        operand = self.operand.render(scale=0.95, cursor=cursor)
        surface = pygame.Surface((operand.get_width()+15, operand.get_height()+5), pygame.SRCALPHA)
        pygame.draw.lines(surface, constants.BLACK, False, [(0, surface.get_height()-10), (5, surface.get_height()), (10, 0), (surface.get_width(), 0)], width=2)
        surface.blit(operand, (10, 5))
        return pygame.transform.smoothscale(surface, tuple(i*scale for i in surface.get_size()))
    
    def evaluate(self, angle_mode="RAD"):
        return lambda x, a=self.operand.evaluate(angle_mode): math.sqrt(a(x))
    
class CubeRoot(UnaryOperator):
    def __init__(self):
        super().__init__()

    def render(self, scale=1, cursor=Cursor(None)):
        operator = Number(3).render(scale=0.7, cursor=cursor)
        operand = self.operand.render(scale=0.95, cursor=cursor)
        surface = pygame.Surface((operand.get_width()+10+operator.get_width(), operand.get_height()+10), pygame.SRCALPHA)
        pygame.draw.lines(surface, constants.BLACK, False, [(operator.get_width()-5, surface.get_height()-10), (operator.get_width(), surface.get_height()), (operator.get_width()+5, 5), (surface.get_width(), 5)], width=2)
        surface.blit(operand, (operator.get_width()+5, 10))
        surface.blit(operator, (0, 0))
        return pygame.transform.smoothscale(surface, tuple(i*scale for i in surface.get_size()))
    
    def evaluate(self, angle_mode="RAD"):
        return lambda x, a=self.operand.evaluate(angle_mode): math.copysign(abs(a(x)) ** (1/3), a(x))
    
class Trig(UnaryOperator):
    def __init__(self, function):
        super().__init__()
        self.type = function

    def render(self, scale=1, cursor=Cursor(None)):
        operand = self.operand.render(cursor=cursor)
        operand = pygame.transform.smoothscale(operand, tuple(i*scale for i in operand.get_size()))
        pixel_size = 30*scale
        font = get_font(pixel_size)
        text1 = font.render(f"{self.type.lower()}(", True, constants.BLACK)
        text2 = font.render(")", True, constants.BLACK)
        surface = pygame.Surface((text1.get_width()+5+text2.get_width()+operand.get_width(), max(operand.get_height(), text1.get_height())), pygame.SRCALPHA)
        surface.blit(text1, (0, 0))
        surface.blit(operand, (text1.get_width()+2.5, 0))
        surface.blit(text2, (text1.get_width()+operand.get_width()+5, 0))
        return surface
    
    def evaluate(self, angle_mode="RAD"):
        if angle_mode == "RAD":
            if self.type == "SIN":
                return lambda x, a=self.operand.evaluate(angle_mode): math.sin(a(x))
            elif self.type == "COS":
                return lambda x, a=self.operand.evaluate(angle_mode): math.cos(a(x))
            elif self.type == "TAN":
                return lambda x, a=self.operand.evaluate(angle_mode): math.tan(a(x))
            elif self.type == "CSC":
                return lambda x, a=self.operand.evaluate(angle_mode): 1/math.sin(a(x))
            elif self.type == "SEC":
                return lambda x, a=self.operand.evaluate(angle_mode): 1/math.cos(a(x))
            elif self.type == "COT":
                return lambda x, a=self.operand.evaluate(angle_mode): 1/math.tan(a(x))
        elif angle_mode == "DEG":
            if self.type == "SIN":
                return lambda x, a=self.operand.evaluate(angle_mode): math.sin(math.radians(a(x)))
            elif self.type == "COS":
                return lambda x, a=self.operand.evaluate(angle_mode): math.cos(math.radians(a(x)))
            elif self.type == "TAN":
                return lambda x, a=self.operand.evaluate(angle_mode): math.tan(math.radians(a(x)))
            elif self.type == "CSC":
                return lambda x, a=self.operand.evaluate(angle_mode): 1/math.sin(math.radians(a(x)))
            elif self.type == "SEC":
                return lambda x, a=self.operand.evaluate(angle_mode): 1/math.cos(math.radians(a(x)))
            elif self.type == "COT":
                return lambda x, a=self.operand.evaluate(angle_mode): 1/math.tan(math.radians(a(x)))
            
class Ln(UnaryOperator):
    def __init__(self):
        super().__init__()

    def render(self, scale=1, cursor=Cursor(None)):
        operand = self.operand.render(cursor=cursor)
        operand = pygame.transform.smoothscale(operand, tuple(i*scale for i in operand.get_size()))
        pixel_size = 30*scale
        font = get_font(pixel_size)
        text1 = font.render("ln(", True, constants.BLACK)
        text2 = font.render(")", True, constants.BLACK)
        surface = pygame.Surface((text1.get_width()+5+text2.get_width()+operand.get_width(), max(operand.get_height(), text1.get_height())), pygame.SRCALPHA)
        surface.blit(text1, (0, 0))
        surface.blit(operand, (text1.get_width()+2.5, 0))
        surface.blit(text2, (text1.get_width()+operand.get_width()+5, 0))
        return surface
    
    def evaluate(self, angle_mode="RAD"):
        return lambda x, a=self.operand.evaluate(angle_mode): math.log(a(x))
    
class Log10(UnaryOperator):
    def __init__(self):
        super().__init__()

    def render(self, scale=1, cursor=Cursor(None)):
        operand = self.operand.render(cursor=cursor)
        operand = pygame.transform.smoothscale(operand, tuple(i*scale for i in operand.get_size()))
        pixel_size = 30*scale
        font = get_font(pixel_size)
        text1 = font.render("log(", True, constants.BLACK)
        text2 = font.render(")", True, constants.BLACK)
        surface = pygame.Surface((text1.get_width()+5+text2.get_width()+operand.get_width(), max(operand.get_height(), text1.get_height())), pygame.SRCALPHA)
        surface.blit(text1, (0, 0))
        surface.blit(operand, (text1.get_width()+2.5, 0))
        surface.blit(text2, (text1.get_width()+operand.get_width()+5, 0))
        return surface
    
    def evaluate(self, angle_mode="RAD"):
        return lambda x, a=self.operand.evaluate(angle_mode): math.log10(a(x))

class Squared(UnaryOperator):
    def __init__(self):
        super().__init__()

    def render(self, scale=1, cursor=Cursor(None)):
        operand = self.operand.render(cursor=cursor)
        operator = Number(2).render(scale=0.7, cursor=cursor)
        surface = pygame.Surface((operand.get_width()+operator.get_width(), operand.get_height()), pygame.SRCALPHA)
        surface.blit(operand, (0, 2.5)) #slight offset
        surface.blit(operator, (operand.get_width(), 0))
        return pygame.transform.smoothscale(surface, tuple(i*scale for i in surface.get_size()))
    
    def evaluate(self, angle_mode="RAD"):
        return lambda x, a=self.operand.evaluate(angle_mode): a(x) ** 2
    
class Cubed(UnaryOperator):
    def __init__(self):
        super().__init__()

    def render(self, scale=1, cursor=Cursor(None)):
        operand = self.operand.render(cursor=cursor)
        operator = Number(3).render(scale=0.7, cursor=cursor)
        surface = pygame.Surface((operand.get_width()+operator.get_width(), operand.get_height()), pygame.SRCALPHA)
        surface.blit(operand, (0, 2.5))
        surface.blit(operator, (operand.get_width(), 0))
        return pygame.transform.smoothscale(surface, tuple(i*scale for i in surface.get_size()))
    
    def evaluate(self, angle_mode="RAD"):
        return lambda x, a=self.operand.evaluate(angle_mode): a(x) ** 3


class Operand(Object):
    def __init__(self, value):
        super().__init__()
        self.value = str(value)
        self.rendered_value = self.value

    def render(self, scale=1, cursor=Cursor(None)): #cursor default arg so that it can be passed through all the render operations without distinguishing type
        pixel_size = 30*scale #dynamic font size instead of smoothscale after
        font = get_font(pixel_size)
        surface = font.render(self.rendered_value, True, constants.BLACK)
        return surface

class Number(Operand):
    def __init__(self, value):
        super().__init__(value)
        self.type = "number"

class Symbol(Operand):
    def __init__(self, value):
        super().__init__(value)
        self.type = "symbol"

        if self.value == "*":
            self.rendered_value = "x"
        elif self.value == "/":
            self.rendered_value = "÷"

class Bracket(Operand):
    def __init__(self, value):
        super().__init__(value)
        self.type = "bracket"

class Variable(Operand):
    def __init__(self, value):
        super().__init__(value)
        self.type = "variable"

        if self.value == "x":
            self.rendered_value = "𝑥"

class Constant(Operand):
    def __init__(self, value):
        super().__init__(value)
        self.type = "variable" #treated as variable by evaluator
        
        if self.value == "PI":
            self.rendered_value = "π"
        elif self.value == "E":
            self.rendered_value = "e"