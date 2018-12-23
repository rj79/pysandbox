from sandbox import Application, Point
import math
import pyglet
import numpy

#
# Credit for explanation and pseudeo-code for hex grids and coordinates goes to https: // www.redblobgames.com/grids/hexagons/
#

SIZE = 32

class Hex:
    def __init__(self, q=0, r=0):
        self.q = q
        self.r = r

    def __repr__(self):
        return '<Hex qr=(%d, %d)>' % (self.q, self.r)


class Cube:
    def __init__(self, q=0, r=0, s=0):
        self.q = q
        self.r = r
        self.s = s
    
    def __repr__(self):
        return '<Cube qrs=(%d, %d, %d)' % (self.q, self.r, self.s)

def cube_round(cube):
    rq = round(cube.q)
    rr = round(cube.r)
    rs = round(cube.s)

    q_diff = abs(rq - cube.q)
    r_diff = abs(rr - cube.r)
    s_diff = abs(rs - cube.s)

    if q_diff > r_diff and q_diff > s_diff:
        rq = -rr - rs
    elif r_diff > s_diff:
        rr = -rq - rs
    else:
        rs = -rq - rr

    return Cube(rq, rr, rs)

def hex_round(hex):
    return cube_to_axial(cube_round(axial_to_cube(hex)))


def point_to_hex(point):
    q = (2 / 3 * point.x) / SIZE
    r = (-1 / 3 * point.x + math.sqrt(3) / 3 * point.y) / SIZE 
    return Hex(q, r)

def hex_to_point(hex):
    return Point(3 / 2 * SIZE * hex.q, math.sqrt(3) / 2 *
          SIZE * hex.q + math.sqrt(3) * SIZE * hex.r)

def cube_to_axial(cube):
    q = cube.q
    r = cube.s
    return Hex(q, r)

def axial_to_cube(hex):
    q = hex.q
    s = hex.r
    r = -q - s
    return Cube(q, r, s)

def flat_hex_corner(center, size, i):
    angle_deg = 60 * i
    angle_rad = angle_deg * math.pi / 180
    return Point(center.x + size * math.cos(angle_rad),
                 center.y + size * math.sin(angle_rad))

def draw_hex(gc, hex, size):
    vertices = [flat_hex_corner(hex_to_point(hex), size, i) for i in range(0, 6)]
    gc.line_loop(*vertices)

def label(text, point):
    return pyglet.text.Label(text,
                      font_name='Mono',
                      font_size=14,
                      x=point.x, y=point.y,
                      anchor_x='left', anchor_y='center')


class App(Application):
    def do_init(self):
        self.hoverhex = None
        self.coord_text = None
        h = math.sqrt(3) * SIZE
        w = 2 * SIZE
        even = True

        self.hexes = {}
        for j in range(0, int((self.get_height() + h) / (h / 2))):  
            for i in range(0, int((self.get_width() + w) / (w * 1.5))):
                x = i * SIZE * 3 + (j % 2) * SIZE * 1.5
                y = j * h / 2
                hex = hex_round(point_to_hex(Point(x, y)))
                self.hexes[(hex.q, hex.r)] = hex
    
        
    def do_mouse_motion(self, point, dx, dy):
        hex = hex_round(point_to_hex(point))
        try:
            self.hoverhex = self.hexes[(hex.q, hex.r)]
        except KeyError:
            print('No Hex found at ', hex.q, hex.r)
        self.coord_text = label('xy=(%d, %d), qr=(%d, %d)' % (point.x, point.y, hex.q, hex.r), Point(40, self.get_height() - 40))

    def do_draw(self, gc):
        self.clear()

        gc.set_stroke(0.5, 0.5, 0, 1)
        for hex in self.hexes.values():
            draw_hex(gc, hex, SIZE)

        gc.set_stroke(1, 1, 0, 1)
        if self.coord_text:
            self.coord_text.draw()


        if self.hoverhex:
            gc.set_stroke(1, 1, 1, 1)
            draw_hex(gc, self.hoverhex, SIZE) 
        gc.set_stroke(0, 1, 0, 1)
        mouse = self.mouse
        gc.stroke_circle(mouse.pos, 11)

if __name__ == '__main__':
    app = App()
    app.start()
