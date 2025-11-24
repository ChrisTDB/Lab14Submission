"""
Button module for Alien Invasion.

Author: Christopher Orta
Date: 11/24/2025

Purpose: Provide a simple `Button` class used for the Play button on the
game's title screen.
"""

import pygame.font
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Lab14_corta1 import AlienInvasion


class Button:
    """Simple rectangular button with centered text.

    The button renders a colored rectangle with a text label and provides a
    convenience method to check whether a mouse position lies within the button.
    """

    def __init__(self, game: 'AlienInvasion', msg):
        """Initialize button attributes and prepare the message image."""
        self.game = game
        self.screen = game.screen
        self.boundaries = game.screen.get_rect()
        self.settings = game.settings
        self.font = pygame.font.Font(self.settings.font_file, 
            self.settings.button_font_size)
        self.rect = pygame.Rect(0,0,self.settings.button_w, self.settings.button_h)
        self.rect.center = self.boundaries.center
        self._prep_msg(msg)

    def _prep_msg(self, msg):
        """Render the button's message to an image and center it in the button."""
        self.msg_image = self.font.render(msg, True, self.settings.text_color, None)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw(self):
        """Draw the button rectangle and its text to the screen."""
        self.screen.fill(self.settings.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)

    def check_clicked(self, mouse_pos):
        """Return True if `mouse_pos` lies within the button rect."""
        return self.rect.collidepoint(mouse_pos)