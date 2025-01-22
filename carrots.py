import pygame
import os
from random import randrange, randint, choice
import sys


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


def start_screen():
    intro_text = ["ЗАСТАВКА", "",
                  "Правила игры:",
                  "Здесь будут правила",
                  ]

    fon = pygame.image.load("pictures_for_my_project\\fon1.jpg")
    fon = pygame.transform.scale(fon, size)
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    clock = pygame.time.Clock()
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
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(FPS)


class Vegeteble(pygame.sprite.Sprite):
    def __init__(self, *group):
        super().__init__(*group)
        self.ind_score = 1
        self.image = self.image_src.copy()
        self.rect = self.image.get_rect()
        self.rect.x = randrange(width)
        self.rect.y = randrange(height)
        self.speed = randrange(1, 5)

    def update(self, *args):
        global score

        self.rect.y += self.speed
        if self.rect.y > height:
            self.kill()
        if args and args[0].type == pygame.MOUSEBUTTONDOWN:  #
            return True
        elif args and args[0].type == pygame.KEYDOWN:  #
            return False
        if pygame.sprite.spritecollideany(self, player_sprite):
            self.kill()
            score += self.ind_score


class Carrot(Vegeteble):
    def __init__(self, *group):
        self.image_src = load_image(f"carrot.png", -1, (30, 30))
        super().__init__(*group)
        self.ind_score = 5


class Cabbage(Vegeteble):
    def __init__(self, *group):
        self.image_src = load_image(f"cabbage.jpg", -1, (60, 60))
        super().__init__(*group)
        self.ind_score = 10


class Pumpkin(Vegeteble):
    def __init__(self, *group):
        self.image_src = load_image(f"pumpkin.jpg", -1, (80, 80))
        super().__init__(*group)
        self.ind_score = 20


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((100, 60))
        self.image.fill('red')
        self.rect = self.image.get_rect()
        self.rect.centerx = width / 2
        self.rect.bottom = height - 10
        self.speedx = 0

    def update(self):
        self.speedx = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -8
        if keystate[pygame.K_RIGHT]:
            self.speedx = 8
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
    background_image = pygame.image.load("pictures_for_my_project\\background1.jpg")
    background_image = pygame.transform.scale(background_image, size)
    all_sprites = pygame.sprite.Group()
    player_sprite = pygame.sprite.Group()
    player = Player()
    all_sprites.add(player)
    player_sprite.add(player)
    score = 0
    paused = False
    FPS = 50
    start_screen()
    font = pygame.font.SysFont("Verdana", 15)
    screen.blit(background_image, (0, 0))

    for i in range(10):
        Carrot(all_sprites)
    for i in range(10):
        Cabbage(all_sprites)
    for i in range(10):
        Pumpkin(all_sprites)
    running = True
    clock = pygame.time.Clock()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    running = False

        screen.blit(background_image, (0, 0))
        score_text = font.render("Счёт: " + str(score), True, 'black')
        screen.blit(score_text, (10, 10))
        all_sprites.draw(screen)
        all_sprites.update()
        pygame.display.flip()
        pygame.time.Clock().tick(60)
    pygame.quit()
