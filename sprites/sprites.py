import pygame
import random
import os

#parameters
width = 800
height = 600
fps = 60

#colors
white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
green = (0,255,0)
blue =(0,0,255)

class Player(pygame.sprite.Sprite):
    #player sprite
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('p1_jump.png').convert()
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        self.rect.center = (width/2,height/2)
        self.y_speed = 5
    def update(self):
        self.rect.x += 3
        self.rect.y += self.y_speed
        if self.rect.bottom > height - 200:
            self.y_speed = -5
        if self.rect.top < 200:
            self.y_speed = 5
        if self.rect.left > width:
            self.rect.right = 0
#initiation
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('My Game')
clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
#gameloop and render
running = True
while running:
    clock.tick(fps)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    #Update
    all_sprites.update()
    screen.fill(blue)
    all_sprites.draw(screen)
    pygame.display.flip()

#termination
pygame.quit()