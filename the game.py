import pygame
import sys

money = 100
fuel = 10
ore = 0
day = 1
max_days = 10
max_cargo = 10

pygame.init()
screen = pygame.display.set_mode((1920, 1080))
clock = pygame.time.Clock()
running = True

bg = pygame.image.load("bg.jpg").convert()
bg = pygame.transform.scale(bg, (1920, 1080))

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.blit(bg, (0, 0))
    
    for i in range 10:
        print("works")    

    pygame.display.flip()

    clock.tick(2000)

pygame.quit()
