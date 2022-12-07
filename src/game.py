from random import randint
from time import time
import pygame
from enemy import Enemy
from entity import Entity
from ship import Ship
import assets
from math import atan2, pi
import config
from utils import Notification, methods

class Game:
    def __init__(self, display: pygame.Surface):
        self.__display_surf = display
        
        self.visible_sprites = pygame.sprite.Group()
        
        self.surface = pygame.Surface(self.__display_surf.get_size())
        self.surface.set_colorkey((0, 0, 0))
        
        self.enemies = []
        
        self.ship = Ship((self.surface.get_width()/2) - 32, (self.surface.get_height()/2) - 32, 64, 64, assets.images["ship"])
        self.visible_sprites.add(self.ship)
        
        self.frames = 0

        self.max_enemies = 10
        self.enemies_killed = 0
        
        self.level = 1
        
        self.bullets = []
        self.current_notification = Notification(f"Level {self.level}", ["Maximum Enemies:", str(self.max_enemies)], 120)
        self.current_notification.show()
        
    def draw(self):
        self.visible_sprites.draw(self.__display_surf)
        self.__display_surf.blit(self.surface, (0, 0))
        
        if self.current_notification:
            self.current_notification.draw(self.__display_surf)
    
    def __draw_health_bar(self):
        font = pygame.font.Font("resources/press_start.ttf", 16)
        text = font.render("HEALTH", False, (255, 255, 255))
        
        position = pygame.Vector2(15, 15)
        
        pygame.draw.rect(self.surface, (50, 50, 50), (position.x, position.y, text.get_width()+10, text.get_height()+10), border_radius=5)
        
        pygame.draw.rect(self.surface, (50, 50, 50), (position.x, position.y+text.get_height()+4, 160, 25), border_radius=5)
        
        self.surface.blit(text, (position.x+5, position.y+7))
        
        
        
        pygame.draw.rect(self.surface, (200, 0, 0), (position.x+5, position.y+text.get_height()+9, 150, 15), border_radius=5)
        pygame.draw.rect(self.surface, (0, 200, 0), (position.x+5, position.y+text.get_height()+9, methods.clamp(150*(self.ship.health/self.ship.max_health), 0, 150), 15), border_radius=5)
        
    def __draw_enemy_counter(self):
        font_large = pygame.font.Font("resources/press_start.ttf", 16)
        font_small = pygame.font.Font("resources/press_start.ttf", 10)
        enemy_text = font_large.render(str(self.enemies_killed), False, (255, 255, 255))
        max_enemy_text = font_small.render(f"/{self.max_enemies}", False, (255, 255, 255))
        
        position = pygame.Vector2(15, 470)
        
        pygame.draw.rect(self.surface, (50, 50, 50), (position.x, position.y, enemy_text.get_width()+max_enemy_text.get_width()+10, enemy_text.get_height()+10), border_radius=5)
        self.surface.blit(enemy_text, (position.x+5, position.y+5))
        self.surface.blit(max_enemy_text, (position.x+enemy_text.get_width()+5, position.y+enemy_text.get_height()+5-max_enemy_text.get_height()))
        
        
    
    
    def update(self):
        if self.current_notification:
            self.current_notification.update()
        
        self.frames += 1
        key = pygame.key.get_pressed()
        
        # move the player
        
        if key[pygame.K_w]:
            for enemy in self.enemies:
                enemy.rect.y += self.ship.velocity
        if key[pygame.K_a]:
            for enemy in self.enemies:
                enemy.rect.x += self.ship.velocity
        if key[pygame.K_s]:
            for enemy in self.enemies:
                enemy.rect.y -= self.ship.velocity
        if key[pygame.K_d]:
            for enemy in self.enemies:
                enemy.rect.x -= self.ship.velocity
            
        # rotate the player based on mouse position
            
        mouse_x, mouse_y = pygame.mouse.get_pos()
        rel_x, rel_y = mouse_x - self.ship.rect.x, mouse_y - self.ship.rect.y
            
        angle = atan2(rel_y, rel_x)
            
        angle = (180 / pi) * -atan2(rel_y, rel_x) - 90
            
        self.ship.image = pygame.transform.rotate(pygame.transform.scale(assets.images["ship"], (64, 64)), int(angle))
        self.ship.rect = self.ship.image.get_rect(center=self.ship.rect.center)
        
        # spawn enemy
        
        if self.frames%config.ENEMY_SPAWN_RATE==0:
            if self.enemies_killed < self.max_enemies:
                pos = pygame.Vector2(randint(0, self.__display_surf.get_width()), randint(0, self.__display_surf.get_height()))
                
                no_spawn_rect = self.ship.rect.copy()
                no_spawn_rect.inflate(110, 80)
                
                while pygame.rect.Rect(pos.x, pos.y, 55, 40).colliderect(no_spawn_rect):
                    pos = pygame.Vector2(randint(0, self.__display_surf.get_width()), randint(0, self.__display_surf.get_height()))
                    
                enemy = Enemy(pos.x, pos.y, 55, 40, assets.images["enemy-frame-1"], 1, [self.ship])
                enemy.image.set_colorkey((0, 0, 0))
                self.visible_sprites.add(enemy)
                self.enemies.append(enemy)
                
                enemy.attack_damage += self.level
                enemy.health += self.level
            else:
                self.enemies_killed = 0
                self.max_enemies *= 1.5
                self.max_enemies = int(self.max_enemies)
                
                self.level += 1
                
                self.current_notification = Notification(f"Level {self.level}", ["Maximum Enemies:", str(self.max_enemies)], 120)
                self.current_notification.show()
                
                config.ENEMY_SPAWN_RATE -= 4
                config.ENEMY_SPAWN_RATE = methods.clamp(config.ENEMY_SPAWN_RATE, 30, 160)
                
                if (PYPRESENCE_OK):
                    config.RPC.update(state="Fighting Enemies", large_image="logo", large_text="Space Invaders", details=f"Level {self.level}", start=config.START_UNIX_TIME, buttons=[{"label": "Join the fun", "url": "https://github.com/AregPrograms/space-invaders/releases/0.0.1"}])
                
                print(self.max_enemies)
        
        # refresh display
        
        for b_index, bullet in enumerate(self.bullets):
            bullet.rect.x += bullet.velocity.x*5
            bullet.rect.y += bullet.velocity.y*5
            
            bullet.iterations += 1
            
            if bullet.iterations > 500:
                self.visible_sprites.remove(bullet)
                del self.bullets[b_index]
                
                continue
            
            for enemy in self.enemies:
                if bullet.rect.colliderect(enemy.rect):
                    enemy.health -= bullet.attack_damage
                    
                    self.visible_sprites.remove(bullet)
                    del self.bullets[b_index]
                    
                    assets.audio["damage"].play()
                    break
        
        self.visible_sprites.update()
        self.surface.fill((0, 0, 0))
        
        for i, text in enumerate(self.ship.visible_text):
            self.surface.blit(text, (self.ship.rect.x, self.ship.rect.y-(i*text.get_height())))
            
        for enemy_index, enemy in enumerate(self.enemies):
            for j, text in enumerate(enemy.visible_text):
                self.surface.blit(text, (enemy.rect.x, enemy.rect.y-(j*text.get_height())))
                
            if enemy.health <= 0:
                self.enemies_killed += 1
                self.visible_sprites.remove(enemy)
                del self.enemies[enemy_index]
        
        self.__draw_health_bar()
        self.__draw_enemy_counter()
        
        self.ship.health = methods.clamp(self.ship.health+0.01, 0, 100)
    
    def input(self, e: pygame.event.Event):
        if e.type == pygame.MOUSEBUTTONDOWN:
            bullet = self.ship.fire()
            self.visible_sprites.add(bullet)
            self.bullets.append(bullet)
