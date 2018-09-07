"""
A small framework for experimentation and visualization. Draws some inspiration
from JavaFX.
"""
from pyglet.window import Window, key
import pyglet
from pyglet.gl import glColor4f, glLineWidth, glBegin, glEnd, glHint
from pyglet.gl import glVertex2f, glClearColor, glEnable, glBlendFunc
from pyglet.gl import glRectf
from pyglet.gl import GL_BLEND, GL_TRIANGLE_FAN, GL_LINES, GL_LINE_LOOP
from pyglet.gl import GL_ONE_MINUS_SRC_ALPHA, GL_SRC_ALPHA
from pyglet.gl import GL_ONE_MINUS_DST_ALPHA, GL_DST_ALPHA
from pyglet.gl import GL_POINT_SMOOTH, GL_POINT_SMOOTH_HINT
from pyglet.gl import GL_LINE_SMOOTH, GL_LINE_SMOOTH_HINT
from pyglet.gl import GL_POLYGON_SMOOTH, GL_POLYGON_SMOOTH_HINT, GL_NICEST
from pyglet.gl import GL_POINTS

from math import pi, cos, sin, sqrt
import os

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
        glEnable(GL_POINT_SMOOTH)
        glEnable(GL_LINE_SMOOTH)
        glEnable(GL_POLYGON_SMOOTH)
        glHint(GL_POINT_SMOOTH_HINT, GL_NICEST)
        glHint(GL_LINE_SMOOTH_HINT, GL_NICEST)
        glHint(GL_POLYGON_SMOOTH_HINT, GL_NICEST)

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
        c = 2 * r * pi
        iterations = int(c / 2)

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

    def fill_rect(self, x, y, w, h):
        glColor4f(*self._fill_color)
        glRectf(x, y, x + w, y + h)

    def stroke_rect(self, x, y, w, h):
        glColor4f(*self._stroke_color)
        glBegin(GL_LINE_LOOP)
        glVertex2f(x, y)
        glVertex2f(x + w, y)
        glVertex2f(x + w, y + h)
        glVertex2f(x, y + h)
        glEnd()

    def line(self, x1, y1, x2, y2):
        glColor4f(*self._stroke_color)
        glLineWidth(self._line_width)
        glBegin(GL_LINES)
        glVertex2f(x1, y1)
        glVertex2f(x2, y2)
        glEnd()

    def point(self, x, y):
        glColor4f(*self._stroke_color)
        glBegin(GL_POINTS)
        glVertex2f(x, y)
        glEnd()

class Mouse:
    def __init__(self):
        self._buttons = [False] * 8
        self._x = 0
        self._y = 0
        self._dx = 0
        self._dy = 0

    @property
    def left_button(self):
        return self._buttons[1]

    @property
    def middle_button(self):
        return self._buttons[2]

    @property
    def right_button(self):
        return self._buttons[4]

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def pos(self):
        return (self._x, self._y)


class Application(Window):
    def __init__(self):
        self._width = 800;
        self._height = 600;
        super().__init__(width=self._width,
                         height=self._height,
                         resizable=False,
                         vsync=False)

        self._mouse = Mouse()

        self._debug = False
        try:
            if os.environ['DEBUG'] in ('1', 'TRUE', 'True'):
                self.push_handlers(pyglet.window.event.WindowEventLogger())
                self._debug = True
        except KeyError:
            pass

        glClearColor(0.0, 0.05, 0.2, 1.0)
        glEnable(GL_BLEND)
        glBlendFunc(GL_DST_ALPHA, GL_ONE_MINUS_DST_ALPHA)

        self._gc = GraphicsContext()
        pyglet.clock.schedule_interval(self._main_loop, 1 / 60)
        self.set_mouse_visible(False)

    @property
    def debug(self):
        return self._debug

    def _main_loop(self, dt):
        self.do_update(dt)

    def get_width(self):
        return self._width

    def get_height(self):
        return self._height

    def do_init(self):
        pass

    def do_update(self, dt):
        pass

    def do_draw(self, gc):
        pass

    def do_mouse_motion(self, x, y, dx, dy):
        pass

    def do_mouse_press(self, x, y, button, modifiers):
        pass

    def do_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        pass

    def do_mouse_release(self, x, y, button, modifiers):
        pass

    def on_draw(self):
        self.do_draw(self._gc)

    @property
    def mouse(self):
        return self._mouse

    def on_mouse_motion(self, x, y, dx, dy):
        self.mouse._x = x
        self.mouse._y = y
        self.mouse._dx = dx
        self.mouse._dy = dy
        self.do_mouse_motion(x, y, dx, dy)

    def on_mouse_press(self, x, y, button, modifiers):
        self.mouse._buttons[button] = True
        self.do_mouse_press(x, y, button, modifiers)

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        self.mouse._x = x
        self.mouse._y = y
        self.mouse._dx = dx
        self.mouse._dy = dy
        self.do_mouse_drag(x, y, dx, dy, buttons, modifiers)

    def on_mouse_release(self, x, y, button, modifiers):
        self.mouse._buttons[button] = False
        self.do_mouse_release(x, y, button, modifiers)

    def on_key_press(self, symbol, modifiers):
        if symbol == key.ESCAPE:
            self.stop()
        else:
            pass

    def on_key_release(self, symbol, modifiers):
        pass

    def stop(self):
        pyglet.app.exit()

    def start(self):
        self.do_init()
        pyglet.app.run()
