"""
Utility functions for the Snake game
"""
import os
import json
import pygame
from settings import CONTROLS


def get_direction_from_key(key):
    """
    Convert a key press to a direction based on the controls mapping.
    
    Args:
        key: The key that was pressed
        
    Returns:
        The corresponding direction or None if the key doesn't map to a direction
    """
    from settings import UP, DOWN, LEFT, RIGHT
    
    # Check the key against the control mappings
    if key in CONTROLS["UP"]:
        return UP
    elif key in CONTROLS["DOWN"]:
        return DOWN
    elif key in CONTROLS["LEFT"]:
        return LEFT
    elif key in CONTROLS["RIGHT"]:
        return RIGHT
    
    return None


def save_high_score(score, difficulty=None, filename="high_score.json"):
    """
    Save the high score to a file.
    
    Args:
        score: The current high score
        difficulty: The difficulty level (EASY, MEDIUM, HARD). If None, uses legacy format.
        filename: The file to save the high score to
    """
    try:
        # Load existing data if the file exists
        data = {}
        if os.path.exists(filename):
            try:
                with open(filename, "r") as f:
                    data = json.load(f)
            except json.JSONDecodeError:
                # If the file is corrupted, start with empty data
                pass
        
        # If difficulty is specified, update the difficulty-specific high score
        if difficulty:
            # Initialize difficulty scores if not present
            if "difficulty_scores" not in data:
                data["difficulty_scores"] = {}
            
            # Update the high score for this difficulty if it's higher
            current_high = data["difficulty_scores"].get(difficulty, 0)
            if score > current_high:
                data["difficulty_scores"][difficulty] = score
        
        # Always update the legacy high score field for backward compatibility
        if "high_score" not in data or score > data["high_score"]:
            data["high_score"] = score
        
        # Write the data to the file
        with open(filename, "w") as f:
            json.dump(data, f)
        return True
    except Exception as e:
        print(f"Error saving high score: {e}")
        return False


def load_high_score(difficulty=None, filename="high_score.json"):
    """
    Load the high score from a file.
    
    Args:
        difficulty: The difficulty level (EASY, MEDIUM, HARD). If None, returns legacy high score.
        filename: The file to load the high score from
        
    Returns:
        The high score for the specified difficulty, or 0 if not found
    """
    # Check if the file exists
    if not os.path.exists(filename):
        return 0
    
    try:
        # Read the data from the file
        with open(filename, "r") as f:
            data = json.load(f)
        
        # If difficulty is specified, return the difficulty-specific high score
        if difficulty and "difficulty_scores" in data:
            return data["difficulty_scores"].get(difficulty, 0)
        
        # Otherwise, return the legacy high score
        return data.get("high_score", 0)
    except (json.JSONDecodeError, FileNotFoundError) as e:
        # Return 0 if there's an error
        print(f"Error loading high score: {e}")
        return 0
    except Exception as e:
        print(f"Unexpected error loading high score: {e}")
        return 0


def grid_to_pixel(grid_pos, grid_size):
    """
    Convert a grid position to a pixel position.
    
    Args:
        grid_pos: A tuple of (x, y) in grid coordinates
        grid_size: The size of each grid cell in pixels
        
    Returns:
        A tuple of (x, y) in pixel coordinates
    """
    x, y = grid_pos
    return (x * grid_size, y * grid_size)


def pixel_to_grid(pixel_pos, grid_size):
    """
    Convert a pixel position to a grid position.
    
    Args:
        pixel_pos: A tuple of (x, y) in pixel coordinates
        grid_size: The size of each grid cell in pixels
        
    Returns:
        A tuple of (x, y) in grid coordinates
    """
    x, y = pixel_pos
    return (x // grid_size, y // grid_size)


class SoundManager:
    """Manages the game's sound effects."""
    
    def __init__(self, enabled=True):
        """
        Initialize the sound manager.
        
        Args:
            enabled: Whether sound is enabled
        """
        self.enabled = enabled
        self.sounds = {}
        self.initialized = False
        
        # Initialize pygame mixer if possible
        if self.enabled:
            try:
                if not pygame.mixer.get_init():
                    pygame.mixer.init()
                self.initialized = True
            except Exception as e:
                print(f"Error initializing sound system: {e}")
                self.enabled = False
                self.initialized = False
    
    def load_sound(self, name, file_path):
        """
        Load a sound effect.
        
        Args:
            name: The name to associate with the sound
            file_path: The path to the sound file
        """
        if not self.enabled or not self.initialized:
            return False
            
        try:
            # Only load if the file exists and is readable
            if os.path.exists(file_path) and os.path.isfile(file_path):
                try:
                    self.sounds[name] = pygame.mixer.Sound(file_path)
                    return True
                except pygame.error as e:
                    print(f"Error loading sound '{name}' from {file_path}: {e}")
            else:
                print(f"Warning: Sound file not found or not accessible: {file_path}")
        except Exception as e:
            print(f"Unexpected error loading sound '{name}': {e}")
        
        return False
    
    def play(self, name):
        """
        Play a sound effect.
        
        Args:
            name: The name of the sound to play
        """
        if not self.enabled or not self.initialized or name not in self.sounds:
            return
        
        try:
            self.sounds[name].play()
        except Exception as e:
            print(f"Error playing sound '{name}': {e}")
    
    def enable(self):
        """Enable sounds."""
        if not self.initialized:
            try:
                if not pygame.mixer.get_init():
                    pygame.mixer.init()
                self.initialized = True
            except Exception as e:
                print(f"Error initializing sound system: {e}")
                return False
        
        self.enabled = True
        return True
    
    def disable(self):
        """Disable sounds."""
        self.enabled = False
        return True
    
    def toggle(self):
        """Toggle sound on/off."""
        if self.enabled:
            self.disable()
        else:
            self.enable()
        return self.enabled
    
    def is_enabled(self):
        """Check if sound is enabled and initialized."""
        return self.enabled and self.initialized 