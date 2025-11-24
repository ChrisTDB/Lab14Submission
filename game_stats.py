from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Lab14_corta1 import AlienInvasion

class GameStats():

    def __init__(self, game: 'AlienInvasion'):
        self.game = game
        self.settings = game.settings
        self.max_score = 0
        self.reset_stats()
    
    def reset_stats(self):
        self.ships_left = self.settings.starting_ship_count
        self.score = 0
        self.level = 1

    def update(self, collisions):
        self._update_score(collisions)
        self._update_max_score()
    
    def _update_max_score(self):
        if self.score > self.max_score:
            self.max_score = self.score
        #print(f"Max: {self.max_score}")
    
    def _update_score(self, collisions):
        for alien in collisions.values():
            self.score += self.settings.alien_points
        #print(f"Basic: {self.score}")
    
    def update_level(self):
        self.level += 1
        
