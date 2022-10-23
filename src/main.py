import json
import pygame
from ship import Ship
from enemy import Enemy
from game import Game
import assets
import config
from menus import MainMenu, Settings
from utils import Notification, SpriteSheet, methods

def main(): 
    # Initialize Constants
    
    WINDOW_RESOLUTION = (500, 500)
    
    # Initialize Window
    
    screen = pygame.display.set_mode(WINDOW_RESOLUTION)
    pygame.display.set_caption("Space Invaders")
    pygame.display.set_icon(assets.images["ship"])
    
    # Initialize Variables
    
    clock = pygame.time.Clock()
    
    MAIN_MENU = MainMenu(screen)
    SETTINGS = Settings(screen)
    GAME = Game(screen)
    
    menu = MAIN_MENU
    
    selection = None
    
    running: bool = True
    
    assets.audio["main_menu"].play(-1)
    
    notification = Notification("Hi!", ["hello"], 60)
    
    notification.show()
    
    enemy_atlas = SpriteSheet("resources/gfx/enemy-atlas.png")
    enemy_atlas = enemy_atlas.extractFromDicts({
        "frame-1":
        {
            "x": 0,
            "y": 0,
            "width": 11,
            "height": 8
        },
        "frame-2":
        {
            "x": 11,
            "y": 0,
            "width": 11,
            "height": 8
        }
    })
    
    assets.images["enemy-frame-1"] = enemy_atlas[0]
    assets.images["enemy-frame-2"] = enemy_atlas[1]
    
    # load settings
    
    with open("resources/settings.json", "r") as f:
        settings = json.load(f)
        
        methods.change_volume(settings["volume"], False)
    
    
    while running:
        clock.tick(config.FRAMERATE)
        for event in pygame.event.get():
            selection = menu.input(event)
            if event.type == pygame.QUIT:
                running = False
                
        screen.blit(pygame.image.load("resources/gfx/bg.png"), (0, 0))
        
        
        if selection == "Play":
            assets.audio["main_menu"].stop()
            menu = GAME
        elif selection == "Settings":
            menu = SETTINGS
        elif selection == "Back":
            menu = MAIN_MENU
         
        menu.update()   
        menu.draw()
        
        notification.update()
        notification.draw(screen)
        
        pygame.display.update()
                
        

if __name__ == "__main__":
    main()
