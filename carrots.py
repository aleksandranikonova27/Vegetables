import pygame
import os
from random import randrange, randint, choice
import sys
import sqlite3
import datetime

SCORE = 0
LEVEL = 0
SCORE_CONST = [50, 250, 300, 400, 500]
VEG_SCORE = [5, 10, 20, 25, 30]
BLACK = 'black'
INTRO_TEXT = ["ЗАСТАВКА", "",
              "Нажмите R чтобы увидеть правила   игры",
              "Нажмите пробел, чтобы поставить игру на паузу",
              "Нажмите Esc, чтобы выйти из игры"]
RULE_TEXT = ['ПРАВИЛА:', '', '']
BACKGROUNDS = [pygame.image.load("pictures_for_my_project\\background1.jpg"),
               pygame.image.load("pictures_for_my_project\\background2.jpg"),
               pygame.image.load("pictures_for_my_project\\background3.jpg"),
               pygame.image.load("pictures_for_my_project\\background4.jpg"),
               pygame.image.load("pictures_for_my_project\\background5.jpg")]
PAUSED = False
LIVES = 2


def load_image(name, color_key=None, *sprite_size):
    fullname = os.path.join('pictures_for_my_project', name)
    try:
        image = pygame.image.load(fullname).convert()
        im1 = pygame.transform.scale(image, (sprite_size))
    except pygame.error as message:
        print('Невозможно загрузить картинку:', fullname)
        raise SystemExit(message)
    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        im1.set_colorkey(color_key)
    else:
        im1 = im1.convert_alpha()
    return im1


def terminate():
    pygame.quit()
    sys.exit()


def massage_screen(cur_fon, coor, color='black', *text):
    intro_text = text[0]
    fon = pygame.image.load(cur_fon)
    fon = pygame.transform.scale(fon, size)
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 25)
    text_coord = coor[1]
    clock = pygame.time.Clock()
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color(color))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = coor[0]
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(FPS)


def game_over(cur_score):
    txt = []
    text_coord = (width / 2 - height / 3, 150)
    con = sqlite3.connect("score.db")
    cur = con.cursor()
    inf1 = cur.execute(f"SELECT score, record_time FROM main WHERE id='1'").fetchone()
    print(inf1)
    record_score, date = inf1[0], inf1[1]
    if cur_score > record_score:
        txt = ['ПОЗДРАВЛЯЕМ! ВЫ ПОБИЛИ ПРОШЛЫЙ РЕКОРД!', f'Прошлый рекорд: {record_score}, был установлен: {date}',
               f'Новый рекорд: {cur_score}',
               f'Счёт: {cur_score}']
        cur.execute(f"UPDATE main SET score='{cur_score}', record_time='{datetime.date.today()}' WHERE id='1'")
    else:
        txt = [f'Ваш счёт: {cur_score}', f'Рекорд: {record_score} был установлен: {date}']
    con.commit()
    massage_screen("pictures_for_my_project\\result_fon.jpg", text_coord, BLACK, txt)


def draw_lives(srf, x, y, lives):
    for i in range(lives):
        rect = L_IM.get_rect()
        rect.x = x + 50 * i
        rect.y = y
        srf.blit(L_IM, rect)


def new_level():
    global LEVEL
    global LIVES
    LEVEL += 1
    LIVES += 1


class Vegetable(pygame.sprite.Sprite):
    def __init__(self, ind, *group):
        super().__init__(*group)
        self.ind_score = VEG_SCORE[ind]
        self.image = vegetables_sp[ind]
        self.rect = self.image.get_rect()
        self.rect.x = randrange(20, width - 50)
        self.rect.y = 0
        self.speed = randrange(1, 5)

    def update(self, *args):
        global SCORE
        global LIVES
        if not PAUSED:
            self.rect.y += self.speed
            if self.rect.y > height:
                self.kill()
                LIVES = LIVES - 1

            if pygame.sprite.spritecollideany(self, player_sprite):
                self.kill()
                SCORE += self.ind_score
                if SCORE >= SCORE_CONST[LEVEL - 1]:
                    new_level()


sheets = [pygame.image.load('pictures_for_my_project\\BunnyIdleF.png'),
          pygame.image.load('pictures_for_my_project\\BunnyIdleL.png'),
          pygame.image.load('pictures_for_my_project\\BunnyIdleR.png')]


class Player(pygame.sprite.Sprite):
    def __init__(self, columns, rows):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((60, 60))
        self.rect = self.image.get_rect()
        self.rect.centerx = width / 2
        self.rect.bottom = height - 10
        self.speedx = 0
        self.sheet_id = 0
        self.frames = []
        self.sheet = sheets[self.sheet_id]
        self.cut_sheet(sheets[self.sheet_id], 10, 1)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(width / 2, height - 100)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        self.speedx = 0
        if not PAUSED:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]
            keystate = pygame.key.get_pressed()
            if keystate[pygame.K_LEFT]:
                self.speedx = -8
                self.sheet_id = 1

            if keystate[pygame.K_RIGHT]:
                self.speedx = 8
                self.sheet_id = 2
            self.rect.x += self.speedx
            if self.rect.right > width:
                self.rect.right = width
            if self.rect.left < 0:
                self.rect.left = 0


if __name__ == '__main__':
    pygame.init()
    size = width, height = 800, 600
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Морковки падают вниз")
    background_image = BACKGROUNDS[LEVEL]
    background_image = pygame.transform.scale(background_image, size)
    all_sprites = pygame.sprite.Group()
    player_sprite = pygame.sprite.Group()
    player = Player(10, 1)
    all_sprites.add(player)
    player_sprite.add(player)
    SCORE_CHECK = pygame.USEREVENT + 1
    pygame.time.set_timer(SCORE_CHECK, 10)
    GAME = pygame.USEREVENT + 2
    pygame.time.set_timer(GAME, 1500)
    vegetables_sp = [load_image(f"carrot.png", -1, (30, 30)),
                     load_image(f"cabbage.jpg", -1, (60, 60)),
                     load_image(f"pumpkin.jpg", -1, (80, 80)),
                     load_image(f"baklajan.jpg", -1, (70, 70)),
                     load_image(f"kukuruza.jpg", -1, (50, 50))]
    L_IM = load_image('hurt.png', -1, (60, 60))

    FPS = 50
    massage_screen("pictures_for_my_project\\fon1.jpg", (50, 50), BLACK, INTRO_TEXT)
    font = pygame.font.SysFont("Verdana", 15)
    screen.blit(background_image, (0, 0))
    new_level()
    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    PAUSED = not PAUSED
                    if PAUSED:
                        pygame.time.set_timer(GAME, 0)
                    else:
                        pygame.time.set_timer(GAME, 1500)
                elif event.key == pygame.K_ESCAPE:
                    game_over(SCORE)
                    terminate()
                elif event.key == pygame.K_r:
                    massage_screen("pictures_for_my_project\\fon2.jpg", (50, 50), BLACK, RULE_TEXT)
            if event.type == GAME:
                if not PAUSED:
                    Vegetable(randrange(LEVEL) % len(vegetables_sp), all_sprites)
                    background_image = pygame.transform.scale(BACKGROUNDS[LEVEL - 1], size)
                    player.update()

                if LIVES <= 0:
                    game_over(SCORE)
                    terminate()
        screen.blit(background_image, (0, 0))
        score_text = font.render(f"Счёт: {SCORE} уровень: {LEVEL}", True, 'black')
        screen.blit(score_text, (10, 10))
        draw_lives(screen, width - 200, 20, LIVES)
        all_sprites.draw(screen)
        all_sprites.update()
        pygame.display.flip()
        pygame.time.Clock().tick(70)
