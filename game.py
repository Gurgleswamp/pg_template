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
        self.player = Player()
        self.sprites = pg.sprite.Group()
        self.sprites.add(self.player)

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

    def update(self):
        self.sprites.update()
        self.clock.tick(FPS)
        
    def draw(self):
        self.screen.fill(BACKGROUND)
        self.sprites.draw(self.screen)
        pg.display.flip()

class Player(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pg.image.load('sprites/player.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (PLAYER_X_POS, PLAYER_Y_POS)  


def main():
    g = Game()
    while True:
        g.events()
        g.update()
        g.draw()

if __name__ == '__main__':
    main()