#importer modules

import pygame
from pygame.locals import *

#taille de l'écran
WIDTH = 400
HEIGHT = 300

#couleur de fond en RGB
background = (255, 255, 255)

fps = 60

#notre joueur
class Sprite(pygame.sprite.Sprite):
    def __init__(self, image, startx, starty):
        super().__init__()
        pygame.sprite.Sprite.__init__(self)

        
        self.image = pygame.image.load((image))
        #rect=rectangle=hitbox
        self.rect = self.image.get_rect()
        self.image.fill(12,31,23)
        
        #on le place où on veut
        self.rect.center = [startx, starty]

        #recevoir les inputs
        def update(self):
            pass

        def draw(self, screen):
            screen.blit(self.image, self.rect)

#notre joueur
class Joueur(pygame.sprite.Sprite):
    def __init__(self, image, startx, starty):
        super().__init__("p1_front.png", startx, starty)   

#un objet
class Box(Sprite):
    def __init__(self, startx, starty):
        super().__init__("p1_front.png", startx, starty)   


def main():
    #initialisation de pygame
    pygame.init()

    #notre écran
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    clock = pygame.time.Clock()

    #boucle infinie pour la durée du jeu
    while True:
        screen.fill(background)
        pygame.display.flip()

        clock.tick(60)





if __name__=="__main__":
    main()