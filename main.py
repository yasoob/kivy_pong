from kivy.app import App
from kivy.uix.widget import Widget
from kivy.vector import Vector
from kivy.clock import Clock
from kivy.properties import NumericProperty, ReferenceListProperty,\
    ObjectProperty
import time


class PongPaddle(Widget):
    score = NumericProperty(0)
    time_bounce = time.time()

    def bounce_ball(self, ball):
        if self.collide_widget(ball):
            # print "Rounded Time: ", round(time.time() - self.time_bounce)
            # if round(time.time() - self.time_bounce) > 0:
            # if (ball.center_x - 50 > -10) and (ball.center_x + 50 < 0)
            vx, vy = ball.velocity
            offset = (ball.center_y - self.center_y) / (self.height / 2)
            print "\n\nPoints:"
            total_width = self.x + 200
            print "Ball Position: ",ball.pos
            print "Ball Center-y: ",ball.center_y-50
            print "Ball Center-x  ",ball.center_x-50
            print "Ball Center-x  ",ball.center_x+50
            print "Self Center-y  ",self.center_y+200
            print "Self Center-x  ",self.center_x+25
            print "Self Center-x  ",self.center_x-25
            print "Total Width:   ",total_width
            print "Paddle x       ",self.x
            if (ball.center_y+50 < total_width) or (ball.center_y-50 > self.x-200):
                bounced = Vector(-1 * vx, vy)
                vel = bounced * 1.1
                ball.velocity = vel.x, vel.y + offset
#           self.time_bounce = time.time()


class PongBall(Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    def move(self):
        self.pos = Vector(*self.velocity) + self.pos


class PongGame(Widget):
    ball = ObjectProperty(None)
    player1 = ObjectProperty(None)
    player2 = ObjectProperty(None)

    def serve_ball(self, vel=(4, 0)):
        self.ball.center = self.center
        self.ball.velocity = vel

    def update(self, dt):
        self.ball.move()

        # bounce of paddles
        self.player1.bounce_ball(self.ball)
        self.player2.bounce_ball(self.ball)

        # bounce ball off bottom or top
        if (self.ball.y < self.y) or (self.ball.top > self.top):
            self.ball.velocity_y *= -1

        # went of to a side to score point?
        if self.ball.x < self.x:
            self.player2.score += 1
            self.serve_ball(vel=(4, 0))
        if self.ball.x > self.width:
            self.player1.score += 1
            self.serve_ball(vel=(-4, 0))

    def on_touch_move(self, touch):
        if touch.x < self.width / 3:
            self.player1.center_y = touch.y
        if touch.x > self.width - self.width / 3:
            self.player2.center_y = touch.y


class PongApp(App):
    def build(self):
        game = PongGame()
        game.serve_ball()
        Clock.schedule_interval(game.update, 1.0 / 60.0)
        return game


if __name__ == '__main__':
    PongApp().run()
