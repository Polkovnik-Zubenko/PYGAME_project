import random
import time
import pygame
import os
import sys
from PIL import Image

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
    background_sprites = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    tunnel_sprites = pygame.sprite.Group()


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


    class AnimatedTunnel(pygame.sprite.Sprite):
        def __init__(self, sheet, columns, rows, x, y):
            super().__init__(tunnel_sprites)
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
    tunnel_image = load_image('tunnel_part1.png')
    tunnel_image.set_alpha(170)
    tunnel_sprites_ = AnimatedTunnel(tunnel_image, 5, 3, 0, 0)
    jim_sprites.rect = jim_sprites.image.get_rect()
    all_sprites.add(jim_sprites)
    jim_sprites.rect.x = 640
    jim_sprites.rect.y = 500
    background_image = load_image('background.png')

    def drawWindow():
        x_rel = x_pos % width
        x_part2 = x_rel - width if x_rel > 0 else x_rel + width
        screen.blit(background_image, (x_rel, 0))
        screen.blit(background_image, (x_part2, 0))
        all_sprites.update()
        tunnel_sprites.update()
        tunnel_sprites.draw(screen)
        all_sprites.draw(screen)


    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        clock.tick(fps)
        drawWindow()
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
