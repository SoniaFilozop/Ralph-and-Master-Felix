import pygame
import os
import sys
import random

number = 1
names_level = ["level1.txt", "level2.txt", "level3.txt", "level4.txt", "level5.txt"]
t = 0
score = 0
kir = []
num = 0
tiles = []
level_g = []
level_number = 1
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
tile_width = tile_height = 50
hod = 1
move = 1


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


tile_images = {
    'window': load_image('window1.png'),
    'window1': load_image('window2.png')
}


class Tile(pygame.sprite.Sprite):
    global tiles

    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            int(tile_width * pos_x), int(tile_height * pos_y))
        tiles.append(self)


def updates_tiles(number):
    global tiles
    tiles[number].image = load_image("window1.png")


def generate_level(level):
    x, y = None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '#':
                Tile('window', x + 3.55, y + 3.3)
            elif level[y][x] == '@':
                Tile('window1', x + 3.55, y + 3.3)
    return x, y


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(all_sprites)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)
        self.mask = pygame.mask.from_surface(self.image)

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
        self.image = self.frames[self.cur_frame]

    def move(self, x, y):
        self.rect.x += x
        self.rect.y += y

    def return_x(self):
        return self.rect.x

    def return_y(self):
        return self.rect.y


class Kirpich(pygame.sprite.Sprite):
    image = load_image("kirpich.png")

    def __init__(self, group):
        super().__init__(group)
        self.image = Kirpich.image
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(200, 300)
        self.rect.y = random.randrange(200, 240)
        self.mask = pygame.mask.from_surface(self.image)

    def delete_this(self, name):
        # если ещё в небе
        if pygame.sprite.collide_mask(self, name) and self.alive():
            lose()


class Ochki(pygame.sprite.Sprite):
    image = load_image("och.png")

    def __init__(self, group):
        super().__init__(group)
        self.image = Ochki.image
        self.rect = self.image.get_rect()


def load_level(filename):
    global level_g
    filename = "data/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('.')
    level_g = list(map(lambda x: x.ljust(max_width, '.'), level_map))
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


FPS = 100


def terminate():
    pygame.quit()
    sys.exit()


def instruction():
    global t
    # Функция выводит правила игры и закрывается автоматически через некоторое время.
    size = width, height = 600, 500
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    clock.tick()
    fon = pygame.transform.scale(load_image('instr.png'), (width, height))
    screen.blit(fon, (0, 0))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        if pygame.time.get_ticks() >= (t + 7000):
            return
        pygame.display.flip()
        clock.tick(FPS)


def start_screen():
    global level_number
    global t
    size = width, height = 600, 500
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    intro_text = ["Нажмите пробел, чтобы запустить первый уровень", "Нажмите цифры 1 - 5 для выбора уровня"]

    fon = pygame.transform.scale(load_image('start.png'), (width, height))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 435
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 30
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    t = pygame.time.get_ticks()
                    return
                elif event.key == pygame.K_1:
                    level_number = 1
                    t = pygame.time.get_ticks()
                    return
                elif event.key == pygame.K_2:
                    level_number = 2
                    t = pygame.time.get_ticks()
                    return
                elif event.key == pygame.K_3:
                    level_number = 3
                    t = pygame.time.get_ticks()
                    return
                elif event.key == pygame.K_4:
                    level_number = 4
                    t = pygame.time.get_ticks()
                    return
                elif event.key == pygame.K_5:
                    level_number = 5
                    t = pygame.time.get_ticks()
                    return
        pygame.display.flip()
        clock.tick(FPS)


def win():
    size = width, height = 600, 500
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    intro_text = ["Score: " + str(score)]
    pygame.mixer.music.load("data/win.mp3")
    pygame.mixer.music.play()
    pygame.mixer.music.set_volume(0.5)
    # Функция активируется, когда все окна починены. Она выводит сообщение о выигрыше и количество набранных очков
    fon = pygame.transform.scale(load_image('you_win.png'), (width, height))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 450
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 30
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    while True:
        for event in pygame.event.get():
            # При нажатии на любую кнопку мыши, крестик или на пробел, игра закрывается
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    terminate()
        pygame.display.flip()
        clock.tick(FPS)


def lose():
    size = width, height = 600, 500
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    intro_text = ["Score: " + str(score)]
    pygame.mixer.music.load("data/game_over.mp3")
    pygame.mixer.music.play()
    pygame.mixer.music.set_volume(0.5)
    # Функция активируется, когда в героя попадает кирпич.
    # Она выводит сообщение о проигрыше и количество набранных очков
    fon = pygame.transform.scale(load_image('game_over.png'), (width, height))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 450
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 30
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    while True:
        for event in pygame.event.get():
            # При нажатии на любую кнопку мыши, крестик или на пробел, игра закрывается
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    terminate()
        pygame.display.flip()
        clock.tick(FPS)


if __name__ == '__main__':
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    pygame.init()
    pygame.mixer.music.load("data/music_fon.mp3")
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.5)
    # Создаем основное окно игры
    pygame.display.set_caption('Ральф и мастер Феликс')
    size = width, height = 600, 500
    screen = pygame.display.set_mode(size)
    running = True
    # Запускаем стартовое окно
    start_screen()
    instruction()
    clock = pygame.time.Clock()
    all_sprites = pygame.sprite.Group()
    sprite = pygame.sprite.Sprite()
    sprite.image = load_image("Build.png")
    sprite.rect = sprite.image.get_rect()
    all_sprites.add(sprite)
    sprite.rect.x = 150
    sprite.rect.y = 150
    # Инициализируем уровень из текстового файла и создаем карту
    level_x, level_y = generate_level(load_level(names_level[level_number - 1]))
    # Создаем все нужные анимации
    walk = AnimatedSprite(load_image("walk.png"), 3, 1, 160, 140)
    felix = AnimatedSprite(load_image("felix.png"), 4, 1, 178, 330)
    bit = AnimatedSprite(load_image("bit.png"), 2, 1, 230, 140)
    och = Ochki(all_sprites)
    for _ in range(5):
        kir.append(Kirpich(all_sprites))
    clock.tick(5)
    # Добавляем анимированные спрайты в общую группу спрайтов
    all_sprites.add(bit)
    all_sprites.add(walk)
    all_sprites.add(felix)
    while running:
        och.kill()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                # При нажатии на стрелки клавиатуры, двигаем героя вверх, вниз, вправо или влево
                if event.key == pygame.K_LEFT:
                    if 150 <= (felix.return_x() - 45) <= 330:
                        felix.move(-47, 0)
                        prig = pygame.mixer.Sound("data/prig.wav")
                        prig.play()
                elif event.key == pygame.K_RIGHT:
                    if 150 <= (felix.return_x() + 45) <= 330:
                        felix.move(47, 0)
                        prig = pygame.mixer.Sound("data/prig.wav")
                        prig.play()
                elif event.key == pygame.K_UP:
                    if 120 <= (felix.return_y() - 55) <= 340:
                        felix.move(0, -55)
                        number += 1
                        prig = pygame.mixer.Sound("data/prig.wav")
                        prig.play()
                elif event.key == pygame.K_DOWN:
                    if 120 <= (felix.return_y() + 55) <= 340:
                        felix.move(0, 55)
                        number += 1
                        prig = pygame.mixer.Sound("data/prig.wav")
                        prig.play()
                # При нажатии на пробел, герой чинит окно, если оно сломанно, и зарабатывает 500 очков
                elif event.key == pygame.K_SPACE:
                    if 150 <= felix.return_x() <= 197 and 120 <= felix.return_y() <= 175:
                        if level_g[0][0] == '@':
                            och.rect.x = felix.return_x() + 35
                            och.rect.y = felix.return_y() - 10
                            all_sprites.add(och)
                            score += 500
                            level_g[0] = '#' + level_g[0][1:]
                            num = 0
                            okno = pygame.mixer.Sound("data/okno.wav")
                            okno.play()
                    elif 197 <= felix.return_x() <= 244 and 120 <= felix.return_y() <= 175:
                        if level_g[0][1] == '@':
                            och.rect.x = felix.return_x() + 35
                            och.rect.y = felix.return_y() - 10
                            all_sprites.add(och)
                            score += 500
                            level_g[0] = level_g[0][0] + '#' + level_g[0][2:]
                            num = 1
                            okno = pygame.mixer.Sound("data/okno.wav")
                            okno.play()
                    elif 244 <= felix.return_x() <= 291 and 120 <= felix.return_y() <= 175:
                        if level_g[0][2] == '@':
                            och.rect.x = felix.return_x() + 35
                            och.rect.y = felix.return_y() - 10
                            all_sprites.add(och)
                            score += 500
                            level_g[0] = level_g[0][:2] + '#' + level_g[3][3]
                            num = 2
                            okno = pygame.mixer.Sound("data/okno.wav")
                            okno.play()
                    elif 291 <= felix.return_x() <= 330 and 120 <= felix.return_y() <= 175:
                        if level_g[0][3] == '@':
                            och.rect.x = felix.return_x() + 35
                            och.rect.y = felix.return_y() - 10
                            all_sprites.add(och)
                            score += 500
                            level_g[0] = level_g[0][:3] + '#'
                            num = 3
                            okno = pygame.mixer.Sound("data/okno.wav")
                            okno.play()
                    elif 150 <= felix.return_x() <= 197 and 175 <= felix.return_y() <= 230:
                        if level_g[1][0] == '@':
                            och.rect.x = felix.return_x() + 35
                            och.rect.y = felix.return_y() - 10
                            all_sprites.add(och)
                            score += 500
                            level_g[1] = '#' + level_g[1][1:]
                            num = 4
                            okno = pygame.mixer.Sound("data/okno.wav")
                            okno.play()
                    elif 197 <= felix.return_x() <= 244 and 175 <= felix.return_y() <= 230:
                        if level_g[1][1] == '@':
                            och.rect.x = felix.return_x() + 35
                            och.rect.y = felix.return_y() - 10
                            all_sprites.add(och)
                            score += 500
                            level_g[1] = level_g[1][0] + '#' + level_g[1][2:]
                            num = 5
                            okno = pygame.mixer.Sound("data/okno.wav")
                            okno.play()
                    elif 244 <= felix.return_x() <= 291 and 175 <= felix.return_y() <= 230:
                        if level_g[1][2] == '@':
                            och.rect.x = felix.return_x() + 35
                            och.rect.y = felix.return_y() - 10
                            all_sprites.add(och)
                            score += 500
                            level_g[1] = level_g[1][:2] + '#' + level_g[1][3]
                            num = 6
                            okno = pygame.mixer.Sound("data/okno.wav")
                            okno.play()
                    elif 291 <= felix.return_x() <= 330 and 175 <= felix.return_y() <= 230:
                        if level_g[1][3] == '@':
                            och.rect.x = felix.return_x() + 35
                            och.rect.y = felix.return_y() - 10
                            all_sprites.add(och)
                            score += 500
                            level_g[1] = level_g[1][:3] + '#'
                            num = 7
                            okno = pygame.mixer.Sound("data/okno.wav")
                            okno.play()
                    elif 150 <= felix.return_x() <= 197 and 230 <= felix.return_y() <= 285:
                        if level_g[2][0] == '@':
                            och.rect.x = felix.return_x() + 35
                            och.rect.y = felix.return_y() - 10
                            all_sprites.add(och)
                            score += 500
                            level_g[2] = '#' + level_g[2][1:]
                            num = 8
                            okno = pygame.mixer.Sound("data/okno.wav")
                            okno.play()
                    elif 197 <= felix.return_x() <= 244 and 230 <= felix.return_y() <= 285:
                        if level_g[2][1] == '@':
                            och.rect.x = felix.return_x() + 35
                            och.rect.y = felix.return_y() - 10
                            all_sprites.add(och)
                            score += 500
                            level_g[2] = level_g[2][0] + '#' + level_g[2][2:]
                            num = 9
                            okno = pygame.mixer.Sound("data/okno.wav")
                            okno.play()
                    elif 244 <= felix.return_x() <= 291 and 230 <= felix.return_y() <= 285:
                        if level_g[2][2] == '@':
                            och.rect.x = felix.return_x() + 35
                            och.rect.y = felix.return_y() - 10
                            all_sprites.add(och)
                            score += 500
                            level_g[2] = level_g[2][:2] + '#' + level_g[2][3]
                            num = 10
                            okno = pygame.mixer.Sound("data/okno.wav")
                            okno.play()
                    elif 291 <= felix.return_x() <= 330 and 230 <= felix.return_y() <= 285:
                        if level_g[2][3] == '@':
                            och.rect.x = felix.return_x() + 35
                            och.rect.y = felix.return_y() - 10
                            all_sprites.add(och)
                            score += 500
                            level_g[2] = level_g[2][:3] + '#'
                            num = 11
                            okno = pygame.mixer.Sound("data/okno.wav")
                            okno.play()
                    elif 150 <= felix.return_x() <= 197 and 285 <= felix.return_y() <= 340:
                        if level_g[3][0] == '@':
                            och.rect.x = felix.return_x() + 35
                            och.rect.y = felix.return_y() - 10
                            all_sprites.add(och)
                            score += 500
                            level_g[3] = '#' + level_g[3][1:]
                            num = 12
                            okno = pygame.mixer.Sound("data/okno.wav")
                            okno.play()
                    elif 197 <= felix.return_x() <= 244 and 285 <= felix.return_y() <= 340:
                        if level_g[3][1] == '@':
                            och.rect.x = felix.return_x() + 35
                            och.rect.y = felix.return_y() - 10
                            all_sprites.add(och)
                            score += 500
                            level_g[3] = level_g[3][0] + '#' + level_g[3][2:]
                            num = 13
                            okno = pygame.mixer.Sound("data/okno.wav")
                            okno.play()
                    elif 244 <= felix.return_x() <= 291 and 285 <= felix.return_y() <= 340:
                        if level_g[3][2] == '@':
                            och.rect.x = felix.return_x() + 35
                            och.rect.y = felix.return_y() - 10
                            all_sprites.add(och)
                            score += 500
                            level_g[3] = level_g[3][:2] + '#' + level_g[3][3]
                            num = 14
                            okno = pygame.mixer.Sound("data/okno.wav")
                            okno.play()
                    elif 291 <= felix.return_x() <= 330 and 285 <= felix.return_y() <= 340:
                        if level_g[3][3] == '@':
                            och.rect.x = felix.return_x() + 35
                            och.rect.y = felix.return_y() - 10
                            all_sprites.add(och)
                            score += 500
                            level_g[3] = level_g[3][:3] + '#'
                            num = 15
                            okno = pygame.mixer.Sound("data/okno.wav")
                            okno.play()
                    updates_tiles(num)
        if number % 3 != 0:
            for i in kir:
                i.delete_this(felix)
                if i.rect.y > 330:
                    i.kill()
                else:
                    i.rect.y += 10
                    clock.tick(50)
            bit.kill()
            if hod != 1:
                all_sprites.add(walk)
            else:
                for i in kir:
                    i.kill()
            if move == 1:
                if walk.return_x() < 300:
                    walk.move(5, 0)
                    clock.tick(80)
                else:
                    move = 2
            else:
                if walk.return_x() > 160:
                    walk.move(-5, 0)
                    clock.tick(80)
                else:
                    move = 1
        else:
            for i in kir:
                i.delete_this(felix)
                all_sprites.add(i)
                if i.rect.y + 10 > 350:
                    i.rect.y = random.randrange(200, 330)
                i.rect.y += 10
                clock.tick(50)
            hod += 1
            walk.kill()
            all_sprites.add(bit)
            bum = pygame.mixer.Sound("data/bum.wav")
            bum.play()
            bum.set_volume(0.7)
            clock.tick(5)
        if level_g == ['####', '####', '####', '####']:
            win()
        all_sprites.update()
        screen.fill((0, 0, 0))
        all_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(3)
    pygame.quit()
