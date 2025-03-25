"""
Snake class for the Snake game
"""
from settings import (INITIAL_SNAKE_LENGTH, INITIAL_SNAKE_POSITION, RIGHT, UP, DOWN, 
                  LEFT, SNAKE_BODY_COLOR, SNAKE_HEAD_COLOR, DIFFICULTY_MEDIUM,
                  DIFFICULTY_EASING_PARAMS)
import math


class Snake:
    """
    Represents the snake in the game.
    Handles movement, growth, and collision detection.
    """
    
    def __init__(self):
        """Initialize the snake with default settings."""
        # Start at the initial position
        self.position = INITIAL_SNAKE_POSITION
        # Start with the default length
        self.body = self._create_initial_body()
        # Start moving to the right
        self.direction = RIGHT
        # Flag to track if the snake has just eaten
        self.just_ate = False
        # Track the last valid direction to prevent 180-degree turns
        self.last_direction = RIGHT
        
        # Animation properties
        self.visual_body = self.body.copy()  # Visual positions for rendering
        self.animation_progress = 0.0  # 0.0 to 1.0, represents progress between grid positions
        self.prev_body = self.body.copy()  # Previous positions for interpolation
        self.moving = False  # Flag to track if snake is currently moving
        
        # Color properties for gradient effect
        self.base_color = SNAKE_BODY_COLOR  # Starting color
        self.color_stage = 0  # Increments with each food eaten
        self.head_color = SNAKE_HEAD_COLOR  # Head color
        
        # Default difficulty for easing curves
        self.difficulty = DIFFICULTY_MEDIUM
    
    def set_difficulty(self, difficulty):
        """
        Set the difficulty level for the snake's movement animations.
        
        Args:
            difficulty: The difficulty level (EASY, MEDIUM, HARD)
        """
        self.difficulty = difficulty
    
    def _create_initial_body(self):
        """Create the initial snake body segments."""
        x, y = INITIAL_SNAKE_POSITION
        # Create segments to the left of the head position
        body = [(x - i, y) for i in range(INITIAL_SNAKE_LENGTH)]
        return body
    
    def move(self):
        """
        Move the snake in the current direction.
        Returns True if the move is valid, False otherwise.
        """
        # Store previous positions for animation BEFORE changing the body
        self.prev_body = self.body.copy()
        self.animation_progress = 0.0
        
        # Set the last valid direction
        self.last_direction = self.direction
        
        # Get the current head position
        head_x, head_y = self.body[0]
        
        # Calculate new head position based on direction
        dx, dy = self.direction
        new_head = (head_x + dx, head_y + dy)
        
        # Add the new head to the beginning of the body
        self.body.insert(0, new_head)
        
        # Remove the tail unless the snake just ate
        if not self.just_ate:
            self.body.pop()
        else:
            # Reset the eating flag
            self.just_ate = False
            
            # For a growing snake, we need to properly initialize the animation
            # by extending the previous body to match the length of the current body
            self.prev_body.append(self.prev_body[-1])  # Duplicate the last segment
        
        # Update visual body with new length
        if len(self.visual_body) != len(self.body):
            self.visual_body = self.body.copy()
            
        # Start animation for the movement
        self.moving = True
            
        # Update the current position to the new head
        self.position = new_head
        
        return True
    
    def update_animation(self, dt, animation_speed=100.0):
        """
        Update the snake's animation progress.
        
        Args:
            dt: Delta time since last frame in seconds
            animation_speed: Speed factor for animation (higher = faster)
        
        Returns:
            True if the animation has completed, False otherwise
        """
        if not self.moving:
            return True  # No animation in progress
        
        # Enhanced animation progress calculation
        # The dynamic animation_speed ensures consistent visual speed regardless of FPS
        self.animation_progress += dt * animation_speed
        
        # Limit animation progress to a maximum of 1.0
        if self.animation_progress >= 1.0:
            self.animation_progress = 1.0
            self.moving = False
            
            # Ensure positions are exactly aligned to grid after animation is done
            self.visual_body = self.body.copy()
            self.update_position_history()
            return True  # Animation has completed
        
        # Apply easing to make movement look more natural
        eased_progress = self._ease_out_quad(self.animation_progress)
        
        # Make sure visual_body has the same number of segments as body
        while len(self.visual_body) < len(self.body):
            # Add segments if missing (e.g., during growth)
            if len(self.prev_body) < len(self.body):
                # If prev_body is short, duplicate the last segment
                self.prev_body.append(self.prev_body[-1] if self.prev_body else self.body[-1])
            self.visual_body.append(self.prev_body[-1])
        
        # Handle shrinking (shouldn't typically happen, but just in case)
        while len(self.visual_body) > len(self.body):
            self.visual_body.pop()
            if len(self.prev_body) > len(self.body):
                self.prev_body.pop()
        
        # Interpolate between previous and current positions for each segment
        for i, segment in enumerate(self.body):
            # Make sure we have valid indices for prev_body
            if i < len(self.prev_body):
                prev_x, prev_y = self.prev_body[i]
                curr_x, curr_y = segment
                
                # Calculate exact position based on eased progress
                x_diff = curr_x - prev_x
                y_diff = curr_y - prev_y
                
                # Apply interpolation with a higher precision calculation
                self.visual_body[i] = (
                    prev_x + x_diff * eased_progress,
                    prev_y + y_diff * eased_progress
                )
            else:
                # Fallback for any extra segments (shouldn't happen with proper synchronization)
                self.visual_body[i] = segment
        
        return False  # Animation is still in progress
    
    def _ease_out_quad(self, t):
        """
        Enhanced easing function for smoother animations.
        Uses difficulty-specific parameters for optimal curves.
        
        Args:
            t: A value between 0 and 1 representing the progress of the animation
            
        Returns:
            A smoothed value between 0 and 1
        """
        # Ensure t is within bounds
        t = max(0.0, min(1.0, t))
        
        # Get difficulty-specific parameters
        # Format: (initial_threshold, middle_threshold, initial_acceleration, middle_deceleration)
        params = DIFFICULTY_EASING_PARAMS.get(self.difficulty, DIFFICULTY_EASING_PARAMS[DIFFICULTY_MEDIUM])
        initial_threshold, middle_threshold, initial_accel, middle_decel = params
        
        # Apply custom easing curve based on difficulty
        if t < initial_threshold:
            # Initial acceleration - quicker at higher difficulties
            return initial_accel * t * t
        elif t < middle_threshold:
            # Middle section - more linear at higher difficulties
            mapped_t = (t - initial_threshold) / (middle_threshold - initial_threshold)
            initial_value = initial_accel * initial_threshold * initial_threshold
            return initial_value + mapped_t * middle_decel
        else:
            # Final deceleration - gentler at lower difficulties
            mapped_t = (t - middle_threshold) / (1.0 - middle_threshold)
            middle_value = initial_accel * initial_threshold * initial_threshold + middle_decel
            # Calculate deceleration based on mapped t
            return middle_value + (1.0 - (1.0 - mapped_t) * (1.0 - mapped_t)) * (1.0 - middle_value)
    
    def get_segment_direction(self, index):
        """
        Get the direction of a specific body segment.
        Useful for rendering the head orientation.
        
        Args:
            index: Index of the segment
            
        Returns:
            Direction as (dx, dy) tuple
        """
        if index >= len(self.body) - 1:
            return self.direction  # Last segment follows the current direction
        
        # Calculate direction from current segment to next segment
        current_x, current_y = self.body[index]
        next_x, next_y = self.body[index + 1]
        
        dx = current_x - next_x
        dy = current_y - next_y
        
        # Normalize to unit vector
        if dx != 0 and dy != 0:
            # Handle diagonal (shouldn't happen in normal gameplay)
            if abs(dx) > abs(dy):
                return (1 if dx > 0 else -1, 0)
            else:
                return (0, 1 if dy > 0 else -1)
        
        return (dx, dy)
    
    def grow(self):
        """Make the snake grow after eating food."""
        self.just_ate = True
        # Increment color stage when growing
        self.color_stage += 1
    
    def get_gradient_color(self, segment_index):
        """
        Calculate a gradient color for a specific segment based on its position and the snake's growth.
        
        Args:
            segment_index: Index of the segment in the body
            
        Returns:
            A color tuple (r, g, b)
        """
        # Base color transitions
        color_transitions = [
            (0, 100, 0),    # Dark green (default)
            (0, 130, 0),    # Brighter green
            (0, 160, 0),    # Even brighter green
            (60, 160, 0),   # Yellow-green
            (120, 160, 0),  # Yellowish
            (180, 160, 0),  # Gold
            (180, 120, 0),  # Orange-gold
            (180, 80, 0),   # Orange
            (220, 80, 0),   # Red-orange
            (220, 40, 0),   # Red
            (220, 0, 80),   # Red-purple
            (180, 0, 160),  # Purple
            (100, 0, 180),  # Purple-blue
            (0, 0, 220),    # Blue
            (0, 100, 220),  # Blue-green
            (0, 180, 220),  # Cyan
        ]
        
        # Color that changes with the snake's overall growth
        base_color_index = min(self.color_stage, len(color_transitions) - 1)
        next_color_index = (base_color_index + 1) % len(color_transitions)
        
        # Get colors to interpolate between
        base_color = color_transitions[base_color_index]
        next_color = color_transitions[next_color_index]
        
        # Add segment-specific variation - segments closer to head are brighter
        total_length = len(self.body)
        if total_length <= 1:
            # For a single segment, use head color
            return self.head_color
            
        # Position factor: 0.0 for head, 1.0 for tail
        position_factor = segment_index / total_length
        
        # Calculate segment color (closer to head = more like base color)
        # Add slight periodic variation based on position
        r1, g1, b1 = base_color
        r2, g2, b2 = next_color
        
        # Add wave effect along body
        wave = math.sin(position_factor * 6.0 + self.color_stage * 0.2) * 0.2 + 0.8
        
        # Interpolate colors
        r = int(r1 * (1 - position_factor) + r2 * position_factor * wave)
        g = int(g1 * (1 - position_factor) + g2 * position_factor * wave)
        b = int(b1 * (1 - position_factor) + b2 * position_factor * wave)
        
        # Ensure values are in valid range
        return (max(0, min(255, r)), max(0, min(255, g)), max(0, min(255, b)))
    
    def get_head_color(self):
        """Get the current head color based on the color stage."""
        # Make head color slightly brighter than the first body segment
        r, g, b = self.get_gradient_color(0)
        # Brighten the color for head
        brightness_boost = 50
        return (
            min(255, r + brightness_boost),
            min(255, g + brightness_boost), 
            min(255, b + brightness_boost)
        )
    
    def check_collision_with_self(self):
        """
        Check if the snake's head collides with its body.
        Returns True if collision detected, False otherwise.
        """
        head = self.body[0]
        # Check if head position exists in rest of body
        return head in self.body[1:]
    
    def check_collision_with_boundaries(self, width, height):
        """
        Check if the snake's head collides with the boundaries.
        Returns True if collision detected, False otherwise.
        """
        head_x, head_y = self.body[0]
        return (
            head_x < 0 or 
            head_x >= width or 
            head_y < 0 or 
            head_y >= height
        )
    
    def change_direction(self, new_direction):
        """
        Change the snake's direction.
        Prevents 180-degree turns.
        """
        # Check if the new direction is opposite to the current direction
        dx, dy = new_direction
        last_dx, last_dy = self.last_direction
        
        # Prevent 180-degree turns
        if (dx != -last_dx or dy != -last_dy):
            self.direction = new_direction
    
    def get_head_position(self):
        """Return the position of the snake's head."""
        return self.body[0]
    
    def get_body(self):
        """Return the snake's body positions."""
        return self.body
    
    def get_visual_body(self):
        """Return the snake's visual body positions for rendering."""
        return self.visual_body
    
    def update_position_history(self):
        """
        Update the position history after an animation is complete.
        This ensures visual positions match actual grid positions.
        """
        # After animation completes, ensure all positions are properly aligned
        self.visual_body = self.body.copy()
        
        # Keep the prev_body in sync with current body for consistent transitions
        self.prev_body = self.body.copy()
        
        # Reset animation progress
        self.animation_progress = 0.0 