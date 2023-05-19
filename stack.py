from .constants import *

class Stack:
    windows, window_history, events, memory = [],[],[],{}
    mousepos, mouserel = (0,0), (0,0)
    mousepressed = keypressed = custom_pos = last_element = window = None
    place_side = place_top = ignore_pos = start_called = False
    last_row_y = 0
    
    @classmethod
    def add_window(cls, win):
        old = cls.windows[-1] if len(cls.windows) > 0 else None
        cls.windows.append(win)
        if cls.window and "relative" in win:
            cls.window["elements"].append(win)
        if not "relative" in win: cls.window_history.append(win)
        cls.window = cls.last_element = win
        cls.memory[win["id"]] = win
        if cls.custom_pos or cls.ignore_pos: win["ignorepos"] = True
        if cls.place_top:
            win["placetop"] = True
            if old: old["topelements"].append(win)
        cls.custom_pos, cls.ignore_pos, cls.place_top, cls.place_side = None, False, False, False
        cls.last_row_y = -settings.MARGIN
        
    @classmethod
    def remove_last(cls):
        normal_els, top_els = [],[]
        for el in cls.window["elements"]:
            if el["placetop"]: top_els.append(el)
            else: normal_els.append(el)
        normal_els.extend(top_els)
        cls.window["elements"] = normal_els
        if len(cls.windows) <= 0: raise DamGUIException("All windows are already closed")
        cls.windows.pop(-1)
        cls.last_row_y = cls.window["ry"]-settings.MARGIN
        if len(cls.windows) > 0: cls.window = cls.windows[-1]
        else: cls.window = None
        
    @classmethod
    def win_check(cls):
        if not cls.window: raise DamGUIException("A window must be opened before creating elements")
        
    @classmethod
    def start_check(cls):
        if not cls.start_called: raise DamGUIException("damgui.frame_start() must be called before creating elements")
        
    @classmethod
    def get_rel(cls):
        if cls.custom_pos: return cls.custom_pos
        x = y = 0
        for el in cls.window["elements"]:
            if (newy:=(el["ry"]+el["sy"])) > y and not el["ignorepos"]: y = newy if not cls.place_side else el["ry"]
        if cls.place_side:
            for el in cls.window["elements"]:
                if el["ry"] == y and (newx:=(el["rx"]+el["sx"])) > x and not el["ignorepos"]: x = newx
            y = cls.last_row_y
        else: cls.last_row_y = y
        return x+settings.MARGIN,y+settings.Y_MARGIN
    
    @classmethod
    def add_element(cls,el):
        cls.window["elements"].append(el)
        if el["id"] != None: cls.memory[el["id"]] = el
        cls.last_element = el
        cls.place_side = False
        if cls.custom_pos or cls.ignore_pos: el["ignorepos"] = True
        if cls.place_top:
            el["placetop"] = True
            cls.window["topelements"].append(el)
        cls.custom_pos, cls.ignore_pos, cls.place_top = None, False, False
    
    @classmethod
    def hovering(cls, rect, parent=None):
        if not rect.collidepoint(cls.mousepos) or not (parent == None or parent["absrect"].collidepoint(cls.mousepos)): return False
        if not cls.place_top and parent:
            for el in parent["topelements"]:
                if el["absrect"].collidepoint(cls.mousepos): return False
        return True
    
    @classmethod
    def clicking(cls, rect, parent=None):
        if not rect.collidepoint(cls.mousepos) or not (parent == None or parent["absrect"].collidepoint(cls.mousepos)) or not cls.mousepressed[0]: return False
        if not cls.place_top and parent:
            for el in parent["topelements"]:
                if el["absrect"].collidepoint(cls.mousepos): return False
        return True
    
    @classmethod
    def was_clicking(cls, id):
        return id in cls.memory and cls.memory[id]["pressed"]
    
    @classmethod
    def was_selected(cls, id):
        return id in cls.memory and cls.memory[id]["selected"]
