import pygame
from game import *

pygame.init()
window = pygame.display.set_mode((1300, 732))
def control():
    background = pygame.image.load("assets/background.png")
    run = True
    walls = [Wall(0, 700, 1300, 32),
             Wall(1300, 0, 20, 732),
             Wall(0, 0, 0, 720)
             ]
    player = Player()
    enemy = Enemy()
    clock = 0
    new_cash =0
    cash = []
    score = 0
    score2 = 0
    while run:
        delta = pygame.time.Clock().tick(120)/1000
        new_cash += delta
        clock += delta

        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                run = False

        player.tick(keys, walls)
        enemy.tick(walls, cash)

        if new_cash >= 2:
            cash.append(Item())
            new_cash = 0
        for item in cash:
            item.tick(walls)
            if item.hitbox.colliderect(player.hitbox):
                cash.remove(item)
                score += item.value
            elif item.hitbox.colliderect(enemy.hitbox):
                cash.remove(item)
                score2 += item.value

        text_image = pygame.font.Font.render(pygame.font.SysFont("arial", 30), f"gotowka: {score} $", True, (0, 0, 0))
        text_image_2 = pygame.font.Font.render(pygame.font.SysFont("arial", 30), f"gotowka: {score2} $", True, (0, 0, 0))

        window.blit(background, (0, 0))
        window.blit(text_image, (0, 0))
        window.blit(text_image_2, (1100, 0))

        player.draw(window)
        enemy.draw(window)
        for item in cash:
            item.draw(window)
        for wall in walls:
            wall.draw(window)

        pygame.display.update()

def menu():
    background = pygame.image.load("assets/background_menu.png")
    run = True
    buttons = [Button(500,300, "graj"), Button(450,430, "wyjscie")]
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        if buttons[0].tick():
            control()
        if buttons[1].tick():
            run = False
        window.blit(background, (0, 0))
        for button in buttons:
            button.draw(window)
        pygame.display.update()
        
if __name__ == "main":
    menu()