from sandbox import Application, Point, key
import numpy as np
import math

SPEED = 0.06
SPEEDSTEP = 0.02

class FunctionPlot:
    def __init__(self, pixel_width, pixel_height):
        self.xmin = -10
        self.xmax = 10
        self.ymin = -10
        self.ymax = 10
        self.pwidth = pixel_width
        self.pheight = pixel_height
        self.functions = []

    def add_function(self, func, color):
        self.functions.append((func, color))

    def set_xrange(self, xmin, xmax):
        self.xmin = xmin
        self.xmax = xmax 

    def draw_axis(self, gc):
        gc.set_stroke(1, 1, 1, 1)
        gc.lines(Point(0, self.pheight / 2), Point(self.pwidth, self.pheight / 2))
        gc.lines(Point(self.pwidth / 2), Point(0, self.pwidth / 2, self.pheight))

    def do_draw(self, gc):
        def scale(point):
            xw = self.xmax - self.xmin
            yw = self.ymax - self.ymin
            return Point(point[0] * self.pwidth / xw + self.pwidth / 2, point[1] * self.pheight / yw + self.pheight / 2)

        self.draw_axis(gc)
        for func, color in self.functions:
            points = func.evaluate(self.xmin, self.xmax)
            gc.set_stroke(*color)
            for point in points:
                gc.lines(*[scale(point) for point in points])

class Sin:
    def evaluate(self, xmin, xmax):
        points = []
        for x in np.linspace(xmin, xmax, 100):
            y = math.sin(x)
            points.append((x, y))
        return points

class Polynomial:
    def __init__(self, coeffs=[]):
        self.coeffs = coeffs

    def evaluate(self, xmin, xmax):
        points = []
        for x in np.linspace(xmin, xmax, 100):
            y = 0
            power = 0
            for coeff in self.coeffs:
                y += coeff * (x ** power)
                power += 1
            points.append((x, y))
        return points


    def set_coeffs(self, coeffs):
        self.coeffs = coeffs

    def set_coeff(self, index, value):
        if index < 0:
            return
        if index > len(self.coeffs):
            while len(self.coeffs) < index + 1:
                self.coeffs.append(0)
            self.coeffs[index] = value

class CoeffModifier:
    def __init__(self, poly, coeffs):
        self.polynomial = poly
        self.coeffs = coeffs
        self.factors = [0] * len(coeffs)
        self.factor_index = 0

    def next_factor_index(self):
        index = self.factor_index + 1
        while index < len(self.coeffs):
            if self.coeffs[index] != 0:
                return index
            index += 1
        return self.factor_index

    def previous_factor_index(self):
        index = self.factor_index - 1
        while index > 0:
            if self.coeffs[index] != 0:
                return index
            index -= 1
        return self.factor_index

    def apply(self):
        self.polynomial.set_coeffs([factor * coeff for factor, coeff in zip(self.factors, self.coeffs)])

    def better(self):
        if self.coeffs[self.factor_index] == 0 or self.factors[self.factor_index] > 0.999:
            self.factors[self.factor_index] = 1
            self.factor_index = self.next_factor_index()
        
        if self.factors[self.factor_index] < 0.999:
            self.factors[self.factor_index] += SPEED

        self.apply()

    def worse(self):
        if self.factors[self.factor_index] > 0.001:
            self.factors[self.factor_index] -= SPEED

        if self.coeffs[self.factor_index] == 0 or self.factors[self.factor_index] < 0.001:
            self.factors[self.factor_index] = 0
            self.factor_index = self.previous_factor_index()

        self.apply()

def sin_factors(n):
    factors = []
    for i in range(n):
        f = (i % 2) / math.factorial(i)
        if i % 4 == 3:
            f = -f
        factors.append(f)
    return factors

class App(Application):
    def do_init(self):
        self.funcplot = FunctionPlot(self.get_width(), self.get_height())
        self.sin = Sin()
        p = sin_factors(29)
        self.better = True
        self.approx = Polynomial(p)
        self.modifier = CoeffModifier(self.approx, p)
        self.funcplot.add_function(self.sin, (1, 1, 0, 0.5))
        self.funcplot.add_function(self.approx, (0, 1, 0, 0.5))

        self.better = True
        self.worse = False
        self.pause = False
        self.auto = True

        self.modifier.apply()

    def do_update(self, dt):
        if not self.pause:
            if self.better:
                self.modifier.better()
            elif self.worse:
                self.modifier.worse()


    def do_draw(self, gc):
        self.clear()
        self.funcplot.do_draw(gc)
 
    def do_key_press(self, symbol, modifiers):
        global SPEED, SPEEDSTEP
        if symbol == key.LEFT:
            self.better = False
            self.worse = True
        if symbol == key.UP:
            SPEED += SPEEDSTEP
            if SPEED > 1:
                SPEED = 1
        elif symbol == key.RIGHT:
            self.better = True
            self.worse = False
        if symbol == key.DOWN:
            SPEED -= SPEEDSTEP
            if SPEED < 0:
                SPEED = 0
        elif symbol == key.SPACE:
            self.pause = not self.pause
        elif symbol == key.ENTER:
            self.auto = not self.auto

    def do_key_release(self, symbol, modifiers):
        if symbol == key.LEFT:
            if not self.auto:
                self.worse = False
        elif symbol == key.RIGHT:
            if not self.auto:
                self.better = False

if __name__ == '__main__':
    app = App()
    app.start()
 
