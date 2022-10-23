from time import sleep
import pygame
import threading

class Entity(pygame.sprite.Sprite):
    def __init__(self, x: float, y: float, 
                 width: float, height: float, 
                 surface: pygame.Surface, max_health: int = 100):
        
        super().__init__()
        

        self.image = pygame.transform.scale(surface, (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        self.health = max_health
        self.max_health = max_health
        
        
        self.visible_text = []
        
        self.damage_font = pygame.font.Font("resources/press_start.ttf", 10)
        
        self.velocity = 5
        
    def update(self):
        if self.health <= 0:
            del self
            
    def handle_text(self, text):
        
        self.visible_text.append(text)
        sleep(1)
        del self.visible_text[0]
            
    def damage(self, damage: int):
        self.health -= damage

        damage_text = self.damage_font.render(f"-{damage}", False, (255, 0, 0))
        damage_text.set_alpha(128)
        
        threading.Thread(target=self.handle_text, args=[damage_text], daemon=True).start()
        
        