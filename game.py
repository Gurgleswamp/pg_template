import pygame as pg
import sys, random
from settings import *

vec = pg.math.Vector2

class Game:
    def __init__(self):
        pg.init()
        pg.font.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        self.screen.fill(BACKGROUND)
        self.clock = pg.time.Clock()
        self.fishRadar = FishRadar()
        self.fishProgress = FishProgress(self.fishRadar)
        self.fish = Fish()
        self.sprites = pg.sprite.Group()
        self.sprites.add(self.fishRadar)
        self.sprites.add(self.fish)
        self.sprites.add(self.fishProgress)

        self.font = pg.font.SysFont('Nimbus Mono PS', 30)
        self.fishCaught = 0
        self.fishNot = 0


    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                if  event.key == pg.K_w:
                    self.fish.resy -= 16          
                if event.key == pg.K_a:
                    self.fish.resx -= 16
                if  event.key == pg.K_s:
                    self.fish.resy += 16
                if  event.key == pg.K_d:
                    self.fish.resx += 16
            if event.type == pg.KEYUP:
                if  event.key == pg.K_w:
                    self.fish.resy = 0         
                if event.key == pg.K_a:
                    self.fish.resx = 0
                if  event.key == pg.K_s:
                    self.fish.resy = 0
                if  event.key == pg.K_d:
                    self.fish.resx = 0
        if not (pg.Rect.colliderect(self.fish.rect, self.fishRadar.rect)):
            self.fishProgress.kill()
            self.fish.kill()
            self.fish = Fish()
            self.fishProgress = FishProgress(self.fishRadar)
            self.sprites.add(self.fish)
            self.sprites.add(self.fishProgress)
            self.fishNot += 1
        if self.fishProgress.image.get_width() >= self.fishRadar.rect.width:
            self.fishProgress.kill()
            self.fish.kill()
            self.fish = Fish()
            self.fishProgress = FishProgress(self.fishRadar)
            self.sprites.add(self.fish)
            self.sprites.add(self.fishProgress)
            self.fishCaught += 1

    def update(self):
        self.sprites.update()
        self.clock.tick(FPS)
        
    def draw(self):
        self.screen.fill(BACKGROUND)
        self.sprites.draw(self.screen)
        fishCaughtText = f'FISH CAUGHT: {self.fishCaught}'
        fishNotText = f'FISH NOT: {self.fishNot}'
        fishCaughtRender = self.font.render(fishCaughtText, False, (255, 255, 255))
        fishNotRender = self.font.render(fishNotText, False, (255, 255, 255))

        self.screen.blit(fishCaughtRender, ((WIDTH // 2) - (self.fishRadar.rect.width // 2), HEIGHT * 3/4))
        self.screen.blit(fishNotRender, ((WIDTH // 2) - (self.fishRadar.rect.width // 2), HEIGHT * 3/4 + 30))

        pg.display.flip()

class FishProgress(pg.sprite.Sprite):
    def __init__(self, fishRadar):
        super().__init__()
        self.image = pg.image.load('sprites/progress.png').convert_alpha()
        self.rect = self.image.get_rect()

        self.rect.center = (fishRadar.rect.left + 16, fishRadar.rect.top - 16)  
    
    def update(self):
        self.image = pg.transform.scale(self.image, (self.image.get_width()+5, self.image.get_height()))
        

class FishRadar(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pg.image.load('sprites/fishRadar2.png').convert_alpha()
        self.image = pg.transform.scale(self.image, (HEIGHT // 2, HEIGHT // 2))
        self.rect = self.image.get_rect()
        self.rect.center = (FISHING_MINIGAME_X_POS, FISHING_MINIGAME_Y_POS)

class Fish(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pg.image.load('sprites/fish.png').convert_alpha()
        self.image = pg.transform.scale(self.image, (self.image.get_width()*3, self.image.get_height()*3))
        self.rect = self.image.get_rect()
        self.rect.center = (FISHING_MINIGAME_X_POS, FISHING_MINIGAME_Y_POS) 
        self.velx = 0
        self.vely = 0
        self.resx = 0
        self.resy = 0
    def update(self):
        roll = random.randint(1, 10)
        if roll == 1:
            self.swim()
        newx = self.rect.x + self.velx + self.resx
        newy = self.rect.y + self.vely + self.resy
        self.rect.x = newx
        self.rect.y = newy
    def swim(self):
        self.velx = random.randint(-15, 15)
        self.vely = random.randint(-15, 15)



def main():
    g = Game()
    while True:
        g.events()
        g.update()
        g.draw()

if __name__ == '__main__':
    main()