"""
Game settings and constants for the Snake game
"""

# Window Settings
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
WINDOW_TITLE = "Snake Game"
FPS = 60
FIXED_FPS = 60  # Increased framerate for much smoother rendering

# Animation fine-tuning constants
ANIMATION_COMPLETE_THRESHOLD = 0.95  # Complete animation at 95% of move interval
ANIMATION_OVERSHOOT_FACTOR = 1.5  # Speed up animation more to ensure completion

# Difficulty Settings - DEFINE THESE FIRST
DIFFICULTY_EASY = 'Easy'
DIFFICULTY_MEDIUM = 'Medium'
DIFFICULTY_HARD = 'Hard'
DEFAULT_DIFFICULTY = DIFFICULTY_MEDIUM

# Easing curve parameters for different difficulties (defined AFTER difficulty constants)
# Format: (initial_threshold, middle_threshold, initial_acceleration, middle_deceleration)
DIFFICULTY_EASING_PARAMS = {
    DIFFICULTY_EASY: (0.25, 0.75, 3.5, 0.65),     # More pronounced curve for slow movement
    DIFFICULTY_MEDIUM: (0.22, 0.72, 3.8, 0.70),   # Adjusted for smoother movement at medium speed
    DIFFICULTY_HARD: (0.20, 0.70, 4.2, 0.75)      # Less sharp curve for more controlable fast movement
}

# Original FPS-based difficulty speeds (kept for backward compatibility)
DIFFICULTY_SPEEDS = {
    DIFFICULTY_EASY: 5,     # 5 FPS (unchanged)
    DIFFICULTY_MEDIUM: 8,   # Reduced from 10 FPS
    DIFFICULTY_HARD: 12     # Reduced from 20 FPS
}

# Movement frames per update for frame-independent movement
DIFFICULTY_MOVE_FRAMES = {
    DIFFICULTY_EASY: 10,
    DIFFICULTY_MEDIUM: 8,   # Increased from 6 (fewer updates per second = slower)
    DIFFICULTY_HARD: 5      # Increased from 3 (fewer updates per second = slower)
}

# Time-based movement intervals (in seconds) for more consistent movement
DIFFICULTY_MOVE_INTERVALS = {
    DIFFICULTY_EASY: 0.14,      # Responsive feel at easy level
    DIFFICULTY_MEDIUM: 0.11,    # Slowed down to be more playable but still challenging
    DIFFICULTY_HARD: 0.08       # Slowed down significantly but still faster than Medium
}

# Header Bar Settings
HEADER_HEIGHT = 50  # Height of the header bar where score is displayed
HEADER_COLOR = (20, 20, 20)  # Slightly lighter than BLACK for visual distinction
HEADER_BORDER_COLOR = (40, 40, 40)  # Color for header border
HEADER_BORDER_WIDTH = 2  # Width of the border between header and game area

# Grid Settings
GRID_SIZE = 20  # Size of each grid cell in pixels
GRID_WIDTH = WINDOW_WIDTH // GRID_SIZE
GRID_HEIGHT = (WINDOW_HEIGHT - HEADER_HEIGHT) // GRID_SIZE  # Adjust grid height to account for header

# Colors (RGB)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
DARK_GREEN = (0, 100, 0)
GRAY = (128, 128, 128)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)

# Snake Settings
INITIAL_SNAKE_LENGTH = 3
INITIAL_SNAKE_POSITION = (GRID_WIDTH // 2, GRID_HEIGHT // 2)
SNAKE_HEAD_COLOR = GREEN
SNAKE_BODY_COLOR = DARK_GREEN

# Food Settings
FOOD_COLOR = RED

# Game States
MENU = 0
PLAYING = 1
GAME_OVER = 2
PAUSED = 3

# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Controls
CONTROLS = {
    "UP": ["UP", "w", "W"],
    "DOWN": ["DOWN", "s", "S"],
    "LEFT": ["LEFT", "a", "A"],
    "RIGHT": ["RIGHT", "d", "D"],
    "PAUSE": ["ESCAPE"],
    "RESTART": ["RETURN"]
}

# Sound Settings
SOUND_ENABLED = True

# Use relative paths that will be resolved to absolute paths in the code
SOUND_EAT = "assets/sounds/eat.wav"
SOUND_GAME_OVER = "assets/sounds/game_over.wav"
SOUND_MOVE = "assets/sounds/move.wav"

# Animation Settings
ANIMATIONS_ENABLED = True  # Master toggle for all animations
ANIMATION_SPEED = 120.0  # Higher values = faster animations

# Improved animation speeds better matched to movement intervals
DIFFICULTY_ANIMATION_SPEEDS = {
    DIFFICULTY_EASY: 300.0,     # Maintained for smooth slow movement
    DIFFICULTY_MEDIUM: 350.0,   # Adjusted to match the new movement interval
    DIFFICULTY_HARD: 450.0      # Reduced to match the new movement interval
}

SNAKE_HEAD_ROTATION = True  # Whether to rotate the snake head based on direction
SMOOTH_MOVEMENT = True  # Whether to use interpolation for smoother movement

# Visual Effects Settings
GRADIENT_COLORS = True  # Whether to use gradient colors for the snake
VISUAL_EFFECTS = True  # Whether to show eat effects, highlights, etc. 