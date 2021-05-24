import pygame
import sys
import random
import neat

pygame.init()
win = pygame.display.set_mode((288, 512))
pygame.display.set_caption("Flappy Bird v2")

# global config
clock = pygame.time.Clock()
tick_count = 0
grav = 0
activate = False
movements = 0, 425
ground_move = 0
multiply = 0
pipe_y = 0
time = 0

# pictures
pipe_img = pygame.image.load('pipe.png')
pipe1_img = pygame.transform.flip(pipe_img, False, True)
bird_img = [pygame.image.load('bird1.png'), pygame.image.load('bird2.png'), pygame.image.load('bird3.png')]
base_img = pygame.image.load('base.png')
bg_img = pygame.image.load('bg.png')

# classes and everything
# player/bird
class player(object):
    def __init__(self, x, y, height, width):
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.Jump = False
        self.rotation = -(grav // 3)
        self.hitbox = pygame.Rect(self.x, self.y, 34, 24)

        # draw
    def draw(self):
        if not activate:
            win.blit(bird_img[tick_count // 10], (self.x, self.y))
        else:
            win.blit(pygame.transform.rotate(bird_img[1], self.rotation), (self.x, self.y))
            if self.rotation >= 15:
                win.blit(pygame.transform.rotate(bird_img[2], self.rotation), (self.x, self.y))
        self.hitbox = (self.x, self.y, 34, 24)
        self.hitbox = pygame.Rect(self.x, self.y, 34, 24)
        # pygame.draw.rect(win, (255, 0, 0), self.hitbox)


class ground(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.current = 0
        self.rel_x = ground_move % base_img.get_width()
        self.font = pygame.font.SysFont('comicsans', 50, False, False)
        self.text = self.font.render(str((time// 10)), True, (255, 255, 255))


    def draw(self):
        global time
        win.blit(base_img, (self.rel_x - base_img.get_width(), self.y))
        # pygame.draw.line(win, (0, 255, 0), (self.rel_x, 0), (self.rel_x, bg_img.get_height()), 3)
        if self.rel_x < 335:
            win.blit(base_img, (self.rel_x, self.y))
        win.blit(self.text, (125, 100))

class pipe(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.hitbox = pygame.Rect(self.x, self.y, 52, 320)
        self.hitbox_top = pygame.Rect(self.x, self.y - 450, 52, 320)

    def draw(self):
        win.blit(pipe_img, (self.x, self.y))
        win.blit(pipe1_img, (self.x, self.y - 450))
        self.hitbox = pygame.Rect(self.x, self.y, 52, 320)
        self.hitbox_top = pygame.Rect(self.x, self.y - 450, 52, 320)
        # pygame.draw.rect(win, (0, 0, 0), self.hitbox)
        # pygame.draw.rect(win, (0, 0, 0), self.hitbox_top)


def redraw():
    win.blit(bg_img, (0, 0))
    player.draw(bird)
    pipe.draw(pipes)
    ground.draw(grounds)

    pygame.display.update()

# mainloop
while 1:
    # classes input
    bird = player(50, 256, 50, 50)
    grounds = ground(ground_move, 425)
    pipes = pipe(grounds.rel_x - 100, pipe_y)
    clock.tick(30)

    for events in pygame.event.get():
        if events.type == pygame.QUIT:
            sys.exit()

        elif events.type == pygame.KEYDOWN:
            if events.key == pygame.K_SPACE:
                activate = True
                grav -= 45
                bird.Jump = True

    # tick count for bird animation (didn't work on class)

    tick_count += 1
    if tick_count >= 30:
        tick_count = 0

    if activate:
        grav += 4
        bird.y += grav
        ground_move -= 5
    else:
        pipe_y = 1000
        ground_move -= 1

    if bird.y >= (bg_img.get_height() - base_img.get_height()):
        time = 0
        grav = 0
        activate = False

    if grounds.rel_x <= bird.x:
        time += 1
        pipe_y = random.randrange(250, 400)

        # collision detection
    if bird.hitbox.colliderect(pipes.hitbox) or bird.hitbox.colliderect(pipes.hitbox_top):
        time = 0
        grav = 0
        pygame.time.delay(100)
        activate = False

    redraw()