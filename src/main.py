# romsk64, 2026

import pygame
import json
import os
import random

file_dir = os.getcwd()
current_dir = os.path.dirname(os.path.abspath(__file__))

if file_dir.lower() != current_dir.lower():
    os.chdir(current_dir)
elif file_dir.lower() == current_dir.lower():
    pass

print(f"ват {os.getcwd()}")

# color constants
C_WHITE = (255, 255, 255)
C_BLACK = (0, 0, 0)
C_RED = (255, 0, 0)
C_BLUE = (0, 0, 255)
C_GREEN = (0, 255, 0)

# json settings
setting_fps: int = 120 # 0 -> разблокированный фпс
setting_window_size: tuple = (1920, 1000)
setting_window_caption: str = "CosmoGames"
setting_window_icon: str = "assets/icon/empire_at_war.jpg"
setting_bg_wid, setting_bg_hid = 1920, 1000
setting_count_file: str = "config/system.txt"
setting_graphic_starcount: int = 250

# program settings
pygame.init()
bg = pygame.display.set_mode(setting_window_size)
pygame.display.set_caption(setting_window_caption)
pygame.display.set_icon(pygame.image.load(setting_window_icon))

_main_ = True
_menu_ = True
_game_ = False
_gameca_ = False
_gamecr_ = False
_settings_ = False
_mcbreak_ = False # menu cycle break
_scbreak_ = False # settings cycle break
_gcbreak_ = False # game cycle break
_gcabreak_ = False
_gcrbreak_ = False
_stdbreak_ = False
_textFPS_ = False
fps = pygame.time.Clock()
log_file = str()
hitbox_flist = list()
starList = [[], []]
for i in range(setting_graphic_starcount):
    starList[0].append(None)
    starList[1].append(None)

# debug
debugFps = fps.get_fps()
debugLevelUp = 1
debugLevelDown = 1
debugCodeExit = 0
debugCodeFly = 0

# classes
class Area():
    def __init__(self, x, y, wid, hid, win, col):
        self.x = x
        self.y = y
        self.wid = wid
        self.hid = hid
        self.win = win
        self.col = col
    def drawArea(self):
        rect = pygame.rect.Rect(self.x, self.y, self.wid, self.hid)
        pygame.draw.rect(self.win, self.col, rect)

        self.rect = rect
    def drawCountur(self, cont_wid: int, cont_col: tuple):
        countur_rect = pygame.rect.Rect(self.x - cont_wid, self.y - cont_wid, self.wid + (cont_wid * 2), self.hid + (cont_wid * 2))
        pygame.draw.rect(self.win, cont_col, countur_rect)

class Text():
    def __init__(self, x, y, win, font, fsize, fcol, fmod = None):
        self.x = x
        self.y = y
        self.win = win
        self.font = font # "assets/fonts/DroidSansMono.ttf"
        self.fsize = fsize
        self.fcol = fcol
        self.fmod = fmod
    def drawText(self, text):
        drawingText = pygame.font.Font(self.font, self.fsize)
        dtext = drawingText.render(text, True, self.fcol)
        self.win.blit(dtext, (self.x, self.y))
    def drawTextAgain(self, text):
        pass

    def drawSysText(self, text):
        drawingText = pygame.font.SysFont(self.font, self.fsize) # желательно consolas
        dtext = drawingText.render(text, True, self.fcol)
        self.win.blit(dtext, (self.x, self.y))
    def drawSysTextAgain(self, text):
        pass

class TextFromMap(): # текст с одной картинки map.png, возможно будет удалено
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Button():
    def __init__(self, x, y, wid, hid, win, col, cont_col, texture = None, cur_cont_col = (255, 255, 255)):
        self.x = x
        self.y = y
        self.wid = wid
        self.hid = hid
        self.win = win
        self.col = col
        self.cont_col = cont_col
        self.texture = texture
        self.cur_cont_col = cur_cont_col
        
        self.cont_wid = 2
    def drawButton(self, fromMain = False): # True/False
        cw = self.cont_wid

        if not fromMain: # отрисовка контура
            downrect = pygame.rect.Rect(self.x - cw, self.y - cw, self.wid + (cw * 2), self.hid + (cw * 2))
            pygame.draw.rect(self.win, self.cont_col, downrect)

        rect = pygame.rect.Rect(self.x, self.y, self.wid, self.hid)
        pygame.draw.rect(self.win, self.col, rect)
        
        self.rect = rect
    def currentButton(self):
        cw = self.cont_wid

        downrect = pygame.rect.Rect(self.x - cw, self.y - cw, self.wid + (cw * 2), self.hid + (cw * 2))
        pygame.draw.rect(self.win, self.cur_cont_col, downrect)

        self.drawButton(True)
        # self.rect.y

class Debug():
    def __init__(self, win):
        global debugFps
        global debugLevelUp # коллекция уровней    в итоге получается вот так:
        global debugLevelDown # сам уровень            debugLevelUp-debugLevelDown

        self.win = win

        self.debugMenu_ = False
        self.debugHitboxMenu_ = False
    def debugMenu(self):
        global debugFps
        global debugLevelUp # коллекция уровней    в итоге получается вот так:
        global debugLevelDown # сам уровень            debugLevelUp-debugLevelDown

        self.debugMenu_ = True
    def debugHitboxMenu(self, obj_list):
        global hitbox_flist

        for _ in len(obj_list):
            hitbox_flist.append(None)
        
        for obj in len(obj_list):
            # wid = obj_list[obj].rect.width
            # hid = obj_list[obj].rect.height
            # x = obj_list[obj].rect.x
            # y = obj_list[obj].rect.y
            
            objhb = Hitbox(obj_list[obj])
            hitbox_flist[obj] = objhb
        self.debugHitboxMenu_ = True
debug = Debug(bg)

class Hitbox(pygame.sprite.Sprite):
    def __init__(self, obj):
        wid = obj.rect.width
        hid = obj.rect.height
        x = obj.rect.x
        y = obj.rect.y

        super().__init__(self)
        self.image_pr = pygame.image.load("assets/game/hitbox.png").convert_alpha()
        self.rect = pygame.rect.Rect(x, y, wid, hid)
        
        self.obj = obj
    def drawHitbox(self):
        wid = self.obj.rect.width
        hid = self.obj.rect.height
        x = self.obj.rect.x
        y = self.obj.rect.y

        wid

class gameclass:
    class SpaceVoyager():
        def __init__(self, win, spdpx, wid, hid, x, y, texture = None):
            self.win = win
            self.spdpx = spdpx
            self.x = x
            self.y = y
            self.wid = wid
            self.hid = hid
            self.texture = texture

            self.attackRect = list()
        # def rectInit(self):
        #     self.rect = pygame.rect.Rect(self.x, self.y, 20, 50)
        def rectDraw(self):
            self.rect = pygame.rect.Rect(self.x, self.y, 20, 50)
            pygame.draw.rect(self.win, C_RED, self.rect)
        def chkCordLimits(self, moveMode): # 1 - вверх, 2 - вниз, 3 - влево, 4 - вправо
            if moveMode == 1:
                # if self.x >= setting_bg_wid or self.x <= 0 or self.y >= setting_bg_hid or self.y <= 0:
                    # return True
                if self.y <= 0:
                    return True
            elif moveMode == 2:
                if (self.y + self.hid) >= setting_bg_hid:
                    return True
            elif moveMode == 3:
                if self.x <= 0:
                    return True
            elif moveMode == 4:
                if (self.x + self.wid) >= setting_bg_wid:
                    return True

        def moveL(self):
            global debugCodeFly

            self.x -= self.spdpx
            if self.chkCordLimits(3):
                self.x += self.spdpx
                debugCodeFly = 1
                return debugCodeFly
            else:
                game_reloadbg(self.win)
                game_reloadsprite()
                return 0
            # self.rect.move(self.x, self.y)
        def moveR(self):
            global debugCodeFly

            self.x += self.spdpx
            if self.chkCordLimits(4):
                self.x -= self.spdpx
                debugCodeFly = 1
                return debugCodeFly
            else:
                game_reloadbg(self.win)
                game_reloadsprite()
                return 0
            # self.rect.move(self.x, self.y)
        def moveUp(self):
            global debugCodeFly
            
            self.y -= self.spdpx
            if self.chkCordLimits(1):
                self.y += self.spdpx
                debugCodeFly = 1
                return debugCodeFly
            else:
                game_reloadbg(self.win)
                game_reloadsprite()
                return 0
            # self.rect.move(self.x, self.y)
        def moveDown(self):
            global debugCodeFly

            self.y += self.spdpx
            if self.chkCordLimits(2):
                self.y -= self.spdpx
                debugCodeFly = 1
                return debugCodeFly
            else:
                game_reloadbg(self.win)
                game_reloadsprite()
                return 0
            # self.rect.move(self.x, self.y)
        
        def attack(self, clickposX, clickposY, enemyList):
            pygame.draw.line(self.win, C_WHITE, (self.x, self.y), (clickposX, clickposY))
            for i in len(enemyList):
                if enemyList[i - 1].collidePoint(clickposX, clickposY):
                    enemyList[i - 1].chgColor(C_RED)
        def testattack(self, clickposX, clickposY):
            pygame.draw.line(self.win, C_WHITE, (self.x, self.y), (clickposX, clickposY))
    
    class Enemy():
        def __init__(self, x, y, color, texture):
            self.x = x
            self.y = y
            self.color = color
            self.texture = texture
        def drawEnemy(self):
            self.rect = pygame.rect.Rect(self.x, self.y, 20, 50)
            pygame.draw.rect(self.win, C_RED, self.rect)
        def chgColor(self, color):
            self.color = color
        def collidePoint(self, clickposX, clickposY):
            if self.rect.collidepoint(clickposX, clickposY):
                return True

class arcanoid:
    class Ball():
        def __init__(self, spdpx, x, y, texture):
            self.x = x
            self.y = y
            self.spdpx = spdpx
            self.texture = texture
        def move(self, naprav): # naprav -> направление
            pass
        def rectInit(self):
            pass
        def drawTexture(self, nx = None, ny = None): # nx -> new x, ny -> new y
            if nx != None and ny != None:
                return 1
            else:
                pass

    class Platform():
        def __init__(self, spdpx, x, y, texture):
            self.x = x
            self.y = y
            self.spdpx = spdpx
            self.texture = texture
        def move(self, naprav): # naprav -> направление
            pass
        def rectInit(self):
            pass
        def drawTexture(self, nx = None, ny = None): # nx -> new x, ny -> new y
            if nx != None and ny != None:
                return 1
            else:
                pass

# statistics
statKills = 0
statTime = 0

# log functions
def startlog():
    global log_file
    
    with open(setting_count_file, "r") as open_col_f:
        open_col = open_col_f.read(10)
        log_file = f"logs/log_{open_col}"
        open_col = int(open_col)
        open_col += 1
    open_col_f.close()
    del open_col_f

    with open(setting_count_file, "w") as open_col_f:
        open_col_f.write(str(open_col))
    open_col_f.close()
    del open_col_f
def log(level: int, message: str, method: str):
    print(f"[{level}: {method}]: {message}")

# standart functions
def menu(bg) -> int:
    # bgArea = Area(0, 0, setting_bg_wid, setting_bg_hid, bg, ())
    bg.fill(C_BLUE)
    return 0
def settings(bg) -> int:
    return 0
def game_drawbg(bg) -> int:
    # пока генерация фона, потом сделаю нормальную картинку или нормальный шум по которому будет фон
    global starList
    global setting_graphic_starcount

    bg.fill(C_BLACK)

    for i in range(setting_graphic_starcount):
        starList[0][i - 1] = random.randint(0, 1920) # x
        starList[1][i - 1] = random.randint(0, 1080) # y
        pygame.draw.rect(bg, C_WHITE, pygame.rect.Rect(starList[0][i - 1], starList[1][i - 1], 3, 3))
    pygame.display.update()

    return 0
def game(bg) -> int: # как та самая игра с уничножением метеоритов
    global starList
    global voyager

    game_drawbg(bg)
    voyager = gameclass.SpaceVoyager(bg, 5, 25, 50, 500, 500)
    # voyager.rectInit()
    voyager.rectDraw()
    
    return 0
def game_reloadbg(bg) -> int:
    global starList
    global voyager

    bg.fill(C_BLACK)

    for i in range(setting_graphic_starcount):
        pygame.draw.rect(bg, C_WHITE, pygame.rect.Rect(starList[0][i - 1], starList[1][i - 1], 3, 3))

    return 0
def game_reloadsprite() -> int:
    global voyager

    voyager.rectDraw()

    return 0
def game_reloadnewbg(bg) -> int:
    global voyager
    
    game_drawbg(bg)
    voyager.rectDraw()

    return 0
def cArcanoid(bg) -> int: # типа арканоида, но в космосе
    
    return 0
def cRaingers(bg) -> int: # что-то типа рпг
    
    return 0
def pause(bg) -> int:
    
    return 0

# cycle
def quit(isInCycle = True, cycleVar = _main_):
    global _main_
    global _stdbreak_

    if isInCycle:
        cycleVar = False
        _main_ = False
        pygame.quit()
        _stdbreak_ = True
        
def reload(): # перезагрузка
    os.system("py -3.12 reload.py")

# startlog()
menu(bg)
text = Text(0, 0, bg, "Consolas", 16, C_WHITE)
text.drawSysText("Привет")

textFPS = Text(0, 0, bg, "Consolas", 16, C_WHITE)

while _main_:
    fps.tick(setting_fps)

    _menu_
    _settings_ # init in cycle
    _scbreak_
    _game_
    _mcbreak_
    _gameca_
    _gamecr_
    _textFPS_

    if _menu_ and not _mcbreak_:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                _settings_ = False
                _game_ = False
                _gameca_ = False
                _gamecr_ = False
                pygame.quit()
                _main_ = False

                _menu_ = False
                _mcbreak_ = True
                break
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F3:
                    print(fps.get_fps())
                elif event.key == pygame.K_1:
                    game(bg) # game
                    _settings_ = False
                    _game_ = True
                    _gameca_ = False
                    _gamecr_ = False

                    _menu_ = False
                    # _mcbreak_ = True
                elif event.key == pygame.K_2:
                    cArcanoid(bg)
                    _settings_ = False
                    _game_ = False
                    _gameca_ = True
                    _gamecr_ = False
                        
                    _menu_ = False
                    _mcbreak_ = True
                elif event.key == pygame.K_3:
                    cRaingers(bg)
                    _settings_ = False
                    _game_ = False
                    _gameca_ = False
                    _gamecr_ = True

                    _menu_ = False
                    _mcbreak_ = True
                elif event.key == pygame.K_4:
                    settings(bg)
                    _settings_ = True
                    _game_ = False
                    _gameca_ = False
                    _gamecr_ = False
                        
                    _menu_ = False
                    _mcbreak_ = True
                elif event.key == pygame.K_5 or event.key == pygame.K_q:
                    _settings_ = False
                    _game_ = False
                    _gameca_ = False
                    _gamecr_ = False
                    # потом будет вопрос действительно ли ты хочешь выйти?
                    pygame.quit()
                    _main_ = False
                    _menu_ = False
                    _mcbreak_ = True
    elif _settings_ and not _scbreak_:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                _settings_ = False
                _game_ = False
                _gameca_ = False
                _gamecr_ = False
                _menu_ = False
                pygame.quit()
                _main_ = False
                _scbreak_ = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pause(bg)
    elif _game_ and not _gcbreak_:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                _game_ = False
                _settings_ = False
                _gameca_ = False
                _gamecr_ = False
                _menu_ = False
                _textFPS_ = False
                pygame.quit()
                _main_ = False
                _gcbreak_ = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pause(bg)
                # debug
                elif event.key == pygame.K_F3:
                    if _textFPS_:
                        _textFPS_ = False
                    elif not _textFPS_:
                        _textFPS_ = True
                elif event.key == pygame.K_KP1:
                    print("Reload background")
                    game_reloadnewbg(bg)
                elif event.key == pygame.K_F12:
                    reload()
                # if event.key == pygame.K_w:
                #     voyager.moveUp()
                # if event.key == pygame.K_s:
                #     voyager.moveD()
                # if event.key == pygame.K_a:
                #     voyager.moveL()
                # if event.key == pygame.K_d:
                #     voyager.moveR()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                clickposX, clickposY = event.pos
                # voyager.attack(clickposX, clickposY)
                voyager.testattack(clickposX, clickposY)
        
        if _textFPS_:
            game_reloadbg(bg)
            game_reloadsprite()
            textFPS.drawSysText(f"FPS: {int(fps.get_fps())}")
        if not _gcbreak_:
            pressed_keys = pygame.key.get_pressed()
            if pressed_keys[pygame.K_w] or pressed_keys[pygame.K_UP]:
                voyager.moveUp()
                if _textFPS_:
                    textFPS.drawSysText(f"FPS: {int(fps.get_fps())}")
            if pressed_keys[pygame.K_s] or pressed_keys[pygame.K_DOWN]:
                voyager.moveDown()
                if _textFPS_:
                    textFPS.drawSysText(f"FPS: {int(fps.get_fps())}")
            if pressed_keys[pygame.K_a] or pressed_keys[pygame.K_LEFT]:
                voyager.moveL()
                if _textFPS_:
                    textFPS.drawSysText(f"FPS: {int(fps.get_fps())}")
            if pressed_keys[pygame.K_d] or pressed_keys[pygame.K_RIGHT]:
                voyager.moveR()
                if _textFPS_:
                    textFPS.drawSysText(f"FPS: {int(fps.get_fps())}")
    if _mcbreak_:
        del _mcbreak_
        break
    elif _scbreak_:
        del _scbreak_
        break
    elif _gcbreak_:
        del _gcbreak_
        break

    elif _stdbreak_:
        del _stdbreak_
        break
    pygame.display.update()

print(f"Exit with code {debugCodeExit}")