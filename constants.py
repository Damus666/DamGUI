import pygame
from typing import Any

_ColorValue = tuple[int,int,int]|list[int]|str|pygame.Color
class settings:
    defaults:dict = {}
    
    PURPLE_THEME = {
        'normal': (65, 0, 117),
        'on_hover': (101, 0, 171),
        "dark":(31,0,61),
        "on_press":(45,0,75),
        "outline":(67, 0, 127),
        "checkbox_inside":"purple",
    }
    
    @classmethod
    def create_fonts(cls, font_name:str="Segoe UI", size_name_table:dict[str,int]={
            "xxs":9,
            "xs":12,
            "s":15,
            "m":20,
            "l":26,
            "xl":32,
            "xxl":50,
            "xxxxl":100
        }, antialiasing:bool=True, y_padding:int=1, from_file:bool=False)->None:
        """Creates all the fonts. Automatically called importing damgui. 
        Can customize using the font name, size-name table (use the example as a base), antialiasing and y padding. If you use from file, provide the file path as the font name"""
        font_function = pygame.font.SysFont if not from_file else pygame.font.Font
        cls.FONT_XXS = font_function(font_name,size_name_table["xxs"])
        cls.FONT_XS = font_function(font_name,size_name_table["xs"])
        cls.FONT_S = font_function(font_name,size_name_table["s"])
        cls.FONT_M = font_function(font_name,size_name_table["m"])
        cls.FONT_L = font_function(font_name,size_name_table["l"])
        cls.FONT_XL = font_function(font_name,size_name_table["xl"])
        cls.FONT_XXL = font_function(font_name,size_name_table["xxl"])
        cls.FONT_XXXXL = font_function(font_name,size_name_table["xxxxl"])
        cls.TEXT_ANTIALIASING = antialiasing
        cls.TEXT_Y_PADDING = y_padding
    
    @classmethod
    def reset(cls)->None:
        """Resets all the settings"""
        cls.FONT = cls.FONT_M
        cls.OUTLINE_ENABLED = True
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
        cls.SCROLLBAR_THICKNESS = 10
        cls.previous = cls.copy()
        
    @classmethod
    def reset_font_size(cls)->None:
        """Sets the font to cls.defaults["FONT"]"""
        cls.FONT = cls.previous["FONT"]
        
    @classmethod
    def set_font_size(cls, size_name:str):
        """Set the current font using the font size. Changing settings.FONT directly is faster"""
        match size_name.lower():
            case "xxs": cls.FONT = cls.FONT_XXS
            case "xs": cls.FONT = cls.FONT_XS
            case "s": cls.FONT = cls.FONT_S
            case "m": cls.FONT = cls.FONT_M
            case "l": cls.FONT = cls.FONT_L
            case "xl": cls.FONT = cls.FONT_XL
            case "xxl": cls.FONT = cls.FONT_XXL
            case "xxxxl": cls.FONT = cls.FONT_XXXXL
        cls.previous = cls.copy()
            
    @classmethod
    def concise_style(cls)->None:
        """Disable the outline and set the corner radius to 0"""
        cls.OUTLINE_ENABLED = False
        cls.CORNER_RADIUS = 0
        cls.previous = cls.copy()
        
    @classmethod
    def end_concise_style(cls)->None:
        """Reset settings changed by the concise style"""
        cls.OUTLINE_ENABLED = True
        cls.CORNER_RADIUS = cls.previous["CORNER_RADIUS"]
        
    @classmethod
    def attached_style(cls, x_attach:bool=True,y_attach:bool=True)->None:
        """Sets margin and y_margin to 0 depending on the arguments"""
        if x_attach: cls.MARGIN = 0
        if y_attach: cls.Y_MARGIN = 0
        cls.previous = cls.copy()
        
    @classmethod
    def end_attached_style(cls)->None:
        """Reset settings changed by the attached style"""
        cls.MARGIN = cls.previous["MARGIN"]
        cls.Y_MARGIN = cls.previous["Y_MARGIN"]
        
    @classmethod
    def change_colors(cls, normal:_ColorValue=None, on_hover:_ColorValue=None, on_press:_ColorValue=None,
                      dark:_ColorValue=None, outline:_ColorValue=None, checkbox_inside:_ColorValue= None)->None:
        """Changes the settings color for every argument that is not None"""
        if normal: cls.ELEMENT_BG_COL = normal
        if on_hover: cls.ELEMENT_HOVER_COL = on_hover
        if on_press: cls.ELEMENT_PRESS_COL = on_press
        if dark: cls.WINDOW_BG_COL = dark
        if outline: cls.OUTLINE_COL = outline
        if checkbox_inside: cls.CHECKBOX_COL = checkbox_inside
        cls.previous = cls.copy()
        
    @classmethod
    def reset_colors(cls, normal:bool=True, on_hover:bool=True, on_press:bool=True, dark:bool=True, outline:bool=True, checkbox_inside:bool=True)->None:
        """Reset colors to default if its flag is set to true (default)"""
        if normal: cls.ELEMENT_BG_COL = settings.previous["ELEMENT_BG_COL"]
        if on_hover: cls.ELEMENT_HOVER_COL = settings.previous["ELEMENT_HOVER_COL"]
        if on_press: cls.ELEMENT_PRESS_COL = settings.previous["ELEMENT_PRESS_COL"]
        if dark: cls.WINDOW_BG_COL = settings.previous["WINDOW_BG_COL"]
        if outline: cls.OUTLINE_COL = settings.previous["OUTLINE_COL"]
        if checkbox_inside: cls.CHECKBOX_COL = settings.previous["CHECKBOX_COL"]
        
    @classmethod
    def color_theme(cls, theme_dict:dict[str,_ColorValue])->None:
        """Load the colors from a dict. Structure: {"color_name":<color_value>}; color_name must be included in settings.change_colors() parameter names"""
        cls.change_colors(**theme_dict)
    
    @classmethod
    def copy(cls)->dict[str,Any]:
        """Return a dict with a copy of the settings"""
        return vars(cls).copy()

    @classmethod
    def init(cls)->None:
        """Automatically called importing damgui"""
        cls.create_fonts()
        cls.reset()
        cls.defaults = cls.copy()
        
    @classmethod
    def set_previous(cls):
        cls.previous = vars(cls).copy()

class DamGUIException(Exception):
    """An exception renamed for damgui problems"""
    