#importer modules

import pygame
from pygame.locals import *

#démarer le jeu
pygame.init()


#taille de l'écran
WIDTH = 1000
HEIGHT = 1000

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Le nom du jeu ici')


#nos images
bg_img = pygame.image.load('/Users/jacobducas/Documents/GitHub/jeu/bg.png')

run = True
while run:

    #remplir l'écran avec notre image
    screen.blit(bg_img, (0,0))

    for event in pygame.event.get():

        #si on clique sur le x en haut à gauche le jeu ferme
        if event.type == pygame.QUIT:
            run = False

pygame.quit()
