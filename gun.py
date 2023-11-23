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
DARK_GREEN = (0, 100, 0)
BROWN = (121, 85, 61)
LILY = (183, 132, 167)
GAME_COLORS = [YELLOW, GREEN, MAGENTA, CYAN]

WIDTH = 800
HEIGHT = 600


class Ball:
    def __init__(self, screen: pygame.Surface, color, x=40, y=450, vx=0, vy=0):
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
        self.live -= 1
        if self.x >= 780 or self.x <= 20:
            self.vx = -self.vx
        if self.y >= 550:
            self.vy = -0.75*self.vy+1
            self.vx = 0.75*self.vx
        if self.y <= 20:
            self.vy = -self.vy
            self.vx = self.vx

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
        if (self.x-obj.x)**2 + (self.y-obj.y)**2 <= (self.r+obj.r)**2:
            return True
        else:
            return False


class Gun1:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.f2_power = 10
        self.f2_on = 0
        self.an = -1
        self.color = GREY
        self.rect = 0
        self.x = 40
        self.y = 530
        self.color_ball = choice(GAME_COLORS)
        self.live = 100
        self.r = 40

    def fire2_start(self):
        self.f2_on = 1

    def fire2_end(self):
        """Выстрел мячом.

        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        global balls1, bullet
        bullet += 1
        new_ball = Ball(self.screen, self.color_ball, self.x+10, self.y)
        new_ball.r += 5
        new_ball.vx = self.f2_power * math.cos(self.an)
        new_ball.vy = - self.f2_power * math.sin(self.an)
        balls1.append(new_ball)
        self.f2_on = 0
        self.f2_power = 10
        self.color_ball = choice(GAME_COLORS)

    def target_up(self):
        """Прицеливание. Против часовой"""
        if - math.pi + math.pi/180 <= self.an <= 0:
            self.an -= math.pi/180

    def target_down(self):
        """Прицеливание. По часовой."""
        if - math.pi <= self.an <= 0 - math.pi/180:
            self.an += math.pi/180

    def draw(self):
        pygame.draw.line(
            self.screen,
            self.color,
            (self.x, self.y),
            (self.x + (self.f2_power + 10) * math.cos(self.an),
             self.y + (self.f2_power + 10) * math.sin(self.an)),
            6
        )
        pygame.draw.circle(
            self.screen,
            GREY,
            (self.x, self.y+5),
            15
        )
        pygame.draw.rect(
            self.screen,
            GREY,
            pygame.Rect(self.x-40, self.y+5, 80, 20)
        )
        pygame.draw.circle(
            self.screen,
            GREY,
            (self.x, self.y + 30),
            10
        )
        pygame.draw.circle(
            self.screen,
            GREY,
            (self.x + 18, self.y + 30),
            10
        )
        pygame.draw.circle(
            self.screen,
            GREY,
            (self.x - 18, self.y + 30),
            10
        )
        pygame.draw.circle(
            self.screen,
            GREY,
            (self.x - 30, self.y + 27),
            6
        )
        pygame.draw.circle(
            self.screen,
            GREY,
            (self.x + 30, self.y + 27),
            6
        )

    def power_up(self):
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 1
            self.color = self.color_ball
        else:
            self.color = GREY

    def move_right(self):
        if 40 <= self.x < 200:
            self.x += 1

    def move_left(self):
        if 40 < self.x <= 200:
            self.x -= 1


class Gun2:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.f2_power = 10
        self.f2_on = 0
        self.an = -math.pi + 1
        self.color = DARK_GREEN
        self.rect = 0
        self.x = 760
        self.y = 530
        self.color_ball = choice(GAME_COLORS)
        self.live = 100
        self.r = 40

    def fire2_start(self):
        self.f2_on = 1

    def fire2_end(self):
        """Выстрел мячом.

        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        global balls2, bullet
        bullet += 1
        new_ball = Ball(self.screen, self.color_ball, self.x+10, self.y)
        new_ball.r += 5
        new_ball.vx = self.f2_power * math.cos(self.an)
        new_ball.vy = - self.f2_power * math.sin(self.an)
        balls2.append(new_ball)
        self.f2_on = 0
        self.f2_power = 10
        self.color_ball = choice(GAME_COLORS)

    def target_down(self):
        """Прицеливание. Против часовой"""
        if - math.pi + math.pi/180 <= self.an <= 0:
            self.an -= math.pi/180

    def target_up(self):
        """Прицеливание. По часовой."""
        if - math.pi <= self.an <= 0 - math.pi/180:
            self.an += math.pi/180

    def draw(self):
        pygame.draw.line(
            self.screen,
            self.color,
            (self.x, self.y),
            (self.x + (self.f2_power + 10) * math.cos(self.an),
             self.y + (self.f2_power + 10) * math.sin(self.an)),
            6
        )
        pygame.draw.circle(
            self.screen,
            DARK_GREEN,
            (self.x, self.y+5),
            15
        )
        pygame.draw.rect(
            self.screen,
            DARK_GREEN,
            pygame.Rect(self.x-40, self.y+5, 80, 20)
        )
        pygame.draw.circle(
            self.screen,
            DARK_GREEN,
            (self.x, self.y + 30),
            10
        )
        pygame.draw.circle(
            self.screen,
            DARK_GREEN,
            (self.x + 18, self.y + 30),
            10
        )
        pygame.draw.circle(
            self.screen,
            DARK_GREEN,
            (self.x - 18, self.y + 30),
            10
        )
        pygame.draw.circle(
            self.screen,
            DARK_GREEN,
            (self.x - 30, self.y + 27),
            6
        )
        pygame.draw.circle(
            self.screen,
            DARK_GREEN,
            (self.x + 30, self.y + 27),
            6
        )

    def power_up(self):

        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 1
            self.color = self.color_ball
        else:
            self.color = DARK_GREEN

    def move_right(self):
        if 600 <= self.x < 760:
            self.x += 1

    def move_left(self):
        if 600 < self.x <= 760:
            self.x -= 1


class TargetClassic:

    def __init__(self, screen: pygame.Surface):
        """
        """
        self.screen = screen
        self.r = randint(20, 50)
        self.x = randint(300, 480)
        self.y = randint(self.r+1, 540-self.r)
        self.color = RED
        self.live = 1
        self.vy = randint(1, 10)

    def hit1(self, point=1):
        """Попадание шарика в цель."""
        global points1
        points1 += point

    def hit2(self, point=1):
        """Попадание шарика в цель."""
        global points2
        points2 += point

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


class TargetJumping:

    def __init__(self, screen: pygame.Surface):
        """
        """
        self.screen = screen
        self.r = randint(20, 50)
        self.x = randint(300, 480)
        self.y = randint(self.r, 540-self.r)
        self.color = BLUE
        self.period = randint(30, 60)
        self.time = self.period
        self.live = 1

    def hit1(self, point=1):
        """Попадание шарика в цель."""
        global points1
        points1 += point

    def hit2(self, point=1):
        """Попадание шарика в цель."""
        global points2
        points2 += point

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


class TargetStatic:

    def __init__(self, screen: pygame.Surface):
        """
        """
        self.screen = screen
        self.r = randint(20, 50)
        self.x = randint(300, 480)
        self.y = randint(self.r, 540-self.r)
        self.color = BLACK
        self.live = 1

    def hit1(self, point=1):
        """Попадание шарика в цель."""
        global points1
        points1 += point

    def hit2(self, point=1):
        """Попадание шарика в цель."""
        global points2
        points2 += point

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


class Projectile:
    def __init__(self, screen: pygame.Surface, x, y):
        self.screen = screen
        self.x = x
        self.y = y
        self.r = 10
        self.color = LILY
        self.live = 1

    def move(self):
        self.y += 1

    def draw(self):
        pygame.draw.circle(
            self.screen,
            self.color,
            (self.x, self.y),
            self.r
        )

    def hittest(self, obj):
        if (self.x-obj.x)**2 + (self.y-obj.y)**2 <= (self.r+obj.r-10)**2:
            return True
        else:
            return False


class Bomb:

    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.r = 25
        self.y = 75
        self.x = 30
        self.color = BROWN
        self.v = randint(1, 10)
        self.period = randint(90, 180)
        self.time = self.period

    def move(self):
        self.x += self.v
        if 25 >= self.x or self.x >= 775:
            self.v = -self.v

    def draw(self):
        pygame.draw.circle(
            self.screen,
            self.color,
            (self.x, self.y),
            self.r
        )

    def attack(self):
        global projectiles
        self.time -= 1
        if self.time <= 0:
            projectiles.append(Projectile(screen, self.x, self.y))
            self.time = self.period


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
bullet = 0
balls1 = []
balls2 = []
bombs = []
targets = []
projectiles = []
points1 = 0
points2 = 0

clock = pygame.time.Clock()
gun1 = Gun1(screen)
gun2 = Gun2(screen)
targets.append(TargetClassic(screen))
targets.append(TargetJumping(screen))
targets.append(TargetStatic(screen))
targets.append(TargetStatic(screen))
targets.append(TargetStatic(screen))
bombs.append(Bomb(screen))
bombs.append(Bomb(screen))
finished = False

while not finished:
    screen.fill(WHITE)
    fonts = [pygame.font.SysFont('times new roman', 20)]
    text1 = fonts[0].render("Your score is: " + str(points1), True, BLACK)
    screen.blit(text1, (0, 0))
    text11 = fonts[0].render("Your health is: " + str(gun1.live), True, BLACK)
    screen.blit(text11, (0, 25))
    text2 = fonts[0].render("Your score is: " + str(points2), True, BLACK)
    screen.blit(text2, (645, 0))
    text22 = fonts[0].render("Your health is: " + str(gun2.live), True, BLACK)
    screen.blit(text22, (645, 25))
    gun1.draw()
    gun2.draw()
    for target in targets:
        target.draw()
    for b in balls1:
        b.draw()
    for b in balls2:
        b.draw()
    for bomb in bombs:
        bomb.draw()
    for p in projectiles:
        p.draw()
    pygame.display.update()

    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                gun1.fire2_start()
            if event.key == pygame.K_RETURN:
                gun2.fire2_start()
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                gun1.fire2_end()
            if event.key == pygame.K_RETURN:
                gun2.fire2_end()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        gun1.move_left()
    if keys[pygame.K_d]:
        gun1.move_right()
    if keys[pygame.K_w]:
        gun1.target_up()
    if keys[pygame.K_s]:
        gun1.target_down()
    if keys[pygame.K_LEFT]:
        gun2.move_left()
    if keys[pygame.K_RIGHT]:
        gun2.move_right()
    if keys[pygame.K_UP]:
        gun2.target_up()
    if keys[pygame.K_DOWN]:
        gun2.target_down()

    for bomb in bombs:
        bomb.move()
        bomb.attack()
    for p in projectiles:
        p.move()
        if p.hittest(gun1):
            gun1.live -= 1
            p.live -= 1
        if p.hittest(gun2):
            gun2.live -= 1
            p.live -= 1
        if p.live <= 0:
            projectiles.remove(p)
    for target in targets:
        target.move()
    for b in balls1:
        b.move()
        for target in targets:
            if b.hittest(target) and target.live:
                target.live = 0
                target.hit1()
                if b.color == MAGENTA:
                    b.live = 0
                elif b.color == CYAN:
                    b.live = 0
                    b.r = 100
                    for t in targets:
                        if b.hittest(t) and t.live:
                            t.live = 0
                            t.hit1()
                            t.__init__(screen)
                            if isinstance(t, TargetClassic) and len(targets) <= 7:
                                targets.append(TargetJumping(screen))
                                targets[-1].draw()
                            if isinstance(t, TargetJumping) and len(targets) <= 7:
                                targets.append(TargetClassic(screen))
                                targets[-1].draw()
                elif b.color == YELLOW:
                    b.live = 0
                    for i in range(3):
                        balls1.append(Ball(screen, MAGENTA, b.x, b.y, randint(-10, 10), randint(-5, 5)))
                target.__init__(screen)
                if isinstance(target, TargetClassic) and len(targets) <= 7:
                    targets.append(TargetJumping(screen))
                    targets[-1].draw()
                if isinstance(target, TargetJumping) and len(targets) <= 7:
                    targets.append(TargetClassic(screen))
                    targets[-1].draw()
        if b.hittest(gun2):
            gun2.live -= 1
            if b.color == GREEN:
                gun2.live -= 9
                b.live = 0
            elif b.color == MAGENTA:
                b.live = 0
            elif b.color == CYAN:
                b.live = 0
                gun2.live -= 6
                b.r = 100
                for t in targets:
                    if b.hittest(t) and t.live:
                        t.live = 0
                        t.hit1()
                        t.__init__(screen)
                        if isinstance(t, TargetClassic) and len(targets) <= 7:
                            targets.append(TargetJumping(screen))
                            targets[-1].draw()
                        if isinstance(t, TargetJumping) and len(targets) <= 7:
                            targets.append(TargetClassic(screen))
                            targets[-1].draw()
            elif b.color == YELLOW:
                b.live = 0
                gun2.live -= 3
        if gun2.live <= 0:
            finished = 1
            print("1st player wins!")
        if b.live <= 0:
            balls1.remove(b)
    gun1.power_up()
    for b in balls2:
        b.move()
        for target in targets:
            if b.hittest(target) and target.live:
                target.live = 0
                target.hit2()
                if b.color == MAGENTA:
                    b.live = 0
                elif b.color == CYAN:
                    b.live = 0
                    b.r = 100
                    for t in targets:
                        if b.hittest(t) and t.live:
                            t.live = 0
                            t.hit2()
                            t.__init__(screen)
                            if isinstance(t, TargetClassic) and len(targets) <= 7:
                                targets.append(TargetJumping(screen))
                                targets[-1].draw()
                            if isinstance(t, TargetJumping) and len(targets) <= 7:
                                targets.append(TargetClassic(screen))
                                targets[-1].draw()

                elif b.color == YELLOW:
                    b.live = 0
                    for i in range(3):
                        balls2.append(Ball(screen, MAGENTA, b.x, b.y, randint(-10, 10), randint(-5, 5)))
                target.__init__(screen)
                if isinstance(target, TargetClassic) and len(targets) <= 7:
                    targets.append(TargetJumping(screen))
                    targets[-1].draw()
                if isinstance(target, TargetJumping) and len(targets) <= 7:
                    targets.append(TargetClassic(screen))
                    targets[-1].draw()
        if b.hittest(gun1):
            gun1.live -= 1
            if b.color == GREEN:
                gun1.live -= 9
                b.live = 0
            elif b.color == MAGENTA:
                b.live = 0
            elif b.color == CYAN:
                b.live = 0
                gun1.live -= 6
                b.r = 100
                for t in targets:
                    if b.hittest(t) and t.live:
                        t.live = 0
                        t.hit1()
                        t.__init__(screen)
                        if isinstance(t, TargetClassic) and len(targets) <= 7:
                            targets.append(TargetJumping(screen))
                            targets[-1].draw()
                        if isinstance(t, TargetJumping) and len(targets) <= 7:
                            targets.append(TargetClassic(screen))
                            targets[-1].draw()
            elif b.color == YELLOW:
                b.live = 0
                gun1.live -= 3
        if gun1.live <= 0:
            finished = 1
            print("2nd player wins!")
        if b.live <= 0:
            balls2.remove(b)
    gun2.power_up()

pygame.quit()
