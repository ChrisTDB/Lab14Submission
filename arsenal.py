"""
Arsenal module.

Author: Christopher Orta
Date: 11/24/2025

Purpose: Manage a group of `Bullet` sprites fired by the player's ship.
Provides update, rendering, off-screen removal, and firing logic.
"""

from bullet import Bullet
from settings import Settings
import pygame
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Lab14_corta1 import AlienInvasion


class Arsenal:
    """Container and manager for bullets fired by the ship."""
    def __init__(self, game: 'AlienInvasion'):
        """Create an empty `arsenal` group associated with the game."""
        self.game = game
        self.settings = game.settings
        self.arsenal = pygame.sprite.Group()

    def update_arsenal(self):
        """Update bullets and remove any that moved off-screen."""
        self.arsenal.update()
        self._remove_bullets_offscreen()

    def _remove_bullets_offscreen(self):
        """Remove bullets whose right edge passed the screen boundary."""
        for bullet in self.arsenal.copy():
            if bullet.rect.right >= self.settings.screen_w + 80:
                self.arsenal.remove(bullet)

    def draw(self):
        """Draw all bullets in the arsenal to the screen."""
        for bullet in self.arsenal:
            bullet.draw_bullet()
    
    def fire_bullet(self):
        """Attempt to fire a new bullet if under the allowed bullet limit.

        Returns True when a bullet is created, False if the cap prevents firing.
        """
        if len(self.arsenal) < self.settings.bullet_amount:
            new_bullet = Bullet(self.game)
            self.arsenal.add(new_bullet)
            return True
        return False