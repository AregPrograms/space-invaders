import pygame

pygame.mixer.init()
pygame.font.init()

audio: dict = {
    "main_menu": pygame.mixer.Sound("resources/music/main_menu_josefpres.wav"),
    
    # SFX
    
    "start": pygame.mixer.Sound("resources/sfx/start.wav"),
    "select": pygame.mixer.Sound("resources/sfx/select.wav"),
    "damage": pygame.mixer.Sound("resources/sfx/damage.wav"),
    "destroy": pygame.mixer.Sound("resources/sfx/destroy.wav"),
    "powerup": pygame.mixer.Sound("resources/sfx/powerup.wav"),
    "shoot": pygame.mixer.Sound("resources/sfx/shoot.wav"),
}

images: dict = {
    "ship": pygame.image.load("resources/images/ship.png")
}