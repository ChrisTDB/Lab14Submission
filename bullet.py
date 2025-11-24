import pygame
from pygame.sprite import Sprite
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Lab14_corta1 import AlienInvasion

class Bullet(Sprite):
    def __init__(self, game: 'AlienInvasion'):
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
        self.x += self.settings.bullet_speed
        self.rect.x = self.x
        
    def draw_bullet(self):
        self.screen.blit(self.image, self.rect)