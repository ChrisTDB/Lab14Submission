"""
Alien sprite module.

Author: Christopher Orta
Date: 11/24/2025

Purpose: Provide the `Alien` class used by the fleet. Aliens are `Sprite`
objects that update their positions and render themselves.
"""

import pygame
from pygame.sprite import Sprite
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from alien_fleet import AlienFleet


class Alien(Sprite):
    """Single alien enemy in the fleet.

    Stores references to the fleet and game for access to screen, settings,
    and shared behavior. Handles its own movement and drawing.
    """
    def __init__(self, fleet: 'AlienFleet', x: float, y: float):
        """Initialize the alien at pixel coordinates (x, y)."""
        super().__init__()
        self.fleet = fleet
        self.screen = fleet.game.screen
        self.boundaries = fleet.game.screen.get_rect()
        self.settings = fleet.game.settings

        self.image = pygame.image.load(self.settings.alien_file)
        self.image = pygame.transform.scale(self.image, (self.settings.alien_h, self.settings.alien_w))
        self.image = pygame.transform.rotate(self.image, -90)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        self.y = float(self.rect.y)
        self.x = float(self.rect.x)

    def update(self):
        """Move the alien according to the fleet direction and its speed."""
        temp_speed = self.settings.fleet_speed

        self.y += temp_speed * self.fleet.fleet_direction
        self.rect.y = self.y
        self.rect.x = self.x

    def check_edges(self):
        """Return True if the alien reached the top or bottom screen edges."""
        return (self.rect.bottom >= self.boundaries.bottom or self.rect.top <= self.boundaries.top)
        
        
    def draw_alien(self):
        """Draw the alien image to the game screen."""
        self.screen.blit(self.image, self.rect)