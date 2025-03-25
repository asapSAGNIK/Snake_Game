"""
Game class for the Snake game
"""
import pygame
import pygame_menu
import math
from snake import Snake
from food import Food
from utils import SoundManager
from settings import (
    WINDOW_WIDTH, WINDOW_HEIGHT, FPS, FIXED_FPS, GRID_SIZE, GRID_WIDTH, GRID_HEIGHT,
    BLACK, WHITE, RED, GREEN, DARK_GREEN, GRAY, BLUE, YELLOW, ORANGE,
    FOOD_COLOR, SNAKE_HEAD_COLOR, SNAKE_BODY_COLOR,
    UP, DOWN, LEFT, RIGHT, CONTROLS,
    MENU, PLAYING, GAME_OVER, PAUSED,
    SOUND_ENABLED, SOUND_EAT, SOUND_GAME_OVER, SOUND_MOVE,
    ANIMATIONS_ENABLED, ANIMATION_SPEED, DIFFICULTY_ANIMATION_SPEEDS, SNAKE_HEAD_ROTATION, SMOOTH_MOVEMENT,
    HEADER_HEIGHT, HEADER_COLOR, HEADER_BORDER_COLOR, HEADER_BORDER_WIDTH,
    GRADIENT_COLORS, VISUAL_EFFECTS,
    DIFFICULTY_EASY, DIFFICULTY_MEDIUM, DIFFICULTY_HARD, DIFFICULTY_SPEEDS, 
    DIFFICULTY_MOVE_FRAMES, DIFFICULTY_MOVE_INTERVALS, DEFAULT_DIFFICULTY,
    ANIMATION_COMPLETE_THRESHOLD, ANIMATION_OVERSHOOT_FACTOR
)


class Game:
    """
    Main game class that manages game state and components.
    """
    
    def __init__(self, sound_enabled=SOUND_ENABLED):
        """Initialize the game, its components, and pygame."""
        # Initialize pygame
        if not pygame.get_init():
            pygame.init()
        
        # Set up the display
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Snake Game")
        
        # Set up the clock for controlling game speed
        self.clock = pygame.time.Clock()
        self.delta_time = 0  # Time elapsed since last frame in seconds
        
        # Difficulty settings
        self.difficulty = DEFAULT_DIFFICULTY
        self.fps = DIFFICULTY_SPEEDS[self.difficulty]
        
        # Frame-independent movement settings
        self.move_frames = DIFFICULTY_MOVE_FRAMES[self.difficulty]  # Frames between snake movements
        self.move_accumulator = 0  # Accumulates frames until next movement
        
        # Time-based movement settings
        self.move_interval = DIFFICULTY_MOVE_INTERVALS[self.difficulty]  # Time between movements in seconds
        self.move_time_accumulator = 0.0  # Accumulates time until next movement
        
        # Animation settings
        self.animation_speed = DIFFICULTY_ANIMATION_SPEEDS[self.difficulty]
        
        # Set up game components
        self.snake = Snake()
        self.food = Food()
        
        # Animation and visual settings - Always enabled
        self.animations_enabled = True
        self.gradient_colors = True
        self.visual_effects = True
        
        # Set up sound manager
        self.sound_manager = SoundManager(enabled=sound_enabled)
        self._load_sounds()
        
        # Game state
        self.state = MENU  # Start with the menu instead of PLAYING
        self.score = 0
        self.high_score = 0
        
        # Difficulty-specific high scores
        self.difficulty_high_scores = {
            DIFFICULTY_EASY: 0,
            DIFFICULTY_MEDIUM: 0,
            DIFFICULTY_HARD: 0
        }
        self._load_high_scores()
        
        # Font for text rendering
        self.font = pygame.font.SysFont(None, 36)
        
        # Flag to control the game loop
        self.running = True
        
        # Menu-related attributes
        self.menu = None
        self.instructions_menu = None
        self.difficulty_menu = None
        
        # Create the main menu and ensure it's the first one displayed
        self._create_main_menu()
        
        # Create the other menus but don't display them yet
        self._create_difficulty_menu()
        
        # Make sure the difficulty menu is disabled and main menu is enabled initially
        if self.difficulty_menu:
            self.difficulty_menu.disable()
        if self.menu:
            self.menu.enable()
    
    def _load_sounds(self):
        """Load all game sounds."""
        # Get the absolute path to the sound directory
        import os
        base_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Use absolute paths for sound files
        eat_sound = os.path.join(base_dir, SOUND_EAT)
        game_over_sound = os.path.join(base_dir, SOUND_GAME_OVER)
        move_sound = os.path.join(base_dir, SOUND_MOVE)
        
        # Load sounds with proper error handling
        self.sound_manager.load_sound("eat", eat_sound)
        self.sound_manager.load_sound("game_over", game_over_sound)
        self.sound_manager.load_sound("move", move_sound)
    
    def _load_high_scores(self):
        """Load all difficulty-specific high scores."""
        from utils import load_high_score
        
        # Load high scores for each difficulty
        for difficulty in [DIFFICULTY_EASY, DIFFICULTY_MEDIUM, DIFFICULTY_HARD]:
            self.difficulty_high_scores[difficulty] = load_high_score(difficulty)
        
        # Set the current high score based on the current difficulty
        self.high_score = self.difficulty_high_scores[self.difficulty]
    
    def _create_main_menu(self):
        """Create the main menu for the game."""
        # Create a menu theme
        theme = pygame_menu.themes.THEME_DARK.copy()
        theme.title_background_color = DARK_GREEN
        theme.title_font_color = WHITE
        theme.background_color = BLACK
        theme.widget_font_color = WHITE
        try:
            theme.widget_selection_effect = pygame_menu.widgets.HighlightSelection()
        except AttributeError:
            # Fallback for older pygame-menu versions
            pass
        
        # Create the menu
        self.menu = pygame_menu.Menu(
            'Snake Game',
            WINDOW_WIDTH, WINDOW_HEIGHT,
            theme=theme,
            onclose=pygame_menu.events.CLOSE
        )
        
        # Add menu items
        self.menu.add.button('Play', self._show_difficulty_menu)
        self.menu.add.button('Instructions', self._show_instructions)
        
        # Check if toggle_switch is available (newer pygame-menu versions)
        try:
            # Only sound toggle remains
            self.menu.add.toggle_switch('Sound', self.sound_manager.enabled, 
                                        onchange=self._toggle_sound)
        except AttributeError:
            # Fallback for older pygame-menu versions
            self.menu.add.selector('Sound: ', 
                                  [('On', True), ('Off', False)],
                                  onchange=self._toggle_sound_old,
                                  default=0 if self.sound_manager.enabled else 1)
        
        self.menu.add.button('Quit', pygame_menu.events.EXIT)
    
    def _create_difficulty_menu(self):
        """Create the difficulty selection menu."""
        # Create a menu theme (similar to main menu theme)
        theme = pygame_menu.themes.THEME_DARK.copy()
        theme.title_background_color = ORANGE
        theme.title_font_color = WHITE
        theme.background_color = BLACK
        theme.widget_font_color = WHITE
        try:
            theme.widget_selection_effect = pygame_menu.widgets.HighlightSelection()
        except AttributeError:
            # Fallback for older pygame-menu versions
            pass
        
        # Create the menu
        self.difficulty_menu = pygame_menu.Menu(
            'Select Difficulty',
            WINDOW_WIDTH, WINDOW_HEIGHT,
            theme=theme,
            onclose=pygame_menu.events.CLOSE
        )
        
        # Add difficulty options with clearer descriptions (no high scores)
        self.difficulty_menu.add.button("EASY (Slow Speed)", lambda: self._start_game_with_difficulty(DIFFICULTY_EASY))
        self.difficulty_menu.add.button("MEDIUM (Normal Speed)", lambda: self._start_game_with_difficulty(DIFFICULTY_MEDIUM))
        self.difficulty_menu.add.button("HARD (Fast Speed)", lambda: self._start_game_with_difficulty(DIFFICULTY_HARD))
        self.difficulty_menu.add.button('Back', self._back_to_main_menu)
    
    def _show_difficulty_menu(self):
        """Show the difficulty selection menu."""
        # Update high scores in case they've changed
        self._load_high_scores()
        
        # Recreate the difficulty menu to reflect updated high scores
        self._create_difficulty_menu()
        
        # Disable all menus first to avoid conflicts
        if self.instructions_menu:
            self.instructions_menu.disable()
        if self.menu:
            self.menu.disable()
            
        # Now enable the difficulty menu
        if self.difficulty_menu:
            self.difficulty_menu.enable()
    
    def _start_game_with_difficulty(self, difficulty):
        """Start a new game with the specified difficulty."""
        self.difficulty = difficulty
        self.fps = DIFFICULTY_SPEEDS[difficulty]  # Keep for backward compatibility
        self.move_frames = DIFFICULTY_MOVE_FRAMES[difficulty]  # Keep for backward compatibility
        self.move_interval = DIFFICULTY_MOVE_INTERVALS[difficulty]  # New time-based approach
        self.animation_speed = DIFFICULTY_ANIMATION_SPEEDS[difficulty]
        self.move_accumulator = 0  # Reset frame accumulator for backward compatibility
        self.move_time_accumulator = 0.0  # Reset time accumulator
        self.high_score = self.difficulty_high_scores[difficulty]
        self.reset_game()
        # Pass the difficulty to the snake for optimal easing curves
        self.snake.set_difficulty(difficulty)
        self.state = PLAYING
    
    def _start_game(self):
        """Start a new game from the menu with default difficulty."""
        self._start_game_with_difficulty(DEFAULT_DIFFICULTY)
    
    def _show_instructions(self):
        """Show the instructions menu."""
        if not self.instructions_menu:
            self._create_instructions_menu()
        
        # Disable all other menus first to avoid conflicts
        if self.difficulty_menu:
            self.difficulty_menu.disable()
        if self.menu:
            self.menu.disable()
            
        # Now enable the instructions menu
        if self.instructions_menu:
            self.instructions_menu.enable()
    
    def _back_to_main_menu(self):
        """Return to the main menu from submenu."""
        # Disable all other menus first
        if self.instructions_menu:
            self.instructions_menu.disable()
        if self.difficulty_menu:
            self.difficulty_menu.disable()
            
        # Now enable the main menu
        if self.menu:
            self.menu.enable()
    
    def handle_events(self):
        """Process pygame events such as key presses and quit events."""
        events = pygame.event.get()
        
        for event in events:
            # Check for quit event
            if event.type == pygame.QUIT:
                self.running = False
            
            # Handle menu events if in menu state
            if self.state == MENU:
                if self.instructions_menu and self.instructions_menu.is_enabled():
                    self.instructions_menu.update(events)
                elif self.difficulty_menu and self.difficulty_menu.is_enabled():
                    self.difficulty_menu.update(events)
                else:
                    self.menu.update(events)
            
            # Only process gameplay events if not in menu
            elif self.state != MENU:
                # Check for key press events
                if event.type == pygame.KEYDOWN:
                    # Handle direction changes
                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                        self.snake.change_direction(UP)
                        self.sound_manager.play("move")
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        self.snake.change_direction(DOWN)
                        self.sound_manager.play("move")
                    elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        self.snake.change_direction(LEFT)
                        self.sound_manager.play("move")
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        self.snake.change_direction(RIGHT)
                        self.sound_manager.play("move")
                        
                    # Handle pause
                    elif event.key == pygame.K_ESCAPE:
                        if self.state == PLAYING:
                            self.state = PAUSED
                        elif self.state == PAUSED:
                            self.state = PLAYING
                        elif self.state == GAME_OVER:
                            # Allow ESC to return to menu from game over screen
                            self.state = MENU
                            
                    # Handle restart after game over or return to menu
                    elif event.key == pygame.K_RETURN:
                        if self.state == GAME_OVER:
                            self.reset_game()
                        elif self.state == PAUSED:
                            self.state = MENU
    
    def update(self):
        """Update the game state."""
        # Calculate delta time for smooth animations
        self.delta_time = self.clock.get_time() / 1000.0  # Convert to seconds
        
        # Only update if the game is actively playing
        if self.state != PLAYING:
            return
        
        # Time-based movement accumulation
        self.move_time_accumulator += self.delta_time
        
        # Check if snake's animation is complete before attempting next move
        animation_complete = True  # Default to true if animations are disabled
        
        # Update snake animations
        if self.animations_enabled and SMOOTH_MOVEMENT:
            # Calculate precise animation timing to ensure smooth transitions
            # Get remaining time until next move to better sync animation speed
            time_until_next_move = max(0.001, self.move_interval - self.move_time_accumulator)
            completion_target = self.move_interval * ANIMATION_COMPLETE_THRESHOLD
            
            # Calculate a dynamic factor that adapts based on how close we are to the next move
            # This ensures animations complete just before the next movement
            animation_factor = ANIMATION_OVERSHOOT_FACTOR / completion_target
            
            # Further adjust the speed dynamically based on how close we are to the next move
            # This creates a more responsive feel as we approach movement time
            time_factor = 1.0 + max(0, (self.move_interval - time_until_next_move) / self.move_interval)
            dynamic_speed = self.animation_speed * animation_factor * time_factor
            
            # Update animation and check if it's complete
            animation_complete = self.snake.update_animation(self.delta_time, dynamic_speed)
        
        # Check if it's time to move the snake and animation is complete
        should_move = False
        if self.move_time_accumulator >= self.move_interval and animation_complete:
            should_move = True
            # Reset accumulator but keep remainder for smooth timing
            self.move_time_accumulator %= self.move_interval
            
            # Update frame accumulator for backward compatibility
            self.move_accumulator += 1
            if self.move_accumulator >= self.move_frames:
                self.move_accumulator = 0
        
        # Move the snake if it's time to do so
        if should_move:
            self.snake.move()
            
            # Check if the snake has eaten food
            if self.snake.get_head_position() == self.food.get_position():
                self.snake.grow()
                self.food.spawn(self.snake.get_body())
                self.score += 1
                self.sound_manager.play("eat")
                
                # Update high score if needed
                if self.score > self.high_score:
                    self.high_score = self.score
                    # Also update difficulty-specific high score
                    self.difficulty_high_scores[self.difficulty] = self.high_score
            
            # Check for collisions that end the game
            if (self.snake.check_collision_with_self() or 
                self.snake.check_collision_with_boundaries(GRID_WIDTH, GRID_HEIGHT)):
                # Game over state
                self.state = GAME_OVER
                self.sound_manager.play("game_over")
                
                # Update and save high score if needed
                if self.score > self.high_score:
                    self.high_score = self.score
                    # Also update difficulty-specific high score
                    self.difficulty_high_scores[self.difficulty] = self.high_score
                    # Save high score immediately
                    from utils import save_high_score
                    save_high_score(self.high_score, difficulty=self.difficulty)
    
    def render(self):
        """Render the game state to the screen."""
        # Clear the screen first
        self.screen.fill(BLACK)
        
        # Display menu if in menu state
        if self.state == MENU:
            # Make sure a menu is active - if not, default to main menu
            if (not (self.instructions_menu and self.instructions_menu.is_enabled()) and
                not (self.difficulty_menu and self.difficulty_menu.is_enabled()) and
                self.menu and not self.menu.is_enabled()):
                self.menu.enable()
                
            # Draw the appropriate menu
            if self.instructions_menu and self.instructions_menu.is_enabled():
                self.instructions_menu.draw(self.screen)
            elif self.difficulty_menu and self.difficulty_menu.is_enabled():
                self.difficulty_menu.draw(self.screen)
            else:
                self.menu.draw(self.screen)
        else:
            # Draw the header bar for score display
            self._draw_header()
            
            # Draw the snake (offsetting for header)
            self._draw_snake()
            
            # Draw the food (offsetting for header)
            self._draw_food()
            
            # Draw game over screen if needed
            if self.state == GAME_OVER:
                self._draw_game_over()
                
            # Draw pause screen if needed
            if self.state == PAUSED:
                self._draw_pause()
        
        # Update the display
        pygame.display.flip()
    
    def _draw_header(self):
        """Draw the header bar with score information."""
        # Draw header background
        header_rect = pygame.Rect(0, 0, WINDOW_WIDTH, HEADER_HEIGHT)
        pygame.draw.rect(self.screen, HEADER_COLOR, header_rect)
        
        # Draw border between header and game area
        border_rect = pygame.Rect(0, HEADER_HEIGHT - HEADER_BORDER_WIDTH, WINDOW_WIDTH, HEADER_BORDER_WIDTH)
        pygame.draw.rect(self.screen, HEADER_BORDER_COLOR, border_rect)
        
        # Draw scores in header
        self._draw_score()
    
    def _draw_score(self):
        """Draw the score in the header area."""
        # Calculate vertical center of header for text alignment
        text_y = (HEADER_HEIGHT - self.font.get_height()) // 2
        
        # Draw current score on left side
        score_text = f"Score: {self.score}"
        score_surface = self.font.render(score_text, True, WHITE)
        self.screen.blit(score_surface, (20, text_y))
        
        # Draw high score on right side
        high_score_text = f"High Score: {self.high_score}"
        high_score_surface = self.font.render(high_score_text, True, WHITE)
        self.screen.blit(high_score_surface, (WINDOW_WIDTH - high_score_surface.get_width() - 20, text_y))
        
        # Draw difficulty in the center
        difficulty_text = f"Difficulty: {self.difficulty}"
        difficulty_surface = self.font.render(difficulty_text, True, WHITE)
        self.screen.blit(difficulty_surface, 
                        ((WINDOW_WIDTH - difficulty_surface.get_width()) // 2, text_y))
    
    def _draw_grid(self):
        """Draw the grid on the screen."""
        # Grid is now hidden by default
        pass
    
    def _draw_snake(self):
        """Draw the snake on the screen."""
        # Choose which body representation to use based on animation settings
        body_to_draw = self.snake.get_visual_body() if (self.animations_enabled and SMOOTH_MOVEMENT) else self.snake.get_body()
        
        # First, draw the snake body as a continuous shape
        if len(body_to_draw) > 1:
            # Get pixel positions for all segments
            pixel_positions = []
            for segment in body_to_draw:
                x, y = segment
                # Convert grid coordinates to pixel coordinates (center of grid cell)
                if isinstance(x, float) and isinstance(y, float):
                    px = int(x * GRID_SIZE + GRID_SIZE // 2)
                    py = int(y * GRID_SIZE + GRID_SIZE // 2) + HEADER_HEIGHT  # Offset for header
                else:
                    px = int(x * GRID_SIZE + GRID_SIZE // 2)
                    py = int(y * GRID_SIZE + GRID_SIZE // 2) + HEADER_HEIGHT  # Offset for header
                pixel_positions.append((px, py))
            
            # Calculate segment size (slightly smaller than grid for smooth appearance)
            segment_radius = GRID_SIZE // 2 - 2
            
            # Draw continuous body (except head)
            if len(pixel_positions) > 1:
                # Draw body segments with lines
                for i in range(1, len(pixel_positions)):
                    # Get gradient color for this segment
                    if self.animations_enabled and self.gradient_colors:
                        color = self.snake.get_gradient_color(i)
                    else:
                        color = SNAKE_BODY_COLOR
                    
                    # Draw a thick line between segments
                    start_pos = pixel_positions[i]
                    end_pos = pixel_positions[i-1]
                    
                    # Draw line with rounded caps
                    pygame.draw.line(self.screen, color, start_pos, end_pos, segment_radius * 2)
                    
                    # Draw circle at joint to smooth appearance
                    pygame.draw.circle(self.screen, color, start_pos, segment_radius)
                    
                    # Draw the first segment circle (at the end of body)
                    if i == len(pixel_positions) - 1:
                        pygame.draw.circle(self.screen, color, end_pos, segment_radius)
                
                # Add subtle highlight effect on top of the snake body
                if self.animations_enabled and self.visual_effects:
                    for i in range(1, len(pixel_positions), 3):  # Add highlight every few segments
                        highlight_pos = pixel_positions[i]
                        highlight_radius = segment_radius // 3
                        highlight_surface = pygame.Surface((highlight_radius * 2, highlight_radius * 2), pygame.SRCALPHA)
                        pygame.draw.circle(highlight_surface, (255, 255, 255, 90), (highlight_radius, highlight_radius), highlight_radius)
                        self.screen.blit(highlight_surface, (highlight_pos[0] - highlight_radius, highlight_pos[1] - highlight_radius))
            
            # Draw the head separately
            head_pos = pixel_positions[0]
            head_rect = pygame.Rect(
                head_pos[0] - segment_radius,
                head_pos[1] - segment_radius,
                segment_radius * 2,
                segment_radius * 2
            )
            
            # Get head color
            head_color = self.snake.get_head_color() if (self.animations_enabled and self.gradient_colors) else SNAKE_HEAD_COLOR
            
            # Draw head with direction indication
            if SNAKE_HEAD_ROTATION and self.animations_enabled:
                self._draw_snake_head_smooth(head_pos, segment_radius, self.snake.direction, head_color)
            else:
                # Draw a slightly larger circle for the head
                pygame.draw.circle(self.screen, head_color, head_pos, segment_radius + 2)
        else:
            # Fallback for single segment (just the head)
            segment = body_to_draw[0]
            x, y = segment
            if isinstance(x, float) and isinstance(y, float):
                rect = pygame.Rect(
                    int(x * GRID_SIZE), 
                    int(y * GRID_SIZE) + HEADER_HEIGHT,  # Offset for header
                    GRID_SIZE, 
                    GRID_SIZE
                )
            else:
                rect = pygame.Rect(
                    x * GRID_SIZE, 
                    y * GRID_SIZE + HEADER_HEIGHT,  # Offset for header
                    GRID_SIZE, 
                    GRID_SIZE
                )
            
            head_color = self.snake.get_head_color() if (self.animations_enabled and self.gradient_colors) else SNAKE_HEAD_COLOR
            pygame.draw.rect(self.screen, head_color, rect)
            pygame.draw.rect(self.screen, BLACK, rect, 1)
    
    def _draw_snake_head_smooth(self, position, radius, direction, color=None):
        """
        Draw a smooth snake head with direction indicated by eyes.
        
        Args:
            position: The center position of the head as (x, y)
            radius: The radius of the head
            direction: The current direction as (dx, dy)
            color: Custom color for the head (optional)
        """
        # Use provided color or default
        head_color = color if color else SNAKE_HEAD_COLOR
        
        # Draw the head circle
        pygame.draw.circle(self.screen, head_color, position, radius + 2)
        
        # Determine eye positions based on direction
        dx, dy = direction
        eye_radius = radius // 4
        eye_offset = radius // 2
        
        if dx == 1:  # RIGHT
            eye_pos_1 = (position[0] + eye_offset, position[1] - eye_offset)
            eye_pos_2 = (position[0] + eye_offset, position[1] + eye_offset)
        elif dx == -1:  # LEFT
            eye_pos_1 = (position[0] - eye_offset, position[1] - eye_offset)
            eye_pos_2 = (position[0] - eye_offset, position[1] + eye_offset)
        elif dy == -1:  # UP
            eye_pos_1 = (position[0] - eye_offset, position[1] - eye_offset)
            eye_pos_2 = (position[0] + eye_offset, position[1] - eye_offset)
        else:  # DOWN
            eye_pos_1 = (position[0] - eye_offset, position[1] + eye_offset)
            eye_pos_2 = (position[0] + eye_offset, position[1] + eye_offset)
        
        # Draw eyes
        pygame.draw.circle(self.screen, BLACK, eye_pos_1, eye_radius)
        pygame.draw.circle(self.screen, BLACK, eye_pos_2, eye_radius)
        
        # Add white highlights to eyes if visual effects are enabled
        if self.visual_effects:
            highlight_radius = eye_radius // 2
            highlight_offset = eye_radius // 3
            
            # Eye highlight positions
            highlight_pos_1 = (eye_pos_1[0] - highlight_offset, eye_pos_1[1] - highlight_offset)
            highlight_pos_2 = (eye_pos_2[0] - highlight_offset, eye_pos_2[1] - highlight_offset)
            
            # Draw eye highlights
            pygame.draw.circle(self.screen, WHITE, highlight_pos_1, highlight_radius)
            pygame.draw.circle(self.screen, WHITE, highlight_pos_2, highlight_radius)
    
    def _draw_food(self):
        """Draw the food on the screen."""
        x, y = self.food.get_position()
        # Calculate the center position of the food
        center_x = int(x * GRID_SIZE + GRID_SIZE // 2)
        center_y = int(y * GRID_SIZE + GRID_SIZE // 2) + HEADER_HEIGHT  # Offset for header
        
        # Draw the food with a basic animation if enabled
        if self.animations_enabled:
            # Make the food pulsate slightly
            pulse = math.sin(pygame.time.get_ticks() * 0.01) * 0.2 + 0.8  # 0.6 to 1.0
            radius = int((GRID_SIZE // 2) * pulse)
            
            # Draw the main food circle
            pygame.draw.circle(self.screen, FOOD_COLOR, (center_x, center_y), radius)
            
            # Add a subtle glow effect
            glow_radius = radius + 4
            
            # Semi-transparent glow
            glow_surface = pygame.Surface((glow_radius * 2, glow_radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(glow_surface, (255, 0, 0, 128), (glow_radius, glow_radius), glow_radius)
            self.screen.blit(glow_surface, (center_x - glow_radius, center_y - glow_radius))
            
            # Add a shine effect if visual effects are enabled
            if self.visual_effects:
                shine_radius = radius // 3
                shine_offset = radius // 3
                shine_pos = (center_x - shine_offset, center_y - shine_offset)
                
                # Draw shine
                shine_surface = pygame.Surface((shine_radius * 2, shine_radius * 2), pygame.SRCALPHA)
                pygame.draw.circle(shine_surface, (255, 255, 255, 180), (shine_radius, shine_radius), shine_radius)
                self.screen.blit(shine_surface, (shine_pos[0] - shine_radius, shine_pos[1] - shine_radius))
        else:
            # Draw regular food without animation - still circular for consistency
            pygame.draw.circle(self.screen, FOOD_COLOR, (center_x, center_y), GRID_SIZE // 2 - 2)
    
    def _draw_game_over(self):
        """Draw the game over screen."""
        # Create a semi-transparent overlay that covers only the game area, not the header
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT - HEADER_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))  # Black with alpha
        self.screen.blit(overlay, (0, HEADER_HEIGHT))
        
        # Draw game over text
        game_over_text = "GAME OVER"
        game_over_surface = self.font.render(game_over_text, True, WHITE)
        text_x = (WINDOW_WIDTH - game_over_surface.get_width()) // 2
        text_y = HEADER_HEIGHT + ((WINDOW_HEIGHT - HEADER_HEIGHT) - game_over_surface.get_height()) // 2 - 50
        self.screen.blit(game_over_surface, (text_x, text_y))
        
        # Draw final score
        final_score_text = f"Final Score: {self.score}"
        final_score_surface = self.font.render(final_score_text, True, WHITE)
        text_x = (WINDOW_WIDTH - final_score_surface.get_width()) // 2
        text_y = HEADER_HEIGHT + ((WINDOW_HEIGHT - HEADER_HEIGHT) - final_score_surface.get_height()) // 2
        self.screen.blit(final_score_surface, (text_x, text_y))
        
        # Draw restart instructions
        restart_text = "Press ENTER to restart"
        restart_surface = self.font.render(restart_text, True, WHITE)
        text_x = (WINDOW_WIDTH - restart_surface.get_width()) // 2
        text_y = HEADER_HEIGHT + ((WINDOW_HEIGHT - HEADER_HEIGHT) - restart_surface.get_height()) // 2 + 50
        self.screen.blit(restart_surface, (text_x, text_y))
        
        menu_text = "Press ESC for main menu"
        menu_surface = self.font.render(menu_text, True, WHITE)
        text_x = (WINDOW_WIDTH - menu_surface.get_width()) // 2
        text_y = HEADER_HEIGHT + ((WINDOW_HEIGHT - HEADER_HEIGHT) - menu_surface.get_height()) // 2 + 100
        self.screen.blit(menu_surface, (text_x, text_y))
    
    def _draw_pause(self):
        """Draw the pause screen."""
        # Create a semi-transparent overlay that covers only the game area, not the header
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT - HEADER_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))  # Black with alpha
        self.screen.blit(overlay, (0, HEADER_HEIGHT))
        
        # Draw pause text
        pause_text = "PAUSED"
        pause_surface = self.font.render(pause_text, True, WHITE)
        text_x = (WINDOW_WIDTH - pause_surface.get_width()) // 2
        text_y = HEADER_HEIGHT + ((WINDOW_HEIGHT - HEADER_HEIGHT) - pause_surface.get_height()) // 2 - 50
        self.screen.blit(pause_surface, (text_x, text_y))
        
        # Draw unpause instructions
        unpause_text = "Press ESC to resume"
        unpause_surface = self.font.render(unpause_text, True, WHITE)
        text_x = (WINDOW_WIDTH - unpause_surface.get_width()) // 2
        text_y = HEADER_HEIGHT + ((WINDOW_HEIGHT - HEADER_HEIGHT) - unpause_surface.get_height()) // 2
        self.screen.blit(unpause_surface, (text_x, text_y))
        
        # Draw menu instructions
        menu_text = "Press ENTER for main menu"
        menu_surface = self.font.render(menu_text, True, WHITE)
        text_x = (WINDOW_WIDTH - menu_surface.get_width()) // 2
        text_y = HEADER_HEIGHT + ((WINDOW_HEIGHT - HEADER_HEIGHT) - menu_surface.get_height()) // 2 + 50
        self.screen.blit(menu_surface, (text_x, text_y))
    
    def reset_game(self):
        """Reset the game to its initial state."""
        self.snake = Snake()
        # Set the difficulty for the snake's animation curves
        self.snake.set_difficulty(self.difficulty)
        self.food = Food()
        self.food.spawn(self.snake.get_body())
        self.score = 0
        self.state = PLAYING
        self.move_accumulator = 0  # Reset frame accumulator for backward compatibility
        self.move_time_accumulator = 0.0  # Reset time accumulator

    def _add_eat_effect(self, position):
        """
        Add a visual effect when food is eaten.
        Not persistent, just drawn for one frame.
        
        Args:
            position: Grid position where the food was eaten
        """
        # Convert grid position to pixel position
        x, y = position
        center_x = int(x * GRID_SIZE + GRID_SIZE // 2)
        center_y = int(y * GRID_SIZE + GRID_SIZE // 2) + HEADER_HEIGHT
        
        # Create a flash effect
        flash_radius = GRID_SIZE * 1.5
        flash_surface = pygame.Surface((flash_radius * 2, flash_radius * 2), pygame.SRCALPHA)
        
        # Gradient flash (more intense in center, fades out)
        for r in range(int(flash_radius), 0, -2):
            alpha = max(0, min(150, int(255 * (r / flash_radius))))
            pygame.draw.circle(flash_surface, (255, 255, 255, alpha), (flash_radius, flash_radius), r)
        
        # Draw the flash
        self.screen.blit(flash_surface, (center_x - flash_radius, center_y - flash_radius))
        
        # Ensure it's immediately visible by updating the display
        pygame.display.update()

    def run(self):
        """Run the main game loop."""
        last_update_time = 0  # Track time for logic updates
        update_interval = 1.0 / 120.0  # Logic updates at 120Hz for more responsive input
        accumulated_time = 0.0  # Time accumulator for fixed timestep
        
        # Main game loop
        while self.running:
            # Calculate delta time
            current_time = pygame.time.get_ticks() / 1000.0  # Current time in seconds
            frame_time = current_time - last_update_time
            last_update_time = current_time
            
            # Cap frame time to prevent spiral of death on slow systems
            frame_time = min(frame_time, 0.25)
            accumulated_time += frame_time
            
            # Handle events (always process input)
            self.handle_events()
            
            # Update game state with fixed timestep for consistent gameplay
            # This decouples input/logic updates from rendering
            while accumulated_time >= update_interval:
                self.update()
                accumulated_time -= update_interval
            
            # Render at the display's refresh rate (controlled by FIXED_FPS)
            self.render()
            
            # Control rendering speed - use fixed FPS for smooth visuals regardless of difficulty
            self.clock.tick(FIXED_FPS)
        
        # Return to caller when the game loop ends
        pygame.quit()

    def _toggle_sound(self, value):
        """Toggle sound on/off."""
        self.sound_manager.enabled = value

    def _toggle_sound_old(self, selected, value):
        """Toggle sound on/off (compatibility with older pygame-menu)."""
        self.sound_manager.enabled = value

    def _toggle_animations(self, value):
        """Toggle animations on/off - disabled as animations are always on."""
        pass

    def _toggle_animations_old(self, selected, value):
        """Toggle animations on/off (compatibility with older pygame-menu) - disabled as animations are always on."""
        pass

    def _toggle_gradient_colors(self, value):
        """Toggle gradient colors on/off - disabled as gradient colors are always on."""
        pass

    def _toggle_gradient_colors_old(self, selected, value):
        """Toggle gradient colors on/off (compatibility with older pygame-menu) - disabled as gradient colors are always on."""
        pass

    def _toggle_visual_effects(self, value):
        """Toggle visual effects on/off - disabled as visual effects are always on."""
        pass

    def _toggle_visual_effects_old(self, selected, value):
        """Toggle visual effects on/off (compatibility with older pygame-menu) - disabled as visual effects are always on."""
        pass

    def _create_instructions_menu(self):
        """Create the instructions menu."""
        # Create a menu theme
        theme = pygame_menu.themes.THEME_DARK.copy()
        theme.title_background_color = BLUE
        theme.title_font_color = WHITE
        theme.background_color = BLACK
        theme.widget_font_color = WHITE
        try:
            theme.widget_selection_effect = pygame_menu.widgets.HighlightSelection()
        except AttributeError:
            # Fallback for older pygame-menu versions
            pass
        
        # Create the menu
        self.instructions_menu = pygame_menu.Menu(
            'Instructions',
            WINDOW_WIDTH, WINDOW_HEIGHT,
            theme=theme,
            onclose=pygame_menu.events.CLOSE
        )
        
        # Add instructions text
        self.instructions_menu.add.label("Use arrow keys or WASD to move the snake.")
        self.instructions_menu.add.label("Eat food to grow and increase your score.")
        self.instructions_menu.add.label("Avoid hitting the walls or your own body.")
        self.instructions_menu.add.label("Press ESC to pause the game.")
        self.instructions_menu.add.label("")
        self.instructions_menu.add.button('Back', self._back_to_main_menu)