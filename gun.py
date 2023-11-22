import math
from random import choice
from random import randint

import pygame


FPS = 30

RED = 0xFF0000
BLUE = 0x0000FF
YELLOW = 0xFFC91F
GREEN = 0x00FF00
MAGENTA = 0xFF03B8
CYAN = 0x00FFCC
BLACK = (0, 0, 0)
WHITE = 0xFFFFFF
GREY = 0x7D7D7D
GAME_COLORS = [YELLOW, GREEN, MAGENTA, CYAN]

WIDTH = 800
HEIGHT = 600


class Ball:
    def __init__(self, screen: pygame.Surface, color, vx = 0, vy = 0, x=40, y=450):
        """ Конструктор класса ball

        Args:
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
        """
        self.screen = screen
        self.x = x
        self.y = y
        self.r = 10
        self.vx = vx
        self.vy = vy
        self.color = color
        self.live = 200

    def move(self):
        """Переместить мяч по прошествии единицы времени.

        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
        и стен по краям окна (размер окна 800х600).
        """
        self.x += self.vx
        self.vy -= 1
        self.y -= self.vy
        self.live -=1
        if self.x >=780 or self.x <=20:
            self.vx = -self.vx
        if self.y >=550 or self.y<= 20:
            self.vy = -0.75*self.vy+1
            self.vx = 0.75*self.vx

    def draw(self):
        pygame.draw.circle(
            self.screen,
            self.color,
            (self.x, self.y),
            self.r
        )

    def hittest(self, obj):
        """Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.

        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """
        if (self.x-obj.x)**2 + (self.y-obj.y)**2<=(self.r+obj.r)**2:
            return True
        else:
            return False



class Gun:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.f2_power = 10
        self.f2_on = 0
        self.an = 1
        self.color = GREY
        self.rect = 0
        self.x = 0
        self.y = 450

    def fire2_start(self, event):
        self.f2_on = 1

    def fire2_end(self, event):
        """Выстрел мячом.

        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        global balls, bullet
        bullet += 1
        new_ball = Ball(self.screen, choice(GAME_COLORS))
        new_ball.r += 5
        self.an = math.atan2((event.pos[1]-new_ball.y), (event.pos[0]-new_ball.x))
        new_ball.vx = self.f2_power * math.cos(self.an)
        new_ball.vy = - self.f2_power * math.sin(self.an)
        balls.append(new_ball)
        self.f2_on = 0
        self.f2_power = 10

    def targetting(self, event):
        """Прицеливание. Зависит от положения мыши."""
        if event:
            self.an = math.atan2((event.pos[1]-450), (event.pos[0]-20))
        if self.f2_on:
            self.color = RED
        else:
            self.color = GREY

    def draw(self):
        pygame.draw.line(
            self.screen,
            self.color,
            (self.x, self.y),
            (self.x + (self.f2_power + 10) * math.cos(self.an),
             self.y + (self.f2_power + 10) * math.sin(self.an)),
            6
        )

    def power_up(self):
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 1
            self.color = YELLOW
        else:
            self.color = GREY


class Target_classic:
    # self.points = 0
    # self.live = 1
    # self.new_target()

    def __init__(self, screen: pygame.Surface):
        """
        """
        self.screen = screen
        self.r = randint(20, 50)
        self.x = randint(600, 780)
        self.y = randint(self.r+1, 540-self.r)
        self.color = RED
        self.live = 1
        self.vy = randint(0,10)

    def hit(self, point=1):
        """Попадание шарика в цель."""
        global points
        points += point

    def move(self):
        """Переместить мяч по прошествии единицы времени.

        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
        и стен по краям окна (размер окна 800х600).
        """
        self.y -= self.vy
        if self.y >= 540 - self.r or self.y <= self.r:
            self.vy = -self.vy

    def draw(self):
        pygame.draw.circle(
            self.screen,
            self.color,
            (self.x, self.y),
            self.r
        )

class Target_jumping:
    # self.points = 0
    # self.live = 1
    # self.new_target()

    def __init__(self, screen: pygame.Surface):
        """
        """
        self.screen = screen
        self.r = randint(20, 50)
        self.x = randint(600, 780)
        self.y = randint(self.r, 540-self.r)
        self.color = BLUE
        self.period = randint(30, 60)
        self.time = self.period
        self.live = 1

    def hit(self, point=1):
        """Попадание шарика в цель."""
        global points
        points += point

    def move(self):
        """Переместить мяч по прошествии единицы времени.

        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
        и стен по краям окна (размер окна 800х600).
        """
        self.time -= 1
        if self.time == 0:
            self.y = randint(self.r, 540 - self.r)
            self.time = self.period

    def draw(self):
        pygame.draw.circle(
            self.screen,
            self.color,
            (self.x, self.y),
            self.r
        )

class Target_static:
    # self.points = 0
    # self.live = 1
    # self.new_target()

    def __init__(self, screen: pygame.Surface):
        """
        """
        self.screen = screen
        self.r = randint(20, 50)
        self.x = randint(600, 780)
        self.y = randint(self.r, 540-self.r)
        self.color = BLACK
        self.live = 1

    def hit(self, point=1):
        """Попадание шарика в цель."""
        global points
        points += point

    def move(self):
        """
        """
        pass

    def draw(self):
        pygame.draw.circle(
            self.screen,
            self.color,
            (self.x, self.y),
            self.r
        )


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
bullet = 0
balls = []
targets = []
points = 0

clock = pygame.time.Clock()
gun = Gun(screen)
targets.append(Target_classic(screen))
targets.append(Target_jumping(screen))
targets.append(Target_static(screen))
targets.append(Target_static(screen))
targets.append(Target_static(screen))
finished = False



while not finished:
    screen.fill(WHITE)
    fonts = [pygame.font.SysFont('times new roman', 20)]
    text1 = fonts[0].render("Your score is: "+str(points), True, BLACK)
    screen.blit(text1, (0, 0))
    gun.draw()
    for target in targets:
        target.draw()
    for b in balls:
        b.draw()
    pygame.display.update()

    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            gun.fire2_start(event)
        elif event.type == pygame.MOUSEBUTTONUP:
            gun.fire2_end(event)
        elif event.type == pygame.MOUSEMOTION:
            gun.targetting(event)

    for target in targets:
        target.move()
    for b in balls:
        b.move()
        for target in targets:
            if b.hittest(target) and target.live:
                target.live = 0
                target.hit()
                if b.color == MAGENTA:
                    b.live = 0
                elif b.color == CYAN:
                    b.live = 0
                    b.r = 100
                    for t in targets:
                        if b.hittest(t) and target.live:
                            target.live = 0
                            target.hit()
                            t.__init__(screen)
                            if isinstance(t, Target_classic) and len(targets)<=10:
                                targets.append(Target_jumping(screen))
                                targets[-1].draw()
                            if isinstance(t, Target_jumping) and len(targets)<=10:
                                targets.append(Target_classic(screen))
                                targets[-1].draw()

                elif b.color == YELLOW:
                    b.live = 0
                    for i in range(3):
                        balls.append(Ball(screen, MAGENTA, randint(-10, 10), randint(-5, 5), b.x, b.y))
                target.__init__(screen)
                if isinstance(target, Target_classic) and len(targets)<=10:
                    targets.append(Target_jumping(screen))
                    targets[-1].draw()
                if isinstance(target, Target_jumping) and len(targets)<=10:
                    targets.append(Target_classic(screen))
                    targets[-1].draw()

        if b.live <= 0:
            balls.remove(b)
    gun.power_up()

pygame.quit()
