# Buster Bros Remake - JavaScript Version

This is a JavaScript conversion of the original Python/Pygame Buster Bros game created by Akeen Zhong.

## Game Description

Buster Bros is an arcade-style balloon-popping game where you control a character that can shoot bullets to pop balloons. Balloons split into smaller ones when hit, and you must clear all balloons to advance levels.

## Features

- **Multiple Levels**: 5 progressively difficult levels with different balloon configurations
- **Balloon Physics**: Balloons bounce off walls and split when hit
- **Player Movement**: Use arrow keys to move left and right
- **Shooting**: Press spacebar to shoot bullets upward
- **Lives System**: You have 3 lives, lose one when touching a balloon
- **Score Tracking**: Keep track of how many balloons you've popped
- **Leaderboard**: High scores are saved locally using browser storage
- **Pause Function**: Press 'P' to pause the game
- **Name Entry**: Enter your name to save your score

## How to Play

1. **Movement**: Use the left and right arrow keys to move your character
2. **Shooting**: Press the spacebar to shoot bullets upward
3. **Objective**: Pop all balloons to advance to the next level
4. **Avoidance**: Don't touch the balloons or you'll lose a life
5. **Pause**: Press 'P' to pause the game

## Balloon Types

- **Large Balloons (Red)**: Split into 2 medium balloons when hit
- **Medium Balloons (Green)**: Split into 2 small balloons when hit  
- **Small Balloons (Blue)**: Disappear when hit

## Level Progression

- **Level 1**: 6 small balloons
- **Level 2**: 1 large balloon
- **Level 3**: 6 medium balloons
- **Level 4**: 2 large balloons + 5 small balloons
- **Level 5**: 6 large balloons
- **Level 6+**: Victory!

## How to Run

1. Open `index.html` in a modern web browser
2. The game will start automatically
3. Click "Start Game" to begin
4. Enter your name when prompted
5. Use the controls described above to play

## Technical Details

- **Language**: JavaScript (ES6+)
- **Graphics**: HTML5 Canvas
- **Storage**: Local Storage for leaderboard
- **No Dependencies**: Pure JavaScript, no external libraries required
- **Browser Compatibility**: Works in all modern browsers

## File Structure

```
javaRewrite/
├── index.html      # Main HTML file with game interface
├── game.js         # Main game logic and JavaScript code
└── README.md       # This file
```

## Differences from Python Version

- Uses HTML5 Canvas instead of Pygame
- Local storage instead of file-based leaderboard
- Web-based interface instead of desktop application
- Simplified graphics (circles instead of sprite images)
- Browser-based sound (not implemented in this version)

## Controls Summary

- **Arrow Keys**: Move left/right
- **Spacebar**: Shoot bullet
- **P**: Pause game
- **Mouse**: Click buttons in menus

Enjoy the game! 