# Color Palette Generator

> A mathematical color space explorer built with Pygame - generates RGBA palettes from trigonometric and algebraic formulas, with real-time pixel inspection and binary matrix visualization.

---

## Demo

https://github.com/asem-sharif-ai/Undergraduate/Year-1/[PyGame] RGBA Palette Generator/Preview.mp4

---

## Overview

Color Palette Generator renders an L×L pixel grid where every pixel's RGBA value is computed from its (x, y) position using mathematical functions - not hardcoded colors or gradients. The result is a continuous color space that changes shape depending on the active palette model.

Hover over any pixel to inspect its RGBA tuple, its binary matrix representation (each channel as an 8-bit vector), and a human-readable color classification. Pin a pixel to lock its values on screen.

Built in year 2 as an exploration of color theory, binary representation, and mathematical modeling of visual space.

---

## Math & Color Models

Every palette maps pixel coordinates (x, y) within an L×L grid to an RGBA value using a different formula.

### RGB Model

Each channel is computed from the pixel's relative position in the grid:
```
R = 255 × (1 - x/L) × (1 - y/L)
G = 255 × (y/L)     × (1 - x/L)
B = 255 × (x/L)     × (1 - y/L)
```

Moving across x increases Blue, moving across y increases Green, and the top-left corner maximizes Red.

### RGBA Model

Same as RGB but with a position-dependent alpha channel that fades toward the bottom-right corner:
```
A = 255 - (10 × (x + y) / (L / 2))
```

### FAV Model (Trigonometric)

Uses `sin` and `cos` to produce a smooth, wave-like color field:
```
R = sin(x/L × π) × 255
G = cos(y/L × π) × 255
B = (sin(x/L × π) + cos(y/L × π)) × 127 + 128
```

### BW Model (Algebraic)

Computes luminance from a difference-of-squares expression:
```
L_value = ((y + x) × (y - x)) / (√2 × L)
R = G = B = L_value
```

### Single & Dual Channel Models

For `R`, `G`, `B`, `W`, `K`, `RG`, `GB`, `RB` - channels are fixed at 255 or 0, and alpha fades diagonally:
```
A = 255 - ((x + y) / (L / 50))
```

---

## Binary Matrix Visualization

Every pixel's RGBA value is decomposed into a 4×8 binary matrix - one row per channel, each row being the 8-bit binary representation of that channel's value (0–255):
```
R : [1 0 1 1 0 0 1 0]
G : [0 1 0 0 1 1 0 1]
B : [1 1 0 0 0 1 0 0]
A : [1 1 1 1 1 1 1 1]
```

This is displayed live on screen as you hover or pin pixels.

---

## Color Classification

The `detect()` function classifies any RGBA tuple into a human-readable label by comparing channel dominance and spread:

| Condition | Label |
|-----------|-------|
| All channels ≤ 10 | Black |
| All channels close, max ≤ 200 | Grey-based |
| All channels close, max ≥ 240 | White |
| One channel dominant by ≥ 100 | Based on R / G / B |
| Two channels dominant | Based on R&G / G&B / R&B |

---

## Palette Models

| Key | Model | Description |
|-----|-------|-------------|
| `RGB` | RGB | Full color space from position |
| `RGBA` | RGBA | RGB with position-based transparency |
| `R` | Red | Red channel only, fading alpha |
| `G` | Green | Green channel only, fading alpha |
| `B` | Blue | Blue channel only, fading alpha |
| `W` | White | All channels 255, fading alpha |
| `K` | Black | All channels 0, fading alpha |
| `RG` | Yellow | Red + Green fixed, fading alpha |
| `GB` | Cyan | Green + Blue fixed, fading alpha |
| `RB` | Magenta | Red + Blue fixed, fading alpha |
| `BW` | Black & White | Algebraic luminance formula |
| `FAV` | Trigonometric | Sin/Cos wave-based color field |

---

## Controls

| Input | Action |
|-------|--------|
| Move mouse | Inspect pixel under cursor |
| Left click | Pin pixel - lock values on screen |
| Right click | Unpin - return to cursor mode |
| Middle click | Cycle to next palette model |
| Scroll wheel | Jump pin to a random position |
| ESC | Quit |

---

## Installation

**Requirements**
- Python 3.8+
- pygame
- numpy
```bash
pip install pygame numpy
```

## Run
```bash
python Main.py
```

---

## Configuration
```python
# Main.py

P = 'FAV'   # Active palette - see palette map above
L = 650     # Window size in pixels (recommended: 551–751)
```

---

## Project Structure
```
Color Palette Generator/
├── Main.py              # Entry point - set palette and window size
├── GeneratePALETTE.py   # Main loop, rendering, interaction
├── ColorPIXEL.py        # RGBA formulas for all palette models
├── Functions.py         # Binary vectors, matrix display, color detection
├── Utils.py             # Null texture generator, cleanup utilities
├── README.md            # Project documentation
└── Preview.mp4          # Demo video
```

---

## Course

**Introduction to Programming / Digital Media**
Faculty of Artificial Intelligence, Menoufia University - Year 2