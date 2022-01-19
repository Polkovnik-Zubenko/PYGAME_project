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
    pygame.mixer.music.load('data/background_sound.mp3')
    pygame.mixer.music.play()
    background_sprites = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    tunnel_sprites_part1 = pygame.sprite.Group()
    tunnel_sprites_part2 = pygame.sprite.Group()
    asteroids_collision_sprites = pygame.sprite.Group()
    planet_sprites = pygame.sprite.Group()
    line_move_sprites = pygame.sprite.Group()
    icon_jim_sprites = pygame.sprite.Group()


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
    icon_jim_sprite.rect.y = 600

    background_image = load_image('background.png')

    startTime = time.time()
    lastTime = startTime


    def drawWindow():
        global can_move
        global step
        x_rel = x_pos % width
        x_part2 = x_rel - width if x_rel > 0 else x_rel + width
        screen.blit(background_image, (x_rel, 0))
        screen.blit(background_image, (x_part2, 0))

        if float('%s' % (totalTime)) < 60.01:
            tunnel_sprites_part1.update()
            tunnel_sprites_part1.draw(screen)
        elif float('%s' % (totalTime)) > 60.01 and float('%s' % (totalTime)) < 65.01:
            tunnel_sprites_part2.update()
            tunnel_sprites_part2.draw(screen)
        else:
            can_move = False
            pygame.mixer.music.pause()

            screen.blit(background_image, (0, 0))

            jim_sprites.rect.x += 6
            jim_sprites.rect.y -= 6

            size_x = 75
            size_y = 53
            sr_zn = (jim_sprites.rect.x - jim_sprites.rect.y) // 3

            planet_sprite.rect.w = 100 if planet_sprite.rect.y == 0 else planet_sprite.rect.w

            if planet_sprite.rect.w < 400:
                planet_sprite.image = pygame.transform.scale(load_image('planet.png'), (size_x + sr_zn, size_y + sr_zn))
                planet_sprite.rect = planet_sprite.image.get_rect()
                planet_sprite.rect.y = 710 - sr_zn

            planet_sprites.draw(screen)
        icon_jim_sprite.rect.y = icon_jim_sprite.rect.y - 0.8125
        print(icon_jim_sprite.rect.y)
        icon_jim_sprites.draw(screen)

        line_move_sprites.draw(screen)

        all_sprites.update()
        all_sprites.draw(screen)


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
