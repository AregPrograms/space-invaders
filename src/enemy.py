
import math
from random import randint
from typing import Iterable
import pygame
import assets

from entity import Entity
from utils import methods

class Enemy(Entity):
    def __init__(self, x: float, y: float, width: float, height: float, surface: pygame.Surface, max_health: int = 1, targets: Iterable[Entity] = None):
        super().__init__(x, y, width, height, surface, max_health)
        self.frame = 0
        
        self.current_img = 0
        
        self.targets = targets
        
        self.velocity = 2
        
        self.attack_damage = 3
    
    def update(self):
        super().update()
        
        if self.targets is None:
            if self.frame%3==0:
                self.rect.x += randint(-5,5)
                self.rect.y += randint(-5,5)
        else:
            current_target = [self.targets[0], methods.rect_distance(self.rect, self.targets[0].rect)]
            
            for entity in self.targets:
                distance = methods.rect_distance(self.rect, entity.rect)
                if distance >= current_target[1]:
                    current_target[0] = entity
                    current_target[1] = distance
                
            # Find direction vector (dx, dy) between enemy and player.
            dx, dy = current_target[0].rect.x - self.rect.x, current_target[0].rect.y - self.rect.y
            dist = math.hypot(dx, dy)
            dx, dy = dx / dist, dy / dist  # Normalize.
            # Move along this normalized vector towards the player at current speed.
            self.rect.x += dx * self.velocity
            self.rect.y += dy * self.velocity
            
            if self.rect.colliderect(current_target[0].rect):
                current_target[0].damage(self.attack_damage)
                self.damage( int(self.attack_damage/2) )
                
                self.rect.x -= (dx * self.velocity)*50
                self.rect.y -= (dy * self.velocity)*50
                    
            
        
        # if self.rect.x < 0:
        #     self.rect.x = 0
        # if self.rect.y < 0:
        #     self.rect.y = 0
            
        # if self.rect.y+self.rect.height > pygame.display.get_surface().get_height():
        #     self.rect.y = pygame.display.get_surface().get_height() - self.rect.y+self.rect.height
            
        # if self.rect.x+self.rect.width > pygame.display.get_surface().get_width():
        #     self.rect.x = pygame.display.get_surface().get_width() - self.rect.x+self.rect.width
        
        if self.current_img == 0:
            self.image = pygame.transform.scale(assets.images["enemy-frame-1"], (55, 40))
            self.image.set_colorkey((0, 0, 0))
            
        if self.current_img == 1:
            self.image = pygame.transform.scale(assets.images["enemy-frame-2"], (55, 40))
            self.image.set_colorkey((0, 0, 0))
            
        self.frame += 1
        
        if self.frame%40 == 0:
            if self.current_img == 0: 
                self.current_img = 1
            elif self.current_img == 1:
                self.current_img = 0