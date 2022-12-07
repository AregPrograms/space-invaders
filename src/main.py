import json
import pygame
from ship import Ship
from enemy import Enemy
from game import Game
import assets
import config
from menus import MainMenu, Settings
from utils import Notification, SpriteSheet, methods
from pypresence import Presence

def main(): 
    # PYPRESENSE
    
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

    if (config.PYPRESENCE_OK):
        config.RPC.update(state="Vibing in the Menu", large_image="logo", large_text="Space Invaders", start=config.START_UNIX_TIME)
    
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
            if (config.PYPRESENCE_OK):
                config.RPC.update(state="Fighting Enemies", large_image="logo", large_text="Space Invaders", details="Level 1", start=config.START_UNIX_TIME, buttons=[{"label": "Join the fun", "url": "https://github.com/AregPrograms/space-invaders/releases/0.0.1"}])
        elif selection == "Settings":
            menu = SETTINGS
            if (config.PYPRESCENCE_OK):
                config.RPC.update(state="Configuring Settings", large_image="logo", large_text="Space Invaders", start=config.START_UNIX_TIME)
        elif selection == "Back":
            menu = MAIN_MENU
            if (config.PYPRESENCE_OK):
                config.RPC.update(state="Vibing in the Menu", large_image="logo", large_text="Space Invaders", start=config.START_UNIX_TIME)
         
        menu.update()
        menu.draw()
        
        pygame.display.update()
                
        

if __name__ == "__main__":
    main()
