import pygame, warnings
pygame.init()
from .stack import Stack as _Stack
from .render import render_all as _render_all
from .base import _render_text,_size_minsize_surf,_base,_relative_rect_pos, _get_basic, _get_pos, _EMPTY_R
from .constants import settings, DamGUIException
from typing import Any, Self

_IntIterable2D = tuple[int,int]|list[int]
class damgui:
    """Easly creates UI elements at runtime"""
    @classmethod
    def begin(cls, id:Any, title:str, pos:_IntIterable2D, min_size:_IntIterable2D, can_drag:bool=True, relative_pos:bool=False)->None:
        """Create a window context or a container depending on the parameters. Must end it with damgui.end()"""
        _Stack.start_check()
        type_ = "window"
        abs = rel = pos
        size = min_size
        if id in _Stack.memory: surf = _Stack.memory[id]["surf"]
        else: surf = pygame.Surface((min_size[0]-settings.MARGIN,min_size[1]-settings.MARGIN),pygame.SRCALPHA)
        surf.fill(0)
        if relative_pos and _Stack.window:
            rel = _Stack.get_rel()
            winpos = _Stack.window["pos"] if _Stack.window else (0,0)
            abs = (rel[0]+winpos[0],rel[1]+winpos[1])
            type_ = "container"
        if id in _Stack.memory and type_ == "window": size = _Stack.memory[id]["size"]
        win = _base(id, type_,True,True,size,abs,rel,pygame.Rect(rel,size),pygame.Rect(abs,size),None,None,title,True,True,True)
        win.update({
            "title":title,
            "pos":abs,
            "can_drag":can_drag,
            "drag_offset":(0,0),
            "minsize":min_size,
            "surf":surf,
        })
        if relative_pos: win["relative"] = True
        if id in _Stack.memory and can_drag:
            win["drag_offset"] = _Stack.memory[id]["drag_offset"]
            win["pos"] = (win["pos"][0]+win["drag_offset"][0],win["pos"][1]+win["drag_offset"][1])
            win["rect"].x += win["drag_offset"][0]; win["rect"].y += win["drag_offset"][1]
            win["absrect"].x += win["drag_offset"][0]; win["absrect"].y += win["drag_offset"][1]
        _Stack.add_window(win)
        if title:
            cls.button(f"{id}_title_bar",title,(surf.get_width()-settings.MARGIN,0),"midleft")
            if cls.last_data()["unhover_press"] and can_drag:
                win["drag_offset"] = (win["drag_offset"][0]+_Stack.mouserel[0],win["drag_offset"][1]+_Stack.mouserel[1])
        
    @staticmethod
    def end()->None:
        """Close the last opened context"""
        _Stack.remove_last()
        
    @staticmethod
    def button(id:Any,text:str, min_size:_IntIterable2D=(0,0), text_pos:str="center", force_size:bool=False)->bool:
        """Create a button element. Return whether the button has been clicked"""
        _Stack.win_check()
        if id in _Stack.memory and (oldel:=_Stack.memory[id])["text"] == text:
            tsurf, size = oldel["tsurf"],oldel["size"]
            if force_size: size = min_size
            if size[0] < min_size[0]: size = (min_size[0],size[1])
            if size[1] < min_size[1]: size = (size[0], min_size[1])
        else: tsurf = _render_text(text); size = _size_minsize_surf(min_size,tsurf,True)
        rel,abs,rect,absrect = _get_basic(size)
        was_clicking = _Stack.was_clicking(id)
        btn = _base( id,"button",True,True,size,abs,rel,rect,absrect,tsurf,_relative_rect_pos(tsurf,rect,text_pos),text)
        _Stack.add_element(btn)
        return btn["pressed"] and not was_clicking
    
    @staticmethod
    def select_button(id:Any,text:str,min_size:_IntIterable2D=(0,0), text_pos:str="center",force_size:bool=False)->bool:
        """A button element that once pressed stays like so until it's pressed again. Return whether it's in the pressed state"""
        _Stack.win_check()
        if id in _Stack.memory and (oldel:=_Stack.memory[id])["text"] == text:
            tsurf, size = oldel["tsurf"],oldel["size"]
            if force_size: size = min_size
            if size[0] < min_size[0]: size = (min_size[0],size[1])
            if size[1] < min_size[1]: size = (size[0], min_size[1])
        else:
            tsurf = _render_text(text); size = _size_minsize_surf(min_size,tsurf,True)
        rel,abs,rect,absrect = _get_basic(size)
        btn = _base( id,"select_button",True,True,size,abs,rel,rect,absrect,tsurf,_relative_rect_pos(tsurf,rect,text_pos),text)
        btn["selected"] = _Stack.was_selected(id)
        was_clicking = _Stack.was_clicking(id)
        _Stack.add_element(btn)
        action_true = btn["pressed"] and not was_clicking
        if action_true: btn["selected"] = not btn["selected"]
        return btn["selected"]
    
    @staticmethod
    def checkbox(id:Any, size:_IntIterable2D)->bool:
        """A damgui.select_button with a special UI"""
        _Stack.win_check()
        rel,abs,rect,absrect = _get_basic(size)
        btn = _base( id,"checkbox",True,True,size,abs,rel,rect,absrect,None,None,"")
        btn["selected"] = _Stack.was_selected(id)
        btn["innerrect"] = rect.inflate(-settings.PADDING*2,-settings.PADDING*2)
        was_clicking = _Stack.was_clicking(id)
        _Stack.add_element(btn)
        action_true = btn["pressed"] and not was_clicking
        if action_true: btn["selected"] = not btn["selected"]
        return btn["selected"]
    
    @staticmethod
    def label(id:Any, text:str, min_size:_IntIterable2D=(0,0), text_pos:str="center", force_size:bool=False)->None:
        """A label displaying text"""
        _Stack.win_check()
        if id in _Stack.memory and (oldel:=_Stack.memory[id])["text"] == text:
            tsurf, size = oldel["tsurf"],oldel["size"]
            if force_size: size = min_size
            if size[0] < min_size[0]: size = (min_size[0],size[1])
            if size[1] < min_size[1]: size = (size[0], min_size[1])
        else:
            tsurf = _render_text(text); size = _size_minsize_surf(min_size,tsurf,True)
        rel,abs,rect,absrect = _get_basic(size)
        _Stack.add_element(_base(id,"label",False,False,size,abs,rel,rect,absrect,tsurf,_relative_rect_pos(tsurf,rect,text_pos),text))
        
    @classmethod
    def container(cls,id:Any, size:_IntIterable2D, outline:bool=True)->None:
        """Creates a container context. Must be closed with damgui.end()"""
        _Stack.win_check()
        cls.begin(id,"",(0,0),size,False,True)
        if not outline: _Stack.last_element["outline"] = False
        
    @staticmethod
    def separator(size:_IntIterable2D)->None:
        """Creates empty space of custom size"""
        _Stack.win_check()
        rel,abs = _get_pos()
        _Stack.add_element(_base(None,"separator",False,False,size,abs,rel,pygame.Rect(rel,size),pygame.Rect(abs,size),None,None,""))
        
    @staticmethod
    def line(length:int,thickness:int,separator_height)->None:
        """Creates a line separator of custom size"""
        _Stack.win_check()
        rel,abs = _get_pos()
        rect = pygame.Rect(rel[0],rel[1]+separator_height//2,length,thickness)
        line = _base(None,"line",True,False,(length,separator_height),abs,rel,rect,pygame.Rect(abs,rect.size),None,None,"")
        line["hovering"] = True
        _Stack.add_element(line)
    
    @staticmethod
    def image(id:Any, surface:pygame.Surface):
        """An image with a custom surface"""
        _Stack.win_check()
        size = surface.get_size()
        rel,abs,rect,absrect = _get_basic(size)
        settings.CORNER_RADIUS = 0
        _Stack.add_element(_base(id,"image",False,True,size,abs,rel,rect,absrect,surface,rect,"",True,True,False,True))
        settings.CORNER_RADIUS = settings.defaults["CORNER_RADIUS"]
    
    @classmethod
    def dropdown(cls, id:Any, options:list[str], start_option:str, min_width:int=0, option_height:int = 30)->tuple[str,bool]:
        """A dropdown element. Return a tuple with the currently selected option and whether the options are showing"""
        _Stack.win_check()
        isopen, option = False, start_option
        if id in _Stack.memory:
            isopen = (olddd:=_Stack.memory[id])["isopen"]
            option = olddd["option"]
        if cls.button(f"{id}_option_btn",option): isopen = not isopen
        w = _Stack.last_element["sx"]+settings.MARGIN
        if cls.place_side().button(f"{id}_arrow_btn","▲" if isopen else "▼"): isopen = not isopen
        w += _Stack.last_element["sx"]
        if w < min_width: w = min_width
        toth = option_height*len(options) + settings.MARGIN*(len(options)+1)
        if isopen:
            settings.Y_MARGIN = settings.MARGIN
            cls.ignore_pos().place_above().container(f"{id}_options_cont",(w,toth))
            for i, opt in enumerate(options):
                if cls.button(f"{id}_option_{i}",opt,(w-settings.MARGIN*2,option_height),"center",True): option, isopen = opt, False
            cls.end()
            settings.Y_MARGIN = settings.defaults["Y_MARGIN"]
        dd = _base(id,"dropdown",False,False,(0,0),(0,0),(0,0),_EMPTY_R,_EMPTY_R,None,None,"",True,True,False,False)
        dd["isopen"], dd["option"] = isopen, option
        _Stack.add_element(dd)
        return option, isopen
    
    @classmethod
    def selection_list(cls, id:Any, options:list[str], multiselect:bool=False, size:_IntIterable2D=(0,30), autoheight:bool=True)->str|list[str]:
        """A selection list element. Depending on the multiselect flag return either the selected option or selected options.
        If autoheight is set to True, the y component of size will be used as the element height"""
        _Stack.win_check()
        seloption, seloptions, optionbtns = None, [], []
        if id in _Stack.memory:
            seloption = (oldel:=_Stack.memory[id])["option"]
            seloptions = oldel["options"]
            optionbtns = oldel["optionbtns"]
        orisize = size
        if autoheight: size = (size[0],size[1]*len(options)+settings.Y_MARGIN*2)
        cls.container(f"{id}_options_cont",size)
        settings.OUTLINE_COL = settings.ELEMENT_BG_COL
        settings.CORNER_RADIUS = 0
        for i, opt in enumerate(options):
            if i > 0: settings.Y_MARGIN = 0
            if cls.select_button((optionid:=f"{id}_option_{i}"),opt,(orisize[0]-settings.MARGIN*2,orisize[1]-settings.Y_MARGIN) if autoheight else (size[0],0),"center",False):
                if multiselect:
                    if opt not in seloptions: seloptions.append(opt)
                else:
                    seloption = opt
                    for optionnnid in optionbtns:
                        optionbtn = _Stack.memory[optionnnid]
                        if optionbtn["text"] != opt: optionbtn["selected"] = False
            else:
                if multiselect:
                    if opt in seloptions: seloptions.remove(opt)
                else:
                    if seloption == opt: seloption = None
            if not multiselect:
                if optionid not in optionbtns: optionbtns.append(optionid)
        cls.end()
        settings.Y_MARGIN = settings.defaults["Y_MARGIN"]
        settings.OUTLINE_COL = settings.defaults["OUTLINE_COL"]
        settings.CORNER_RADIUS = settings.defaults["CORNER_RADIUS"]
        sl = _base(id,"selection_list",False,False,(0,0),(0,0),(0,0),_EMPTY_R,_EMPTY_R,None,None,"",False,False,False,False)
        sl["option"], sl["options"], sl["optionbtns"] = seloption, seloptions, optionbtns
        _Stack.add_element(sl)
        return seloption if not multiselect else seloptions
    
    @staticmethod
    def frame_start()->None:
        """Reset the stack to prepare for a new frame. Call before the event loop"""
        _Stack.events, _Stack.windows, _Stack.window_history = [],[],[]
        _Stack.window = _Stack.last_element = None
        _Stack.mousepos,_Stack.mouserel = pygame.mouse.get_pos(), pygame.mouse.get_rel()
        _Stack.mousepressed, _Stack.keypressed = pygame.mouse.get_pressed(), pygame.key.get_pressed()
        _Stack.start_called = True
        
    @staticmethod
    def register_event(event:pygame.event.Event)->None:
        """Register a pygame event to be used by elements. Call after damgui.frame_start()"""
        _Stack.start_check()
        _Stack.events.append(event)
        
    @staticmethod
    def frame_end(surface:pygame.Surface)->None:
        """Ends the frame and render everything to a surface"""
        if _Stack.window: raise DamGUIException("All windows must be closed before ending the frame")
        _render_all(surface)
        _Stack.start_called = False
        
    @staticmethod
    def interact_data(id:Any)->dict[str,bool]:
        """Return the interaction data of an element. (hovering, pressed, unhover_press, selected)"""
        data = {
            "hovering":False,
            "pressed":False,
            "unhover_press":False,
            "selected":False,
        }
        if not id in _Stack.memory:
            warnings.warn(f"Interaction data is a default value as no element of id '{id}' exists")
            return data
        element = _Stack.memory[id]
        data["hovering"] = element["hovering"]
        data["pressed"] = element["pressed"]
        data["unhover_press"] = element["unhover_press"]
        data["selected"] = element["selected"]
        return data
    
    @classmethod
    def last_interaction(cls)->dict[str,bool]:
        """Return damgui.interact_data() for the last created element"""
        if _Stack.last_element: return cls.interact_data(_Stack.last_element["id"])
        raise DamGUIException("An element must be created to get its interaction data")
        
    @staticmethod
    def element_data(id:Any)->dict[str,Any]:
        """Return the data in memory of an element. Caution when changing attributes"""
        if id in _Stack.memory: return _Stack.memory[id]
        raise DamGUIException(f"No element exist of id '{id}'")
    
    @staticmethod
    def id_exists(id:Any)->bool:
        """Return whether it exist an element in memory of an id"""
        return id in _Stack.memory
        
    @staticmethod
    def last_data()->dict[str,Any]:
        """Return damgui.element_data() for the last created element"""
        if not _Stack.last_element: raise DamGUIException("An element must be created to get its data")
        return _Stack.last_element
    
    @classmethod
    def place_side(cls)->Self:
        """The next element will be placed side to the previous"""
        _Stack.place_side = True
        return cls
    
    @classmethod
    def custom_pos(cls, position:_IntIterable2D)->Self:
        """The next element will be placed at a custom position"""
        _Stack.custom_pos = position
        return cls
    
    @classmethod
    def ignore_pos(cls)->Self:
        """The next element won't affect other elements position in the current context"""
        _Stack.ignore_pos = True
        return cls
    
    @classmethod
    def place_above(cls)->Self:
        """The next element will be rendered after all other elements in the current context"""
        _Stack.place_top = True
        return cls
    
    @staticmethod
    def get_stack()->_Stack:
        """Return the stack. Caution"""
        return _Stack
