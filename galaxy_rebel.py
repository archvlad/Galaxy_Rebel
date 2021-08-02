import pygame
import math
import random
from pygame.time import get_ticks

width = 768
height = 600

pygame.init()
display_surface = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
pygame.display.set_caption('Galaxy Rebel')
icon = pygame.image.load('icon.png').convert_alpha()
pygame.display.set_icon(icon)


def game():
    pygame.mixer.music.load('battle.ogg')
    pygame.mixer.music.set_volume(1)
    pygame.mixer.music.play(-1)
    laser_snd = pygame.mixer.Sound('laser_snd.mp3')
    laser_enm_snd = pygame.mixer.Sound('laser_enm_snd.mp3')
    enm_lasers = []
    player_img = pygame.image.load('player.png').convert_alpha()
    bg_img = pygame.image.load('space.png').convert_alpha()
    laser = pygame.image.load('laser.png').convert_alpha()
    enemy = pygame.image.load('enemy.png').convert_alpha()
    enm_laser = pygame.image.load('enm_laser.png').convert_alpha()
    lasers = []
    enemies = []
    flag = False
    health = 100
    reload_time = 0
    px = py = 400
    bg_y = 0
    movex = movey = 0
    speed = 8
    laser_speed = 20
    pygame.time.set_timer(pygame.USEREVENT, 3000)
    running = True

    class Enemy:

        def __init__(self, x, y, rect):
            self.x = x
            self.y = y
            self.rect = rect
            self.flag = False
            self.reloading = 0
            self.lives = 3

        def shoot(self):
            if not self.flag:
                enm_lasers.append([self.x + 25, self.y - 15])
                laser_enm_snd.play()
                self.reloading = pygame.time.get_ticks()
                self.flag = True
            if self.flag:
                if pygame.time.get_ticks() - self.reloading >= 200:
                    self.flag = False

    def spawn_enemies():
        enemy_rect = []
        num = random.randint(2, 5)
        for i in range(num):
            ok = False
            while not ok:
                x = random.randint(0, width - 64)
                y = random.randint(-300, -64)
                en_rc = pygame.Rect(x, y, 64, 64)
                if pygame.Rect.collidelist(en_rc, enemy_rect) == -1:
                    enemy_rect.append(en_rc)
                    enemies.append(Enemy(x, y, en_rc))
                    ok = True
    spawn_enemies()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.USEREVENT:
                spawn_enemies()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            running = False
        movex = movey = 0
        if keys[pygame.K_w] and keys[pygame.K_a]:
            movey -= speed * math.sin(math.pi / 4)
            movex -= speed * math.cos(math.pi / 4)
        elif keys[pygame.K_w] and keys[pygame.K_d]:
            movey -= speed * math.sin(math.pi / 4)
            movex += speed * math.cos(math.pi / 4)
        elif keys[pygame.K_s] and keys[pygame.K_a]:
            movey += speed * math.sin(math.pi / 4)
            movex -= speed * math.cos(math.pi / 4)
        elif keys[pygame.K_s] and keys[pygame.K_d]:
            movey += speed * math.sin(math.pi / 4)
            movex += speed * math.cos(math.pi / 4)
        elif keys[pygame.K_w]:
            movey -= speed
        elif keys[pygame.K_s]:
            movey += speed
        elif keys[pygame.K_a]:
            movex -= speed
        elif keys[pygame.K_d]:
            movex += speed
        if keys[pygame.K_w] and keys[pygame.K_s]:
            movey = 0
        if keys[pygame.K_a] and keys[pygame.K_d]:
            movex = 0
        px += movex
        py += movey
        if px < 0:
            px = 0
        if px + player_img.get_width() > width:
            px = width - player_img.get_width()
        if py < 0:
            py = 0
        if py + player_img.get_height() > height:
            py = height - player_img.get_height()
        if keys[pygame.K_SPACE]:
            if not flag:
                flag = True
                lasers.append([px + 25, py])
                laser_snd.play()
                reload_time = pygame.time.get_ticks()
        if flag:
            if pygame.time.get_ticks() - reload_time >= 100:
                flag = False
        for enm in enemies:
            enm.y += 1.2
            enm.rect = pygame.Rect(enm.x, enm.y, 64, 32)
            if random.randint(1, 100) == 1:
                enm.shoot()
            if enm.y >= height:
                enemies.remove(enm)
        for enm_lsr in enm_lasers:
            enm_lsr[1] += 9
            if enm_lsr[1] >= height:
                enm_lasers.remove(enm_lsr)
            lst_rect = pygame.Rect(enm_lsr[0], enm_lsr[1], 15, 64)
            if lst_rect.colliderect(pygame.Rect(px, py + 32, 64, 32)):
                try:
                    health -= 10
                    if health <= 0:
                        running = False
                    enm_lasers.remove(enm_lsr)
                except ValueError:
                    pass
        for lsr in lasers:
            lsr[1] -= laser_speed
            if lsr[1] + 64 <= 0:
                lasers.remove(lsr)
            for enm in enemies:
                if enm.rect.colliderect(pygame.Rect(lsr[0], lsr[1], 15, 64)):
                    try:
                        lasers.remove(lsr)
                        enm.lives -= 1
                        if enm.lives == 0:
                            enemies.remove(enm)
                    except ValueError:
                        pass
        display_surface.blit(bg_img, (0, bg_y))
        for lsr in lasers:
            display_surface.blit(laser, lsr)
        for enm_lsr in enm_lasers:
            display_surface.blit(enm_laser, enm_lsr)
        display_surface.blit(player_img, (px, py))
        for enm in enemies:
            display_surface.blit(enemy, (enm.x, enm.y))
            pygame.draw.rect(display_surface, (50, 50, 50),
                             (enm.x, enm.y - 3, 64, 5), border_radius=3)
            pygame.draw.rect(display_surface, (230, 0, 0),
                             (enm.x, enm.y - 3, (enm.lives / 3) * 64, 5), border_radius=3)
        pygame.draw.rect(display_surface, (50, 50, 50),
                         (px, py + 64, 64, 5), border_radius=3)
        pygame.draw.rect(display_surface, (0, 230, 0),
                         (px, py + 64, (health / 100) * 64, 5), border_radius=3)
        pygame.display.update()
        clock.tick(60)


def menu():
    music = pygame.mixer.music.load('music_2.ogg')
    pygame.mixer.music.set_volume(1)
    pygame.mixer.music.play(-1)
    back_menu = pygame.image.load('back_menu.png').convert_alpha()
    select_btn = pygame.image.load('select_btn.png').convert_alpha()
    runnings = True
    play_btn = pygame.rect.Rect(30, 300, 300, 75)
    options_btn = pygame.rect.Rect(30, 390, 300, 75)
    credits_btn = pygame.rect.Rect(30, 480, 300, 75)
    while runnings:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                runnings = False
        mouse = pygame.mouse.get_pos()
        display_surface.blit(back_menu, (0, 0))
        if pygame.Rect.collidepoint(play_btn, mouse):
            display_surface.blit(select_btn, play_btn)
            if pygame.mouse.get_pressed()[0]:
                game()
        if pygame.Rect.collidepoint(options_btn, mouse):
            display_surface.blit(select_btn, options_btn)
            if pygame.mouse.get_pressed()[0]:
                pass
        if pygame.Rect.collidepoint(credits_btn, mouse):
            display_surface.blit(select_btn, credits_btn)
            if pygame.mouse.get_pressed()[0]:
                pass
        print('menu')
        print(pygame.mouse.get_pressed())
        pygame.display.update()
        clock.tick(60)


menu()

pygame.quit()
