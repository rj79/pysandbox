"""
A small framework for experimentation and visualization. Draws some inspiration
from JavaFX.
"""
from pyglet.window import Window, key
import pyglet
from pyglet.gl import glColor4f, glLineWidth, glBegin, glEnd, glVertex2f
from pyglet.gl import glClearColor, glEnable, glBlendFunc
from pyglet.gl import GL_BLEND, GL_TRIANGLE_FAN, GL_LINES, GL_LINE_LOOP
from pyglet.gl import GL_ONE_MINUS_SRC_ALPHA, GL_SRC_ALPHA
from pyglet.gl import GL_ONE_MINUS_DST_ALPHA, GL_DST_ALPHA
from math import pi, cos, sin, sqrt

class Point:
    def __init__(self, *args):
        self.x = 0
        self.y = 0
        self.set(*args)

    def set(self, *args):
        if len(args) == 0:
            self.x = 0
            self.y = 0
        elif len(args) == 1 and type(args[0]) == Point:
            self.x = args[0].x
            self.y = args[0].y
        elif len(args) == 2:
            self.x = args[0]
            self.y = args[1]

    def distance(self, other):
        dx = self.x - other.x
        dy = self.y - other.y
        return sqrt(dx * dx + dy * dy)

    def __repr__(self):
        return "<Point {} {}>".format(float(self.x), float(self.y))


class GraphicsContext:
    def __init__(self):
        self._stroke_color = (1, 1, 1, 1)
        self._fill_color = (1, 1, 1, 1)
        self._line_width = 1

    def _color(self, *args):
        c = list(*args)
        if len(c) == 3:
            c.append(1)
        return c

    def set_fill(self, *args):
        self._fill_color = self._color(args)

    def set_stroke(self, *args):
        self._stroke_color = self._color(args)

    def set_line_width(self, width):
        self._line_width = width

    def _circle(self, x, y, r, color, filled):
        c = int(2 * r * pi)
        iterations = c / 2

        s = sin(2 * pi / iterations)
        c = cos(2 * pi / iterations)

        dx, dy = r, 0

        glColor4f(*color)
        if filled:
            glBegin(GL_TRIANGLE_FAN)
            glVertex2f(x, y)
        else:
            glLineWidth(self._line_width)
            glBegin(GL_LINE_LOOP)
            glVertex2f(x + dx, y + dy)

        for i in range(int(iterations) + 1):
            glVertex2f(x + dx, y + dy)
            dx, dy = (dx * c - dy * s), (dy * c + dx * s)
        glEnd()

    def stroke_circle(self, x, y, r):
        self._circle(x, y, r, self._stroke_color, False)

    def fill_circle(self, x, y, r):
        self._circle(x, y, r, self._fill_color, True)

    def line(self, x1, y1, x2, y2):
        glColor4f(*self._stroke_color)
        glLineWidth(self._line_width)
        glBegin(GL_LINES)
        glVertex2f(x1, y1)
        glVertex2f(x2, y2)
        glEnd()


class Application(Window):
    def __init__(self):
        self._width = 800;
        self._height = 600;
        super().__init__(width=self._width,
                         height=self._height,
                         resizable=False,
                         vsync=False)

        glClearColor(0.0, 0.05, 0.2, 1.0)
        glEnable(GL_BLEND)
        glBlendFunc(GL_DST_ALPHA, GL_ONE_MINUS_DST_ALPHA)

        self._gc = GraphicsContext()
        pyglet.clock.schedule_interval(self._main_loop, 1 / 100)

    def _main_loop(self, dt):
        self.do_update(dt)
        self.do_draw(self._gc)

    def get_width(self):
        return self._width

    def get_height(self):
        return self._height

    def do_init(self, gc):
        pass

    def do_update(self, dt):
        pass

    def do_draw(self, gc):
        pass

    def on_draw(self):
        # Ignore
        pass

    def on_mouse_motion(self, x, y, dx, dy):
        #print(x, y, dx, dy)
        pass

    def on_mouse_press(self, x, y, button, modifiers):
        print(x, y, button, modifiers)

    def on_mouse_release(self, x, y, button, modifiers):
        print(x, y, button, modifiers)

    def on_key_press(self, symbol, modifiers):
        if symbol == key.ESCAPE:
            self.stop()
        else:
            print(symbol, modifiers)

    def on_key_release(self, symbol, modifiers):
        print(symbol, modifiers)

    def stop(self):
        pyglet.app.exit()

    def start(self):
        self.do_init()
        pyglet.app.run()
