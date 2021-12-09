import pygame
import sys
import random

# Setup
screen_height = 600
screen_width = 800
pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
pygame.display.set_caption("Game")
pygame.display.set_icon(pygame.image.load("Player_Icon.png"))

# Start screen
start_img = [pygame.image.load("Start_Button_0.png"), pygame.image.load("Start_Button_1.png")]
restart_img = [pygame.image.load("Restart_0.png"), pygame.image.load("Restart_1.png")]
over_button = False

# start and end screen
def draw_rect():
    global over_button
    (x, y) = pygame.mouse.get_pos()
    if start is True:
        wdt = 180
        hgt = 72
        x_pos = screen_width / 2 - wdt / 2
        y_pos = screen_height / 2 - hgt / 2
        if x_pos < x < x_pos + wdt and y_pos < y < y_pos + hgt:
            screen.blit(pygame.transform.scale(start_img[0], (wdt, hgt)), (x_pos, y_pos))
            # 30 zu 12
            over_button = True
        else:
            # if not over button
            screen.blit(pygame.transform.scale(start_img[1], (wdt, hgt)), (x_pos, y_pos))
        screen.blit(pygame.transform.scale(pygame.image.load("Controls.png"), (300, 300)),
                    (screen_width / 2 - 100, screen_height / 2))
        screen.blit(pygame.transform.scale(pygame.image.load("Stand_Front.png"), (300, 300)), (250, -25))
    if game_over is True or winner is True:
        wdt = 320
        hgt = 72
        x_pos = screen_width / 2 - wdt / 2
        y_pos = 480
        if game_over:
            screen.blit(pygame.image.load("Game_Over.png"), (screen_width/2 - 188, 50))
            screen.blit(pygame.image.load("Player_Dead.png"), (screen_width / 2 - 128, 120))
        if winner:
            screen.blit(pygame.image.load("Victory.png"), (screen_width / 2 - 144, 50))
            screen.blit(pygame.image.load("Player_Front.png"), (screen_width / 2 - 128, 120))
        if x_pos < x < x_pos + wdt and y_pos < y < y_pos + hgt:
            screen.blit(pygame.transform.scale(restart_img[0], (wdt, hgt)), (x_pos, y_pos))
            # 30 zu 12
            over_button = True
        else:
            # if not over button
            screen.blit(pygame.transform.scale(restart_img[1], (wdt, hgt)), (x_pos, y_pos))

# variables for starting/ending game
winner = False
game_over = False
start = True
game = False


# Variables for Game
display_scroll = [0, 0]
coin_count = [0]
map_size = 500
wall_size = 100
SPEED = 6
x_grid = -1200
y_grid = -1200
# Classes and Functions

# background
def draw_bg():
    global x_grid
    global y_grid
    if not(display_scroll[1] < -map_size or display_scroll[1] > map_size):
        y_grid = display_scroll[1]
    if not(display_scroll[0] < -map_size or display_scroll[0] > map_size):
        x_grid = display_scroll[0]
    screen.blit(pygame.transform.scale(pygame.image.load("Bodenlowqua.png"), (1800, 1600)), (-map_size - x_grid, -map_size - y_grid))

# win condition
def win():
    global winner
    global game
    if player.y <= wall_size - 20 and -map_size - x_grid + 850 <= player.x <= -map_size - x_grid + 925 and pressed[pygame.K_w]:
        if o.coin_count == 9:
            winner = True
            game = False

# collision detection
def collide(x, y, e_x, e_y, wdt, hgt, e_wdt, e_hgt):
    if not (x > e_x + e_wdt or x + wdt < e_x or
            y > e_y + e_hgt or y + hgt < e_y):
        return True
    return False

# hearts, coins and sword uses
class Overlay:
    def __init__(self):
        self.coin_count = 0
        self.herz_count = 0
        self.herz = [pygame.image.load("Herz_0.png"), pygame.image.load("Herz_1.png"), pygame.image.load("Herz_2.png"),
                     pygame.image.load("Herz_3.png"), pygame.image.load("Herz_4.png"), pygame.image.load("Herz_5.png")]
        self.coins = [pygame.image.load("Coin_0.png"), pygame.image.load("Coin_1.png"), pygame.image.load("Coin_2.png"),
                      pygame.image.load("Coin_3.png"), pygame.image.load("Coin_4.png"), pygame.image.load("Coin_5.png"),
                      pygame.image.load("Coin_6.png"), pygame.image.load("Coin_7.png"), pygame.image.load("Coin_8.png"),
                      pygame.image.load("Coin_9.png")]
        self.sword_rez = [pygame.image.load("Swd_Rez_0.png"), pygame.image.load("Swd_Rez_1.png"), pygame.image.load("Swd_Rez_2.png"),
                          pygame.image.load("Swd_Rez_3.png"), pygame.image.load("Swd_Rez_4.png")]

    def update(self):
        if self.herz_count <= 5:
            screen.blit(self.herz[self.herz_count], (screen_width - 120, 0))
            screen.blit(self.coins[self.coin_count], (screen_width - 220, 0))
            if swd.sword_use <= 0:
                screen.blit(self.sword_rez[4], (screen_width - 300, 0))
            elif swd.sword_use <= 15:
                screen.blit(self.sword_rez[3], (screen_width - 300, 0))
            elif swd.sword_use <= 30:
                screen.blit(self.sword_rez[2], (screen_width - 300, 0))
            elif swd.sword_use <= 45:
                screen.blit(self.sword_rez[1], (screen_width - 300, 0))
            elif swd.sword_use <= 60:
                screen.blit(self.sword_rez[0], (screen_width - 300, 0))


class Player:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.animate_down = [pygame.image.load("Player.png"), pygame.image.load("F_Step_1.png"), pygame.image.load("F_Step_2.png"),
                             pygame.image.load("Player.png"), pygame.image.load("F_Step_3.png"), pygame.image.load("F_Step_4.png")]
        self.animate_up = [pygame.image.load("Player_H.png"), pygame.image.load("H_Step_1.png"), pygame.image.load("H_Step_2.png"),
                           pygame.image.load("Player_H.png"), pygame.image.load("H_Step_3.png"), pygame.image.load("H_Step_4.png")]
        self.animate_l = [pygame.image.load("Player_L.png"), pygame.image.load("L_Step_1.png"), pygame.image.load("L_Step_2.png"),
                          pygame.image.load("Player_L.png"), pygame.image.load("L_Step_3.png"), pygame.image.load("L_Step_4.png")]
        self.animation_count = 0
        self.last_input = 0
        self.moving_dir = 0

    def movement(self):
        if pressed[pygame.K_a]:
            self.last_input = 2
            self.moving_dir = 2
            if -map_size <= display_scroll[0] <= map_size:
                display_scroll[0] -= SPEED
            elif display_scroll[0] < -map_size or display_scroll[0] > map_size:
                self.x -= SPEED
                display_scroll[0] -= SPEED
                if self.x < 25:
                    self.x += SPEED
                    display_scroll[0] += SPEED
        if pressed[pygame.K_d]:
            self.last_input = 4
            self.moving_dir = 4
            if -map_size <= display_scroll[0] <= map_size:
                display_scroll[0] += SPEED
            elif display_scroll[0] < -map_size or display_scroll[0] > map_size:
                self.x += SPEED
                display_scroll[0] += SPEED
            if self.x + self.width > screen_width - 25:
                self.x -= SPEED
                display_scroll[0] -= SPEED
        if pressed[pygame.K_w]:
            self.last_input = 1
            self.moving_dir = 1
            if -map_size <= display_scroll[1] <= map_size:
                display_scroll[1] -= SPEED
            elif display_scroll[1] < -map_size or display_scroll[1] > map_size:
                display_scroll[1] -= SPEED
                self.y -= SPEED
            if self.y < wall_size - 20:
                self.y += SPEED
                display_scroll[1] += SPEED
        if pressed[pygame.K_s]:
            self.last_input = 3
            self.moving_dir = 3
            if -map_size <= display_scroll[1] <= map_size:
                display_scroll[1] += SPEED
            elif display_scroll[1] < -map_size or display_scroll[1] > map_size:
                display_scroll[1] += SPEED
                self.y += SPEED
            if self.y + self.height > screen_height - 25:
                display_scroll[1] -= SPEED
                self.y -= SPEED

    def animate(self):
        self.animation_count += 1
        if self.animation_count + 1 > 24:
            self.animation_count = 0
        if self.last_input == 1 and self.moving_dir != 1:
            screen.blit(self.animate_up[0], (self.x, self.y))
        if self.last_input == 1 and self.moving_dir == 1:
            screen.blit(self.animate_up[self.animation_count//4], (self.x, self.y))
        if self.last_input == 2 and self.moving_dir != 2:
            screen.blit(self.animate_l[0], (self.x, self.y))
        if self.last_input == 2 and self.moving_dir == 2:
            screen.blit(self.animate_l[self.animation_count//4], (self.x, self.y))
        if self.last_input == 3 and self.moving_dir != 3:
            screen.blit(self.animate_down[0], (self.x, self.y))
        if self.last_input == 3 and self.moving_dir == 3:
            screen.blit(self.animate_down[self.animation_count//4], (self.x, self.y))
        if self.last_input == 4 and self.moving_dir != 4:
            screen.blit(pygame.transform.flip(self.animate_l[0], True, False), (self.x, self.y))
        if self.last_input == 4 and self.moving_dir == 4:
            screen.blit(pygame.transform.flip(self.animate_l[self.animation_count//4], True, False), (self.x, self.y))
        self.moving_dir = 0
        if self.last_input == 0 and self.moving_dir == 0:
            screen.blit(self.animate_down[0], (self.x, self.y))

    def update(self):
        self.movement()
        self.animate()


class Sword:
    def __init__(self):
        self.sword_rez = 0
        self.sword_use = 60
        self.x = -5000
        self.y = -5000

    def update(self):
        if pressed[pygame.K_SPACE] and self.sword_use > 0:
            if player.last_input == 1:
                screen.blit(pygame.transform.scale(pygame.image.load("Sword_Up.png"), (21, 42)), (player.x, player.y - 42))
                self.x = player.x
                self.y = player.y - 42
            if player.last_input == 2:
                screen.blit(pygame.transform.scale(pygame.image.load("Sword_L.png"), (42, 21)), (player.x - 42, player.y + 22))
                self.x = player.x - 42
                self.y = player.y + 22
            if player.last_input == 3:
                screen.blit(pygame.transform.flip(pygame.transform.scale(pygame.image.load("Sword_Up.png"), (21, 42)), False, True), (player.x + 15, player.y + player.height))
                self.x = player.x + 15
                self.y = player.y + player.height
            if player.last_input == 4:
                screen.blit(pygame.transform.flip(pygame.transform.scale(pygame.image.load("Sword_L.png"), (42, 21)), True, False), (player.x + player.width, player.y + 22))
                self.x = player.x + player.width
                self.y = player.y + 22
            self.sword_use -= 1
        else:
            self.sword_rez += 1
            if self.sword_rez == 120:
                self.sword_use = 60
                self.sword_rez = 0


class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 32
        self.height = 42
        self.enemy_input = 0
        self.lives = 7
        self.counter = 0
        self.move = False
        self.left = False

    def update(self):
        if self.lives > 0:
            self.attack()
            self.collision()
            self.animate()

    def attack(self):
        if -map_size <= display_scroll[0] <= map_size:
            if pressed[pygame.K_a]:
                self.x += SPEED
            if pressed[pygame.K_d]:
                self.x -= SPEED
        if -map_size <= display_scroll[1] <= map_size:
            if pressed[pygame.K_w]:
                self.y += SPEED
            if pressed[pygame.K_s]:
                self.y -= SPEED

        offset = [(self.x - player.x), (self.y - player.y)]
        if abs(offset[0]) <= 300 and abs(offset[1]) <= 300:  # inactive enemy at certain offset
            if self.x + self.width < player.x:
                self.x += random.randrange(2, 5)
                self.enemy_input = 4
                self.move = True
                self.left = False
            if self.x > player.x + player.width:
                self.x -= random.randrange(2, 5)
                self.enemy_input = 2
                self.move = True
                self.left = True
            if self.y + self.height < player.y:
                self.y += random.randrange(2, 5)
                self.enemy_input = 3
                self.move = True
            if self.y > player.y + player.height:
                self.y -= random.randrange(2, 5)
                self.enemy_input = 1
                self.move = True

    def collision(self):
        global game_over
        global game
        knockback = 80
        if o.herz_count <= 5:
            # collision player
            if collide(self.x, self.y, player.x, player.y, self.width, self.height, player.width, player.height):
                if self.enemy_input == 1:
                    self.y += knockback
                    o.herz_count += 1
                if self.enemy_input == 2:
                    self.x += knockback
                    o.herz_count += 1
                if self.enemy_input == 3:
                    self.y -= knockback
                    o.herz_count += 1
                if self.enemy_input == 4:
                    self.x -= knockback
                    o.herz_count += 1
                if self.y < wall_size - 20:
                    self.y = wall_size - 20
                if self.y + self.height > screen_height - 25:
                    self.y = screen_height - 25 - self.height
                if self.x < 25:
                    self.x = 25
                if self.x + self.width > screen_width - 25:
                    self.x = screen_width - 25 - self.width
        else:
            game_over = True
            game = False
        if player.last_input == 1 or player.last_input == 3:
            # collision sword
            if collide(self.x, self.y, swd.x, swd.y, self.width, self.height, 21, 42):
                if self.enemy_input == 1:
                    self.y += knockback
                    self.lives -= 1
                if self.enemy_input == 3:
                    self.y -= knockback
                    self.lives -= 1
                if self.y < wall_size - 20:
                    self.y = wall_size - 20
                if self.y + self.height > screen_height - 25:
                    self.y = screen_height - 25 - self.height
            swd.x = -5000
            swd.y = -5000
        if player.last_input == 2 or player.last_input == 4:
            if collide(self.x, self.y, swd.x, swd.y, self.width, self.height, 42, 21):
                if self.enemy_input == 2:
                    self.x += knockback
                    self.lives -= 1
                if self.enemy_input == 4:
                    self.x -= knockback
                    self.lives -= 1
                if self.x < 25:
                    self.x = 25
                if self.x + self.width > screen_width - 25:
                    self.x = screen_width - 25 - self.width
            swd.x = -5000
            swd.y = -5000
        # chest enemy collision does not work yet
        '''if not(self.x > chest.new_x + 88 or self.x + self.width < chest.new_x or self.y > chest.new_y + 64 or self.y + self.height < chest.new_y):
            if self.x + self.width > chest.new_x:
                self.x = chest.new_x - self.width
            if self.y < chest.new_y + 64:
                self.y = chest.new_y + 64
            if self.x > chest.new_x + 88:
                self.x = chest.new_x + 88
            if self.y + self.height > chest.new_y:
                self.y = chest.new_y - self.height'''

    def animate(self):
        self.counter += 1
        if self.move is True:
            if self.left is False:
                if self.counter >= 16:
                    self.counter = 0
                if self.counter <= 3:
                    screen.blit(pygame.image.load("enemy_0.png"), (self.x - 8, self.y + 3))
                elif self.counter <= 7:
                    screen.blit(pygame.image.load("enemy_1.png"), (self.x - 5, self.y))
                elif self.counter <= 11:
                    screen.blit(pygame.image.load("enemy_2 .png"), (self.x - 5, self.y - 6))
                elif self.counter <= 15:
                    screen.blit(pygame.image.load("enemy_1.png"), (self.x - 5, self.y))
                self.move = False
            if self.left is True:
                if self.counter >= 16:
                    self.counter = 0
                if self.counter <= 3:
                    screen.blit(pygame.transform.flip(pygame.image.load("enemy_0.png"), True, False), (self.x - 8, self.y + 3))
                elif self.counter <= 7:
                    screen.blit(pygame.transform.flip(pygame.image.load("enemy_1.png"), True, False), (self.x - 5, self.y))
                elif self.counter <= 11:
                    screen.blit(pygame.transform.flip(pygame.image.load("enemy_2 .png"), True, False), (self.x - 5, self.y - 6))
                elif self.counter <= 16:
                    screen.blit(pygame.transform.flip(pygame.image.load("enemy_1.png"), True, False), (self.x - 5, self.y))
                self.move = False
        else:
            if self.counter >= 36:
                self.counter = 0
            if self.counter <= 8:
                screen.blit(pygame.image.load("enemy_sleep_0.png"), (self.x - 8, self.y + 3))
            elif self.counter <= 16:
                screen.blit(pygame.image.load("enemy_sleep_1.png"), (self.x - 5, self.y))
            elif self.counter <= 24:
                screen.blit(pygame.image.load("enemy_sleep_2.png"), (self.x - 5, self.y - 6))
            elif self.counter <= 35:
                screen.blit(pygame.image.load("enemy_sleep_1.png"), (self.x - 5, self.y))


class Block:  # still buggy
    def __init__(self, x, y):
        self.width = 50
        self.height = self.width
        self.x = x
        self.y = y
        self.new_x = self.x
        self.new_y = self.y
    def main(self):
        if -map_size <= display_scroll[0] <= map_size:
            self.new_x = self.x - display_scroll[0]
        if -map_size <= display_scroll[1] <= map_size:
            self.new_y = self.y - display_scroll[1]
        if collide(self.new_x, self.new_y, player.x, player.y, self.width, self.height, player.width, player.height):
            if pressed[pygame.K_w]:
                player.y += SPEED + 5
                display_scroll[1] += SPEED + 5
            if pressed[pygame.K_a]:
                player.x += SPEED + 5
                display_scroll[0] += SPEED + 5
            if pressed[pygame.K_s]:
                player.y -= SPEED - 5
                display_scroll[1] -= SPEED - 5
            if pressed[pygame.K_d]:
                player.x -= SPEED - 5
                display_scroll[0] -= SPEED - 5

        screen.blit(pygame.transform.scale(pygame.image.load("Stein.png"), (self.width, self.height)), (self.new_x, self.new_y))


class Coins:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.new_x = self.x
        self.new_y = self.y
        self.got_coin = False
        self.collected = False

    def update(self):
        if self.collected is False:
            if -map_size <= display_scroll[0] <= map_size:
                self.new_x = self.x - display_scroll[0]
            if -map_size <= display_scroll[1] <= map_size:
                self.new_y = self.y - display_scroll[1]
            if (self.new_x > player.x + player.width or self.new_x + 28 < player.x or
                self.new_y > player.y + player.height or self.new_y + 28 < player.y) and self.got_coin is False:
                screen.blit(pygame.image.load("Coin.png"), (self.new_x, self.new_y))
            else:
                self.got_coin = True
                if self.collected is False:
                    o.coin_count += 1
                    self.collected = True


class Key:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.got_key = False
        self.new_x = self.x
        self.new_y = self.y

    def update(self):
        if self.got_key is False:
            if -map_size <= display_scroll[0] <= map_size:
                self.new_x = self.x - display_scroll[0]
            if -map_size <= display_scroll[1] <= map_size:
                self.new_y = self.y - display_scroll[1]
            if (self.new_x > player.x + player.width or self.new_x + 24 < player.x or
                self.new_y > player.y + player.height or self.new_y + 28 < player.y) and self.got_key is False:
                screen.blit(pygame.image.load("Key.png"), (self.new_x, self.new_y))
            else:
                self.got_key = True


class Chest:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.new_x = self.x
        self.new_y = self.y
        self.open = [pygame.image.load("Chest_0.png"), pygame.image.load("Chest_1.png")]
        self.open_count = 0
        self.counter = 0
        self.active_count = False
        self.counted = False

    def update(self):
        if -map_size <= display_scroll[0] <= map_size:
            self.new_x = self.x - display_scroll[0]
        if -map_size <= display_scroll[1] <= map_size:
            self.new_y = self.y - display_scroll[1]
        if not(self.new_x > player.x + player.width or self.new_x + 88 < player.x or
                self.new_y > player.y + player.height or self.new_y + 64 < player.y):
            if pressed[pygame.K_w]:
                player.y += SPEED
                display_scroll[1] += SPEED
            if pressed[pygame.K_d]:
                player.x -= SPEED
                display_scroll[0] -= SPEED
            if key.got_key is True and self.counter < 30:
                self.open_count = 1
                self.active_count = True
                if self.counted is False:
                    o.coin_count += 3
                    self.counted = True

        screen.blit(self.open[self.open_count], (self.new_x, self.new_y))
        if self.open_count == 1 and self.active_count is True and self.counter < 30:
            self.counter += 1
            screen.blit(pygame.image.load("Coinbag.png"), (self.new_x + 31, self.new_y - 7))


# Main Loop
while True:
    if game:
        pressed = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT or pressed[pygame.K_ESCAPE]:
                sys.exit()
        screen.fill((0, 0, 0))
        draw_bg()
        win()
        # actual program
        # update as a main function of each object/class
        # b.main()
        player.update()
        c1.update()
        c2.update()
        c3.update()
        c4.update()
        c5.update()
        c6.update()
        key.update()
        swd.update()
        e.update()
        swd.update()
        e2.update()
        swd.update()
        e3.update()
        chest.update()
        o.update()

        pygame.display.flip()  # update the image
    # menu screen
    if start is True or game_over is True or winner is True:
        pressed = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT or pressed[pygame.K_ESCAPE]:
                sys.exit()
        screen.fill((0, 0, 0))
        pygame.mouse.set_visible(True)
        draw_rect()
        if event.type == pygame.MOUSEBUTTONDOWN and over_button is True:
            # Class objects
            player = Player(400, 320, 32, 48)
            c1 = Coins(62.5, -387.5)
            c2 = Coins(-337.5, -237.5)
            c3 = Coins(412.5, 112.5)
            c4 = Coins(812.5, 812.5)
            c5 = Coins(612.5, -137.5)
            c6 = Coins(212.5, 712.5)
            key = Key(-337.5, 912.5)
            swd = Sword()
            e = Enemy(-37.5, -387.5)
            e2 = Enemy(-287.5, 887.5)
            e3 = Enemy(1175, - 350)
            chest = Chest(1156, -420)
            o = Overlay()
            o.herz_count = 0
            o.coin_count = 0
            display_scroll = [0, 0]
            # b = Block(250, 100)
            start = False
            game_over = False
            winner = False
            game = True
            pygame.mouse.set_visible(False)
    # end
    pygame.display.update()
    clock.tick(30)
