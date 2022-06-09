import pygame as pg
import sys
from settings import *

vec = pg.math.Vector2

class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        self.screen.fill(BACKGROUND)
        self.clock = pg.time.Clock()
        self.sprites = pg.sprite.Group()
        self.player = Player()
        self.sprites.add(self.player)
        milliseconds_delay = 100
        self.bullet_event = pg.USEREVENT + 1
        pg.time.set_timer(self.bullet_event, milliseconds_delay)

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            
            if event.type == self.bullet_event:
                keys = pg.key.get_pressed()
                if keys[pg.K_d] or keys[pg.K_a] or keys[pg.K_s] or keys[pg.K_w]:
                    self.shoot()


    def update(self):
        self.sprites.update()
        self.clock.tick(FPS)
        
    def draw(self):
        self.screen.fill(BACKGROUND)
        self.sprites.draw(self.screen)
        pg.display.flip()

    def shoot(self):
        bullet = Bullet(self.player.pos, self.player.vel)
        self.sprites.add(bullet)

class Player(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pg.image.load("sprites/player.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT * 0.25)
        self.pos = vec(WIDTH // 2, HEIGHT * 0.25)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.health = 100

    def draw(self, win):
        win.blit(self.image, self.rect)   

    def update(self):
        self.acc = vec(0, 0)
        keys = pg.key.get_pressed()
        if keys[pg.K_d]:
            if self.pos.x < WIDTH-16:
                self.acc.x = PLAYER_ACC
            else:
                self.vel.x = 0
                self.vel.y = 0
        if keys[pg.K_a]:
            if self.pos.x > 16:
                self.acc.x = -PLAYER_ACC
            else:
                self.vel.x = 0
                self.vel.y = 0
        if keys[pg.K_w]:
            if self.pos.y > 16:
                self.acc.y = -PLAYER_ACC
            else:
                self.vel.x = 0
                self.vel.y = 0
        if keys[pg.K_s]:
            if self.pos.y < HEIGHT-16:
                self.acc.y = PLAYER_ACC
            else:
                self.vel.x = 0
                self.vel.y = 0

        self.acc += self.vel * -PLAYER_FRICTION
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        self.rect.center = self.pos

class Bullet(pg.sprite.Sprite):
    def __init__(self, playerpos, playerdir):
        super().__init__()
        self.image = pg.Surface((10, 10))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = vec(playerpos)
        self.acc = vec(playerdir)
        if self.acc != [0, 0]:
            self.acc = self.acc.normalize()

    def update(self):
        self.rect.x += self.acc.x * 10
        self.rect.y += self.acc.y * 10
        

def main():
    g = Game()
    while True:
        g.events()
        g.update()
        g.draw()

if __name__ == '__main__':
    main()