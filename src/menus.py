from math import cos
import time
import pygame
import assets

def clamp(n, smallest, largest): 
    return max(smallest, min(n, largest))

def blitRotate(surf, image, pos, originPos, angle): # took from https://stackoverflow.com/questions/4183208/how-do-i-rotate-an-image-around-its-center-using-pygame, dont judge, just a programmer, its natural at this point

    # offset from pivot to center
    image_rect = image.get_rect(topleft = (pos[0] - originPos[0], pos[1]-originPos[1]))
    offset_center_to_pivot = pygame.math.Vector2(pos) - image_rect.center
    
    # roatated offset from pivot to center
    rotated_offset = offset_center_to_pivot.rotate(-angle)

    # roatetd image center
    rotated_image_center = (pos[0] - rotated_offset.x, pos[1] - rotated_offset.y)

    # get a rotated image
    rotated_image = pygame.transform.rotate(image, angle)
    rotated_image_rect = rotated_image.get_rect(center = rotated_image_center)

    # rotate and blit the image
    surf.blit(rotated_image, rotated_image_rect)


class MainMenu:
    
    
    def __init__(self, display: pygame.Surface):
        self.display_surf = display
        self.surface = pygame.Surface(display.get_size())
        
        self.surface.set_colorkey((0, 0, 0))
        
        self.selected = 0
        self.max_selection = 3
        
                
        self.options = [
            "Play",
            "Settings",
            "Help",
            "About"
        ]

        self.title_vector = pygame.Vector2(30, 50)
        
    def __draw_title(self):
        title_font = pygame.font.Font("resources/press_start.ttf", 56) # load the title font
        
        # move title
        
        self.title_vector.y += cos(time.perf_counter())/5
        self.title_vector.x += cos(time.perf_counter()+0.5)/5
        

        # display word "SPACE"

        space_text = title_font.render("SPACE", False, (255, 255, 255))
        space_text_background = title_font.render("SPACE", False, (50, 50, 50))

        # draw to surface

        self.surface.blit(space_text_background, (self.title_vector.x-5, self.title_vector.y+5))
        
        self.surface.blit(space_text, (self.title_vector.x, self.title_vector.y))
        
        # display word "INVADERS"

        invaders_text = title_font.render("INVADERS", False, (255, 255, 255))
        invaders_text_background = title_font.render("INVADERS", False, (50, 50, 50))

        # draw to surface

        self.surface.blit(invaders_text_background, (self.title_vector.x-5, self.title_vector.y+invaders_text.get_height()+15))
        self.surface.blit(invaders_text, (self.title_vector.x, self.title_vector.y+invaders_text.get_height()+10))

        # display image beside title
        
        blitRotate(self.surface, pygame.transform.scale(assets.images["ship"], (50, 50)), (self.title_vector.x + space_text.get_width()+50, self.title_vector.y+15), (25, 25), cos(time.perf_counter()+0.5)*50)
        
    def __draw_log(self):
        # draw rectangle
        
        pygame.draw.rect(self.surface, (255, 255, 255), (20, 200, 175, 275), border_radius=7)
        pygame.draw.rect(self.surface, (30, 30, 30), (25, 205, 165, 265), border_radius=7)
        
        # draw title text
        
        title_font = pygame.font.Font("resources/press_start.ttf", 24)
        log_text = title_font.render("-LOG-", True, (255, 255, 255))
        log_text_bg = title_font.render("-LOG-", True, (50, 50, 50))
        
        self.surface.blit(log_text_bg, (23+((165/2)-log_text.get_width()/2),233))
        self.surface.blit(log_text, (25+((165/2)-log_text.get_width()/2),230))
        
        # draw log info
        
        text = [
            "0.0.0",
            "this is an",
            "unreleased",
            "version for",
            "custom space",
            "invaders!"
        ]
        
        text_font = pygame.font.Font("resources/press_start.ttf", 10)
        
        text_y = 250
        
        for line in text:
            rendered_line = text_font.render(line, True, (255, 255, 255))
            rendered_line_bg = text_font.render(line, True, (50, 50, 50))
            
            text_y += rendered_line.get_height()+15
            
            self.surface.blit(rendered_line_bg, (23+((165/2)-rendered_line.get_width()/2),text_y+1))
            self.surface.blit(rendered_line, (25+((165/2)-rendered_line.get_width()/2),text_y))
            
    def __draw_buttons(self):
        btn_font = pygame.font.Font("resources/press_start.ttf", 25)
        
        for i in range(len(self.options)):
            text = None
            if i == self.selected:
                text = btn_font.render(f"> {self.options[i]}", False, (0, 150, 150))
                pygame.draw.rect(self.surface, (20,20,20), (225-13, 200+(i*(text.get_height()+10))-5, text.get_width()+26, text.get_height()+10), border_radius=15)
            else:
                text = btn_font.render(f"  {self.options[i]}", False, (255, 255, 255))
                
            self.surface.blit(text, (225, 200+(i*(text.get_height()+10))))

    def update(self):
        #self.surface.blit(pygame.image.load("resources/images/bg.png"), (0, 0))
        self.surface.fill((0, 0, 0))
        
        self.__draw_title()
        self.__draw_log()
        self.__draw_buttons()
        
    def input(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            if event.key == 1073741906 or event.key == 119:
                self.selected -= 1
                self.selected = self.max_selection if self.selected <= -1 else self.selected
                
                assets.audio["select"].play()
            if event.key == 1073741905 or event.key == 115:
                self.selected += 1
                self.selected = 0 if self.selected >= self.max_selection+1 else self.selected
                
                assets.audio["select"].play()
                
            if event.key == 13:
                selected = self.options[self.selected]
                
                if selected == "Play":
                    assets.audio["start"].play()
                    
                if selected == "Help":
                    assets.audio["unavailable"].play()
                    
                if selected == "About":
                    assets.audio["unavailable"].play()
                
                return self.options[self.selected]
        
    def draw(self):
        self.display_surf.blit(self.surface, (0, 0))
        
class Settings:
    def __init__(self, display: pygame.Surface):
        self.display_surf = display
        self.surface = pygame.Surface(display.get_size())
        self.surface.set_colorkey((0, 0, 0))
        
        self.options = [
            ["Decrease Volume", "Increase Volume"],
            ["Back", "Other?"]
        ]

        self.__option_x = 0
        self.__option_y = 0
        
        self.title_vector = pygame.Vector2((30, 30))
        
    def __draw_title(self):
        title_font = pygame.font.Font("resources/press_start.ttf", 56) # load the title font
        
        # move title
        
        #self.title_vector.y += cos(time.perf_counter())/5
        self.title_vector.x += cos(time.perf_counter()+0.5)/5
        

        # display word "SETTINGS"


        settings_text = title_font.render("SETTINGS", False, (255, 255, 255))
        settings_text_background = title_font.render("SETTINGS", False, (50, 50, 50))

        # draw to surface

        self.surface.blit(pygame.transform.rotate(settings_text_background, cos(self.title_vector.x/15)*2), (self.title_vector.x-5, self.title_vector.y+5))
        self.surface.blit(pygame.transform.rotate(settings_text, cos(self.title_vector.x/15)*2), (self.title_vector.x, self.title_vector.y))
        
    def __draw_options(self):
        self.text_font = pygame.font.Font("resources/press_start.ttf", 24)
        
        volume_up = pygame.transform.flip(pygame.transform.scale(assets.images["volume_up"].copy(), (64, 64)), True, True)
        volume_down = pygame.transform.scale(assets.images["volume_down"].copy(), (64, 64))
        
        self.surface.blit(volume_up, (386, 200))
        self.surface.blit(volume_down, (50, 200))
        
        back_btn_text = self.text_font.render("Back", True, (255, 255, 255))
        other_btn_text = self.text_font.render("Other?", True, (255, 255, 255))
        
        self.surface.blit(back_btn_text, (50, 350))
        self.surface.blit(other_btn_text, (300, 350))
        
        pygame.draw.rect(self.surface, (255, 255, 255), (60, 270, 70, 10), 5) if self.options[self.__option_y][self.__option_x] == "Decrease Volume" else None
        pygame.draw.rect(self.surface, (255, 255, 255), (374, 270, 86, 10), 5)if self.options[self.__option_y][self.__option_x] == "Increase Volume" else None 
        pygame.draw.rect(self.surface, (255, 255, 255), (50, 382, back_btn_text.get_width(), 10), 5)if self.options[self.__option_y][self.__option_x] == "Back" else None 
        pygame.draw.rect(self.surface, (255, 255, 255), (300, 382, other_btn_text.get_width(), 10), 5) if self.options[self.__option_y][self.__option_x] == "Other?" else None
        
    def update(self):
        self.surface.fill((0, 0, 0))
        self.__draw_title()
        self.__draw_options()
        
    def input(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            # w: 119, 1073741906
            # a: 97, 1073741904
            # s: 115, 1073741905
            # d: 100, 1073741903

            if event.key == 119 or event.key == 1073741906: # up
                if self.__option_y > 0:
                    self.__option_y -= 1
                    
                    assets.audio["select"].play()

                if not self.__option_x < len(self.options[self.__option_y]):
                    self.__option_x = len(self.options[self.__option_y])-1

            if event.key == 115 or event.key == 1073741905: # down
                if self.__option_y < len(self.options)-1:
                    self.__option_y += 1
                    
                    assets.audio["select"].play()

                if not self.__option_x < len(self.options[self.__option_y]):
                    self.__option_x = len(self.options[self.__option_y])-1
                    
            if event.key == 97 or event.key == 1073741904: # left
                if self.__option_x > 0:
                    self.__option_x -= 1
                    
                    assets.audio["select"].play()
            
            if event.key == 100 or event.key == 1073741903: # right
                if self.__option_x < len(self.options[self.__option_y])-1:
                    self.__option_x += 1
                    
                    assets.audio["select"].play()
                    
            if event.key == 13: # enter
                option = self.options[self.__option_y][self.__option_x]
                
                if option == "Decrease Volume":
                    assets.volume = clamp(assets.volume-1, 0, 10)
                    
                    for key in assets.audio.keys():
                        assets.audio[key].set_volume(assets.volume/10)
                        
                if option == "Increase Volume":
                    
                    assets.volume = clamp(assets.volume+1, 0, 10)
                    
                    for key in assets.audio.keys(): 
                        assets.audio[key].set_volume(assets.volume/10)
                        
                if option == "Other?":
                    assets.audio["unavailable"].play()
                        
                if option == "Back":
                    return "Back"
                
          

    def draw(self):
        self.display_surf.blit(self.surface, (0, 0))
