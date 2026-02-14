# romsk64, 2026

import pygame
import json
import os

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

_menu_ = True
_game_ = False
_settings_ = False
_mcbreak_ = False # menu cycle break
_scbreak_ = False # settings cycle break
_gcbreak_ = False # game cycle break
fps = pygame.time.Clock()
log_file = str()

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

        self.rectArea = rect
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
    def currentButton(self):
        cw = self.cont_wid

        downrect = pygame.rect.Rect(self.x - cw, self.y - cw, self.wid + (cw * 2), self.hid + (cw * 2))
        pygame.draw.rect(self.win, self.cur_cont_col, downrect)

        self.drawButton(True)

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
def menu(bg):
    # bgArea = Area(0, 0, setting_bg_wid, setting_bg_hid, bg, ())
    bg.fill(C_BLUE)
def settings(bg):
    pass
def game(bg): # как та самая игра с уничножением метеоритов
    pass
def cArcanoid(bg): # типа арканоида, но в космосе
    pass
def cRaingers(bg): # что-то типа рпг
    pass

# features
def debugMenu(bg):
    global debugFps
    global debugLevelUp # коллекция уровней    в итоге получается вот так:
    global debugLevelDown # сам уровень            debugLevelUp-debugLevelDown

# startlog()
menu(bg)
text = Text(0, 0, bg, "Consolas", 16, (255, 255, 255))
text.drawSysText("Привет")

while _menu_:
    fps.tick(setting_fps)

    _settings_ # init in cycle
    _game_
    _mcbreak_

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            _settings_ = False
            _game_ = False
            pygame.quit()
            _menu_ = False
            _mcbreak_ = True
            break
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F3:
                print(fps.get_fps())
            if event.key == pygame.K_1:
                pass # game
    if _mcbreak_:
        del _mcbreak_
        break
    pygame.display.update()