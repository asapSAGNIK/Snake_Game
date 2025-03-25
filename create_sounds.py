"""
Script to generate sound effects for the Snake game.
This creates simple synthesized sounds since we can't directly upload audio files.
"""
import os
import sys
import pygame
import numpy as np
from scipy.io import wavfile


def ensure_dir(file_path):
    """Ensure that the directory for the file exists."""
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        try:
            os.makedirs(directory)
            print(f"Created directory: {directory}")
        except Exception as e:
            print(f"Error creating directory {directory}: {e}")
            return False
    return True


def create_eat_sound(file_path, sample_rate=44100):
    """Create a sound effect for eating food."""
    try:
        duration = 0.3  # seconds
        t = np.linspace(0, duration, int(sample_rate * duration), False)
        
        # Create a sound that goes up in frequency (like a "pop")
        freq_start = 300
        freq_end = 1200
        frequency = np.linspace(freq_start, freq_end, len(t))
        
        # Create a sound wave that fades out
        signal = 0.5 * np.sin(2 * np.pi * frequency * t) * np.exp(-5 * t)
        
        # Convert to 16-bit data
        signal = (signal * 32767).astype(np.int16)
        
        # Save as a WAV file
        if ensure_dir(file_path):
            wavfile.write(file_path, sample_rate, signal)
            print(f"Created eat sound: {file_path}")
            return True
        return False
    except Exception as e:
        print(f"Error creating eat sound: {e}")
        return False


def create_game_over_sound(file_path, sample_rate=44100):
    """Create a sound effect for game over."""
    try:
        duration = 1.0  # seconds
        t = np.linspace(0, duration, int(sample_rate * duration), False)
        
        # Create a sound that goes down in frequency (sad sound)
        freq_start = 400
        freq_end = 150
        frequency = np.linspace(freq_start, freq_end, len(t))
        
        # Create a sound wave
        signal = 0.5 * np.sin(2 * np.pi * frequency * t) * np.exp(-2 * t)
        
        # Add a bit of noise for texture
        noise = 0.1 * np.random.normal(0, 1, len(t))
        signal = signal + noise * np.exp(-5 * t)
        
        # Convert to 16-bit data
        signal = (signal * 32767).astype(np.int16)
        
        # Save as a WAV file
        if ensure_dir(file_path):
            wavfile.write(file_path, sample_rate, signal)
            print(f"Created game over sound: {file_path}")
            return True
        return False
    except Exception as e:
        print(f"Error creating game over sound: {e}")
        return False


def create_move_sound(file_path, sample_rate=44100):
    """Create a sound effect for snake movement."""
    try:
        duration = 0.1  # seconds
        t = np.linspace(0, duration, int(sample_rate * duration), False)
        
        # Create a very short, quiet sound
        frequency = 200
        signal = 0.1 * np.sin(2 * np.pi * frequency * t) * np.exp(-20 * t)
        
        # Convert to 16-bit data
        signal = (signal * 32767).astype(np.int16)
        
        # Save as a WAV file
        if ensure_dir(file_path):
            wavfile.write(file_path, sample_rate, signal)
            print(f"Created move sound: {file_path}")
            return True
        return False
    except Exception as e:
        print(f"Error creating move sound: {e}")
        return False


def verify_sound_file(file_path):
    """Verify that a sound file exists and is playable."""
    if not os.path.exists(file_path):
        print(f"Sound file does not exist: {file_path}")
        return False
    
    try:
        # Try to load the sound with pygame
        pygame.mixer.init()
        sound = pygame.mixer.Sound(file_path)
        # If we get here, the sound loaded successfully
        return True
    except Exception as e:
        print(f"Error verifying sound file {file_path}: {e}")
        return False
    

def main():
    """Generate all sound effects."""
    print("Generating sound effects...")
    
    # Use absolute paths for more reliable file operations
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Create sounds
    eat_sound_path = os.path.join(base_dir, "assets", "sounds", "eat.wav")
    game_over_sound_path = os.path.join(base_dir, "assets", "sounds", "game_over.wav")
    move_sound_path = os.path.join(base_dir, "assets", "sounds", "move.wav")
    
    # Track success of sound creation
    success = True
    
    # Create and verify each sound
    if not create_eat_sound(eat_sound_path) or not verify_sound_file(eat_sound_path):
        success = False
    
    if not create_game_over_sound(game_over_sound_path) or not verify_sound_file(game_over_sound_path):
        success = False
    
    if not create_move_sound(move_sound_path) or not verify_sound_file(move_sound_path):
        success = False
    
    if success:
        print("Sound effects generated successfully!")
        return True
    else:
        print("WARNING: Some sound effects could not be generated.")
        return False


if __name__ == "__main__":
    # Initialize pygame for sound verification
    pygame.init()
    result = main()
    pygame.quit()
    
    # Return exit code based on success
    sys.exit(0 if result else 1) 