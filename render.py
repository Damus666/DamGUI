from .stack import Stack
from .constants import *
import pygame

def render_all(surface):
    for window in Stack.window_history: render_window(surface,window)
        
def render_element(surface, element):
    if element["type"] == "window" or element["type"] == "container":
        render_window(surface, element)
        return
    conf = element["settings"]
    if element["bg"]:
        col = conf["ELEMENT_BG_COL"]
        if element["darkbg"]: col = conf["WINDOW_BG_COL"]
        if element["hovering"]: col = conf["ELEMENT_HOVER_COL"]
        if element["pressed"] or (element["selected"] and not element["hovering"]): col = conf["ELEMENT_PRESS_COL"]
        pygame.draw.rect(surface,col,element["rect"],0,conf["CORNER_RADIUS"])
    if element["outline"] and not element["surfbg"]:
        pygame.draw.rect(surface,conf["OUTLINE_COL"],element["rect"],conf["OUTLINE_SIZE"],conf["CORNER_RADIUS"])
    if element["tsurf"]:
        surface.blit(element["tsurf"],element["trect"])
        if element["surfbg"] and element["outline"]: 
            pygame.draw.rect(surface,conf["OUTLINE_COL"],element["rect"],conf["OUTLINE_SIZE"],conf["CORNER_RADIUS"])
    if element["type"] == "checkbox":
        if element["selected"]: pygame.draw.rect(surface,conf["CHECKBOX_COL"],element["innerrect"],0,conf["CORNER_RADIUS"])
        
def render_window(surface, window):
    conf = window["settings"]
    sx,sy = window["minsize"]
    if window["type"] == "window":
        for el in window["elements"]:
            er = el["rx"]+el["sx"]
            eb = el["ry"]+el["sy"]
            if er > sx: sx = er
            if eb > sy: sy = eb
        sx+=conf["MARGIN"];sy+=conf["MARGIN"]
        window["rect"].w = sx
        window["rect"].h = sy
        window["absrect"].size = window["rect"].size
        window["size"] = window["rect"].size
        if window["surf"].get_size() != (sx,sy): window["surf"] = pygame.Surface((sx-conf["MARGIN"],sy-conf["MARGIN"]),pygame.SRCALPHA)
    pygame.draw.rect(surface,conf["WINDOW_BG_COL"],window["rect"],0,conf["CORNER_RADIUS"])
    if window["outline"]: pygame.draw.rect(surface,conf["OUTLINE_COL"],window["rect"],conf["OUTLINE_SIZE"],conf["CORNER_RADIUS"])
    for el in window["elements"]:
        render_element(window["surf"],el)
    surface.blit(window["surf"],window["rect"])
    