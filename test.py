import sys, pygame

pygame.init()
screen = pygame.display.set_mode((1200,800))
clock = pygame.time.Clock()

click = False

from damgui import damgui
from damgui import settings

while True:
    damgui.frame_start()
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        damgui.register_event(e)
    screen.fill("black")
    
    damgui.begin("main_win","Main Window",(50,50),(1100,700))
    
    damgui.end()
        
    damgui.frame_end(screen)
    clock.tick(500)
    pygame.display.update()
            
        