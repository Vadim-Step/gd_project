from gd_funct import *
import pygame
from pygame import mixer
import random

FPS = 100

pygame.init()
size = width, height = 1900, 500
screen = pygame.display.set_mode(size)

level1_passed = False
level2_passed = False
level3_passed = False
level1_perc = 0
level2_perc = 0
level3_perc = 0


def game_function():
    global level1_passed, level2_passed, level3_passed, level1_perc, level2_perc, level3_perc
    fon = pygame.transform.scale(load_image('pictures/gd_bg.jpg'), (2200, 600))
    screen.blit(fon, (-115, 0))
    lvl1, lvl2, lvl3 = load_image('pictures/easy.png'), load_image('pictures/normal1.png'), load_image(
        'pictures/harder1.png')
    screen.blit(lvl1, (450, 250))
    screen.blit(lvl2, (850, 250))
    screen.blit(lvl3, (1250, 250))
    clock = pygame.time.Clock()
    pygame.display.set_caption('GEOMETRY CRASH')
    tick = load_image('pictures/tick1.png')
    home = pygame.transform.scale(load_image('pictures/home-green.png'), (40, 40))
    flag = True
    camera = Camera()
    player, jumping, PAUSE, portal1, portal2, death_effect, moving_down = \
        False, False, False, False, False, False, False
    play = pygame.transform.scale(load_image('pictures/play.jpg'), (50, 50))
    pause = pygame.transform.scale(load_image('pictures/pause.jpg'), (50, 50))
    pulsating_effects, smoke, fireworks = [], [], []
    level, death, len_count, count, stage, FPS, speed = 0, 0, 0, 0, 0, 100, 0.1
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            level_data = start_level(event, flag)
            if level_data:
                percentage, flag, audio, level = level_data
                death_sound = mixer.Sound(f'gd_data/music/death_sound{level}.mp3')
                file = f'gd_data/levels/level{level}.txt'
                file2 = f'pictures/background{level}.jpg'
                player, level_x, level_y = generate_level(load_level(file), level)
                fon2 = pygame.transform.scale(load_image(file2), (tile_size * level_x, 450))
                x = player.x
                y = player.y
                smoke_player = AnimatedSprite(load_image('effects/smokepuff.png'), 8, 8,
                                              player.rect.x - 50, player.y, True)
                while len(pulsating_effects) < 20:
                    if level == 1:
                        pulsating_effect = AnimatedSprite(
                            load_image(f'effects/effect{random.choice([1, 2])}.png'), 10, 6,
                            random.choice(range(100, tile_size * level_x)),
                            random.choice(range(100, 400)), False)
                    if level == 2:
                        pulsating_effect = AnimatedSprite(
                            load_image(f'effects/effect{random.choice([3, 4])}.png'), 8, 2,
                            random.choice(range(100, tile_size * level_x)),
                            random.choice(range(100, 400)), False)
                    if level == 3:
                        pulsating_effect = AnimatedSprite(
                            load_image(f'effects/effect{random.choice([5, 6])}.png'), 4, 4,
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
                    mixer.unpause()
                if 975 <= event.pos[0] <= 1025 and 25 <= event.pos[1] <= 75:
                    PAUSE = True
                    mixer.pause()
                if 1025 <= event.pos[0] <= 1075 and 25 <= event.pos[1] <= 75:
                    screen.blit(fon, (-115, 0))
                    screen.blit(lvl1, (450, 250))
                    screen.blit(lvl2, (850, 250))
                    screen.blit(lvl3, (1250, 250))
                    player, jumping, PAUSE, portal1, portal2, death_effect, moving_down = \
                        False, False, False, False, False, False, False
                    pulsating_effects, smoke, fireworks = [], [], []
                    speed, death, FPS = 0.1, 0, 100
                    len_count, level, stage, percentage, camera.dy = 0, 0, 0, 0, 0
                    flag = True
                    audio.stop()
                    renew()
            if event.type == pygame.KEYDOWN:
                if not PAUSE and not death:
                    if event.key == pygame.K_UP:
                        if level == 1:
                            x_delta, y_delta = player.careful_move(0, 1, wall_group)
                            x += x_delta
                            y += y_delta
                        elif level != 1 and not moving_down and not jumping:
                            jumping = True
                    if event.key == pygame.K_DOWN and level == 1:
                        x_delta, y_delta = player.careful_move(0, -1, wall_group)
                        x += x_delta
                        y += y_delta
                if event.key == pygame.K_SPACE:
                    PAUSE = not PAUSE
                    if PAUSE:
                        mixer.pause()
                    else:
                        mixer.unpause()
        if flag:
            font = pygame.font.Font(None, 100)
            ticks = [(450, 400), (850, 400), (1250, 400)]
            coords = [(500, 450), (900, 450), (1300, 450)]
            percentages_levels = [level1_passed, level2_passed, level3_passed,
                                  level1_perc, level2_perc, level3_perc]
            for i in range(3):
                if percentages_levels[i]:
                    screen.blit(tick, ticks[i])
                else:
                    screen.blit(font.render(str(percentages_levels[i + 3]) + '%', True, (100, 255, 100)),
                                coords[i])
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
                        if x_delta or y_delta:
                            moving_down = True
                        else:
                            moving_down = False
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
                        fireworks_ = [(load_image(f'effects/firework1.png'), 6, 5, player.rect.x - 25),
                                      (load_image(f'effects/firework2.png'), 5, 8, player.rect.x - 25),
                                      (load_image(f'effects/firework3.png'), 5, 5, player.rect.x - 25)]
                        for i in range(25, 400, 100):
                            firework = AnimatedSprite(*fireworks_[level - 1], i, False)

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
                audio.stop()
                if not death:
                    death_sound.play()
                    if level == 1:
                        level1_perc = max(level1_perc, percentage)
                        death_effect = AnimatedSprite(load_image('effects/death_effect1.png'), 8, 4,
                                                      player.rect.x - 50, player.rect.y - 70, False)
                    elif level == 2:
                        level2_perc = max(level2_perc, percentage)
                        death_effect = AnimatedSprite(load_image('effects/death_effect2.png'), 4, 4,
                                                      player.rect.x - 50, player.rect.y - 70, False)
                    elif level == 3:
                        level3_perc = max(level3_perc, percentage)
                        death_effect = AnimatedSprite(load_image('effects/death_effect3.png'), 5, 4,
                                                      player.rect.x - 50, player.rect.y - 70, False)
                FPS = 20
            if (level == 1 and death == 20) or (level > 1 and death == 15):
                screen.blit(fon, (-115, 0))
                screen.blit(lvl1, (450, 250))
                screen.blit(lvl2, (850, 250))
                screen.blit(lvl3, (1250, 250))
                player, jumping, PAUSE, portal1, portal2, death_effect, moving_down = \
                    False, False, False, False, False, False, False
                speed, death, FPS = 0.1, 0, 100
                pulsating_effects, smoke, fireworks = [], [], []
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
                    smok = AnimatedSprite(load_image('effects/Smoke.png'), 6, 5,
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
            pygame.draw.rect(screen, (76, 76, 76), (1025, 25, 50, 50))
            len_count += speed
            to_blit = count_percent(level_x, tiles_group, player, percentage)
            percentage = to_blit
            percent = font.render(str(to_blit) + '%', True, (100, 255, 100))
            screen.blit(home, (1025, 33))
            screen.blit(percent, (850, 30))
            screen.blit(play, (925, 25))
            screen.blit(pause, (975, 25))

        pygame.display.flip()
        clock.tick(FPS)
