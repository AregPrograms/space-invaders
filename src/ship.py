import threading
import pygame
from bullet import Bullet
from entity import Entity
import assets

class Ship(Entity):
    def fire(self):
        start = pygame.math.Vector2(self.rect.center)

        SPEED = 5

        # ---

        mouse = pygame.mouse.get_pos()

        distance = mouse - start

        position = pygame.math.Vector2(start) # duplicate # start position in start of canon
        #position = pygame.math.Vector2(end)   # duplicate # start position in end of canon

        speed = distance.normalize() * SPEED
        
        b = Bullet(self.rect.centerx, self.rect.centery, 16, 16, pygame.Surface((16, 16)), 1)
        
        assets.audio["shoot"].play()
        
        b.velocity = speed
        
        b.attack_damage = 5
        
        b.iterations = 0
        
        return b