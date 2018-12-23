import sandbox

class MyApp(sandbox.Application):
    def do_init(self):
        self.radius = 10
        self.pos = sandbox.Point()
        self.dx = 2
        self.dy = 3

    def do_update(self, dt):
        self.pos.x += self.dx
        if self.pos.x < self.radius:
            self.pos.x = self.radius - self.pos.x
            self.dx = -self.dx
        if self.pos.x > self.get_width() - self.radius:
            self.pos.x = self.pos.x - (self.pos.x - (self.get_width() - self.radius))
            self.dx = -self.dx

        self.pos.y += self.dy
        if self.pos.y < self.radius:
            self.pos.y = self.radius - self.pos.y
            self.dy = -self.dy
        if self.pos.y > self.get_height() - self.radius:
            self.pos.y = self.pos.y - (self.pos.y - (self.get_height() - self.radius))
            self.dy = -self.dy


    def do_draw(self, gc):
        self.clear()
        gc.set_fill(1, 1, 0, 0.5)
        gc.fill_circle(self.pos, self.radius)


if __name__ == '__main__':
    app = MyApp()
    app.start()
