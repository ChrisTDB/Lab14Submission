import pygame
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Lab14_corta1 import AlienInvasion
    from arsenal import Arsenal

class Ship:
    def __init__(self, game: 'AlienInvasion', arsenal: 'Arsenal'):
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
        self.rect.midleft = self.boundaries.midleft
        self.y = float(self.rect.y)

    def update(self):
        # updating the position of the ship
        self._update_ship_movement()
        self.arsenal.update_arsenal()

    def _update_ship_movement(self):
        temp_speed = self.settings.ship_speed
        if self.moving_up and self.rect.top > self.boundaries.top:
            self.y -= temp_speed
        if self.moving_down and self.rect.bottom < self.boundaries.bottom:
            self.y += temp_speed
        
        self.rect.y = self.y

    def draw(self):
        self.arsenal.draw()
        self.screen.blit(self.image, self.rect)

    def fire(self):
        return self.arsenal.fire_bullet()

    def check_collisions(self, other_group):
        if pygame.sprite.spritecollideany(self, other_group):
            self._center_ship()
            return True
        return False
    