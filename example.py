import sys, pygame
from damgui import damgui
from damgui import settings

screen = pygame.display.set_mode((1200,800))
clock = pygame.time.Clock()
Stack = damgui.get_stack() # caution, not meant to be used by the user

while True:
    damgui.frame_start()
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        damgui.register_event(e)
    screen.fill("black")
    
    damgui.begin("main_win","Main Window",(50,50),(100,100))
    
    damgui.container("BIG",(500,400))
    
    damgui.selection_list("example_sellst",[f"OPT {i}" for i in range(5)],True,(200,300),False)
    
    if damgui.button("example_btn","Button Text"):
        print("Clicked!")
    
    settings.FONT = settings.FONT_L
    damgui.place_side().label("example_l","Label Text")
    settings.FONT = settings.defaults["FONT"]
    
    damgui.end()
    
    damgui.end()
        
    damgui.frame_end(screen)
    clock.tick(500)
    pygame.display.update()    
        