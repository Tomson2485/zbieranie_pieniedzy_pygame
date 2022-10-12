import pygame.image
import random

def random_cash():
    digit = random.randint(1,100)
    if digit <= 60:
        return 0
    elif digit > 60 and digit <= 80:
        return 1
    elif digit > 80 and digit <= 95:
        return 2
    elif digit > 95:
        return 3

class Button():
    def __init__(self,x_cord, y_cord, file_name):
        self.x_cord = x_cord
        self.y_cord = y_cord
        self.button_image = pygame.image.load(f"assets/{file_name}.png")
        self.button_image_v2 = pygame.image.load(f"assets/{file_name}_v2.png")
        self.hitbox = pygame.Rect(self.x_cord, self.y_cord, self.button_image_v2.get_width(), self.button_image.get_height())

    def tick(self):
        if self.hitbox.collidepoint(pygame.mouse.get_pos()):
            if pygame.mouse.get_pressed()[0]:
                return True

    def draw(self, win):
        if self.hitbox.collidepoint(pygame.mouse.get_pos()):
            win.blit(self.button_image_v2, (self.x_cord, self.y_cord))
        else:
            win.blit(self.button_image, (self.x_cord, self.y_cord))

class Wall:
    def __init__(self, x_cord, y_cord, width, height):
        self.x_cord = x_cord
        self.y_cord = y_cord
        self.width = width
        self.height = height
        self.hitbox = pygame.Rect(self.x_cord, self.y_cord, self.width, self.height)

    def draw(self,window):
        pygame.draw.rect(window, (135, 47, 1), self.hitbox)

class Physics:
    def __init__(self, x_cord, y_cord, width, height, acc=0.0, max_vel=0):
        self.x_cord = x_cord
        self.y_cord = y_cord
        self.width = width
        self.height = height
        self.acc = acc
        self.vel_level = 0
        self.vel_vertical = 0
        self.max_vel = max_vel
        self.gravity = 0.5
        self.jumping = False

        self.previous_x = x_cord
        self.previous_y = y_cord
        self.hitbox = pygame.Rect(self.x_cord, self.y_cord, self.width, self.height)

    def physics_tick(self, walls):
        self.vel_vertical += self.gravity
        self.x_cord += self.vel_level
        self.y_cord += self.vel_vertical

        self.hitbox = pygame.Rect(self.x_cord, self.y_cord, self.width, self.height)

        for wall in walls:
            if wall.hitbox.colliderect(self.hitbox):
                #kolizja od góry
                if self.y_cord <= wall.y_cord + wall.height < self.previous_y:
                    self.y_cord = self.previous_y
                    self.vel_vertical = 0
                #kolizja od dołu
                if self.y_cord + self.height > wall.y_cord > self.previous_y:
                    self.y_cord = self.previous_y
                    self.vel_vertical = 0
                    self.jumping = False
                #kolizja od lewej
                if self.x_cord <= wall.x_cord < self.previous_x:
                    self.x_cord = self.previous_x
                    self.vel_level = 0
                #kolizja od prawej
                if self.x_cord + self.width >= wall.x_cord > self.previous_x + self.width:
                    self.x_cord = self.previous_x
                    self.vel_level = 0


        self.previous_y = self.y_cord
        self.previous_x = self.x_cord

    def physic_on_cash(self, walls):
        if not self.jumping:
            self.gravity = 3.0
            self.vel_vertical += self.gravity
            self.y_cord = self.vel_vertical
        self.hitbox = pygame.Rect(self.x_cord, self.y_cord, self.width, self.height)
        for wall in walls:
            if wall.hitbox.colliderect(self.hitbox):
                if self.y_cord + self.height > wall.y_cord > self.previous_y:
                    self.y_cord = wall.y_cord - self.height
                    self.vel_vertical = 0
                    self.jumping = True
        self.previous_y = self.y_cord


class Player(Physics):
    def __init__(self):
        self.player_img = pygame.image.load("assets/player.png")
        width = self.player_img.get_width()
        height = self.player_img.get_height()
        self.power_jump = 8
        super().__init__(10, 625, width, height, 0.5, 5)

    def tick(self, keys, walls):
        self.physics_tick(walls)
        if keys[pygame.K_a] and self.vel_level > self.max_vel *-1:
            self.vel_level -= self.acc
        if keys[pygame.K_d] and self.vel_level < self.max_vel:
            self.vel_level += self.acc
        if keys[pygame.K_w] and self.jumping is False:
            self.vel_vertical -= self.power_jump
            self.jumping = True
        if not(keys[pygame.K_d] or keys[pygame.K_a]):
            if self.vel_level > 0:
                self.vel_level -= self.acc
            elif self.vel_level < 0:
                self.vel_level += self.acc

    def draw(self, window):
        window.blit(self.player_img, (self.x_cord, self.y_cord))


class Item(Physics):
    def __init__(self):
        x = random.randint(20, 1200)
        y = 0
        self.coins_image = [
            pygame.image.load("assets/cash1.png"),
            pygame.image.load("assets/cash2.png"),
            pygame.image.load("assets/cash3.png"),
            pygame.image.load("assets/cash4.png")
        ]
        self.coins_index = random_cash()
        width = self.coins_image[self.coins_index].get_width()
        height = self.coins_image[self.coins_index].get_height()
        super().__init__(x, y, width, height)
        self.on_down = False
        self.value = 0

    def tick(self, walls):
        if self.coins_index == 0:
            self.value = random.randint(1,100)
        elif self.coins_index == 1:
            self.value = random.randint(100, 1000)
        elif self.coins_index == 2:
            self.value = random.randint(1000, 10000)
        elif self.coins_index == 3:
            self.value = random.randint(10000, 100000)
        self.physic_on_cash(walls)

    def draw(self, win):
        win.blit(self.coins_image[self.coins_index], (self.x_cord, self.y_cord))

class Enemy(Physics):
    def __init__(self):
        self.enemy_img = pygame.image.load("assets/enemy.png")
        width = self.enemy_img.get_width()
        height = self.enemy_img.get_height()
        self.power_jump = 8
        super().__init__(1200, 625, width, height, 0.5, 5)

    def go_left(self):
        if -self.vel_level < self.max_vel:
            self.vel_level -= self.acc

    def go_right(self):
        if self.vel_level < self.max_vel:
            self.vel_level += self.acc

    def go_up(self):
        pass

    def tick(self, walls, item):
        self.physics_tick(walls)
        for i in item:
            if i.x_cord > self.x_cord:
                self.go_right()
            elif i.x_cord < self.x_cord:
                self.go_left()

    def draw(self, win):
        win.blit(self.enemy_img, (self.x_cord, self.y_cord))