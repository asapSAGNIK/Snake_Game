"""
Main entry point for the Snake game
"""
import os
import sys
import pygame
from game import Game
from utils import load_high_score, save_high_score


def initialize_sounds():
    """Create sound files if they don't exist."""
    # Get the absolute path to the sound directory
    base_dir = os.path.dirname(os.path.abspath(__file__))
    sound_dir = os.path.join(base_dir, "assets", "sounds")
    
    # Ensure sounds directory exists
    if not os.path.exists(sound_dir):
        try:
            os.makedirs(sound_dir)
            print(f"Created sound directory: {sound_dir}")
        except Exception as e:
            print(f"ERROR: Could not create sound directory: {e}")
            return False
    
    # Check if sound files need to be created
    eat_sound = os.path.join(sound_dir, "eat.wav")
    game_over_sound = os.path.join(sound_dir, "game_over.wav")
    move_sound = os.path.join(sound_dir, "move.wav")
    
    # Check if any sound files are missing
    files_exist = (
        os.path.exists(eat_sound) and
        os.path.exists(game_over_sound) and
        os.path.exists(move_sound)
    )
    
    if not files_exist:
        print("Sound files missing, generating them now...")
        try:
            # Import and run the sound generation script
            from create_sounds import main as create_sounds
            success = create_sounds()
            if not success:
                print("WARNING: Sound generation was not completely successful.")
                print("Some sound features may not work correctly.")
                return False
            return True
        except ImportError as e:
            print(f"ERROR: Could not import sound generation module: {e}")
            print("Make sure numpy and scipy are installed: pip install numpy scipy")
            return False
        except Exception as e:
            print(f"ERROR: Failed to generate sound files: {e}")
            print("Game will continue without sound effects.")
            return False
    
    # Verify the sound files are valid
    try:
        pygame.mixer.init()
        for sound_file in [eat_sound, game_over_sound, move_sound]:
            try:
                # Try to load each sound file
                sound = pygame.mixer.Sound(sound_file)
                print(f"Verified sound file: {os.path.basename(sound_file)}")
            except Exception as e:
                print(f"WARNING: Sound file {sound_file} is invalid: {e}")
                return False
        return True
    except Exception as e:
        print(f"ERROR: Could not initialize sound system: {e}")
        return False


def main():
    """
    Main function to run the Snake game.
    """
    # Initialize pygame
    try:
        pygame.init()
        print("Pygame initialized successfully.")
    except Exception as e:
        print(f"ERROR: Failed to initialize pygame: {e}")
        return
    
    # Initialize sound files if needed
    sound_initialized = initialize_sounds()
    if not sound_initialized:
        print("WARNING: Sound initialization failed. Game will run without sound.")
    
    try:
        # Create and run the game
        game = Game(sound_enabled=sound_initialized)
        
        # Load the high score
        game.high_score = load_high_score()
        
        # Run the game loop
        game.run()
        
        # Save all difficulty high scores when the game exits
        for difficulty, score in game.difficulty_high_scores.items():
            save_high_score(score, difficulty=difficulty)
    except Exception as e:
        print(f"ERROR: Game crashed: {e}")
    finally:
        # Clean up pygame
        pygame.quit()
        print("Game exited.")


if __name__ == "__main__":
    # Game initialization
    main() 
