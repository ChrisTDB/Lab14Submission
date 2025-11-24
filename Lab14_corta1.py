"""
Alien Invasion Game - Main Game Module

Author: Christopher Orta
Date: 11/24/2025

Purpose: This module contains the main AlienInvasion game class that manages the overall
game loop, collision detection, event handling, screen updates, and game state management
for a Pygame-based space shooter game where the player controls a ship to defend against
an invading alien fleet.
"""

import sys
import pygame
from settings import Settings
from ship import Ship
from arsenal import Arsenal
from game_stats import GameStats
#from alien import Alien
from alien_fleet import AlienFleet
from button import Button
from hud import HUD
from time import sleep

class AlienInvasion:
    """
    Main game class that manages the Alien Invasion game.
    
    This class initializes the game environment, manages the game loop, handles all events,
    controls collisions, and manages game state including the ship, aliens, and HUD.
    """
    def __init__(self):
        """
        Initialize the Alien Invasion game.
        
        Sets up pygame, loads game settings, creates the game screen, initializes
        game objects (ship, aliens, HUD), loads sounds, and sets up the play button.
        """
        pygame.init()
        self.settings = Settings()
        self.settings.initialize_dynamic_settings()

        self.screen = pygame.display.set_mode((self.settings.screen_w, self.settings.screen_h))
        pygame.display.set_caption(self.settings.name)

        self.bg = pygame.image.load(self.settings.bg_file)
        self.bg = pygame.transform.scale(self.bg, (self.settings.screen_w, self.settings.screen_h))

        self.game_stats = GameStats(self)
        self.HUD = HUD(self)
        self.running = True
        self.clock = pygame.time.Clock()

        pygame.mixer.init()
        self.laser_sound = pygame.mixer.Sound(self.settings.laser_sound)
        self.laser_sound.set_volume(0.7)

        self.impact_sound = pygame.mixer.Sound(self.settings.impact_sound)
        self.impact_sound.set_volume(0.7)

        self.ship = Ship(self, Arsenal(self))
        self.alien_fleet = AlienFleet(self)
        self.alien_fleet.create_fleet()

        self.play_button = Button(self, 'Play')
        self.game_active = False

    def run_game(self):
        """
        Run the main game loop.
        
        Continuously checks for events, updates game objects when active, checks for
        collisions, and updates the display at the specified FPS rate. Runs until
        the game is terminated by the player.
        """
        #Game Loop
        while self.running:
            self._check_events()
            if self.game_active:
                self.ship.update()
                self.alien_fleet.update_fleet()
                self._check_collisions()
            self._update_screen()
            self.clock.tick(self.settings.FPS)

    def _check_collisions(self):
        """
        Check all collisions in the game.
        
        Detects and handles collisions between the ship and aliens, aliens reaching
        the left edge of the screen, and projectiles hitting aliens. Updates game
        statistics, plays sound effects, resets levels, and increases difficulty as needed.
        """
        #check collision for ship
        if self.ship.check_collisions(self.alien_fleet.fleet):
            self._check_game_status()
            #subtract a life
        #check collisions for aliens and left of screen
        if self.alien_fleet.check_fleet_left():
            self._check_game_status()
        #check collisions of projectiles and aliens
        collisions = self.alien_fleet.check_collisions(self.ship.arsenal.arsenal)
        if collisions:
            self.impact_sound.play()
            self.impact_sound.fadeout(500)
            self.game_stats.update(collisions)
            self.HUD.update_scores()
        
        if self.alien_fleet.check_destroyed_status():
            self._reset_level()
            self.settings.increase_difficulty()
            self.game_stats.update_level()
            self.HUD.update_level()
        
    def _check_game_status(self):
        """
        Check and update the game status after a collision.
        
        Decrements the ship count if ships remain, resets the level, and pauses briefly.
        If no ships remain, ends the game by setting game_active to False.
        """
        if self.game_stats.ships_left > 0:
            self.game_stats.ships_left -= 1
            self._reset_level()
            sleep(0.5)
        else:
            self.game_active = False

    def _reset_level(self):
        """
        Reset the current level.
        
        Clears all projectiles and aliens from the screen, then creates a new alien fleet
        to prepare for the next wave of enemies.
        """
        self.ship.arsenal.arsenal.empty()
        self.alien_fleet.fleet.empty()
        self.alien_fleet.create_fleet()

    def restart_game(self):
        """
        Restart the game for a new play session.
        
        Reinitializes settings, resets game statistics, updates the HUD display,
        resets the level, centers the ship, hides the mouse cursor, and sets
        the game to active state.
        """
        self.settings.initialize_dynamic_settings()
        self.game_stats.reset_stats()
        self.HUD.update_scores()
        self._reset_level()
        self.ship._center_ship()
        self.game_active = True
        pygame.mouse.set_visible(False)

    def _update_screen(self):
        """
        Update the game display.
        
        Draws the background, ship, aliens, and HUD to the screen. Displays the
        play button when the game is inactive, and updates the display with all
        rendered elements.
        """
        self.screen.blit(self.bg, (0,0))
        self.ship.draw()
        self.alien_fleet.draw()
        self.HUD.draw()

        if not self.game_active:
            self.play_button.draw()
            pygame.mouse.set_visible(True)

        pygame.display.flip()

    def _check_events(self):
        """
        Check for and handle all pygame events.
        
        Processes quit events, keyboard input (both key down and key up), and mouse
        button clicks. Saves game data when quitting and exits the game appropriately.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                self.game_stats.save_scores()
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and self.game_active == True:
                self._check_keydown_event(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_event(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self._check_button_clicked()
    
    def _check_button_clicked(self):
        """
        Check if the play button was clicked.
        
        Gets the mouse position and checks if it intersects with the play button.
        If clicked, restarts the game.
        """
        mouse_pos = pygame.mouse.get_pos()
        if self.play_button.check_clicked(mouse_pos):
            self.restart_game()

    def _check_keyup_event(self, event):
        """
        Handle key release events.
        
        Processes key up events for ship movement (UP/DOWN arrows), quit command (Q),
        and stops the corresponding movement flags when keys are released.
        
        Args:
            event: The pygame key up event containing the key information.
        """
        if event.key == pygame.K_UP:
            self.ship.moving_up = False
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = False
        elif event.key == pygame.K_q:
            self.running = False
            pygame.quit()
            sys.exit()

    def _check_keydown_event(self, event):
        """
        Handle key press events.
        
        Processes key down events for ship movement (UP/DOWN arrows), firing projectiles
        (SPACE), and quit command (Q). Plays laser sound when firing and saves scores
        when quitting.
        
        Args:
            event: The pygame key down event containing the key information.
        """
        if event.key == pygame.K_UP:
            self.ship.moving_up = True
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = True
        elif event.key == pygame.K_SPACE:
            if self.ship.fire():
                self.laser_sound.play()
                self.laser_sound.fadeout(250)
                #play laser sound
        elif event.key == pygame.K_q:
            self.running = False
            self.game_stats.save_scores()
            pygame.quit()
            sys.exit()
    

if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()