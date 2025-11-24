import pygame
from alien import Alien
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Lab14_corta1 import AlienInvasion

class AlienFleet:

    def __init__(self, game: 'AlienInvasion'):
        self.game = game
        self.settings = game.settings
        self.fleet = pygame.sprite.Group()
        self.fleet_direction = self.settings.fleet_direction
        self.fleet_drop_speed = self.settings.fleet_drop_speed

        self.create_fleet()

    def create_fleet(self):
        alien_h = self.settings.alien_h
        alien_w = self.settings.alien_w
        screen_h = self.settings.screen_h
        screen_w = self.settings.screen_w

        fleet_h, fleet_w = self.calculate_fleet_size(alien_h, screen_h, alien_w, screen_w)
        x_offset, y_offset = self.calculate_offsets(
            alien_h, fleet_h, alien_w, fleet_w, screen_h, screen_w
        )
        self._create_rectangle_fleet(
            fleet_w, fleet_h, alien_w, alien_h, x_offset, y_offset
        )

    def calculate_fleet_size(self, alien_h, screen_h, alien_w, screen_w):
        fleet_h = (screen_h // alien_h)
        fleet_w = ((screen_w / 2)// alien_w)
        if fleet_h % 2 == 0:
            fleet_h -= 1
        else:
            fleet_h -= 2

        if fleet_w % 2 == 0:
            fleet_w -= 1
        else:
            fleet_w -= 2

        return int(fleet_h), int(fleet_w)

    def calculate_offsets(
        self, alien_h, fleet_h, alien_w, fleet_w, screen_h, screen_w
    ):
        half_screen = screen_w // 2
        fleet_vertical_space = fleet_h * alien_h
        fleet_horizontal_space = fleet_w * alien_w
        y_offset = int((screen_h - fleet_vertical_space) // 2)
        x_offset = half_screen + int((half_screen - fleet_horizontal_space) // 2)

        return x_offset, y_offset

    def _create_rectangle_fleet(
        self, fleet_w: int, fleet_h: int, alien_w: int, alien_h: int, x_offset: int, y_offset: int
    ):
        for col in range(fleet_w):
            for row in range(fleet_h):
                current_y = alien_h * row + y_offset
                current_x = alien_w * col + x_offset
                if row % 2 == 0 or col % 2 == 0:
                    continue
                self._create_alien(current_y, current_x)

    def _create_alien(self, current_x: int, current_y: int):
        new_alien = Alien(self, current_y, current_x)

        self.fleet.add(new_alien)

    def _check_fleet_edges(self):
        alien: Alien
        for alien in self.fleet:
            if alien.check_edges():
                self._drop_alien_fleet()
                self.fleet_direction *= -1
                break

    def _drop_alien_fleet(self):
        for alien in self.fleet:
            alien.x -= self.fleet_drop_speed

    def update_fleet(self):
        self._check_fleet_edges()
        self.fleet.update()

    def draw(self):
        alien: 'Alien'
        for alien in self.fleet:
            alien.draw_alien()

    def check_collisions(self, other_group):
        return pygame.sprite.groupcollide(self.fleet, other_group, True, True)

    def check_fleet_left(self):
        alien: Alien
        for alien in self.fleet:
            if alien.rect.right < 0:
                return True
        return False

    def check_destroyed_status(self):
        return not self.fleet
