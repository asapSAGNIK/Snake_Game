"""
Food class for the Snake game
"""
import random
from settings import GRID_WIDTH, GRID_HEIGHT


class Food:
    """
    Represents the food in the game.
    Handles random placement and collision detection.
    """
    
    def __init__(self):
        """Initialize the food with a random position."""
        self.position = self._generate_random_position()
    
    def _generate_random_position(self):
        """Generate a random position for the food within the grid."""
        x = random.randint(0, GRID_WIDTH - 1)
        y = random.randint(0, GRID_HEIGHT - 1)
        return (x, y)
    
    def spawn(self, snake_body):
        """
        Spawn the food at a new random position, ensuring it doesn't overlap with the snake.
        
        Args:
            snake_body: List of (x, y) tuples representing the snake's body
            
        Returns:
            The new position of the food
        """
        # Generate a new position for the food
        new_position = self._generate_random_position()
        
        # Ensure the food doesn't spawn inside the snake
        attempts = 0
        max_attempts = 100  # Prevent infinite loops
        
        while new_position in snake_body and attempts < max_attempts:
            new_position = self._generate_random_position()
            attempts += 1
            
        # Update the food position
        self.position = new_position
        
        return self.position
    
    def get_position(self):
        """Return the current position of the food."""
        return self.position
    
    def is_collision(self, position):
        """
        Check if the given position collides with the food.
        
        Args:
            position: (x, y) tuple to check against food position
            
        Returns:
            True if there's a collision, False otherwise
        """
        return position == self.position 