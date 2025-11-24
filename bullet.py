"""
Bullet module.

Author: Christopher Orta
Date: 11/24/2025

Purpose: Define the `Bullet` sprite used by the player's ship. Bullets
move horizontally across the screen and render themselves.
"""

import pygame
from pygame.sprite import Sprite
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Lab14_corta1 import AlienInvasion


class Bullet(Sprite):
    """Projectile fired by the player's ship.

    The `Bullet` class extends `pygame.sprite.Sprite` and manages its
    position, movement, and rendering.
    """
    def __init__(self, game: 'AlienInvasion'):
        """Create a new bullet positioned at the ship's mid-left point."""
        super().__init__()
        self.screen = game.screen
        self.settings = game.settings

        self.image = pygame.image.load(self.settings.bullet_file)
        self.image = pygame.transform.scale(self.image, (self.settings.bullet_w, self.settings.bullet_h))
        self.image = pygame.transform.rotate(self.image, -90)

        self.rect = self.image.get_rect()
        self.rect.midleft = game.ship.rect.midleft
        self.x = float(self.rect.x)

    def update(self):
        """Move the bullet to the right each frame by its speed."""
        self.x += self.settings.bullet_speed
        self.rect.x = self.x
        
    def draw_bullet(self):
        """Draw the bullet image to the screen."""
        self.screen.blit(self.image, self.rect)