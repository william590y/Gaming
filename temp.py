import pygame
import random

#parameters
width = 360
height = 480
fps = 30

#colors
white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
green = (0,255,0)
blue =(0,0,255)

#initiation
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('My Game')
clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()
#gameloop and render
running = True
while running:
    clock.tick(fps)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    #Update
    all_sprites.update()
    screen.fill(black)
    all_sprites.draw(screen)
    pygame.display.flip()

#termination
pygame.quit()
