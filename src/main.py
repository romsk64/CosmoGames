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

# json settings
setting_fps = 60
setting_window_size = (1920, 1000)
setting_window_caption = "CosmoGames"
setting_window_icon = "images/icon/empire_at_war.jpg"

# program settings
pygame.init()
bg = pygame.display.set_mode(setting_window_size)
pygame.display.set_caption(setting_window_caption)
pygame.display.set_icon(pygame.image.load(setting_window_icon))

_menu_ = True
_game_ = False
_settings_ = False
fps = pygame.time.Clock()
log_file = str()

class Button():
    def __init__(self, x, y, wid, hid, win, col, cont_col, texture = None):
        self.x = x
        self.y = y
        self.wid = wid
        self.hid = hid
        self.win = win
        self.col = col
        self.cont_col = cont_col
        self.texture = texture
        
        self.cont_wid = 2
    def drawButton(self, fromMain): # True/False
        rect = pygame.rect.Rect(self.x, self.y, self.wid, self.hid)
        pygame.draw.rect(self.win, self.col, rect)

        rect = pygame.rect.Rect(self.x, self.y, self.wid, self.hid)
        pygame.draw.rect(self.win, self.col, rect)
    def currentButton(self):
        pass

def startlog():
    global log_file
    
    with open("system.txt", "r") as open_col_f:
        open_col = open_col_f.read(10)
        log_file = f"logs/log_{open_col}"
        open_col = int(open_col)
        open_col += 1
    open_col_f.close()
    del open_col_f

    with open("system.txt", "w") as open_col_f:
        open_col_f.write(str(open_col))
    open_col_f.close()
    del open_col_f

def log(level: int, message: str, method: str):
    print(f"[{level}: {method}]: {message}")

def menu(bg):
    pass
def settings(bg):
    pass
def main(bg):
    pass

# startlog()
fps.tick()