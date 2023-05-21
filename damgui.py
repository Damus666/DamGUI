import pygame, warnings
pygame.init()
from .stack import Stack as _Stack
from .render import render_all as _render_all
from .base import _render_text,_size_minsize_surf,_base,_relative_rect_pos, _get_basic, _get_pos, _EMPTY_R, _ColorValue
from .constants import settings, DamGUIException
from typing import Any, Self

_IntIterable2D = tuple[int,int]|list[int]
settings.init()

class damgui:
    """Easly creates UI elements at runtime"""
    @classmethod
    def begin(cls, id:str, title:str, pos:_IntIterable2D, min_size:_IntIterable2D, can_drag:bool=True, relative_pos:bool=False,auto_size:bool=True,can_scroll:bool=True)->None:
        """Create a window context or a container depending on the parameters. Must end it with damgui.end(). A window will auto-resize based on the content"""
        _Stack.start_check()
        type_ = "window"
        abs = rel = pos
        size = realsize = min_size
        scrolloffset = (0,0)
        if id in _Stack.memory: surf = (oldwin:=_Stack.memory[id])["surf"]; scrolloffset = oldwin["scrolloffset"]; realsize = oldwin["realsize"]
        else: surf = pygame.Surface((min_size[0]-settings.MARGIN,min_size[1]-settings.Y_MARGIN),pygame.SRCALPHA)
        surf.fill(0)
        if relative_pos and _Stack.window:
            rel = _Stack.get_rel()
            winpos = _Stack.window["pos"] if _Stack.window else (0,0)
            abs = (rel[0]+winpos[0],rel[1]+winpos[1])
            type_ = "container"
        if id in _Stack.memory and (type_ == "window" or auto_size): size = _Stack.memory[id]["size"]
        if type_ == "container" and surf.get_size() != size:
            surf = pygame.Surface((size[0]-settings.MARGIN,size[1]-settings.MARGIN),pygame.SRCALPHA)
        win = _base(id, type_,True,True,size,abs,rel,pygame.Rect(rel,size),pygame.Rect(abs,size),None,None,title,True,True,True,scrolloffset=scrolloffset)
        win.update({
            "title":title,
            "pos":abs,
            "can_drag":can_drag,
            "drag_offset":(0,0),
            "minsize":min_size,
            "surf":surf,
            "autosize":auto_size,
            "can_scroll":can_scroll,
            "realsize":realsize,
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
        if can_scroll:
            if win["realsize"][0] > win["size"][0]:
                _scrollbar("horizontal", win, id)
            if win["realsize"][1] > win["size"][1]:
                _scrollbar("vertical", win, id)

    @staticmethod
    def end()->None:
        """Close the last opened context"""
        _Stack.remove_last()
        
    @staticmethod
    def button(id:str, text:str, min_size:_IntIterable2D=(0,0), text_pos:str="center", force_size:bool=False)->bool:
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
        action = btn["pressed"] and (not was_clicking and not _Stack.pressed_last_frame)
        if action: btn["press_allow"] = True
        if not _Stack.mousepressed[0]: btn["press_allow"] = False
        return action
    
    @staticmethod
    def image_button(id:str, surface:pygame.Surface):
        _Stack.win_check()
        surfsize = surface.get_size()
        size = (surfsize[0]+settings.PADDING*2,surfsize[1]+settings.PADDING*2)
        rel,abs,rect,absrect = _get_basic(size)
        was_clicking = _Stack.was_clicking(id)
        btn = _base(id,"image_button",True,True,size,abs,rel,rect,absrect,surface,surface.get_rect(center=rect.center))
        _Stack.add_element(btn)
        action = btn["pressed"] and (not was_clicking and not _Stack.pressed_last_frame)
        if action: btn["press_allow"] = True
        if not _Stack.mousepressed[0]: btn["press_allow"] = False
        return action
    
    @staticmethod
    def select_button(id:str,text:str,min_size:_IntIterable2D=(0,0), text_pos:str="center",force_size:bool=False)->bool:
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
        action_true = btn["pressed"] and (not was_clicking and not _Stack.pressed_last_frame)
        if action_true: btn["selected"] = not btn["selected"]; btn["press_allow"] = True
        if not _Stack.mousepressed[0]: btn["press_allow"] = False
        return btn["selected"]
    
    @staticmethod
    def checkbox(id:str, size:_IntIterable2D)->bool:
        """A damgui.select_button with a special UI"""
        _Stack.win_check()
        rel,abs,rect,absrect = _get_basic(size)
        btn = _base( id,"checkbox",True,True,size,abs,rel,rect,absrect,None,None,"")
        btn["selected"] = _Stack.was_selected(id)
        btn["innerrect"] = rect.inflate(-settings.PADDING*2,-settings.PADDING*2)
        was_clicking = _Stack.was_clicking(id)
        _Stack.add_element(btn)
        action_true = btn["pressed"] and (not was_clicking and not _Stack.pressed_last_frame)
        if action_true: btn["selected"] = not btn["selected"]; btn["press_allow"] = True
        if not _Stack.mousepressed[0]: btn["press_allow"] = False
        return btn["selected"]
    
    @staticmethod
    def progress_bar(id:str, size:_IntIterable2D, max_value:int|float, current_value:int|float, fill_color:_ColorValue="red", fill_direction:str="left-right"):
        """A progress bar element. Can customize the color and the fill direction"""
        _Stack.win_check()
        rel, abs, rect, absrect = _get_basic(size)
        if not fill_direction in ("left-right","right-left","up-down","down-up"): raise DamGUIException("Supported progress bar fill directions are: left-right, right-left, up-down, down-up")
        if "left" in fill_direction:
            cur_size = (current_value*size[0])/max_value
            fill_rect = pygame.Rect(rel,(cur_size,size[1]))
        elif "up" in fill_direction:
            cur_size = (current_value*size[1])/max_value
            fill_rect = pygame.Rect(rel,(size[0],cur_size))
        if fill_direction == "right-left": fill_rect.topright = rect.topright
        if fill_direction == "down-up": fill_rect.bottomright = rect.bottomright
        fill_rect.inflate_ip(-settings.MARGIN*2 if (fill_rect.w-(settings.MARGIN*2) >= 1) else 0,-settings.MARGIN*2  if (fill_rect.h-(settings.MARGIN*2) >= 1) else 0)
        pbar = _base(id, "progress_bar",True,True,size,abs,rel,rect,absrect,None,None,"",False,False)
        pbar["fill_rect"],pbar["fill_color"] = fill_rect,fill_color
        _Stack.add_element(pbar)
    
    @staticmethod
    def label(id:str, text:str, min_size:_IntIterable2D=(0,0), text_pos:str="center", force_size:bool=False)->None:
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
    def container(cls,id:str, size:_IntIterable2D, outline:bool=True, auto_size:bool=False, can_scroll:bool=True)->None:
        """Creates a container context. Must be closed with damgui.end()"""
        _Stack.win_check()
        cls.begin(id,"",(0,0),size,False,True,auto_size,can_scroll)
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
    def image(id:str, surface:pygame.Surface):
        """An image with a custom surface"""
        _Stack.win_check()
        size = surface.get_size()
        rel,abs,rect,absrect = _get_basic(size)
        settings.CORNER_RADIUS = 0
        _Stack.add_element(_base(id,"image",False,True,size,abs,rel,rect,absrect,surface,rect,"",True,True,False,True))
        settings.CORNER_RADIUS = settings.defaults["CORNER_RADIUS"]
        
    @classmethod
    def slideshow(cls,id:str, surfaces:list[pygame.Surface], fancy_arrows:bool=False)->pygame.Surface:
        """Implements 2 buttons to go through a list of images. Return the currently displaying image"""
        if (surfaces_len:=len(surfaces)) <= 0: raise DamGUIException("'surfaces' parameter of damgui.slide_show() must be a non-empty sequence")
        index = 0
        if id in _Stack.memory: index = _Stack.memory[id]["surface_index"]
        if surfaces_len <= index: index = surfaces_len-1
        surface = surfaces[index]
        sizes = surface.get_size()
        cls.container(f"{id}_container",sizes,True,True)
        __cont = _Stack.last_element
        prev = settings.ELEMENT_BG_COL
        settings.ELEMENT_BG_COL = settings.WINDOW_BG_COL
        settings.OUTLINE_ENABLED = False
        if cls.button(f"{id}_left_btn","<" if not fancy_arrows else "◀",(0,sizes[1])):
            if index > 0: index -= 1
        settings.OUTLINE_ENABLED = True
        cls.place_side().image(f"{id}_image",surface)
        settings.OUTLINE_ENABLED = False
        if cls.place_side().button(f"{id}_right_btn",">" if not fancy_arrows else "▶",(0,sizes[1])):
            if index < surfaces_len-1: index += 1
        settings.ELEMENT_BG_COL = prev
        settings.OUTLINE_ENABLED = True
        cls.end()
        rel,abs = _get_pos()
        slideshow = _base(id,"slideshow",False,False,__cont["size"],__cont["abs"],__cont["rel"],_EMPTY_R,_EMPTY_R)
        slideshow["surface_index"] = index
        _Stack.add_element(slideshow)
        return surface
    
    @classmethod
    def dropdown(cls, id:str, options:list[str], start_option:str, min_width:int=0, min_option_height:int = 30, min_btn_size=(0,0))->tuple[str,bool]:
        """A dropdown element. Return a tuple with the currently selected option and whether the options are showing"""
        _Stack.win_check()
        isopen, option = False, start_option
        if id in _Stack.memory:
            isopen = (olddd:=_Stack.memory[id])["isopen"]
            option = olddd["option"]
        if cls.button(f"{id}_option_btn",option,min_btn_size): isopen = not isopen
        __button = _Stack.last_element
        w = _Stack.last_element["sx"]-settings.MARGIN
        option_height = _Stack.last_element["sy"]
        settings.set_previous()
        settings.MARGIN = 0
        if cls.place_side().button(f"{id}_arrow_btn","▲" if isopen else "▼"): isopen = not isopen
        settings.MARGIN = settings.previous["MARGIN"]
        w += _Stack.last_element["sx"]
        if w < min_width: w = min_width
        if option_height < min_option_height: option_height = min_option_height
        toth = option_height*len(options) + settings.MARGIN*(len(options)+1)
        if isopen:
            settings.Y_MARGIN = 0
            cls.ignore_pos().place_above().container(f"{id}_options_cont",(w,toth),True,True)
            settings.OUTLINE_COL = settings.ELEMENT_BG_COL
            settings.CORNER_RADIUS = 0
            for i, opt in enumerate(options):
                if i > 0: settings.Y_MARGIN = settings.MARGIN
                if cls.button(f"{id}_option_{i}",opt,(w-settings.MARGIN,option_height),"center",True): option, isopen = opt, False
            cls.end()
            settings.Y_MARGIN = settings.previous["Y_MARGIN"]
            settings.OUTLINE_COL = settings.previous["OUTLINE_COL"]
            settings.CORNER_RADIUS = settings.previous["CORNER_RADIUS"]
        dd = _base(id,"dropdown",False,False,(w,option_height),__button["abs"],__button["rel"],_EMPTY_R,_EMPTY_R,None,None,"",True,True,False,False)
        dd["isopen"], dd["option"] = isopen, option
        _Stack.add_element(dd)
        return option, isopen
    
    @classmethod
    def selection_list(cls, id:str, options:list[str], multi_select:bool=False, size:_IntIterable2D=(0,30), auto_height:bool=True)->str|list[str]:
        """A selection list element. Depending on the multi_select flag return either the selected option or selected options.
        If auto_height is set to True, the y component of size will be used as the element height"""
        _Stack.win_check()
        seloption, seloptions, optionbtns = None, [], []
        if id in _Stack.memory:
            seloption = (oldel:=_Stack.memory[id])["option"]
            seloptions = oldel["options"]
            optionbtns = oldel["optionbtns"]
        orisize = size
        if auto_height: size = (size[0],size[1]*len(options)+settings.Y_MARGIN*2)
        cls.container(f"{id}_options_cont",size)
        __cont = _Stack.last_element
        settings.set_previous()
        settings.OUTLINE_COL = settings.ELEMENT_BG_COL
        settings.CORNER_RADIUS = 0
        for i, opt in enumerate(options):
            if i > 0: settings.Y_MARGIN = 0
            if cls.select_button((optionid:=f"{id}_option_{i}"),opt,(orisize[0]-settings.MARGIN*2,orisize[1]-settings.Y_MARGIN) if auto_height else (size[0]-settings.MARGIN*2,0),"center",False):
                if multi_select:
                    if opt not in seloptions: seloptions.append(opt)
                else:
                    seloption = opt
                    for optionnnid in optionbtns:
                        optionbtn = _Stack.memory[optionnnid]
                        if optionbtn["text"] != opt: optionbtn["selected"] = False
            else:
                if multi_select:
                    if opt in seloptions: seloptions.remove(opt)
                else:
                    if seloption == opt: seloption = None
            if not multi_select:
                if optionid not in optionbtns: optionbtns.append(optionid)
        cls.end()
        settings.Y_MARGIN = settings.previous["Y_MARGIN"]
        settings.OUTLINE_COL = settings.previous["OUTLINE_COL"]
        settings.CORNER_RADIUS = settings.previous["CORNER_RADIUS"]
        sl = _base(id,"selection_list",False,False,__cont["size"],__cont["abs"],__cont["rel"],_EMPTY_R,_EMPTY_R,None,None,"",False,False,False,False)
        sl["option"], sl["options"], sl["optionbtns"] = seloption, seloptions, optionbtns
        _Stack.add_element(sl)
        return seloption if not multi_select else seloptions
    
    @classmethod
    def slider(cls, id:str, width:int, direction:str="horizontal", thickness:int=15, start_rel:float = 0.5, handle_size:int=30)->float:
        """A slider element. Can be horizontal or vertical and higly customizable. Return a value between 0-1 representing the percentage the handle is on"""
        _Stack.win_check()
        if direction not in ("horizontal","vertical","h","v"): raise DamGUIException("Supported directions for sliders are 'horizontal', 'vertical', 'h', 'v'")
        if direction == "h": direction = "horizontal"
        handle_pos = (start_rel*width)-handle_size//2
        if id in _Stack.memory: handle_pos = _Stack.memory[id]["handle_pos"]
        size = (width,thickness) if direction == "horizontal" else (thickness,width)
        rel, abs, rect, absrect = _get_basic(size,offset:=((handle_size//2,handle_size//2-thickness//2) if direction =="horizontal" else (handle_size//2-thickness//2,handle_size//2)))
        slider = _base(id,"slider",True,True,size,abs,rel,rect,absrect,None,None,"",False,False,True,False,offset)
        _Stack.add_element(slider)
        __prevcr = settings.CORNER_RADIUS
        settings.CORNER_RADIUS = handle_size//2
        cls.custom_pos((rel[0]+handle_pos,rel[1]-handle_size//2+thickness//2) if direction == "horizontal" else (rel[0]-handle_size//2+thickness//2,rel[1]+handle_pos))
        cls.button(f"{id}_handle_btn","",(handle_size,handle_size))
        if _Stack.last_element["unhover_press"]:
            if direction == "horizontal": handle_pos += _Stack.mouserel[0]
            else: handle_pos += _Stack.mouserel[1]
            if handle_pos < -handle_size//2: handle_pos = -handle_size//2
            elif handle_pos > width-handle_size//2: handle_pos = width-handle_size//2
        slider["handle_pos"] = handle_pos
        settings.CORNER_RADIUS = __prevcr
        return (handle_pos+handle_size//2)/width
    
    @classmethod
    def auto_scroll(cls, container_id:str, scroll_amount:float=0.5, direction:str="vertical")->bool:
        """The scrollbar of a selected container will be placed at a chosen percentage. scroll_amount is clamped 0-1. Return whether the new scrollbar position is different"""
        scroll_amount = pygame.math.clamp(scroll_amount,0.0,1.0)
        if direction == "h": direction = "horizontal"
        if direction == "v": direction = "vertical"
        if direction not in ("horizontal","vertical"): raise DamGUIException(f"Can only scroll in either vertical or orizontal directions, not '{direction}'")
        if not container_id in _Stack.memory: raise DamGUIException(f"No container exists of id '{container_id}' to scroll in")
        scrollbar_id = f"{container_id}_scrollbar_{direction}"
        if not scrollbar_id in _Stack.memory:
            warnings.warn(f"The scrollbar of container '{container_id}' with direction '{direction}' does not exist, no scrolling has been applied")
            return False
        scrollbar = _Stack.memory[scrollbar_id]
        previouspos = scrollbar["handle_pos"]
        scrollbar["handle_pos"] = (scrollbar["width"]-scrollbar["handle_size"])*scroll_amount
        return scrollbar["handle_pos"] != previouspos
    
    @staticmethod
    def frame_start()->None:
        """Reset the stack to prepare for a new frame. Call before the event loop"""
        _Stack.events, _Stack.windows, _Stack.window_history = [],[],[]
        _Stack.window = _Stack.last_element = None
        _Stack.mousepos,_Stack.mouserel = pygame.mouse.get_pos(), pygame.mouse.get_rel()
        _Stack.mousepressed, _Stack.keypressed = pygame.mouse.get_pressed(), pygame.key.get_pressed()
        _Stack.start_called = True
        _Stack.element_num = 0
        
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
        _Stack.pressed_last_frame = _Stack.mousepressed[0]
        
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
        """Return the data in memory for the last created element"""
        if not _Stack.last_element: raise DamGUIException("An element must be created to get its data")
        return _Stack.last_element
    
    @classmethod
    def place_side(cls)->Self:
        """The next element will be placed side to the previous"""
        _Stack.place_side = True
        return cls
    
    @classmethod
    def custom_pos(cls, position:_IntIterable2D)->Self:
        """The next element will be placed at a custom position relative to the current context"""
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
    
    @classmethod
    @property
    def stack(cls)->_Stack:
        """The stack. Caution (its not meant to be used by the user)"""
        return _Stack
    
    @classmethod
    @property
    def element_count(cls)->int:
        """How many elements have been created so far in the frame"""
        return _Stack.element_num
    
def _scrollbar(direction, win, id):
    """An internal element to allow scolling on containers"""
    THICNESS = settings.SCROLLBAR_THICKNESS
    id = f"{id}_scrollbar_{direction}"
    handle_pos = 0
    if id in _Stack.memory: handle_pos = _Stack.memory[id]["handle_pos"]
    if direction == "horizontal":
        size = (win["size"][0]-THICNESS-settings.MARGIN*4,THICNESS)
        rel = (settings.MARGIN*2,win["size"][1]-settings.MARGIN-THICNESS)
        width = size[0]
    else:
        size = (THICNESS,win["size"][1]-settings.MARGIN*2)
        rel = (win["size"][0]-settings.MARGIN-THICNESS,settings.MARGIN)
        width = size[1]
    sizetouse,realsizetouse = (win["size"][0],win["realsize"][0]) if direction == "horizontal" else (win["size"][1],win["realsize"][1])
    handle_size = (width*sizetouse)/realsizetouse
    abs = (win["pos"][0]+rel[0],win["pos"][1]+rel[1])
    scov = (handle_pos*realsizetouse)/width
    if direction == "horizontal":
        scrolloffset = (scov,win["scoy"])
        handle_position = (rel[0]+handle_pos,rel[1])
        button_size = (handle_size,THICNESS)
    else:
        scrolloffset = (win["scox"],scov)
        handle_position = (rel[0],rel[1]+handle_pos)
        button_size = (THICNESS,handle_size)
    scrollbar = _base(id,"scrollbar",True,True,size,abs,rel,pygame.Rect(rel,size),pygame.Rect(rel,size),None,None,"",False,False,True)
    damgui.ignore_pos().place_above()
    _Stack.add_element(scrollbar)
    win["scrolloffset"] = scrolloffset
    win["scox"] = scrolloffset[0]
    win["scoy"] = scrolloffset[1]
    damgui.ignore_pos().place_above().custom_pos(handle_position)
    damgui.button(f"{id}_handle","",button_size,force_size=True)
    if _Stack.last_element["unhover_press"]:
        if direction == "horizontal": handle_pos += _Stack.mouserel[0]
        else: handle_pos += _Stack.mouserel[1]
        if handle_pos < 0: handle_pos = 0
        if handle_pos > width-handle_size: handle_pos = width-handle_size
    scrollbar["handle_pos"] = handle_pos
    scrollbar["width"] = width
    scrollbar["handle_size"] = handle_size
