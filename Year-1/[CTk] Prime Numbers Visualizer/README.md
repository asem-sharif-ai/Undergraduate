# Prime Numbers Visualizer

A desktop GUI that highlights prime numbers in a color-coded grid using the Sieve of Eratosthenes and Binary Search.

![Python](https://img.shields.io/badge/Python-3.x-blue) ![customtkinter](https://img.shields.io/badge/GUI-customtkinter-blue)

## About

Renders numbers from 0 to N in a scrollable grid. Prime numbers are highlighted in gold, non-primes in dark green. Supports toggling number labels and adjusting grid column count.

## Algorithms

- **Sieve of Eratosthenes** — finds all primes up to N in O(n log log n)
- **Binary Search** — checks if each number is prime at render time in O(log n)

## Install
```bash
pip install numpy customtkinter
```

## Usage
```python
Primes(numbers_range=1000, line_step=25, hide_numbers=False)

# numbers_range  →  upper limit (100-10,000)
# line_step      →  columns per row (10-30)
# hide_numbers   →  hide labels, show colors only
```

## Color legend

| Color | Meaning |
|-------|---------|
| 🟨 Gold | Prime |
| 🟩 Dark green | Composite |