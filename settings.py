"""
Settings module for Alien Invasion.

Author: Christopher Orta
Date: 11/24/2025

Purpose: Centralized game configuration. The `Settings` class stores static
and dynamic settings used throughout the game and provides methods to
initialize and scale dynamic values as difficulty increases.
"""

from pathlib import Path


class Settings:
    """Container for game settings and configuration.

    Static values (file paths, window size, colors) are initialized in
    the constructor. Dynamic values such as speeds are set in
    `initialize_dynamic_settings()` so they can be reset between games.
    """
    def __init__(self):
        """Initialize static settings for the game."""
        self.name: str = 'Alien Invasion'
        self.screen_w = 1200
        self.screen_h = 800
        self.FPS = 60
        self.bg_file = Path.cwd() / 'Assets' / 'images' / 'Starbasesnow.png'
        self.difficulty_scale = 1.1
        self.scores_file = Path.cwd() / 'Assets' / 'file' / 'scores.json'

        self.ship_file = Path.cwd() / 'Assets' / 'images' / 'ship2(no bg).png'
        self.ship_w = 40
        self.ship_h = 60
        

        self.bullet_file = Path.cwd() / 'Assets' / 'images' / 'laserBlast.png'
        self.laser_sound = Path.cwd() / 'Assets' / 'sound' / 'laser.mp3'
        self.impact_sound = Path.cwd() / 'Assets' / 'sound' / 'impactSound.mp3'
        
        self.alien_file = Path.cwd() / 'Assets' / 'images' / 'enemy_4.png'
        self.alien_w = 40
        self.alien_h = 40
        self.fleet_direction = 1

        self.button_w = 200
        self.button_h = 50
        self.button_color = (0,135,50)

        self.text_color = (255,255,255)
        self.button_font_size = 48
        self.HUD_font_size = 20
        self.font_file = Path.cwd() / 'Assets' / 'Fonts' / 'Silkscreen' / 'Silkscreen-Bold.ttf'

    def initialize_dynamic_settings(self):
        """Initialize settings that may change throughout the game.

        This method is called when starting or restarting a game to set
        movement speeds, bullet limits, and point values to their base
        values.
        """
        self.ship_speed = 10
        self.starting_ship_count = 3
        self.bullet_speed = 20
        self.bullet_amount = 50
        self.bullet_w = 25
        self.bullet_h = 80
        self.fleet_speed = 5
        self.fleet_drop_speed = 40
        self.alien_points = 50

    def increase_difficulty(self):
        """Scale dynamic settings to increase game difficulty."""
        self.ship_speed *= self.difficulty_scale
        self.bullet_speed *= self.difficulty_scale
        self.fleet_speed *= self.difficulty_scale

            