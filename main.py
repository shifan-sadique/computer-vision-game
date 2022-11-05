# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import cv2
from cgi import test
from multiprocessing.connection import wait
import pygame
import random
from sys import exit
pygame.init()
screen=pygame.display.set_mode((1400,700))

def set_screen():
    pygame.display.set_caption("computer vision game")
    clock=pygame.time.Clock()
    test_font = pygame.font.Font(None,20)
    test_surface=pygame.Surface((1400,700))
    test_surface.fill('White')
    text_surface=test_font.render("mygame",False,'Red')

    ball=pygame.image.load("ball.png").convert_alpha()
    colorflag=1
    red=pygame.image.load("red.png").convert_alpha()
    blue=pygame.image.load("blue.png").convert_alpha()
    xposr=random.randrange(0,700,35)
    xposb=random.randrange(0,700,150)
    y_posr=0
    y_posb=0
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
            screen.blit(red,(xposr,y_posr))
            screen.blit(blue,(xposb,y_posb))
        else:
            if y_posr<=-700:
                y_posr=700
                y_posb=y_posb-4
                screen.blit(red,(xposr,y_posr))
                screen.blit(blue,(xposb,y_posb))
            elif y_posb<=-700:
                y_posb=700
                y_posr=y_posr-4
                screen.blit(blue,(xposb,y_posb))
                screen.blit(red,(xposr,y_posr))

            xposb=random.randint(0,700)
            xposr=random.randint(0,700)
            if colorflag==1:
                colorflag=0
            else:
                colorflag=1

        pygame.display.update()
        clock.tick(30)




def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')
    set_screen()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
