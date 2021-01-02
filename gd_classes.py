import pygame
import os
import sys

pygame.init()
size = width, height = 1900, 500
screen = pygame.display.set_mode(size)

all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
wall_group = pygame.sprite.Group()
end_group = pygame.sprite.Group()
start_group = pygame.sprite.Group()
spike_group = pygame.sprite.Group()
blade_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
death_group = pygame.sprite.Group()
portal1_group = pygame.sprite.Group()
portal2_group = pygame.sprite.Group()
groups = [tiles_group, wall_group, end_group, start_group, spike_group, blade_group, portal1_group,
          portal2_group]


def load_image(name, colorkey=None):
    fullname = os.path.join('gd_data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image.convert_alpha()


def jump(camera, jumping, fps_c, player, stage):
    if jumping and fps_c % 3 == 0:
        jump_stages = [-0.25, -0.25, -0.25, -0.25, -0.25, -0.25, -0.25, -0.25, -0.25, -0.25,
                       0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.44]
        jump = jump_stages[stage]
        player.move(0, jump)
        camera.update(player)
        for sprite in all_sprites:
            camera.apply(sprite)


def terminate():
    pygame.quit()
    sys.exit()


def load_level(filename):
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def generate_level(level, num=1):
    new_player, x, y = None, None, None
    if num == 1:
        for y in range(len(level)):
            for x in range(len(level[y])):
                if level[y][x] == '.':
                    Tile('empty', x, y)
                if level[y][x] == '*':
                    Tile('blade', x, y)
                if level[y][x] == '^':
                    Tile('blade1', x, y)
                if level[y][x] == '%':
                    Tile('blade2', x, y)
                if x == len(level[y]) - 1 and 0 < y < 10:
                    Tile('end', x, y)
                elif x == 0:
                    Tile('start', x, y)
                elif level[y][x] == '#':
                    Tile('wall', x, y)
                if level[y][x] == ':':
                    Tile('empty', x, y)
                    Tile('empty', x, y + 1)
                    Tile('portal1', x, y)
                if level[y][x] == '<':
                    Tile('empty', x, y)
                    Tile('spike', x, y)
                if level[y][x] == '>':
                    Tile('empty', x, y)
                    Tile('spike2', x, y)
                if level[y][x] == ';':
                    Tile('empty', x, y)
                    Tile('empty', x, y + 1)
                    Tile('portal2', x, y)
                if level[y][x] == '@':
                    Tile('empty', x, y)
                    new_player = Player(x, y, player_image1)
        return new_player, x, y
    if num == 2 or num == 3:
        for y in range(len(level)):
            for x in range(len(level[y])):
                if level[y][x] == '.':
                    Tile('empty2', x, y)
                if level[y][x] == '*':
                    Tile('blade', x, y)
                if level[y][x] == '^':
                    Tile('blade1', x, y)
                if level[y][x] == '%':
                    Tile('blade2', x, y)
                if x == len(level[y]) - 1:
                    Tile('end', x, y)
                if x == 0:
                    Tile('start', x, y)
                if level[y][x] == '#':
                    Tile('wall2', x, y)
                if level[y][x] == ':':
                    Tile('empty2', x, y)
                    Tile('empty2', x, y + 1)
                    Tile('portal1', x, y)
                if level[y][x] == ';':
                    Tile('empty2', x, y)
                    Tile('empty2', x, y + 1)
                    Tile('portal2', x, y)
                if level[y][x] == '<':
                    Tile('empty2', x, y)
                    Tile('spike', x, y)
                if level[y][x] == '>':
                    Tile('empty2', x, y)
                    Tile('spike2', x, y)
                if level[y][x] == '@':
                    Tile('empty2', x, y)
                    new_player = Player(x, y, player_image2)
        return new_player, x, y


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y, spin):
        super().__init__(all_sprites, death_group)
        self.frames = []
        self.spin = spin
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        if self.spin:
            self.image = pygame.transform.rotate(self.frames[self.cur_frame], 90)
        else:
            self.image = self.frames[self.cur_frame]

    def move(self, x, y):
        if x and y:
            self.rect.x = x
            self.rect.y = y


tile_images = {
    'wall2': load_image('objects/block1.png'),
    'wall': load_image('objects/gd_block.jpg'),
    'end': load_image('objects/gd_block.jpg'),
    'start': load_image('objects/gd_block.jpg'),
    'blade': load_image('objects/sawblade.png'),
    'blade1': load_image('objects/blade.png'),
    'blade2': load_image('objects/sawblade1.png'),
    'spike': load_image('objects/spike1.png'),
    'spike2': pygame.transform.flip(load_image('objects/spike1.png'), False, True),
    'empty': load_image('objects/gd_blue.png'),
    'empty2': load_image('objects/gd_pink.jpg'),
    'portal1': load_image('objects/portal1.png', -1),
    'portal2': load_image('objects/portal2.png', -1)
}
player_image1 = load_image('pictures/gdship.png', -1)
player_image2 = load_image('pictures/gd_icon1.png', 1)
player_image3 = load_image('pictures/gdship.png', 1)
tile_width = tile_height = tile_size = 50
player = None


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        if tile_type == 'wall' or tile_type == 'wall2':
            super().__init__(wall_group, all_sprites)
        elif tile_type == 'end':
            super().__init__(end_group, all_sprites)
        elif tile_type == 'start':
            super().__init__(start_group, all_sprites)
        elif tile_type == 'spike' or tile_type == 'spike2':
            super().__init__(spike_group, all_sprites)
        elif tile_type == 'blade' or tile_type == 'blade1' or tile_type == 'blade2':
            super().__init__(blade_group, all_sprites)
        elif tile_type == 'portal1':
            super().__init__(portal1_group, all_sprites)
        elif tile_type == 'portal2':
            super().__init__(portal2_group, all_sprites)
        elif tile_type == 'empty' or tile_type == 'empty2':
            super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 25, tile_height * pos_y + 25)
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.x = self.rect.x
        self.y = self.rect.y

    def rotate(self):
        self.image = pygame.transform.rotate(self.image, 90)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, player_image):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.x = pos_x
        self.y = pos_y
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 15 + 25, tile_height * pos_y + 5 + 25)

    def move(self, x, y):
        self.rect.x += x * tile_width
        self.rect.y += y * tile_height

    def careful_move(self, x, y, group):
        self.move(x, -y)
        if pygame.sprite.spritecollideany(self, group):
            self.move(-x, y)
            return 0, 0
        return x, y

    def collide_check(self, group):
        return pygame.sprite.spritecollideany(self, group)


class Camera:
    def __init__(self):
        self.dx = 0
        self.dy = 0

    def apply(self, obj):
        obj.rect.x += self.dx

    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - width // 2)
        self.dy += 1
