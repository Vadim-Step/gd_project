from gd_classes import *
import pygame
from pygame import mixer
import random

FPS = 100

pygame.init()
size = width, height = 1900, 500
screen = pygame.display.set_mode(size)

level1_passed = 0
level2_passed = 0
level3_passed = 0
level1_perc = 0
level2_perc = 0
level3_perc = 0


def start_level(event, flag):
    if event.type == pygame.MOUSEBUTTONDOWN and flag:
        if 450 <= event.pos[0] <= 645 and 250 <= event.pos[1] <= 455:
            level = 1
        elif 850 <= event.pos[0] <= 1045 and 250 <= event.pos[1] <= 455:
            level = 2
        elif 1250 <= event.pos[0] <= 1445 and 250 <= event.pos[1] <= 455:
            level = 3
        else:
            level = 0
        if level != 0:
            percentage = 0
            flag = False
            mixer.pre_init()
            mixer.init()
            audio = mixer.Sound('gd_data\gd_mus1.mp3')
            #audio.play()
            return percentage, flag, audio, level
        return False


def count_percent(level_x, tiles_group, player, percent):
    koeff = level_x / 100
    for i in tiles_group:
        if i.rect:
            if i.rect.x - 10 <= player.rect.x - 30 <= i.rect.x + 10:
                percentage = int(i.pos_x / koeff) + 2
                return percentage
    return percent


def renew():
    all_sprites.empty()
    tiles_group.empty()
    wall_group.empty()
    end_group.empty()
    spike_group.empty()
    blade_group.empty()
    player_group.empty()
    portal1_group.empty()
    portal2_group.empty()
    start_group.empty()
    death_group.empty()


def start():
    global level1_passed, level2_passed, level3_passed, level1_perc, level2_perc, level3_perc
    fon = pygame.transform.scale(load_image('gd_fon.png'), (1900, 600))
    screen.blit(fon, (0, 0))
    lvl1 = load_image('easy.png')
    screen.blit(lvl1, (450, 250))
    lvl2 = load_image('normal1.png')
    screen.blit(lvl2, (850, 250))
    lvl3 = load_image('harder1.png')
    screen.blit(lvl3, (1250, 250))
    pygame.display.set_caption('Перемещение героя. Новый уровень')
    tick = load_image('tick1.png')
    flag = True
    camera = Camera()
    player = False
    stage = 0
    count = 0
    FPS = 100
    jumping = False
    speed = 0.1
    PAUSE = False
    play = pygame.transform.scale(load_image('play.jpg'), (50, 50))
    pause = pygame.transform.scale(load_image('pause.jpg'), (50, 50))
    len_count = 0
    portal1 = False
    portal2 = False
    death_effect = False
    moving_down = False
    fireworks = []
    smoke = []
    pulsating_effects = []
    death = 0
    level = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            lvl = start_level(event, flag)
            if lvl:
                percentage, flag, audio, level = lvl
                if level == 1:
                    file = 'gd_data/points.txt'
                    file2 = 'phon2.png'
                if level == 2:
                    file = 'gd_data/points2.txt'
                    file2 = 'fon.jpg'
                if level == 3:
                    file = 'gd_data/points.txt'
                    file2 = 'city.jpg'
                player, level_x, level_y = generate_level(load_level(file), level)
                fon2 = pygame.transform.scale(load_image(file2), (tile_size * level_x, 450))
                x = player.x
                y = player.y
                smoke_player = AnimatedSprite(load_image('smokepuff.png'), 8, 8,
                                              player.rect.x - 50, player.y, True)
                while len(pulsating_effects) < 20:
                    if level == 1:
                        pulsating_effect = AnimatedSprite(
                            load_image(f'effect{random.choice([1, 2])}.png'), 10, 6,
                            random.choice(range(100, tile_size * level_x)),
                            random.choice(range(100, 400)), False)
                    if level == 2:
                        pulsating_effect = AnimatedSprite(
                            load_image(f'effect{random.choice([3, 4])}.png'), 8, 2,
                            random.choice(range(100, tile_size * level_x)),
                            random.choice(range(100, 400)), False)
                    if level == 3:
                        pulsating_effect = AnimatedSprite(
                            load_image(f'effect{random.choice([5, 6])}.png'), 4, 4,
                            random.choice(range(100, tile_size * level_x)),
                            random.choice(range(100, 400)), False)
                    if not pygame.sprite.spritecollideany(pulsating_effect, wall_group) and \
                            not pygame.sprite.spritecollideany(pulsating_effect, portal1_group) \
                            and not pygame.sprite.spritecollideany(pulsating_effect, portal2_group) \
                            and not pygame.sprite.spritecollideany(pulsating_effect, blade_group):
                        pulsating_effects.append(pulsating_effect)
                    else:
                        pulsating_effect.kill()
            if event.type == pygame.MOUSEBUTTONDOWN and not flag:
                if 925 <= event.pos[0] <= 975 and 25 <= event.pos[1] <= 75:
                    PAUSE = False
                if 975 <= event.pos[0] <= 1025 and 25 <= event.pos[1] <= 75:
                    PAUSE = True
            if event.type == pygame.KEYDOWN:
                if not PAUSE and not death:
                    if event.key == pygame.K_UP:
                        if level == 1:
                            x_delta, y_delta = player.careful_move(0, 1, wall_group)
                            x += x_delta
                            y += y_delta
                        elif level != 1 and not moving_down:
                            jumping = True
                    if event.key == pygame.K_DOWN and level == 1:
                        x_delta, y_delta = player.careful_move(0, -1, wall_group)
                        x += x_delta
                        y += y_delta
                if event.key == pygame.K_SPACE:
                    PAUSE = not PAUSE
        if flag:
            font = pygame.font.Font(None, 100)
            if level1_passed:
                screen.blit(tick, (450, 400))
            else:
                percent = font.render(str(level1_perc) + '%', True, (100, 255, 100))
                screen.blit(percent, (500, 450))
            if level2_passed:
                screen.blit(tick, (850, 400))
            else:
                percent = font.render(str(level2_perc) + '%', True, (100, 255, 100))
                screen.blit(percent, (900, 450))
            if level3_passed:
                screen.blit(tick, (1250, 400))
            else:
                percent = font.render(str(level3_perc) + '%', True, (100, 255, 100))
                screen.blit(percent, (1300, 450))
        if player and not flag and not PAUSE:
            screen.fill((0, 0, 0))
            if not death:
                if level != 1:
                    jump(camera, jumping, count, player, stage)
                    if jumping and count % 3 == 0:
                        stage += 1
                        if stage == 20:
                            jumping = False
                            stage = 0
                    if count % 2 == 0 and not jumping:
                        x_delta, y_delta = player.careful_move(0, -0.14, wall_group)
                        x += x_delta
                        y += y_delta
                count += 1
                if player.collide_check(wall_group):
                    jumping = False
                    stage = 0
                    player.move(0, -0.25)
                camera.update(player)
                if not player.collide_check(wall_group) and \
                        not player.collide_check(end_group):
                    player.move(speed, 0)
                if player.collide_check(portal1_group) and not portal1:
                    if speed < 0.2:
                        speed += 0.05
                    portal1 = True
                if not player.collide_check(portal1_group):
                    portal1 = False
                if player.collide_check(portal2_group) and not portal2:
                    if speed > 0.06:
                        speed -= 0.05
                    portal2 = True
                if not player.collide_check(portal2_group):
                    portal2 = False
            if pygame.sprite.spritecollideany(player, end_group):
                if player.collide_check(end_group):
                    if not fireworks:
                        for i in range(25, 400, 100):
                            if level == 1:
                                firework = AnimatedSprite(load_image(f'firework1.png'), 6, 5,
                                                          player.rect.x - 25, i, False)
                            if level == 2:
                                firework = AnimatedSprite(load_image(f'firework2.png'), 5, 8,
                                                          player.rect.x - 25, i, False)
                            if level == 3:
                                firework = AnimatedSprite(load_image(f'firework3.png'), 5, 5,
                                                          player.rect.x - 25, i, False)
                            fireworks.append(firework)
                    FPS = 20
                    if level == 1:
                        level1_passed = True
                    if level == 2:
                        level2_passed = True
                    if level == 3:
                        level3_passed = True
            elif pygame.sprite.spritecollideany(player, wall_group) or \
                    player.collide_check(spike_group) or \
                    player.collide_check(blade_group):
                if not death:
                    if level == 1:
                        level1_perc = max(level1_perc, percentage)
                        death_effect = AnimatedSprite(load_image('death_effect1.png'), 8, 4,
                                                     player.rect.x - 50, player.rect.y - 70, False)
                    elif level == 2:
                        level2_perc = max(level2_perc, percentage)
                        death_effect = AnimatedSprite(load_image('death_effect2.png'), 4, 4,
                                                     player.rect.x - 50, player.rect.y - 70, False)
                    elif level == 3:
                        level3_perc = max(level3_perc, percentage)
                        death_effect = AnimatedSprite(load_image('death_effect3.png'), 5, 4,
                                                     player.rect.x - 50, player.rect.y - 70, False)
                FPS = 20
            if (level == 1 and death == 20) or (level > 1 and death == 15):
                screen.blit(fon, (0, 0))
                screen.blit(lvl1, (450, 250))
                screen.blit(lvl2, (850, 250))
                screen.blit(lvl3, (1250, 250))
                player = False
                jumping = False
                speed = 0.1
                death = False
                death_effect = False
                FPS = 100
                fireworks = []
                smoke = []
                pulsating_effects = []
                len_count, level, stage, percentage, camera.dy = 0, 0, 0, 0, 0
                flag = True
                audio.stop()
                renew()

        if not flag and not PAUSE:
            if not death:
                for sprite in all_sprites:
                    camera.apply(sprite)
                for i in start_group:
                    x = i.rect.x
                    break
            if death_effect:
                death_effect.update()
                death += 1
            for i in fireworks:
                i.update()
            if fireworks:
                death += 1
            if count % 10 == 0:
                for i in blade_group:
                    i.rotate()
            if not smoke:
                for i in range(0, 400, 50):
                    smok = AnimatedSprite(load_image('Smoke.png'), 6, 5,
                                          tile_size * level_x + 700, i, False)
                    smoke.append(smok)
            for i in smoke:
                i.update()
            screen.blit(fon2, (x + 50, 75))
            if count % 5 == 0:
                for i in pulsating_effects:
                    i.update()
            wall_group.draw(screen)
            spike_group.draw(screen)
            if not death:
                player_group.draw(screen)
            portal1_group.draw(screen)
            portal2_group.draw(screen)
            smoke_player.update()
            smoke_player.move(player.rect.x - 100, player.rect.y - 50)
            blade_group.draw(screen)
            death_group.draw(screen)
            font = pygame.font.Font(None, 50)
            pygame.draw.rect(screen, (76, 76, 76), (850, 25, 75, 50))
            len_count += speed
            to_blit = count_percent(level_x, tiles_group, player, percentage)
            percentage = to_blit
            perc = font.render(str(to_blit) + '%', True,
                               (100, 255, 100))
            screen.blit(perc, (850, 30))
            screen.blit(play, (925, 25))
            screen.blit(pause, (975, 25))

        pygame.display.flip()
        clock.tick(FPS)


pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((1900, 600))
start()
