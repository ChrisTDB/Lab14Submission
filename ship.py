"""
Ship module for Alien Invasion.

Author: Christopher Orta
Date: 11/24/2025

Purpose: Provides the `Ship` class which represents the player's ship,
manages movement, rendering, firing via the `Arsenal`, and collision checks.
"""

import pygame
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Lab14_corta1 import AlienInvasion
    from arsenal import Arsenal


class Ship:
    """
    Player-controlled ship.
    
    Attributes:
        game: Reference to the main game object.
        settings: Game settings object.
        screen: Pygame display surface.
        boundaries: Screen rectangle for boundary checks.
        image, rect: Pygame image and rect for the ship sprite.
        moving_up/moving_down: Movement flags.
        arsenal: Arsenal instance used to fire bullets.
    """
    def __init__(self, game: 'AlienInvasion', arsenal: 'Arsenal'):
        """
        Initialize the ship.

        Loads the ship image, scales and rotates it, centers the ship, and
        initializes movement flags and the linked `Arsenal`.
        """
        self.game = game
        self.settings = game.settings
        self.screen = game.screen
        self.boundaries = self.screen.get_rect()

        self.image = pygame.image.load(self.settings.ship_file)
        self.image = pygame.transform.scale(self.image, (self.settings.ship_w, self.settings.ship_h))
        self.image = pygame.transform.rotate(self.image, -90)

        self.rect = self.image.get_rect()
        self._center_ship()
        self.moving_up = False
        self.moving_down = False
        self.arsenal = arsenal
        
    def _center_ship(self):
        """Center the ship at the left-middle of the screen."""
        self.rect.midleft = self.boundaries.midleft
        self.y = float(self.rect.y)

    def update(self):
        """Update ship position and its arsenal each frame."""
        self._update_ship_movement()
        self.arsenal.update_arsenal()

    def _update_ship_movement(self):
        """Apply movement flags to the ship's vertical position."""
        temp_speed = self.settings.ship_speed
        if self.moving_up and self.rect.top > self.boundaries.top:
            self.y -= temp_speed
        if self.moving_down and self.rect.bottom < self.boundaries.bottom:
            self.y += temp_speed
        
        self.rect.y = self.y

    def draw(self):
        """Draw the ship and its arsenal to the screen."""
        self.arsenal.draw()
        self.screen.blit(self.image, self.rect)

    def fire(self):
        """Fire a bullet via the associated `Arsenal`.

        Returns True if a bullet was successfully fired, False otherwise.
        """
        return self.arsenal.fire_bullet()

    def check_collisions(self, other_group):
        """Check for collisions between this ship and a group of sprites.

        If a collision occurs, the ship is re-centered and True is returned.
        """
        if pygame.sprite.spritecollideany(self, other_group):
            self._center_ship()
            return True
        return False
    