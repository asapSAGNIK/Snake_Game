# 🐍 Snake Game

A modern implementation of the classic Snake game built with Python and Pygame, featuring smooth animations and enhanced visual effects.

![Python Version](https://img.shields.io/badge/python-3.x-blue.svg)
![Pygame](https://img.shields.io/badge/pygame-2.x-red.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)




https://github.com/user-attachments/assets/3bd671c9-7842-4501-81b3-affffa29183d


## ✨ Features

- 🎮 Smooth, frame-independent movement system
- 🌈 Dynamic gradient colors for the snake
- 🎵 Custom sound effects
- 📊 Difficulty-based high score system
- 🎨 Modern visual effects and animations
- ⚡ Responsive controls with WASD/Arrow keys
- ⏸️ Pause and resume functionality
- 🏆 High score tracking per difficulty level

## 🚀 Getting Started

### Prerequisites

- Python 3.x
- pip (Python package installer)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/snake-game.git
   cd snake-game
   ```

2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the game:
   ```bash
   python snake_game/main.py
   ```

## 🎮 How to Play

1. **Start Game**: Select 'Play' from the main menu
2. **Choose Difficulty**:
   - Easy (Slow Speed)
   - Medium (Normal Speed)
   - Hard (Fast Speed)

### Controls

- **Movement**: Arrow keys or WASD
- **Pause**: ESC key
- **Resume**: ESC key when paused
- **Restart**: ENTER key (after game over)
- **Return to Menu**: ESC key (when game over)

## 🏗️ Project Structure

```
snake_game/
├── main.py          # Game entry point
├── game.py          # Main game logic and rendering
├── snake.py         # Snake class and movement mechanics
├── food.py          # Food spawning and collision
├── settings.py      # Game constants and configurations
├── utils.py         # Utility functions
└── assets/          # Game resources
    └── sounds/      # Sound effects
```

## 🎯 Game Mechanics

- **Frame-Independent Movement**: Smooth movement regardless of frame rate
- **Progressive Difficulty**: Speed increases with each difficulty level
- **Score System**: Points awarded for each food item collected
- **Collision Detection**: Precise boundary and self-collision checking
- **Visual Feedback**: Dynamic colors and effects for game events

## 🔧 Technical Details

### Key Components

- **Game Engine**: Built with Pygame for efficient 2D rendering
- **Animation System**: Custom interpolation for smooth movement
- **Sound System**: Dynamic sound generation and playback
- **State Management**: Robust game state handling
- **Menu System**: Intuitive menu navigation with pygame-menu

### Performance Features

- Time-based movement system for consistent gameplay
- Optimized collision detection
- Efficient rendering with double buffering
- Smooth animation transitions

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create a new branch (`git checkout -b feature/improvement`)
3. Make your changes
4. Commit your changes (`git commit -am 'Add new feature'`)
5. Push to the branch (`git push origin feature/improvement`)
6. Create a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Inspired by the classic Snake game
- Built with [Pygame](https://www.pygame.org/)
- Menu system powered by [pygame-menu](https://pygame-menu.readthedocs.io/)



## Project Structure

- `main.py`: Entry point to the game
- `game.py`: Main game class
- `snake.py`: Snake class
- `food.py`: Food class
- `settings.py`: Game constants and settings
- `utils.py`: Utility functions
- `assets/`: Directory for images, sounds, and fonts 
