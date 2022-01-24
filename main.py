import time
import pygame
import os
import sys


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Earthworm Jim, Andy Asteroids')
    size = width, height = 1280, 760
    screen = pygame.display.set_mode(size)
    running = True
    x_pos = 0
    v = 300
    fps = 30
    start_frame = time.time()
    noi = 4
    frames_per_second = 8
    clock = pygame.time.Clock()
    can_move = True
    counter_bubbles = 9
    pygame.mixer.music.load('data/background_sound.mp3')
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play()
    sound_race_won = pygame.mixer.Sound('data/race_won.mp3')
    sound_race_lost = pygame.mixer.Sound('data/race_lost.mp3')
    background_sprites = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    tunnel_sprites_part1 = pygame.sprite.Group()
    tunnel_sprites_part2 = pygame.sprite.Group()
    asteroids_collision_sprites = pygame.sprite.Group()
    planet_sprites = pygame.sprite.Group()
    line_move_sprites = pygame.sprite.Group()
    icon_jim_sprites = pygame.sprite.Group()
    race_won_sprites = pygame.sprite.Group()
    race_lost_sprites = pygame.sprite.Group()
    bubbles_sprites = pygame.sprite.Group()


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


    class AnimatedSprite(pygame.sprite.Sprite):
        def __init__(self, sheet, columns, rows, x, y):
            super().__init__(all_sprites)
            self.frames = []
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
            self.cur_frame = int((time.time() - start_frame) * frames_per_second % noi)
            self.image = self.frames[self.cur_frame]


    class AnimatedTunnelPart1(pygame.sprite.Sprite):
        def __init__(self, sheet, columns, rows, x, y):
            super().__init__(tunnel_sprites_part1)
            self.frames = []
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

                    tmp = sheet.subsurface(pygame.Rect(
                        frame_location, self.rect.size))
                    self.frames.append(pygame.transform.scale(tmp, (1280, 760)))

        def update(self):
            self.cur_frame = int((time.time() - start_frame) * 15 % 15)
            self.image = self.frames[self.cur_frame]


    class AnimatedTunnelPart2(pygame.sprite.Sprite):
        def __init__(self, sheet, columns, rows, x, y):
            super().__init__(tunnel_sprites_part2)
            self.frames = []
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
                    tmp2 = sheet.subsurface(pygame.Rect(
                        frame_location, self.rect.size))
                    self.frames.append(pygame.transform.scale(tmp2, (1280, 760)))

        def update(self):
            self.cur_frame = int((time.time() - start_frame) * 30 % 8)
            self.image = self.frames[self.cur_frame]


    class AsteroidCollision(pygame.sprite.Sprite):
        def __init__(self, sheet, columns, rows, x, y):
            super().__init__(asteroids_collision_sprites)
            self.frames = []
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
            self.cur_frame = int((time.time() - start_frame) * frames_per_second % noi)
            self.image = self.frames[self.cur_frame]


    class AnimateRaceWon(pygame.sprite.Sprite):
        def __init__(self, sheet, columns, rows, x, y):
            super().__init__(race_won_sprites)
            self.frames = []
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
            self.cur_frame = int((time.time() - start_frame) * 7 % 7)
            self.image = self.frames[self.cur_frame]


    class AnimateRaceLost(pygame.sprite.Sprite):
        def __init__(self, sheet, columns, rows, x, y):
            super().__init__(race_lost_sprites)
            self.frames = []
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
            self.cur_frame = int((time.time() - start_frame) * 7 % 9)
            self.image = self.frames[self.cur_frame]


    class AnimateBubbles(pygame.sprite.Sprite):
        def __init__(self, sheet, columns, rows, x, y):
            super().__init__(bubbles_sprites)
            self.frames = []
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
            self.cur_frame = int((time.time() - start_frame) * 7 % 9)
            self.image = self.frames[self.cur_frame]

    jim_sprites = AnimatedSprite(load_image("jim_sprites.png"), 4, 1, 0, 0)
    jim_sprites.rect.x = 640
    jim_sprites.rect.y = 500

    tunnel_image_part1 = load_image('tunnel_part1.png')
    tunnel_image_part1.set_alpha(150)
    tunnel_sprites_part1_ = AnimatedTunnelPart1(tunnel_image_part1, 5, 3, 0, 0)

    tunnel_image_part2 = load_image('tunnel_part2.png')
    tunnel_image_part2.set_alpha(170)
    tunnel_sprites_part2_ = AnimatedTunnelPart2(tunnel_image_part2, 4, 2, 0, 0)

    asteroids_col_sprites = AsteroidCollision(load_image("asteroids_collision.png"), 6, 1, 0, 0)

    planet_sprite = pygame.sprite.Sprite()
    planet_sprite.image = load_image('planet.png')
    planet_sprite.rect = planet_sprite.image.get_rect()
    planet_sprites.add(planet_sprite)

    line_move_sprite = pygame.sprite.Sprite()
    line_move_sprite.image = load_image('move_line.png')
    line_move_sprite.rect = line_move_sprite.image.get_rect()
    line_move_sprites.add(line_move_sprite)
    line_move_sprite.rect.x = 80
    line_move_sprite.rect.y = 100

    icon_jim_sprite = pygame.sprite.Sprite()
    icon_jim_sprite.image = load_image('icon_jim.png')
    icon_jim_sprite.rect = icon_jim_sprite.image.get_rect()
    icon_jim_sprites.add(icon_jim_sprite)
    icon_jim_sprite.rect.x = 30
    icon_jim_sprite.rect.y = 650

    race_won_sprite = AnimateRaceWon(load_image("race_won.png"), 7, 1, 0, 0)
    race_won_sprite.rect.x = 1280
    race_won_sprite.rect.y = -10

    race_lost_sprite = AnimateRaceLost(load_image("race_lost.png"), 9, 1, 0, 0)
    race_lost_sprite.rect.x = 1280
    race_lost_sprite.rect.y = -10

    bubble_sprite = AnimateBubbles(load_image('bubbles.png'), 16, 1, 640, 380)

    background_image = load_image('background.png')

    startTime = time.time()
    lastTime = startTime


    def drawIntro():
        img_fon = pygame.image.load('data/intro_back.png')
        font = pygame.font.SysFont("calibri", 35)
        text_welcome = font.render("Создатели: ", True, (180, 180, 180))
        text_welcome2 = font.render("Александр Харченко и Сергеев Илья", True, (180, 180, 180))
        button = font.render('Далее', True, (255, 0, 0))
        width_rect, height_rect = 100, 45
        rect = pygame.Rect(875, 635, width_rect, height_rect)
        pygame.draw.rect(screen, pygame.Color("BLACK"), rect)
        running_fon = True
        while running_fon:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                   pygame.quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if rect.collidepoint(event.pos):
                        running_fon = False

            screen.blit(pygame.transform.scale(img_fon, [1280, 760]), [0, 0])
            screen.blit(text_welcome, [850, 560])
            screen.blit(text_welcome2, [700, 600])
            screen.blit(button, [880, 640])
            if not running_fon:
                screen.fill(0)
            pygame.display.update()


    def drawHistory():
        font = pygame.font.SysFont("calibri", 24)
        text = font.render("История игры", True, (180, 180, 180))
        text_play = font.render("Начать игру", True, (255, 0, 0))
        width_rect, height_rect = 125, 30
        rect = pygame.Rect(1280 / 2 - 50, 650, width_rect, height_rect)
        pygame.draw.rect(screen, pygame.Color("BLACK"), rect)
        running_fon = True
        while running_fon:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                   pygame.quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if rect.collidepoint(event.pos):
                        running_fon = False

            screen.blit(text, [1280 / 2 - 50, 760 / 2])
            screen.blit(text_play, [1280 / 2 - 50, 650])
            if not running_fon:
                screen.fill(0)
            pygame.display.update()


    def drawWindow():
        global can_move
        global counter_bubbles

        x_rel = x_pos % width
        x_part2 = x_rel - width if x_rel > 0 else x_rel + width
        screen.blit(background_image, (x_rel, 0))
        screen.blit(background_image, (x_part2, 0))

        if float('%s' % (totalTime)) < 60.01:
            tunnel_sprites_part1.update()
            tunnel_sprites_part1.draw(screen)

            bubbles_sprites.update()
            bubbles_sprites.draw(screen)
        elif float('%s' % (totalTime)) > 60.01 and float('%s' % (totalTime)) < 65.01:
            tunnel_sprites_part2.update()
            tunnel_sprites_part2.draw(screen)
        elif float('%s' % (totalTime)) > 65.01:
            can_move = False

            screen.blit(background_image, (0, 0))

            jim_sprites.rect.x += 8
            jim_sprites.rect.y -= 6

            size_x = 100
            size_y = 53
            sr_zn = (jim_sprites.rect.x - jim_sprites.rect.y) // 3
            planet_sprite.rect.w = 100 if planet_sprite.rect.y == 0 else planet_sprite.rect.w
            if planet_sprite.rect.w < 400:
                planet_sprite.image = pygame.transform.scale(load_image('planet.png'), (size_x + sr_zn, size_y + sr_zn))
                planet_sprite.rect = planet_sprite.image.get_rect()
                planet_sprite.rect.y = 710 - sr_zn
            print(planet_sprite.rect.x, planet_sprite.rect.y)
            planet_sprites.draw(screen)
            print(jim_sprites.rect.x)
            if jim_sprites.rect.x > 1700 and counter_bubbles >= 10:
                pygame.mixer.music.pause()
                sound_race_won.play()
                race_won_sprite.rect.x -= 4
                race_won_sprite.rect.y += 3
                race_won_sprites.update()
                race_won_sprites.draw(screen)
            elif jim_sprites.rect.x > 1700 and counter_bubbles < 10:
                pygame.mixer.music.pause()
                sound_race_lost.play()
                race_lost_sprite.rect.x -= 4
                race_lost_sprite.rect.y += 3
                race_lost_sprites.update()
                race_lost_sprites.draw(screen)
            if race_won_sprite.rect.y > 780 or race_lost_sprite.rect.y > 780:
                sound_race_won.stop()
                sound_race_lost.stop()

        icon_jim_sprites.draw(screen)

        line_move_sprites.draw(screen)

        all_sprites.update()
        all_sprites.draw(screen)

    drawIntro()
    drawHistory()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        clock.tick(fps)
        lapTime = round(time.time() - lastTime, 2)
        totalTime = round(time.time() - startTime, 2)
        drawWindow()
        if can_move:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_w]:
                jim_sprites.rect.y = jim_sprites.rect.y - 5
            elif keys[pygame.K_d]:
                jim_sprites.rect.x = jim_sprites.rect.x + 5
            elif keys[pygame.K_s]:
                jim_sprites.rect.y = jim_sprites.rect.y + 5
            elif keys[pygame.K_a]:
                jim_sprites.rect.x = jim_sprites.rect.x - 5
        x_pos += v / fps
        pygame.display.flip()
    pygame.quit()
