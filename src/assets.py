import pygame

pygame.mixer.init()
pygame.font.init()

volume = 10 # maximum 10

# pre-load all the assets

audio: dict = {
    "main_menu": pygame.mixer.Sound("resources/music/main_menu_josefpres.wav"),
    
    # SFX
    
    "start": pygame.mixer.Sound("resources/sfx/start.wav"),
    "select": pygame.mixer.Sound("resources/sfx/select.wav"),
    "damage": pygame.mixer.Sound("resources/sfx/damage.wav"),
    "destroy": pygame.mixer.Sound("resources/sfx/destroy.wav"),
    "powerup": pygame.mixer.Sound("resources/sfx/powerup.wav"),
    "shoot": pygame.mixer.Sound("resources/sfx/shoot.wav"),
    "unavailable": pygame.mixer.Sound("resources/sfx/unavailable.wav")
}

images: dict = {
    "ship": pygame.image.load("resources/gfx/ship.png"),
    "volume_up": pygame.image.load("resources/gfx/volume-up.png"),
    "volume_down": pygame.image.load("resources/gfx/volume-down.png")
}

audio["unavailable"].set_volume(2)