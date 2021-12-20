import pygame
import random
from pygame import draw
from pygame.event import pump
from pygame.locals import *
from pygame.mask import from_surface
from pygame import mixer

pygame.init()
pygame.mixer.pre_init(44100, -16, 2, 512)
mixer.init()


clock = pygame.time.Clock()
fps = 60

lignes = 3
colonnes = 5
ennemi_cooldown = 1000
dernier_tir_ennemi = pygame.time.get_ticks()
countdown = 3
dernier_compte = pygame.time.get_ticks()
game_over = 0
largeur = 600
height = 800

font30 = pygame.font.Font("/Users/jacobducas/Downloads/Helvetica-Font/Helvetica.ttf", 30)
font40 = pygame.font.Font("/Users/jacobducas/Downloads/Helvetica-Font/Helvetica.ttf", 40)
#son
boom_fx = pygame.mixer.Sound("/Users/jacobducas/Desktop/GitHub/jeu/explosion.wav")
boom_fx.set_volume(0.25)

boom2_fx = pygame.mixer.Sound("/Users/jacobducas/Desktop/GitHub/jeu/explosion2.wav")
boom_fx.set_volume(0.25)

laser_fx = pygame.mixer.Sound("/Users/jacobducas/Desktop/GitHub/jeu/laser.wav")
laser_fx.set_volume(0.25)
ecran = pygame.display.set_mode((largeur, height))
pygame.display.set_caption('Aliens')

rouge = (255, 0, 0)
vert = (0, 255, 0)
blanc = (255, 255, 255)
#images 
background = pygame.image.load("/Users/jacobducas/Desktop/GitHub/jeu/bg.png")

def creer_background():
    ecran.blit(background, (0, 0))

def texte(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    ecran.blit(img, (x, y))

class Vaisseau(pygame.sprite.Sprite):
    def __init__(self, x, y, health):
        pygame.sprite.Sprite.__init__(self) 
        self.image = pygame.image.load("/Users/jacobducas/Desktop/GitHub/jeu/spaceship.png")
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.health_start = health
        self.health_remaining = health
        self.dernier_tir = pygame.time.get_ticks()

    def update(self):
        speed = 8
        cooldown = 500
        game_over = 0
        #inputs
        touches = pygame.key.get_pressed()
        if touches[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= speed
        if touches[pygame.K_RIGHT] and self.rect.right < largeur:
            self.rect.x += speed
      
        temps = pygame.time.get_ticks()

      
        if touches[pygame.K_SPACE] and (temps - self.dernier_tir) > cooldown :
            laser_fx.play()
            balles = Balles(self.rect.centerx, self.rect.top)
            balles_group.add(balles)
            self.dernier_tir = temps

        self.mask = pygame.mask.from_surface(self.image)

        #barre de vie
        pygame.draw.rect(ecran, rouge, (self.rect.x, (self.rect.bottom + 10), self.rect.width, 15))
        if self.health_remaining > 0:
            pygame.draw.rect(ecran, vert, (self.rect.x, (self.rect.bottom + 10), int(self.rect.width * (self.health_remaining / self.health_start)), 15))
        elif self.health_remaining <= 0:
            explosion = Boom(self.rect.centerx, self.rect.centery, 3)
            boom_group.add(explosion)  
            self.kill() 
            game_over = -1
        return game_over
class Balles(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self) 
        self.image = pygame.image.load("/Users/jacobducas/Desktop/GitHub/jeu/bullet.png")
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

    def update(self):
        self.rect.y -= 5
        if self.rect.bottom < 0:
            self.kill()
        if pygame.sprite.spritecollide(self, ennemi_group, True):
            self.kill()
            boom_fx.play()
            explosion = Boom(self.rect.centerx, self.rect.centery, 2)
            boom_group.add(explosion)

class Ennemi(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self) 
        self.image = pygame.image.load("//Users/jacobducas/Desktop/GitHub/jeu/alien" + str(random.randint(1,5)) + ".png")
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.compteur = 0
        self.deplcaer = 1
    def update(self):
        self.rect.x +=  self.deplcaer
        self.compteur += 1
        if abs(self.compteur) > 75:
            self.deplcaer *= -1
            self.compteur *= self.deplcaer

class Balles_Ennemi(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self) 
        self.image = pygame.image.load("/Users/jacobducas/Desktop/GitHub/jeu/alien_bullet.png")
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

    def update(self):
        self.rect.y += 2
        if self.rect.top > height:
            self.kill()
        if pygame.sprite.spritecollide(self, vaisseau_group, False, pygame.sprite.collide_mask):
            self.kill()
            boom2_fx.play()
            vaisseau.health_remaining -= 1
            explosion = Boom(self.rect.centerx, self.rect.centery, 1)
            boom_group.add(explosion)

class Boom(pygame.sprite.Sprite):
    def __init__(self, x, y, size):
        pygame.sprite.Sprite.__init__(self) 
        self.images = []
        for c in range(1, 6):
            img = pygame.image.load(f"/Users/jacobducas/Desktop/GitHub/jeu/exp{c}.png")
            if size == 1:
                img = pygame.transform.scale(img, (20, 20))
            if size == 2:
                img = pygame.transform.scale(img, (40, 40))
            if size == 3:
                img = pygame.transform.scale(img, (160, 160))
            self.images.append(img)
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.compteur = 0

    def update(self):
        boom_vitesse = 3
        self.compteur += 1

        if self.compteur >= boom_vitesse and self.index < len(self.images) - 1:
            self.compteur = 0
            self.index += 1
            self.image = self.images[self.index]

        if self.index >= len(self.images) - 1 and self.compteur >= boom_vitesse:
            self.kill()


ennemi_group = pygame.sprite.Group()
vaisseau_group = pygame.sprite.Group()
balles_group = pygame.sprite.Group()
balles_ennemi_group = pygame.sprite.Group()
boom_group = pygame.sprite.Group()

def aliens():
    for l in range(lignes):
        for i in range(colonnes):
            alien = Ennemi(100 + i * 100, 100 + l * 70)
            ennemi_group.add(alien)
aliens()

vaisseau = Vaisseau(int(largeur / 2), height - 100, 3 )
vaisseau_group.add(vaisseau)

run = True
while run:

    clock.tick(fps) 
    #bg
    creer_background()
    if countdown == 0:


        temps = pygame.time.get_ticks()

        if temps - dernier_tir_ennemi > ennemi_cooldown and len(balles_ennemi_group) < 5 and len(ennemi_group) > 0:
            attacking_alien = random.choice(ennemi_group.sprites())
            balle_ennemi = Balles_Ennemi(attacking_alien.rect.centerx, attacking_alien.rect.bottom)
            balles_ennemi_group.add(balle_ennemi)
            dernier_tir_ennemi = temps

        if len(ennemi_group) == 0:
            game_over = 1
        
        if game_over == 0:
    #event

    #deplacer vaisseau
            game_over = vaisseau.update()
        

        #sprites
            balles_group.update()
            ennemi_group.update()
            balles_ennemi_group.update()
        else:
            if game_over == -1:
                texte("Game Over", font40, blanc, int(largeur / 2 - 100), int(height / 2 + 50))   
            if game_over == 1:
                texte("You Win", font40, blanc, int(largeur / 2 - 100), int(height / 2 + 50))   
    if countdown > 0:
        texte("DÉBUT", font40, blanc, int(largeur / 2 - 65), int(height / 2 + 50))
        texte(str(countdown), font40, blanc, int(largeur / 2 - 10), int(height / 2 + 100))
        timer = pygame.time.get_ticks()
        if timer - dernier_compte > 1000:
            countdown -= 1
            dernier_compte = timer
    boom_group.update()
    #sprite groups afficher
    vaisseau_group.draw(ecran)
    balles_group.draw(ecran)
    ennemi_group.draw(ecran)
    balles_ennemi_group.draw(ecran)
    boom_group.draw(ecran)


    for event in pygame.event.get():
       if event.type == pygame.QUIT:
           run = False

    pygame.display.update()


pygame.quit() 
