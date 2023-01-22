import os
import sys
import pygame
import random
from module import Button

pygame.init()

FPS = 50
WIDTH = 850
HEIGHT = 550
STEP = 50

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

player = None
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
stone_group = pygame.sprite.Group()
monstr_group = pygame.sprite.Group()
monstr_group2 = pygame.sprite.Group()

pygame.mixer.music.load("sound/fon.mp3")
volume = 0.2
pygame.mixer.music.set_volume(volume)
pygame.mixer.music.play(-1)


def load_image(name, colorkey=None): # мне надо вместо none написать -1
    fullname = os.path.join('data', name)
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
    return image


def load_level(filename):
    filename = "data/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    print(max_width)
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(x, y)
    return new_player, x, y


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    intro_text = ["Спаси принцессу", "",
                  "Сюжет игры:",
                  "Ты рыцарь. Тебе",
                  "нужно спасти",
                  "принцессу от дракона.",
                  "Для этого тебе нужно",
                  "собрать сонные зелье.", "",
                  "Как играть:",
                  "Для движение исполь-",
                  "зуй стрелки на",
                  "клавиатуре.",
                  "Для вкл музыки",
                  "используй кнопку M,",
                  "а для выкл пробел"]
    # F0FFFF
    fon = pygame.transform.scale(load_image('fonpr.png'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    button = Button(213, 40, ('#A9A9A9'), ('#F0FFFF'))
    button.draw(5, 500, 'Начать игру', screen)
    font = pygame.font.Font(None, 25)
    font1 = pygame.font.Font(None, 15)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, True, pygame.Color('#98FB98'))
        intro_rect = string_rendered.get_rect()
        text_coord += 7
        intro_rect.top = text_coord
        intro_rect.x = 8
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            act = button.mouse_click(5, 500, 'Начать игру', screen)
            if act == 1:
                return
        pygame.display.flip()
        clock.tick(FPS)


tile_images = {'wall': load_image('stena.jpg'), 'empty': load_image('grass.jpg')}
player_image = load_image('prin.png')
stone_image = load_image('slepp1.png')
tile_width = tile_height = 50
monstr_image = load_image('dr.png')
monstr_image2 = load_image('dr2.png')


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(tile_width * pos_x + 15, tile_height * pos_y + 5)
        self.pos = (pos_x, pos_y)

    def update(self, x, y):
        self.pos = (x, y)
        self.rect = self.image.get_rect().move(
            tile_width * self.pos[0] + 15, tile_height * self.pos[1] + 5)


class Stone(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(stone_group, all_sprites)
        self.image = stone_image
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)


class Koshei(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(monstr_group, all_sprites)
        self.image = monstr_image
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)
        self.pos_x = tile_width * pos_x
        self.pos_y = tile_height * pos_y
        self.y_start = self.pos_y
        self.y_stop = self.y_start + 100
        self.step = 1

    def update(self):
        if self.pos_y > self.y_stop or self.pos_y < self.y_start:
            self.step = -self.step
        self.pos_y += self.step
        self.rect = self.image.get_rect().move(
            self.pos_x, self.pos_y)


class Koshei2(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(monstr_group2, all_sprites)
        self.image = monstr_image2
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)
        self.pos_x = tile_width * pos_x
        self.pos_y = tile_height * pos_y
        self.x_start = self.pos_x
        self.x_stop = self.x_start + 100
        self.step = 1

    def update(self):
        if self.pos_x > self.x_stop or self.pos_x < self.x_start:
            self.step = -self.step
        self.pos_x += self.step
        self.rect = self.image.get_rect().move(
            self.pos_x, self.pos_y)


def move(hero, movement, level_map, max_x, max_y):

    x, y = hero.pos
    if movement == "up":
        if y > 0 and (level_map[y - 1][x] == "." or level_map[y - 1][x] == "@"):
            hero.update(x, y - 1)
    elif movement == "down":
        if y < max_y and (level_map[y + 1][x] == "." or level_map[y + 1][x] == "@"):
            hero.update(x, y + 1)
    elif movement == "left":
        if x > 0 and (level_map[y][x - 1] == "." or level_map[y][x - 1] == "@"):
            hero.update(x - 1, y)
    elif movement == "right":
        if x < max_x and (level_map[y][x + 1] == "." or level_map[y][x + 1] == "@"):
            hero.update(x + 1, y)


def bad_end():
    img = load_image('g.jpg', -1)
    screen.blit(img, (150, 150))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
        pygame.display.flip()
        clock.tick(FPS)


def good_end():
    img = load_image('fon1.png')
    screen.blit(img, (0, 0))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
        pygame.display.flip()
        clock.tick(FPS)


def level_1():
    global timer, count_stone
    level_map = load_level("levelex.txt")
    player, max_x, max_y = generate_level(level_map)
    li1 = []
    k = 0
    while k != 5:
        x = random.randint(0, max_x - 1)
        y = random.randint(0, max_y - 1)
        if level_map[y][x] == '.' and (x, y) not in li1:
            k += 1
            li1.append((x, y))
    print(li1)
    for el in li1:
        izum = Stone(el[0], el[1])
        #stone_group.add(izum)

    running = True
    font_1 = pygame.font.Font(None, 50)
    font_2 = pygame.font.Font(None, 50)
    font_3 = pygame.font.Font(None, 19)
    font_4 = pygame.font.Font(None, 19)
    font_5 = pygame.font.Font(None, 19)
    text_name = font_1.render('Спаси принцессу!', True, (255, 255, 255))
    text_name1 = font_3.render('Тебе нужно собрать все сонные зелья,', True, (255, 255, 255))
    text_name2 = font_4.render('чтобы усыпить дракона и спасти', True, (255, 255, 255))
    text_name3 = font_5.render('прекрасную принцессу.', True, (255, 255, 255))

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == timer_event:
                timer -= 1
                print(timer)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    move(player, "up", level_map, max_x, max_y)
                elif event.key == pygame.K_DOWN:
                    move(player, "down", level_map, max_x, max_y)
                elif event.key == pygame.K_LEFT:
                    move(player, "left", level_map, max_x, max_y)
                elif event.key == pygame.K_RIGHT:
                    move(player, "right", level_map, max_x, max_y)

        screen.fill(pygame.Color('#003300'))  # цвет экрана в моем случаи розовый

        tiles_group.draw(screen)
        player_group.draw(screen)
        stone_group.draw(screen)
        monstr_group.draw(screen)

        conflict1 = pygame.sprite.spritecollide(player, stone_group, True)
        if conflict1:
            count_stone += 1
            print(count_stone)
        screen.blit(text_name, (550, 10))
        screen.blit(text_name1, (550, 70))
        screen.blit(text_name2, (550, 85))
        screen.blit(text_name3, (550, 100))
        text_timer = font_2.render(f'Время: {str(timer)}', True, (255, 255, 255)) # надо сделать красиво
        screen.blit(text_timer, (550, 150))
        text_count = font_2.render(f'Сонное Зелье: {str(count_stone)}', True, (255, 255, 255))
        screen.blit(text_count, (550, 300))
        monstr_group.update()
        if timer == 0:
            bad_end()
        if count_stone == 5:
            tiles_group.empty()
            player_group.empty()
            stone_group.empty()
            monstr_group.empty()
            all_sprites.empty()
            level_2() # переход на второй уровень
        pygame.display.flip()

        clock.tick(FPS)


def level_2():
    global timer, count_stone
    level_map = load_level("levelex2.txt")
    player, max_x, max_y = generate_level(level_map)
    li1 = []
    k = 0
    while k != 5:
        x = random.randint(0, max_x - 1)
        y = random.randint(0, max_y - 1)
        if level_map[y][x] == '.' and (x, y) not in li1:
            k += 1
            li1.append((x, y))
    print(li1)
    for el in li1:
        izum = Stone(el[0], el[1])
        stone_group.add(izum)

    m = Koshei(4, 7)
    monstr_group.add(m)
    m2 = Koshei(5, 2)
    monstr_group.add(m2)

    running = True
    font_1 = pygame.font.Font(None, 50)
    font_2 = pygame.font.Font(None, 50)
    font_3 = pygame.font.Font(None, 19)
    font_4 = pygame.font.Font(None, 19)
    font_5 = pygame.font.Font(None, 19)
    text_name = font_1.render('Спаси принцессу!', True, (255, 255, 255))
    text_name1 = font_3.render('Тебе нужно собрать все сонные зелья,', True, (255, 255, 255))
    text_name2 = font_4.render('чтобы усыпить дракона и спасти', True, (255, 255, 255))
    text_name3 = font_5.render('прекрасную принцессу.', True, (255, 255, 255))

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == timer_event:
                timer -= 1
                print(timer)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    move(player, "up", level_map, max_x, max_y)
                elif event.key == pygame.K_DOWN:
                    move(player, "down", level_map, max_x, max_y)
                elif event.key == pygame.K_LEFT:
                    move(player, "left", level_map, max_x, max_y)
                elif event.key == pygame.K_RIGHT:
                    move(player, "right", level_map, max_x, max_y)

        screen.fill(pygame.Color('#003300'))

        tiles_group.draw(screen)
        player_group.draw(screen)
        stone_group.draw(screen)
        monstr_group.draw(screen)

        conflict1 = pygame.sprite.spritecollide(player, stone_group, True)
        if conflict1:
            count_stone += 1
            print(count_stone)
        screen.blit(text_name, (550, 10))
        screen.blit(text_name1, (550, 70))
        screen.blit(text_name2, (550, 85))
        screen.blit(text_name3, (550, 100))
        text_timer = font_2.render(f'Время: {str(timer)}', True, (255, 255, 255))  # надо сделать красиво
        screen.blit(text_timer, (550, 150))
        text_count = font_2.render(f'Сонное Зелье: {str(count_stone)}', True, (255, 255, 255))
        screen.blit(text_count, (550, 300))
        monstr_group.update()
        if timer == 0:
            bad_end()
        if count_stone == 10:
            tiles_group.empty()
            player_group.empty()
            stone_group.empty()
            monstr_group.empty()
            all_sprites.empty()
            level_3()  # переход на второй уровень
        pygame.display.flip()

        clock.tick(FPS)


def level_3():
    global timer, count_stone
    level_map = load_level("levelex3.txt")
    player, max_x, max_y = generate_level(level_map)
    li1 = []
    k = 0
    while k != 5:
        x = random.randint(0, max_x - 1)
        y = random.randint(0, max_y - 1)
        if level_map[y][x] == '.' and (x, y) not in li1:
            k += 1
            li1.append((x, y))
    print(li1)
    for el in li1:
        izum = Stone(el[0], el[1])
        stone_group.add(izum)

    m = Koshei(4, 7)
    monstr_group.add(m)
    m2 = Koshei(8, 2)
    monstr_group.add(m2)
    m3 = Koshei2(7, 6)
    monstr_group.add(m3)
    m4 = Koshei2(2, 4)
    monstr_group.add(m4)


    running = True
    sound = True
    font_1 = pygame.font.Font(None, 50)
    font_2 = pygame.font.Font(None, 50)
    font_3 = pygame.font.Font(None, 19)
    font_4 = pygame.font.Font(None, 19)
    font_5 = pygame.font.Font(None, 19)
    text_name = font_1.render('Спаси принцессу!', True, (255, 255, 255))
    text_name1 = font_3.render('Тебе нужно собрать все сонные зелья,', True, (255, 255, 255))
    text_name2 = font_4.render('чтобы усыпить дракона и спасти', True, (255, 255, 255))
    text_name3 = font_5.render('прекрасную принцессу.', True, (255, 255, 255))

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == timer_event:
                timer -= 1
                print(timer)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused = not paused
                if event.key == pygame.K_m:
                    sound = not sound
                    if sound:
                        pygame.mixer.music.pause()
                    else:
                        pygame.mixer.music.unpause()
                if event.key == pygame.K_UP:
                    move(player, "up", level_map, max_x, max_y)
                elif event.key == pygame.K_DOWN:
                    move(player, "down", level_map, max_x, max_y)
                elif event.key == pygame.K_LEFT:
                    move(player, "left", level_map, max_x, max_y)
                elif event.key == pygame.K_RIGHT:
                    move(player, "right", level_map, max_x, max_y)

        screen.fill(pygame.Color('#003300'))

        tiles_group.draw(screen)
        player_group.draw(screen)
        stone_group.draw(screen)
        monstr_group.draw(screen)

        conflict1 = pygame.sprite.spritecollide(player, stone_group, True)
        if conflict1:
            count_stone += 1
            print(count_stone)
        screen.blit(text_name, (550, 10))
        screen.blit(text_name1, (550, 70))
        screen.blit(text_name2, (550, 85))
        screen.blit(text_name3, (550, 100))
        text_timer = font_2.render(f'Время: {str(timer)}', True, (255, 255, 255))  # надо сделать красиво
        screen.blit(text_timer, (550, 150))
        text_count = font_2.render(f'Сонное Зелье: {str(count_stone)}', True, (255, 255, 255))
        screen.blit(text_count, (550, 300))
        monstr_group.update()
        conflict2 = pygame.sprite.spritecollide(m, player_group, True)
        if conflict2:
            bad_end()
        conflict3 = pygame.sprite.spritecollide(m2, player_group, True)
        if conflict3:
            bad_end()
        conflict4 = pygame.sprite.spritecollide(m3, player_group, True)
        if conflict4:
            bad_end()
        conflict5 = pygame.sprite.spritecollide(m4, player_group, True)
        if conflict5:
            bad_end()
        if timer == 0 and count_stone != 15:
            bad_end()
        if timer >= 0 and count_stone == 15:
            good_end()
        pygame.display.flip()

        clock.tick(FPS)


start_screen()
timer = 60
timer_event = pygame.USEREVENT + 1
pygame.time.set_timer(timer_event, 1000)
count_stone = 0
level_1()
terminate()
