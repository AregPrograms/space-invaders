from typing import Iterable
import pygame

class Notification:
    def __init__(self, title: str, text: Iterable[str], visible_frames: int = 480):
        # initialize fonts
        
        title_font = pygame.font.Font("resources/atari.ttf", 24)
        text_font = pygame.font.Font("resources/atari.ttf", 16)
        
        # create text
        
        self.title_text = title_font.render(title, True, (255, 255, 255))

        self.lines = []
        
        self.__longest_line_width: int = 0
        self.__height = 0
        
        for line in text:
            rendered_text = text_font.render(line, True, (230, 230, 230))
            
            self.lines.append(rendered_text)
            
            self.__longest_line_width = rendered_text.get_width() if rendered_text.get_width() > self.__longest_line_width else self.__longest_line_width
            
            self.__height += rendered_text.get_height()
            
        self.__longest_line_width = self.title_text.get_width() if self.title_text.get_width() > self.__longest_line_width else self.__longest_line_width
        self.__height += self.title_text.get_height()
        
        
        # initialize other settings
        
        self.visible_frames = visible_frames
        self.__frames = 0
        self.__state = "hidden" # can be showing, hidden, or hiding, visible
        
        # make surface
        
        self.surface = pygame.Surface((self.__longest_line_width+50, self.__height+50), pygame.SRCALPHA)
        pygame.draw.rect(self.surface, (50, 50, 50), (0, 0, self.__longest_line_width+50, self.__height+50), border_radius=40)
        pygame.draw.rect(self.surface, (40,40,40), (0, 0, self.__longest_line_width+50, self.__height+50), border_radius=40, width=5)
        
        draw_y = 15
        self.surface.blit(self.title_text, ((self.surface.get_width()/2)-self.title_text.get_width()/2, draw_y))
        draw_y += self.title_text.get_height()+15
        
        pygame.draw.rect(self.surface, (40,40,40), ((self.surface.get_width()/2)-(self.title_text.get_width()+30)/2, 
                                                   draw_y-9, self.title_text.get_width()+30, 5), border_radius=5)
        
        for line in self.lines:
            self.surface.blit(line, ((self.surface.get_width()/2)-line.get_width()/2, draw_y))
            draw_y += line.get_height()
            
        self.position = pygame.Vector2(250-self.surface.get_width()/2, -self.surface.get_height())
        
        self.__vel = 0.1
        
    def draw(self, surface: pygame.Surface):
        surface.blit(self.surface, self.position)
        
    def show(self):
        """Show the notification (make it appear from the top of the screen)
        """
        self.__state = "showing"
        
    def hide(self):
        """Hide the notification (automatically hides after `visible_frames` frames, defined in constructor)
        """
        self.__state = "hiding"
        
    def update(self):
        if self.__state == "showing":
            self.__vel += 0.4
            self.position.y += self.__vel
            
            if self.position.y >= 15:
                self.__frames = 0
                self.__vel = 0.1
                self.__state = "visible"
                self.vel = 0.1
                
        if self.__state == "visible":
            self.__frames += 1
    
            if self.__frames >= self.visible_frames:
                print("hiding")
                self.hide()
                
                
        if self.__state == "hiding":
            self.__vel += 0.4
            self.position.y -= self.__vel
            
            if self.position.y <= -self.surface.get_height():
                self.__state = "hidden"
                self.vel = 0.1