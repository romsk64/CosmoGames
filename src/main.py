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
setting_fps: int = 60 # 0 -> разблокированный фпс
setting_window_size: tuple = (1920, 1000)
setting_window_caption: str = "CosmoGames"
setting_window_icon: str = "assets/icon/empire_at_war.jpg"
setting_bg_wid, setting_bg_hid = 1920, 1000
setting_count_file: str = "config/system.txt"

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
fps = pygame.time.Clock()
log_file = str()
hitbox_flist = list()

# debug
debugFps = fps.get_fps()
debugLevelUp = 1
debugLevelDown = 1

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
def game(bg) -> int: # как та самая игра с уничножением метеоритов
    # bg.blit(pygame.image.load())

    # пока генерация фона, потом сделаю нормальную картинку или нормальный шум по которому будет фон
    bg.fill(C_BLACK)

    for i in range(250):
        pygame.draw.rect(bg, C_WHITE, pygame.rect.Rect(random.randint(0, 1920), random.randint(0, 1080), 3, 3))
    pygame.display.update()

    return 0   
def cArcanoid(bg) -> int: # типа арканоида, но в космосе
    
    return 0
def cRaingers(bg) -> int: # что-то типа рпг
    
    return 0
def pause(bg) -> int:
    
    return 0

# features
# def debugMenu(bg):
#     global debugFps
#     global debugLevelUp # коллекция уровней    в итоге получается вот так:
#     global debugLevelDown # сам уровень            debugLevelUp-debugLevelDown

# def debugHitboxMenu(bg, obj_list):
#     global hitbox_flist

#     for _ in len(obj_list):
#         hitbox_flist.append(None)

#     for obj in len(obj_list):
#         # wid = obj_list[obj].rect.width
#         # hid = obj_list[obj].rect.height
#         # x = obj_list[obj].rect.x
#         # y = obj_list[obj].rect.y
        
#         objhb = Hitbox(obj_list[obj])
#         hitbox_flist[obj] = objhb

# cycle
def reload(): # перезагрузка
    pass

# startlog()
menu(bg)
text = Text(0, 0, bg, "Consolas", 16, (255, 255, 255))
text.drawSysText("Привет")

while _main_:
    fps.tick(setting_fps)

    _menu_
    _settings_ # init in cycle
    _scbreak_
    _game_
    _mcbreak_
    _gameca_
    _gamecr_

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
                pygame.quit()
                _main_ = False
                _gcbreak_ = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pause(bg)
                # debug
                elif event.key == pygame.K_KP1:
                    print("Reload background")
                    game(bg)
    if _mcbreak_:
        del _mcbreak_
        break
    elif _scbreak_:
        del _scbreak_
        break
    elif _gcbreak_:
        del _gcbreak_
        break
    pygame.display.update()

    # while _settings_:
    #     fps.tick(setting_fps)

    #     _settings_ # init in cycle
    #     _game_
    #     _mcbreak_
    #     _gameca_
    #     _gamecr_

    #     for event in pygame.event.get():
    #         if event.type == pygame.QUIT:
    #             _settings_ = False
    #             _game_ = False
    #             _gameca_ = False
    #             _gamecr_ = False
    #             pygame.quit()
    #             _settings_ = False
    #             _scbreak_ = True
    #             break