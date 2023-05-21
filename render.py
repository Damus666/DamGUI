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
        if ((element["pressed"] or element["unhover_press"]) and element["canrenderpress"]) or (element["selected"] and not element["hovering"]): col = conf["ELEMENT_PRESS_COL"]
        
        pygame.draw.rect(surface,col,element["rect"],0,conf["CORNER_RADIUS"])
    if element["outline"] and not element["surfbg"]:
        pygame.draw.rect(surface,conf["OUTLINE_COL"],element["rect"],conf["OUTLINE_SIZE"],conf["CORNER_RADIUS"])
    if element["tsurf"]:
        surface.blit(element["tsurf"],element["trect"])
        if element["surfbg"] and element["outline"]: 
            pygame.draw.rect(surface,conf["OUTLINE_COL"],element["rect"],conf["OUTLINE_SIZE"],conf["CORNER_RADIUS"])
    if element["type"] == "checkbox":
        if element["selected"]: pygame.draw.rect(surface,conf["CHECKBOX_COL"],element["innerrect"],0,conf["CORNER_RADIUS"])
    elif element["type"] == "progress_bar":
        pygame.draw.rect(surface,element["fill_color"],element["fill_rect"],0,conf["CORNER_RADIUS"])
        
def render_window(surface, window):
    conf = window["settings"]
    sx,sy = window["minsize"]
    scox,scoy = window["scrolloffset"]
    realx, realy = window["size"]
    if window["can_scroll"]:
        for el in window["elements"]:
            er = el["rx"]+el["sx"]
            eb = el["ry"]+el["sy"]
            if er > sx: sx = er
            if eb > sy: sy = eb
            if er+scox > realx: realx = er+scox
            if eb+scoy > realy: realy = eb+scoy
        window["realsize"] = (realx, realy)
        sx+=conf["MARGIN"];sy+=conf["Y_MARGIN"]
        if window["autosize"]:
            window["rect"].w = sx
            window["rect"].h = sy
            window["absrect"].size = window["rect"].size
            window["size"] = window["rect"].size
            if window["surf"].get_size() != (sx,sy): window["surf"] = pygame.Surface((sx-conf["MARGIN"],sy-conf["Y_MARGIN"]),pygame.SRCALPHA)
    pygame.draw.rect(surface,conf["WINDOW_BG_COL"],window["rect"],0,conf["CORNER_RADIUS"])
    for el in window["elements"]:
        render_element(window["surf"],el)
    surface.blit(window["surf"],window["rect"])
    if window["outline"]: pygame.draw.rect(surface,conf["OUTLINE_COL"],window["rect"],conf["OUTLINE_SIZE"],conf["CORNER_RADIUS"])
    