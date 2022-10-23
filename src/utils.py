import json
from math import ceil
import math
from typing import Dict, Iterable, Tuple
import pygame
import assets

pygame.init()

class methods:
    @staticmethod
    def clamp(n, smallest, largest): 
        return max(smallest, min(n, largest))
    
    @staticmethod
    def change_volume(value: float, write: bool = True):
        """Change the volume of the game's audio, and adjust `settings.json`

        Args:
            value (float): The desired volume from 0 - 10

        Returns:
            None
        """
        
        assets.volume = methods.clamp(value, 0, 10)
                    
        for key in assets.audio.keys(): 
            assets.audio[key].set_volume(assets.volume/10)
            
        
        if write:
            with open("resources/settings.json", "r+") as f:
                settings = json.load(f)
                
                settings["volume"] = assets.volume
                
                f.seek(0)
                f.truncate(0)
                
                f.write(json.dumps(settings))
    
    @staticmethod
    # stole this from stackoverflow :troll:
    def rect_distance(rect1, rect2):
        x1, y1 = rect1.topleft
        x1b, y1b = rect1.bottomright
        x2, y2 = rect2.topleft
        x2b, y2b = rect2.bottomright
        left = x2b < x1
        right = x1b < x2
        top = y2b < y1
        bottom = y1b < y2
        if bottom and left:
            return math.hypot(x2b-x1, y2-y1b)
        elif left and top:
            return math.hypot(x2b-x1, y2b-y1)
        elif top and right:
            return math.hypot(x2-x1b, y2b-y1)
        elif right and bottom:
            return math.hypot(x2-x1b, y2-y1b)
        elif left:
            return x1 - x2b
        elif right:
            return x2 - x1b
        elif top:
            return y1 - y2b
        elif bottom:
            return y2 - y1b
        else:  # rectangles intersect
            return 0.

class Notification:
    def __init__(self, title: str, text: Iterable[str], visible_frames: int = 480):
        # initialize fonts
        
        title_font = pygame.font.Font("resources/press_start.ttf", 24)
        text_font = pygame.font.Font("resources/press_start.ttf", 16)
        
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
                self.hide()
                
                
        if self.__state == "hiding":
            self.__vel += 0.4
            self.position.y -= self.__vel
            
            if self.position.y <= -self.surface.get_height():
                self.__state = "hidden"
                self.vel = 0.1
                
class SpriteSheet:
    """A spritesheet is an image with other images nested inside. Use this to extract the images from the spritesheet"""

    def __init__(self, fileName: str) -> None:
        self.image = pygame.image.load(fileName).convert_alpha()

    def extract(self, x: int, y: int, width: int, height: int, bgcolor: Tuple[int, int, int] = None, size: Tuple[int, int] = None) -> pygame.Surface:
        """Extract an image from the spritesheet"""
        # create an empty black surface

        image = pygame.Surface((width, height)).convert_alpha()

        # if background color is specified, set the surface background to that color

        if bgcolor:
            image.fill(bgcolor)
        else:
            image.set_colorkey((0, 0, 0))

        # place a cropped image of the spritesheet onto the surface

        image.blit(self.image, (0, 0), (x, y, width, height))

        # if a size is specified, scale it up to that size

        if size:
            image = pygame.transform.scale(image, (size[0], size[1]))

            # set color key to black if no bgcolor specified

            if not bgcolor:
                image.set_colorkey((0, 0, 0))

        return image

    def extractFromDicts(self, items: Iterable[Dict]) -> Iterable[pygame.Surface]:
        """Extract images from a list of dictionaries formatted as {x: int, y: int, width: int, height: int}"""
        output = []

        # iterable should contain dictionaries with keys: x, y, width, height

        for item in items:
            # extract the image by using the x, y, width, height values of the dictionary "item"

            obj = self.extract(items[item]["x"], items[item]["y"],
                               items[item]["width"], items[item]["height"])

            output.append(obj)

        return output

    def tile(self, spriteSize: Tuple[int, int]) -> Iterable[pygame.Surface]:
        output = []

        for y in range(ceil(self.image.get_height()/spriteSize[1])):
            for x in range(ceil(self.image.get_width()/spriteSize[0])):
                output.append(self.extract(
                    x*spriteSize[0], y*spriteSize[1], spriteSize[0], spriteSize[1]))

        return output


class Animation:
    def __init__(self, sprites: Iterable[pygame.Surface], fps: int = 10) -> None:
        self.sprites = sprites
        self.fps = fps

        self.sprite = sprites[0].convert_alpha()
        self.spriteIndex = 0
        self.framesSkipped = 0
        self.spriteAmount = len(sprites)

    def update(self, windowFramerate=0) -> pygame.Surface:
        """Go to the next frame in the animation"""
        self.framesSkipped += 1
        if windowFramerate > 0:
            # making animation always a certain FPS, even if the framerate is low
            if self.framesSkipped >= windowFramerate/self.fps:  # divide the desired fps by the current fps to get how many frames skipped, then if the current amount of frames skipped is over or equal to the desired amount, go onto the next frame of the animation
                self.framesSkipped = 0

                if self.spriteIndex != self.spriteAmount - 1:
                    self.spriteIndex += 1  # check if the current sprite is not the last sprite in animation
                else:
                    self.spriteIndex = 0  # current sprite is last sprite, so return back to the first sprite

                # set the current animation sprite
                self.sprite = self.sprites[self.spriteIndex].convert_alpha()
        else:
            self.framesSkipped = 0
            if self.spriteIndex != self.spriteAmount - 1:
                self.spriteIndex += 1  # check if the current sprite is not the last sprite in animation
            else:
                self.spriteIndex = 0  # current sprite is last sprite

            self.sprite = self.sprites[self.spriteIndex].convert_alpha()

        return self.sprite

    def reset(self) -> None:
        """Reset the animation back to frame zero."""
        self.framesSkipped = 0
        self.spriteIndex = 0
        self.sprite = self.sprites[0].convert_alpha()
