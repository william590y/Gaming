import pygame
import random

def newmob():
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)
    
def shieldbar(surf,x,y,pct):
    if pct<0:
        pct = 0
    blength = 100
    bheight = 10
    fill = (pct/100)*blength
    outline_rect = pygame.Rect(x,y,blength,bheight)
    fill_rect = pygame.Rect(x,y,fill,bheight)
    pygame.draw.rect(surf, green, fill_rect)
    pygame.draw.rect(surf, white, outline_rect,2)

#parameters
width = 360
height = 480
fps = 60

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

font_name = pygame.font.match_font('arial')
def draw(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, white)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x,y)
    surf.blit(text_surface,text_rect)
    
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player, (50,30))
        self.rect = self.image.get_rect()
        self.radius = 20
        #pygame.draw.circle(self.image,red,self.rect.center,self.radius)
        self.rect.centerx = width/2
        self.rect.bottom = height - 10
        self.speedx = 0
        self.shield = 100
        self.shoot_delay = 250
        self.last_shot = pygame.time.get_ticks()
        
    def update(self):
        self.speedx = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -5
        if keystate[pygame.K_RIGHT]:
            self.speedx = 5
        if keystate[pygame.K_SPACE]:
            self.shoot()
        if self.rect.right > width:
            self.rect.right = width
        if self.rect.left < 0:
            self.rect.left = 0
        self.rect.x += self.speedx
    
    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            bullet = Bullet(self.rect.centerx,self.rect.top)
            all_sprites.add(bullet)
            bullets.add(bullet)
            shoot_sound.play()
            
class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = random.choice(meteor_images)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width*.85/2)
        #pygame.draw.circle(self.image,red,self.rect.center,self.radius)
        self.rect.x = random.randrange(width - self.rect.width)
        self.rect.y = random.randrange(-150,-40)
        self.speedy = random.randrange(1,8)
        self.speedx = random.randrange(-3,3)
        self.rot = 0
        self.rot_speed = random.randrange(-8,8)
        self.last_update = pygame.time.get_ticks()
    
    def rotate(self):
        now =pygame.time.get_ticks()
        if now - self.last_update > 50:
             self.last_update = now
             self.rot = (self.rot + self.rot_speed)%360
             new_image = pygame.transform.rotate(self.image_orig,self.rot)
             old_center = self.rect.center
             self.image = new_image
             self.rect = self.image.get_rect()
             self.rect.center = old_center
             
    def update(self):
        self.rotate()
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.top > height + 10 or self.rect.left < -25 or self.rect.right > width + 25:
            self.rect.x = random.randrange(width - self.rect.width)
            self.rect.y = random.randrange(-100,-40)
            self.speedy = random    .randrange(1,8)

class Bullet(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10
        
    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()

class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = self.size[0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50
    
    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(self.size):
                self.kill()
            else:
                center = self.rect.center
                self.image = self.size[self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center
                
#load graphics
background = pygame.image.load('background.png')
background_rect = background.get_rect()
player = pygame.image.load('ship.png')
bullet = pygame.image.load('laser.png')
meteor_images = []
for i in range(1,11):
    meteor_images.append(pygame.image.load('mob{}.png'.format(i)))
lg = []
sm = []
for i in range(9):
    img = pygame.image.load('regularExplosion0{}.png'.format(i))
    img_lg = pygame.transform.scale(img,(75,75))
    lg.append(img_lg)
    img_sm = pygame.transform.scale(img,(32,32))
    sm.append(img_sm)
    
#load audio
shoot_sound = pygame.mixer.Sound('laser.wav')
pygame.mixer.music.load('music.ogg')
pygame.mixer.music.set_volume(.4)

#load all sprites
all_sprites = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
mobs = pygame.sprite.Group()
for i in range(8):
    newmob()
bullets = pygame.sprite.Group()
score = 0

pygame.mixer.music.play(loops = -1)
#gameloop and render
running = True
while running:
    clock.tick(fps)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #Update
    all_sprites.update()
    hits = pygame.sprite.groupcollide(mobs,bullets,True,True)
    for hit in hits:
        score += 60 - hit.radius
        newmob()
        expl = Explosion(hit.rect.center,lg)
        all_sprites.add(expl)
        
    hits = pygame.sprite.spritecollide(player, mobs,True,pygame.sprite.collide_circle)
    for hit in hits:
        player.shield -= hit.radius*2
        newmob()
        expl = Explosion(hit.rect.center,sm)
        all_sprites.add(expl)
        if player.shield <=0:
            running = False
    
    screen.fill(black)
    screen.blit(background,background_rect)
    all_sprites.draw(screen)
    draw(screen,str(score),25,width/2,10)
    shieldbar(screen,5,5,player.shield)
    pygame.display.flip()

#termination
pygame.quit()
print('Score:{}'.format(score))
