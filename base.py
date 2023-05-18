from .constants import *
from .stack import Stack

def _size_minsize_surf(minsize,surf,istext=False):
    ypadding = settings.PADDING if not istext else settings.TEXT_Y_PADDING
    return max(minsize[0],surf.get_width()+settings.PADDING*2), max(minsize[1],surf.get_height()+ypadding*2)    
def _size_surf(surf,istext=False):
    ypadding = settings.PADDING if not istext else settings.TEXT_Y_PADDING
    return surf.get_width()+settings.PADDING*2, surf.get_height()+ypadding*2
def _render_text(text):
    return settings.FONT.render(str(text),settings.TEXT_ANTIALIASING,settings.TEXT_COL)

def _relative_rect_pos(surf ,rect, posname):
    pos = None
    match posname:
        case "center": pos = rect.center
        case "topleft": pos = (rect.left+settings.MARGIN,rect.top+settings.MARGIN)
        case "topright": pos = (rect.right-settings.MARGIN,rect.top+settings.MARGIN)
        case "bottomleft": pos = (rect.left+settings.MARGIN,rect.bottom-settings.MARGIN)
        case "bottomright": pos = (rect.right+settings.MARGIN,rect.bottom-settings.MARGIN)
        case "midleft": pos = (rect.left+settings.MARGIN,rect.centery)
        case "midright": pos = (rect.right-settings.MARGIN,rect.centery)
        case "midtop": pos = (rect.centerx,rect.top+settings.MARGIN)
        case "midbottom": pos = (rect.centerx,rect.bottom-settings.MARGIN)
    return surf.get_rect(**{posname:pos})

def _get_basic(size):
    winpos = Stack.window["pos"]; rel = Stack.get_rel()
    abs = (winpos[0]+rel[0],winpos[1]+rel[1])
    return rel, abs, pygame.Rect(rel,size), pygame.Rect(abs,size)

def _get_pos():
    winpos = Stack.window["pos"]; rel = Stack.get_rel()
    return rel, (winpos[0]+rel[0],winpos[1]+rel[1])
    
def _base(id,type,bg,outline,size,abs,rel,rect,absrect,tsurf=None,trect=None,text="",canpress=True,canhover=True,darkbg=False,surfbg=False):
    el = {
        "id":id,
        "type":type,
        "bg":bg,
        "darkbg":darkbg,
        "outline":outline,
        "size":size,
        "sx":size[0],
        "sy":size[1],
        "abs":abs,
        "ax":abs[0],
        "ay":abs[1],
        "rel":rel,
        "rx":rel[0],
        "ry":rel[1],
        "rect":rect,
        "absrect":absrect,
        "tsurf":tsurf,
        "trect":trect,
        "text":text,
        "ignorepos":False,
        "placetop":False,
        "surfbg":surfbg,
        "hovering":Stack.hovering(absrect,Stack.window) if canhover else False,
        "pressed":Stack.clicking(absrect,Stack.window) if canpress else False,
        "unhover_press":False,
        "selected":False,
        "settings":settings.copy(),
        "elements":[],
        "topelements":[],
        "parent":Stack.window,
    }
    if el["pressed"] or (id in Stack.memory and Stack.memory[id]["unhover_press"]): el["unhover_press"] = True
    if not Stack.mousepressed[0]: el["unhover_press"] = False
    return el

_EMPTY_R = pygame.Rect(0,0,0,0)
