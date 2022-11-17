import pygame
import random
import cv2
from sys import exit
pygame.init()
screen=pygame.display.set_mode((1200,700))
class balloon:
    def __init__(self,color):
        self.color=color
        self.xpos=random.randrange(0,700,100)
        self.ypos=random.randint(0,700)

def set_screen():
    pygame.display.set_caption("computer vision game")
    clock=pygame.time.Clock()
    test_font = pygame.font.Font(None,20)
    test_surface=pygame.Surface((1400,700))
    test_surface.fill('White')
    text_surface=test_font.render("mygame",False,'Red')
    ball=pygame.image.load("ball.png").convert_alpha()
    r=pygame.image.load("red.png").convert_alpha()
    red=balloon(r)
    b=pygame.image.load("blue.png").convert_alpha()
    b=pygame.transform.scale(b,(500,500))
    blue=balloon(b)
    xposr=red.xpos
    xposb=blue.xpos
    y_posr=red.ypos
    y_posb=blue.ypos
    while True:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                exit()
        screen.blit(test_surface,(0,0))
        screen.blit(text_surface,(300,50))
        screen.blit(ball,(700,700))
        if y_posr > -700 and y_posb > -700:
            y_posb=y_posb-4
            y_posr=y_posr-4
            print("1")
            screen.blit(r,(xposr,y_posr))
            screen.blit(b,(xposb,y_posb))

        else:
            if y_posr<=-700:
                red=balloon(r)
                x_posr=red.xpos
                y_posr=red.ypos
                y_posb=y_posb-4
                screen.blit(r,(xposr,y_posr))
                screen.blit(b,(xposb,y_posb))
            elif y_posb<=-700:
                blue=balloon(b)
                xposb=blue.xpos
                y_posb=blue.ypos
                y_posr=y_posr-4
                screen.blit(b,(xposb,y_posb))
                screen.blit(r,(xposr,y_posr))
            # xposb=random.randint(0,700)
            # xposr=random.randint(0,700)

        pygame.display.update()
        clock.tick(30)
set_screen()