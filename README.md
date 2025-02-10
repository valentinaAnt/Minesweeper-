# Minesweeper-
Description

This is a Python-based Minesweeper clone built using the Pygame library. The game features multiple difficulty levels, interactive gameplay, a timer, and a leaderboard to track the best scores.

Features

Three difficulty levels: Easy, Medium, Hard

Random mine placement with number hints

Flagging system to mark suspected mines

Timer that tracks the game duration

Leaderboard to store best times per difficulty

Background music and sound effects

Graphical interface using Pygame

Installation

Prerequisites

Make sure you have Python installed (version 3.x recommended). You also need to install Pygame.

pip install pygame

How to Run

Clone the repository:

git clone https://github.com/yourusername/minesweeper-clone.git
cd minesweeper-clone

Run the game:

python main.py

Controls

Left Click - Reveal a tile

Right Click - Place/Remove a flag

Game Rules

Reveal all non-mine tiles to win

Clicking on a mine ends the game

Numbered tiles indicate how many mines are adjacent

File Structure

minesweeper-clone/
│── assets/                  # Game images and icons
│── audios/                  # Sound effects and background music
│── elements.py              # Game elements and tile assets
│── main.py                  # Main game loop and logic
│── sprites.py               # Board and tile mechanics
│── README.md                # Project documentation

Future Improvements

Add more game modes (e.g., timed challenge, infinite mode)

Implement online multiplayer support

Enhance UI with animations and better visuals
