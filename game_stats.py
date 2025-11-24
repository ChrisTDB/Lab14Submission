"""
Game statistics module.

Author: Christopher Orta
Date: 11/24/2025

Purpose: Provide the `GameStats` class to track score, lives, level,
and persist high score information between runs.
"""

import json
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Lab14_corta1 import AlienInvasion


class GameStats:
    """Track and manage statistics for the current game session.

    Responsibilities include loading/saving high score data, tracking
    current score, remaining ships, and advancing levels.
    """

    def __init__(self, game: 'AlienInvasion'):
        """Initialize game statistics and load persisted scores."""
        self.game = game
        self.settings = game.settings
        self.max_score = 0
        self.init_saved_scores()
        self.reset_stats()

    def init_saved_scores(self):
        """Load saved hi-score from disk or create defaults if missing."""
        self.path = self.settings.scores_file
        if  self.path.exists() and self.path.stat.__sizeof__() > 20:
            contents = self.path.read_text()
            scores = json.loads(contents)
            self.hi_score = scores.get('hi_score', 0)
        else:
            self.hi_score = 0
            self.save_scores()

    def save_scores(self):
        """Persist score-related information to the configured file."""
        scores = {
            'hi_score': self.hi_score
        }
        contents = json.dumps(scores, indent=4)
        try:
            self.path.write_text(contents)
        except FileNotFoundError as e:
            print(f"File not found: {e}")


    def reset_stats(self):
        """Reset mutable statistics for a new game session."""
        self.ships_left = self.settings.starting_ship_count
        self.score = 0
        self.level = 1

    def update(self, collisions):
        """Update scores based on collisions mapping returned from fleet checks."""
        self._update_score(collisions)
        self._update_max_score()
        self._update_hi_score()
    
    def _update_max_score(self):
        """Track the session max score."""
        if self.score > self.max_score:
            self.max_score = self.score

    def _update_hi_score(self):
        """Update the all-time high score when current score exceeds it."""
        if self.score > self.hi_score:
            self.hi_score = self.score
    
    def _update_score(self, collisions):
        """Add points for each destroyed alien included in collisions."""
        for alien in collisions.values():
            self.score += self.settings.alien_points
    
    def update_level(self):
        """Advance the game level by one."""
        self.level += 1
        
