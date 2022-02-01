import random
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
    fps = 60
    start_frame = time.time()
    clock = pygame.time.Clock()
    counter_bubbles = 16
    state = True
    time_now = 0
    pause_start = 0
    pause_time = 0
    difficult_flag = 0
    pygame.mixer.music.load('data/background_sound.mp3')
    sound_bubble = pygame.mixer.Sound('data/bubble_sound.mp3')
    sound_race_won = pygame.mixer.Sound('data/race_won.mp3')
    sound_race_lost = pygame.mixer.Sound('data/race_lost.mp3')
    sound_asteroid = pygame.mixer.Sound('data/asteroid_sound.mp3')
    sound_groovy = pygame.mixer.Sound('data/end.wav')
    all_sprites = pygame.sprite.Group()
    bubbles_sprites = pygame.sprite.Group()
    asteroid_sprites = pygame.sprite.Group()
    end_sprites = pygame.sprite.Group()

    gameplay_sprites = pygame.sprite.Group()
    game_ending_sprites = pygame.sprite.Group()


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
        def __init__(self, sheet, columns, rows, x, y, *groups):
            super().__init__(all_sprites, *groups)
            self.frames = self.cut_sheet(sheet, columns, rows)
            self.cur_frame = 0
            self.image = self.frames[self.cur_frame]
            self.rect = self.image.get_rect()
            self.mask = pygame.mask.from_surface(self.image)
            self.rect = self.rect.move(x, y)
            self.tmp = 0

        @staticmethod
        def scale_frames(frames, scale_width, scale_height):
            return [pygame.transform.scale(item, (scale_width, scale_height)) for item in frames]

        @staticmethod
        def cut_sheet(sheet, columns, rows):
            frames = []
            rect = pygame.Rect(0, 0, sheet.get_width() // columns, sheet.get_height() // rows)
            for j in range(rows):
                for i in range(columns):
                    frame_location = (rect.w * i, rect.h * j)
                    frames.append(sheet.subsurface(pygame.Rect(frame_location, rect.size)))
            return frames


    class AnimatedJim(AnimatedSprite):
        def __init__(self, base_sheet, base_columns, base_rows,
                     asteroid_sheet, asteroid_columns, asteroid_rows,
                     won_sheet, won_columns, won_rows,
                     lost_sheet, lost_columns, lost_rows,
                     x, y, *groups):
            super().__init__(base_sheet, base_columns, base_rows, x, y, *groups)
            self.flag_coll = False
            self.asteroid_frames = self.cut_sheet(asteroid_sheet, asteroid_columns, asteroid_rows)
            self.won_frames = self.cut_sheet(won_sheet, won_columns, won_rows)
            self.lost_frames = self.cut_sheet(lost_sheet, lost_columns, lost_rows)
            self.rect.move(x, y)
            self.can_move = True
            self.game_ended = False
            self.is_lost = False
            self.tmp = 0

        def ast_coll(self):
            if not self.flag_coll:
                self.flag_coll = True

        def move_right(self):
            if self.can_move:
                self.rect.x = self.rect.x + 5
                self.rect.y = -((self.rect.x - 640) ** 2 + 340 ** 2) ** 0.5 + 845

        def move_left(self):
            if self.can_move:
                self.rect.x = self.rect.x - 5
                self.rect.y = -((self.rect.x - 640) ** 2 + 340 ** 2) ** 0.5 + 845

        def ending_game(self):
            self.can_move = False
            if not self.game_ended:
                self.rect.x += 4
                self.rect.y -= 3

        def end_game(self, is_lost=False):
            self.game_ended = True
            self.is_lost = is_lost

        def get_coords(self):
            return self.rect.x, self.rect.y

        def update(self):
            if self.game_ended:
                self.rect.x -= 3
                self.rect.y += 2
                if self.is_lost:
                    self.cur_frame = int((time.time() - start_frame) * 7 % 9)
                    self.image = self.lost_frames[self.cur_frame]
                else:
                    self.cur_frame = int((time.time() - start_frame) * 7 % 7)
                    self.image = self.won_frames[self.cur_frame]
            else:
                if self.flag_coll:
                    self.tmp = int((time.time() - start_frame) * 8 % 6)
                    self.cur_frame = self.tmp
                    self.image = self.asteroid_frames[self.cur_frame]
                    self.tmp += 1
                    if self.tmp == 6:
                        self.tmp = 0
                        self.flag_coll = False
                else:
                    self.cur_frame = int((time.time() - start_frame) * 8 % 4)
                    self.image = self.frames[self.cur_frame]


    class AnimatedTunnel(AnimatedSprite):
        def __init__(self, part_1_sheet, part_2_sheet, part_1_columns, part_1_rows,
                     part_2_columns, part_2_rows, x, y, *groups):
            super().__init__(part_1_sheet, part_1_columns, part_1_rows, x, y, *groups)
            self.frames = self.scale_frames(self.frames, 1280, 760)
            self.frames_part_2 = self.scale_frames(self.cut_sheet(part_2_sheet, part_2_columns, part_2_rows), 1280, 760)

            self.rect = self.frames[self.cur_frame].get_rect()
            self.part_1 = True

        def enable_part_2(self):
            self.part_1 = False

        def update(self):
            if self.part_1:
                self.cur_frame = int((time.time() - start_frame) * 15 % 15)
                self.image = self.frames[self.cur_frame]
            else:
                self.cur_frame = int((time.time() - start_frame) * 30 % 8)
                self.image = self.frames_part_2[self.cur_frame]


    class BaseSprite(pygame.sprite.Sprite):
        def __init__(self, image, x, y, *groups):
            super().__init__(all_sprites, *groups)
            self.image = image
            self.rect = self.image.get_rect()
            self.rect = self.rect.move(x, y)


    class BigPlanet(BaseSprite):
        def __init__(self, image, x, y, *groups):
            super().__init__(image, x, y, *groups)

        def transform(self, jim_coords):
            sr_zn = (jim_coords[0] - jim_coords[1]) // 3
            self.rect.w = 100 if self.rect.y == 0 else self.rect.w
            if self.rect.w < 400:
                self.image = pygame.transform.scale(load_image('planet.png'), (100 + sr_zn, 53 + sr_zn))
                self.rect = self.image.get_rect()
                self.rect.y = 710 - sr_zn


    class AnimateIconJim(BaseSprite):
        def __init__(self, image, x, y, *groups):
            super().__init__(image, x, y, *groups)
            self.y = self.rect.y

        def update(self):
            if self.rect.y < 100:
                self.rect.y = self.rect.y
            else:
                self.y = self.y - 0.8125 / 6
                self.rect.y = self.y


    class BaseMovingSprite(BaseSprite):
        def __init__(self, sheet, x, y, *groups):
            super().__init__(sheet, x, y, *groups)
            self.x = x
            self.y = y
            self.base_image = self.image
            self.image = pygame.transform.scale(self.image, (20, 20))
            self.rect = self.image.get_rect()
            self.mask = pygame.mask.from_surface(self.image)
            self.rect = self.rect.move(x, y)
            self.size_x = 20
            self.size_y = 20

        def update(self):
            self.size_x += 0.1
            self.size_y += 0.1
            x = self.rect.x
            y = self.rect.y
            self.image = pygame.transform.scale(self.base_image, (self.size_x, self.size_y))
            self.rect = self.image.get_rect()
            self.mask = pygame.mask.from_surface(self.image)
            self.rect = self.rect.move(x + random.randint(-5, 5), y + random.randint(0, 1))


    class BubbleSprite(BaseMovingSprite):
        def __init__(self, sheet, x, y, *groups):
            super().__init__(sheet, x, y, *groups)


    class AsteroidSprite(BaseMovingSprite):
        def __init__(self, sheet, x, y, *groups):
            super().__init__(sheet, x, y, *groups)


    class AnimateEndGame(pygame.sprite.Sprite):
        def __init__(self, sheet, columns, rows, x, y):
            super().__init__(end_sprites)
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
            self.cur_frame = int((time.time() - start_frame) * 7 % 5)
            self.image = self.frames[self.cur_frame]


    def draw_intro():
        img_fon = pygame.transform.scale(pygame.image.load('data/1.png'), [1280, 760])
        font = pygame.font.SysFont("calibri", 35)
        text_welcome = font.render("Создатели: ", True, (180, 180, 180))
        text_welcome2 = font.render("Александр Харченко и Сергеев Илья", True, (180, 180, 180))
        button = font.render('Далее', True, (0, 0, 255))
        width_rect, height_rect = 100, 45
        rect = pygame.Rect(880, 670, width_rect, height_rect)
        pygame.draw.rect(screen, pygame.Color("BLACK"), rect)
        running_fon = True
        while running_fon:
            for action in pygame.event.get():
                if action.type == pygame.QUIT:
                    pygame.quit()
                if action.type == pygame.MOUSEBUTTONDOWN:
                    if rect.collidepoint(action.pos):
                        running_fon = False
            screen.fill((0, 0, 0))
            screen.blit(img_fon, [0, 0])
            screen.blit(text_welcome, [850, 560])
            screen.blit(text_welcome2, [700, 615])
            screen.blit(button, [880, 670])
            if not running_fon:
                screen.fill(0)
            pygame.display.update()


    def draw_history():
        global pause_time, pause_start, difficult_flag

        font = pygame.font.SysFont("calibri", 24)
        font_button_choice = pygame.font.SysFont("calibri", 24, True)
        text = font.render("Давным-давно, в далекой-далекой галактике развитая цивилизация "
                           "разумных червей находиться ", True, (180, 180, 180))
        text2 = font.render("в шаге от исчезновения, одной из главных причин становится недостаток кислорода "
                            "на планете.", True, (180, 180, 180))
        text3 = font.render("В Сенате было принято решение отправить в космос миллионы "
                            "сборщиков воздуха. Однако", True, (180, 180, 180))
        text4 = font.render("приспособиться к открытому космосу "
                            "удалось далеко не всем. Наш главный герой - червяк Джим,", True, (180, 180, 180))
        text5 = font.render("один из немногих счастливчиков, кто смог это сделать. Ваша же цель "
                            "управляя им A(влево) и D(вправо)", True, (180, 180, 180))
        text6 = font.render("собирать драгоценные пузырьки воздуха. Увы, без нужного количества кислорода "
                            "вернуться домой", True, (180, 180, 180))
        text7 = font.render("невозможно. Доберитесь до планеты как можно быстрее, но будьте "
                            "осторожны! Перед началом игры", True, (180, 180, 180))
        text8 = font.render("необходимо выбрать уровень сложности. Удачи!", True, (180, 180, 180))
        easy_level = font.render("Легкий уровень сложности", True, (0, 255, 0))
        medium_level = font.render("Обычный уровень сложности", True, (255, 255, 0))
        hard_level = font.render("Тяжелый уровень сложности", True, (255, 0, 0))
        width_rect_level, height_rect_level = 320, 30
        rect_1 = pygame.Rect(50, 580, width_rect_level, height_rect_level)
        rect_2 = pygame.Rect(480, 580, width_rect_level, height_rect_level)
        rect_3 = pygame.Rect(940, 580, width_rect_level, height_rect_level)
        text_play = font.render("Начать игру", True, (0, 0, 255))
        width_rect, height_rect = 125, 30
        rect = pygame.Rect(1280 / 2 - 50, 650, width_rect, height_rect)
        pygame.draw.rect(screen, pygame.Color("BLACK"), rect)
        running_fon = True
        choice_diff = False
        while running_fon:
            for action2 in pygame.event.get():
                if action2.type == pygame.QUIT:
                    pygame.quit()
                if action2.type == pygame.MOUSEBUTTONDOWN:
                    if rect_1.collidepoint(action2.pos):
                        easy_level = font_button_choice.render("_______________________", True, (0, 255, 0))
                        pygame.display.update()
                        difficult_flag = 1
                        choice_diff = True
                    if rect_2.collidepoint(action2.pos):
                        medium_level = font_button_choice.render("_________________________", True, (255, 255, 0))
                        difficult_flag = 2
                        choice_diff = True
                    if rect_3.collidepoint(action2.pos):
                        hard_level = font_button_choice.render("________________________", True, (255, 0, 0))
                        difficult_flag = 3
                        choice_diff = True
                    if choice_diff:
                        if rect.collidepoint(action2.pos):
                            running_fon = False
                            pause_time = 0

            screen.blit(text, [116, 124])
            screen.blit(text2, [116, 158])
            screen.blit(text3, [116, 192])
            screen.blit(text4, [116, 226])
            screen.blit(text5, [116, 260])
            screen.blit(text6, [116, 294])
            screen.blit(text7, [116, 328])
            screen.blit(text8, [116, 362])
            screen.blit(easy_level, [50, 580])
            screen.blit(medium_level, [480, 580])
            screen.blit(hard_level, [940, 580])
            screen.blit(text_play, [1280 / 2 - 70, 650])
            if not running_fon:
                screen.fill(0)
            pygame.display.update()


    tunnel_image_part1 = load_image('tunnel_part1.png')
    tunnel_image_part1.set_alpha(150)
    tunnel_image_part2 = load_image('tunnel_part2.png')
    tunnel_image_part2.set_alpha(170)

    tunnel_sprite = AnimatedTunnel(tunnel_image_part1, tunnel_image_part2, 5, 3, 4, 2, 0, 0, gameplay_sprites)

    planet_sprite = BigPlanet(load_image('planet.png'), -1000, 0, game_ending_sprites)

    jim_sprites = AnimatedJim(load_image("jim_sprites.png"), 4, 1,
                              load_image('asteroids_collision.png'), 6, 1,
                              load_image("race_won.png"), 7, 1,
                              load_image("race_lost.png"), 9, 1,
                              590, 500, gameplay_sprites, game_ending_sprites)

    line_move_sprite = BaseSprite(load_image('move_line.png'), 80, 100, gameplay_sprites)

    icon_jim_sprite = AnimateIconJim(load_image('icon_jim.png'), 30, 650, gameplay_sprites)

    bubble_sprite = BubbleSprite(load_image('bubble.png'), 520, 230, bubbles_sprites, gameplay_sprites)

    asteroid_sprite = AsteroidSprite(load_image('asteroid.png'), 520, 230, asteroid_sprites, gameplay_sprites)

    end_sprite = AnimateEndGame(load_image('end.png'), 6, 1, 540, 300)

    background_image = load_image('background.png')

    startTime = time.time()
    lastTime = startTime

    pause_text = pygame.font.SysFont('Consolas', 32).render('Pause', True, pygame.color.Color('White'))


    def bubbles_chet_func():
        global counter_bubbles

        font = pygame.font.SysFont("calibri", 36)
        bubble_img = pygame.image.load("data/bubble.png")
        text = font.render(f"{counter_bubbles} X ", True, (180, 180, 180))
        screen.blit(pygame.transform.scale(bubble_img, [50, 50]), [1220, 10])
        screen.blit(text, [1170, 21])
        pygame.display.update()


    def draw_window():
        global counter_bubbles, time_now, difficult_flag

        x_rel = x_pos % width
        x_part2 = x_rel - width if x_rel > 0 else x_rel + width
        screen.blit(background_image, (x_rel, 0))
        screen.blit(background_image, (x_part2, 0))

        time_now = float('%s' % totalTime) - pause_time

        time_const = 62.01

        if time_now < time_const:
            rand = random.randint(1, 10000)
            print(rand)
            if rand in [i for i in range(9940, 10000)]:
                BubbleSprite(load_image('bubble.png'), 520, 230, bubbles_sprites, gameplay_sprites)
            if rand in [i for i in range(9930, 10000)]:
                AsteroidSprite(load_image('asteroid.png'), 520, 230, asteroid_sprites, gameplay_sprites)

            for asteroid in asteroid_sprites:
                if pygame.sprite.collide_mask(asteroid, jim_sprites):
                    jim_sprites.ast_coll()
                    asteroid.kill()
                    sound_asteroid.play()
                    counter_bubbles -= 2

            for bubble in bubbles_sprites:
                if pygame.sprite.collide_mask(bubble, jim_sprites):
                    bubble.kill()
                    sound_bubble.play()
                    counter_bubbles += 1

            gameplay_sprites.draw(screen)

        elif not time_now <= time_const and time_now < time_const + 5:
            tunnel_sprite.enable_part_2()
            gameplay_sprites.draw(screen)

            for asteroid in asteroid_sprites:
                if pygame.sprite.collide_mask(asteroid, jim_sprites):
                    jim_sprites.ast_coll()
                    asteroid.kill()
                    sound_asteroid.play()
                    counter_bubbles -= 2

            for bubble in bubbles_sprites:
                if pygame.sprite.collide_mask(bubble, jim_sprites):
                    bubble.kill()
                    sound_bubble.play()
                    counter_bubbles += 1

        elif time_now > time_const + 5:

            screen.blit(background_image, (0, 0))

            jim_sprites.ending_game()

            planet_sprite.transform(jim_sprites.get_coords())

            if jim_sprites.get_coords()[0] > 1650:
                pygame.mixer.music.pause()
                if difficult_flag == 1 and counter_bubbles < 5:
                    jim_sprites.end_game(counter_bubbles < 5)
                    sound_race_lost.play()
                elif difficult_flag == 1 and counter_bubbles > 5:
                    jim_sprites.end_game(counter_bubbles < 5)
                    sound_race_won.play()
                if difficult_flag == 2 and counter_bubbles < 10:
                    jim_sprites.end_game(counter_bubbles < 10)
                    sound_race_lost.play()
                elif difficult_flag == 2 and counter_bubbles > 10:
                    jim_sprites.end_game(counter_bubbles < 10)
                    sound_race_won.play()
                if difficult_flag == 3 and counter_bubbles < 15:
                    jim_sprites.end_game(counter_bubbles < 15)
                    sound_race_lost.play()
                elif difficult_flag == 3 and counter_bubbles > 15:
                    jim_sprites.end_game(counter_bubbles < 15)
                    sound_race_won.play()

            game_ending_sprites.update()
            game_ending_sprites.draw(screen)

            if jim_sprites.rect.y > 780:
                sound_race_won.stop()
                sound_race_lost.stop()
                screen.fill((255, 255, 255))
                end_sprites.update()
                end_sprites.draw(screen)
                sound_groovy.play()

        all_sprites.update()


    draw_intro()
    draw_history()
    pygame.mixer.music.play()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    state = False
                    pause_start = time.time()
                if event.key == pygame.K_SPACE:
                    state = True
                    pygame.mixer.music.play()
                    pause_time += time.time() - pause_start
        lapTime = round(time.time() - lastTime, 2)
        totalTime = round(time.time() - startTime, 2)
        if state:
            clock.tick(fps)
            draw_window()
            bubbles_chet_func()
            keys = pygame.key.get_pressed()
            if keys[pygame.K_d]:
                jim_sprites.move_right()
            elif keys[pygame.K_a]:
                jim_sprites.move_left()
            x_pos += v / fps
        else:
            screen.blit(pause_text, (640, 330))
            pygame.mixer.music.stop()
        pygame.display.flip()
    pygame.quit()
