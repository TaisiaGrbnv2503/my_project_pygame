import os
import sys
import pygame

pygame.init()

FPS = 50
WIDTH = 550
HEIGHT = 550
STEP = 50

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

player = None
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()


def load_image(name, colorkey=None):
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
    intro_text = ["Марио движется", "",
                  "Нажмите любую кнопку чтобы начать играть",
                  "Используете стрелки вверх и",
                  " вниз для хождение наверх и вниз",
                  "Используете стрелки вправо и ",
                  " влево для хождение направо и налево"]

    fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(FPS)


tile_images = {'wall': load_image('pink_kirpich.jpg'), 'empty': load_image('kamen.jpg')}
player_image = load_image('pink_princess.webp')

tile_width = tile_height = 50


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group)
        self.image = player_image
        self.rect = self.image.get_rect().move(tile_width * pos_x + 15, tile_height * pos_y + 5)
        self.pos = (pos_x, pos_y)

    def move(self, x, y):
        self.pos = (x, y)
        self.rect = self.image.get_rect().move(
            tile_width * self.pos[0] + 15, tile_height * self.pos[1] + 5)


def move(hero, movement):
    x, y = hero.pos
    if movement == "up":
        if y > 0 and level_map[y - 1][x] == ".":
            hero.move(x, y - 1)
    elif movement == "down":
        if y < max_y - 1 and level_map[y + 1][x] == ".":
            hero.move(x, y + 1)
    elif movement == "left":
        if x > 0 and level_map[y][x - 1] == ".":
            hero.move(x - 1, y)
    elif movement == "right":
        if x < max_x - 1 and level_map[y][x + 1] == ".":
            hero.move(x + 1, y)


start_screen()
level_map = load_level("levelex.txt")
player, max_x, max_y = generate_level(level_map)


counter = 15

timer_event = pygame.USEREVENT+1
pygame.time.set_timer(timer_event, 1000)

running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == timer_event:
            counter -= 1
            print(counter)
            if counter == 0:
                running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                move(player, "up")
            elif event.key == pygame.K_DOWN:
                move(player, "down")
            elif event.key == pygame.K_LEFT:
                move(player, "left")
            elif event.key == pygame.K_RIGHT:
                move(player, "right")
    screen.fill(pygame.Color(0, 0, 0))
    tiles_group.draw(screen)
    player_group.draw(screen)

    pygame.display.flip()

    clock.tick(FPS)

terminate()