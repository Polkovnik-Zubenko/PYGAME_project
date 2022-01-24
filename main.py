import time
import pygame
import os
import sys
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow

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
    state = True
    time_now = 0
    pygame.mixer.music.load('data/background_sound.mp3')
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


    class Ui_MainWindow(object):
        def setupUi(self, MainWindow):
            MainWindow.setObjectName("MainWindow")
            MainWindow.resize(640, 428)
            self.centralwidget = QtWidgets.QWidget(MainWindow)
            self.centralwidget.setObjectName("centralwidget")
            self.horizontalSlider = QtWidgets.QSlider(self.centralwidget)
            self.horizontalSlider.setGeometry(QtCore.QRect(140, 140, 331, 22))
            self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
            self.horizontalSlider.setObjectName("horizontalSlider")
            self.label = QtWidgets.QLabel(self.centralwidget)
            self.label.setGeometry(QtCore.QRect(260, 100, 131, 16))
            self.label.setObjectName("label")
            self.label_2 = QtWidgets.QLabel(self.centralwidget)
            self.label_2.setGeometry(QtCore.QRect(100, 140, 31, 16))
            self.label_2.setObjectName("label_2")
            self.label_3 = QtWidgets.QLabel(self.centralwidget)
            self.label_3.setGeometry(QtCore.QRect(480, 140, 55, 16))
            self.label_3.setObjectName("label_3")
            self.label_5 = QtWidgets.QLabel(self.centralwidget)
            self.label_5.setGeometry(QtCore.QRect(260, 210, 131, 16))
            self.label_5.setObjectName("label_5")
            self.horizontalSlider_2 = QtWidgets.QSlider(self.centralwidget)
            self.horizontalSlider_2.setGeometry(QtCore.QRect(140, 250, 331, 22))
            self.horizontalSlider_2.setOrientation(QtCore.Qt.Horizontal)
            self.horizontalSlider_2.setObjectName("horizontalSlider_2")
            self.label_6 = QtWidgets.QLabel(self.centralwidget)
            self.label_6.setGeometry(QtCore.QRect(100, 250, 31, 16))
            self.label_6.setObjectName("label_6")
            self.label_7 = QtWidgets.QLabel(self.centralwidget)
            self.label_7.setGeometry(QtCore.QRect(480, 250, 55, 16))
            self.label_7.setObjectName("label_7")
            self.pushButton = QtWidgets.QPushButton(self.centralwidget)
            self.pushButton.setGeometry(QtCore.QRect(270, 320, 141, 41))
            self.pushButton.setObjectName("pushButton")
            MainWindow.setCentralWidget(self.centralwidget)
            self.menubar = QtWidgets.QMenuBar(MainWindow)
            self.menubar.setGeometry(QtCore.QRect(0, 0, 640, 26))
            self.menubar.setObjectName("menubar")
            MainWindow.setMenuBar(self.menubar)
            self.statusbar = QtWidgets.QStatusBar(MainWindow)
            self.statusbar.setObjectName("statusbar")
            MainWindow.setStatusBar(self.statusbar)

            self.retranslateUi(MainWindow)
            QtCore.QMetaObject.connectSlotsByName(MainWindow)

        def retranslateUi(self, MainWindow):
            _translate = QtCore.QCoreApplication.translate
            MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
            self.label.setText(_translate("MainWindow", "VOLUME MAIN MUSIC"))
            self.label_2.setText(_translate("MainWindow", "MIN"))
            self.label_3.setText(_translate("MainWindow", "MAX"))
            self.label_5.setText(_translate("MainWindow", "VOLUME SOUNDS"))
            self.label_6.setText(_translate("MainWindow", "MIN"))
            self.label_7.setText(_translate("MainWindow", "MAX"))
            self.pushButton.setText(_translate("MainWindow", "PushButton"))


    class MyWidget(QMainWindow, Ui_MainWindow):
        def __init__(self, vSl=100):
            super().__init__()
            self.setupUi(self)
            self.setWindowTitle('Settings')
            self.pushButton.setText('Вернуться в игру')
            self.horizontalSlider.setMinimum(0)
            self.horizontalSlider.setMaximum(100)
            self.horizontalSlider.setValue(vSl)
            self.horizontalSlider.valueChanged[int].connect(self.slaider)
            self.horizontalSlider_2.setMinimum(0)
            self.horizontalSlider_2.setMaximum(100)
            self.horizontalSlider_2.setValue(vSl)
            self.horizontalSlider_2.valueChanged[int].connect(self.slaider2)
            self.pushButton.clicked.connect(self.closewindow)

        def slaider(self, value1):
            pygame.mixer.music.set_volume(value1 * 0.01)

        def slaider2(self, value2):
            sound_race_won.set_volume(value2 * 0.01)
            sound_race_lost.set_volume(value2 * 0.01)

        def closewindow(self):
            global state

            self.destroy()
            state = True


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


    class BigPlanet(pygame.sprite.Sprite):
        def __init__(self, x, y):
            super().__init__(planet_sprites)
            self.image = load_image('planet.png')
            self.rect = self.image.get_rect()
            self.rect = self.rect.move(x, y)


    class LineMove(pygame.sprite.Sprite):
        def __init__(self, x, y):
            super().__init__(line_move_sprites)
            self.image = load_image('move_line.png')
            self.rect = self.image.get_rect()
            self.rect = self.rect.move(x, y)


    class AnimateIconJim(pygame.sprite.Sprite):
        def __init__(self, x, y):
            super().__init__(icon_jim_sprites)
            self.image = load_image('icon_jim.png')
            self.rect = self.image.get_rect()
            self.rect = self.rect.move(x, y)
            self.y = self.rect.y

        def update(self):
            if self.rect.y < 100:
                self.rect.y = self.rect.y
            else:
                self.y = self.y - 0.8125 / 3
                self.rect.y = self.y


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
    jim_sprites.rect.x = 590
    jim_sprites.rect.y = 500

    tunnel_image_part1 = load_image('tunnel_part1.png')
    tunnel_image_part1.set_alpha(150)
    tunnel_sprites_part1_ = AnimatedTunnelPart1(tunnel_image_part1, 5, 3, 0, 0)

    tunnel_image_part2 = load_image('tunnel_part2.png')
    tunnel_image_part2.set_alpha(170)
    tunnel_sprites_part2_ = AnimatedTunnelPart2(tunnel_image_part2, 4, 2, 0, 0)

    asteroids_col_sprites = AsteroidCollision(load_image("asteroids_collision.png"), 6, 1, 0, 0)

    planet_sprite = BigPlanet(0, 0)

    line_move_sprite = LineMove(80, 100)

    icon_jim_sprite = AnimateIconJim(30, 650)

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

    pause_text = pygame.font.SysFont('Consolas', 32).render('Pause', True, pygame.color.Color('White'))


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
        global time_now

        x_rel = x_pos % width
        x_part2 = x_rel - width if x_rel > 0 else x_rel + width
        screen.blit(background_image, (x_rel, 0))
        screen.blit(background_image, (x_part2, 0))

        time_now = float('%s' % (totalTime))
        time_const = 63.01
        print(time_now)

        if time_now < time_const:
            tunnel_sprites_part1.update()
            tunnel_sprites_part1.draw(screen)

        elif time_now > time_const and time_now < time_const + 5:
            tunnel_sprites_part2.update()
            tunnel_sprites_part2.draw(screen)
        elif time_now > time_const + 5:
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
            planet_sprites.draw(screen)
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
        icon_jim_sprites.update()
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
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    state = False
                if event.key == pygame.K_SPACE:
                    state = True
        lapTime = round(time.time() - lastTime, 2)
        totalTime = round(time.time() - startTime, 2)
        if state:
            clock.tick(fps)

            drawWindow()
            if can_move:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_d]:
                    jim_sprites.rect.x = jim_sprites.rect.x + 5
                elif keys[pygame.K_a]:
                    jim_sprites.rect.x = jim_sprites.rect.x - 5
            x_pos += v / fps
        else:
            screen.blit(pause_text, (640, 330))
            app = QApplication(sys.argv)
            ex = MyWidget()
            ex.show()
            sys.exit(app.exec_())
        pygame.display.flip()
    pygame.quit()
