import pygame

class settings:
    defaults:dict = {}
    @classmethod
    def create_fonts(cls, font_name="Segoe UI"):
        cls.FONT_XXS = pygame.font.SysFont(font_name,9)
        cls.FONT_XS = pygame.font.SysFont(font_name,12)
        cls.FONT_S = pygame.font.SysFont(font_name,15)
        cls.FONT_M = pygame.font.SysFont(font_name,20)
        cls.FONT_L = pygame.font.SysFont(font_name,26)
        cls.FONT_XL = pygame.font.SysFont(font_name,30)
        cls.FONT_XXL = pygame.font.SysFont(font_name,50)
        cls.FONT_XXXXL = pygame.font.SysFont(font_name,100)
    
    @classmethod
    def reset(cls):
        cls.FONT = cls.FONT_M
        cls.TEXT_COL = "white"
        cls.TEXT_ANTIALIASING = True
        cls.MARGIN = 3
        cls.PADDING = 5
        cls.CORNER_RADIUS = 4
        cls.TEXT_Y_PADDING = 1
        cls.OUTLINE_SIZE = 1
        cls.Y_MARGIN = 4
        cls.WINDOW_BG_COL = (20,20,20)
        cls.ELEMENT_BG_COL = (30,30,30)
        cls.ELEMENT_HOVER_COL = (40,40,40)
        cls.ELEMENT_PRESS_COL = (22,22,22)
        cls.OUTLINE_COL = (50,50,50)
        cls.CHECKBOX_COL = (0,100,200)
    
    @classmethod
    def copy(cls): return vars(cls).copy()

settings.create_fonts()
settings.reset()
settings.defaults = settings.copy()

class DamGUIException(Exception):...
    