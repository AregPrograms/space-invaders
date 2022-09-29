import pygame
from ship import Ship
from enemy import Enemy
import assets
from menus import MainMenu

def main(): 
    # Initialize Constants
    
    WINDOW_RESOLUTION = (500, 500)
    
    # Initialize Window
    
    screen = pygame.display.set_mode(WINDOW_RESOLUTION)
    pygame.display.set_caption("Space Invaders")
    pygame.display.set_icon(assets.images["ship"])
    
    # Initialize Variables
    
    clock = pygame.time.Clock()
    
    menu = MainMenu(screen)
    
    selection = None
    
    running: bool = True
    
    assets.audio["main_menu"].play(-1)
    
    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if not selection == "Play": selection = menu.input(event)
            if event.type == pygame.QUIT:
                running = False
                
        screen.blit(pygame.image.load("resources/images/bg.png"), (0, 0))
        
        if not selection == "Play":
            menu.update()
            menu.draw()
        elif not selection == "Settings":
            menu.update()
            menu.draw()
        elif not selection == "Help":
            menu.update()
            menu.draw()
        elif not selection == "About":
            menu.update()
            menu.draw()
        else:
            assets.audio["main_menu"].stop()
            
            
        
        pygame.display.update()
                
        

if __name__ == "__main__":
    main()