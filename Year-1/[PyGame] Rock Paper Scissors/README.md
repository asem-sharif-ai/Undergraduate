# Rock Paper Scissors - Simulation

> An autonomous simulation where Rock, Paper, and Scissors pieces roam the screen, collide, and convert each other in real time - built with Pygame and sprite-based collision detection.

---

## Demo

![Simulation](demo.gif)

---

## Overview

Rather than a turn-based game, this is a **zero-player simulation** - all three types move independently across the screen with randomized velocities, and when two opposing pieces collide, the loser converts to the winner's type. The last surviving type wins.

Built in year 1 as an exploration of object-oriented design, sprite physics, and collision resolution in Python.

---

## Mechanics

### Autonomous Movement

Each piece is initialized with a random velocity on both axes:
```
velocity_x = random.uniform(-2.5, 5)
velocity_y = random.uniform(-2.5, 5)
```

Every frame, a small random nudge is added to each velocity to simulate natural, unpredictable drift - preventing pieces from moving in perfectly straight lines:
```
velocity_x += random.uniform(-0.1, 0.1)
velocity_y += random.uniform(-0.1, 0.1)
```

### Boundary Reflection

When a piece hits a screen edge, its velocity on that axis is inverted - simulating a bounce:
```
if left <= 0 or right >= WIDTH:   velocity_x *= -1
if top  <= 0 or bottom >= HEIGHT: velocity_y *= -1
```

### Collision Resolution

Collisions are detected using `pygame.sprite.groupcollide()`. When two pieces collide, the RPS rule is applied and the loser converts:

| Piece A | Piece B | Result |
|---------|---------|--------|
| Rock | Scissors | Scissors → Rock |
| Scissors | Paper | Paper → Scissors |
| Paper | Rock | Rock → Paper |

Conversion is instant - the losing piece changes its type and image in place without being removed from the group.

### Help System

To prevent one type from going extinct too early, a configurable help system spawns additional pieces of the minority type every N seconds:
```python
HELP = {'Apply': True, 'Number': 2, 'Duration': 4}
```

Every 4 seconds, 2 pieces of the least-represented type are added to the arena.

### Win Conditions

The simulation ends when either:
- The timer runs out → winner is the type with the highest count
- All pieces convert to one type → that type wins immediately

---

## Configuration
```python
PIECE_NUMBER = 15     # pieces per type (15 Rock, 15 Paper, 15 Scissors)
R            = 40     # sprite size in pixels
GAME_TIME    = 15     # simulation duration in seconds

HELP = {
    'Apply'   : True,  # enable/disable help system
    'Number'  : 2,     # pieces to spawn per interval
    'Duration': 4      # interval in seconds
}
```

---

## Controls

| Key | Action |
|-----|--------|
| SPACE | Reset simulation |
| TAB | Freeze for 1 second |
| ESC | Quit |

---

## Installation

**Requirements**
- Python 3.8+
- pygame
- Sprite images: `_Rock.png`, `_Paper.png`, `_Scissors.png` in the same directory
```bash
pip install pygame
```

## Run
```bash
python RPS.py
```

---

## Project Structure
```
Rock Paper Scissors/
├── RPS.py           # Full simulation source
├── README.md        # Project documentation
├── demo.gif         # Simulation demo
├── _Rock.png        # Rock sprite
├── _Paper.png       # Paper sprite
└── _Scissors.png    # Scissors sprite
```