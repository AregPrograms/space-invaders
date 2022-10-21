import pygame
from ship import Ship

class Game:
  def __init__(self, display: pygame.Surface):
    self.__display_surf = display

    self.ship = Ship(self.__display_surface)
