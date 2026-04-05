import numpy as np
import tkinter as tk
from time import time

def hex(color: int):
    return f'#{color:02x}{color:02x}{color:02x}'

def grayscale(color: str):
    RGB = int(color[1:], 16)
    return (((RGB >> 16) & 0xFF) + ((RGB >> 8) & 0xFF) + (RGB & 0xFF)) // 3

GRID = '#101010'
NOISE = 10
EVENTS = ['<B1-Motion>', '<Button-1>', '<Button-3>', '<MouseWheel>']

class Canvas(tk.Canvas):
    def __init__(self, master, pixel_size=15, callback=lambda *a, **kw: None, **kwargs):
        super().__init__(
            master,
            bg='#000000',
            highlightthickness=1,
            width=pixel_size * 28,
            height=pixel_size * 28,
            **kwargs
        )

        self.pixel_size = pixel_size
        self.callback = callback
        self.image_matrix = np.zeros((28, 28), dtype=np.uint8)

        self.pen_size = 3
        self.pen_color = hex(255)

        self.last_action_time = 0
        self.inactivity_threshold = 0.75  # 75 ms
        self.checking_inactivity = False

        self.clear_canvas()

    def activate(self):
        self.bind(EVENTS[0], self.draw_pixel)
        self.bind(EVENTS[1], self.draw_pixel)
        self.bind(EVENTS[2], self.clear_canvas)
        self.bind(EVENTS[3], self.adjust_pixel)

    def deactivate(self):
        self.clear_canvas()
        self.unbind(EVENTS[0])
        self.unbind(EVENTS[1])
        self.unbind(EVENTS[2])
        self.unbind(EVENTS[3])

    def draw_grid(self):
        for i in range(1, 28):
            pos = i * self.pixel_size
            self.create_line(pos, 0, pos, self.pixel_size * 28, fill=GRID)
            self.create_line(0, pos, self.pixel_size * 28, pos, fill=GRID)

    def draw_pixel(self, event):
        col = event.x // self.pixel_size
        row = event.y // self.pixel_size

        if not (0 <= row < 28 and 0 <= col < 28):
            return

        center = grayscale(self.pen_color)
        self.fill_pixel(row, col, self.pen_color)

        offset = (self.pen_size - 1) // 2
        for i in range(-offset, offset + 1):
            for j in range(-offset, offset + 1):
                if i == 0 and j == 0:
                    continue
                r, c = row + i, col + j
                if 0 <= r < 28 and 0 <= c < 28:
                    base = np.exp(-(i**2 + j**2) / (0.75 * offset**2)) if offset else 1
                    factor = max(0, min(1, base + np.random.uniform(-1, 1) * (NOISE / center)))
                    value = np.clip(self.image_matrix[r, c] + int(center * factor), 0, 255)
                    self.fill_pixel(r, c, hex(value))

        self.last_action_time = time()
        if not self.checking_inactivity:
            self.checking_inactivity = True
            self.after(10, self._check_idle)

    def fill_pixel(self, row, col, color):
        x1 = col * self.pixel_size
        y1 = row * self.pixel_size
        x2 = x1 + self.pixel_size
        y2 = y1 + self.pixel_size
        self.create_rectangle(x1, y1, x2, y2, fill=color, outline=color)
        self.image_matrix[row, col] = grayscale(color)

    def adjust_pixel(self, event, step=10):
        col = event.x // self.pixel_size
        row = event.y // self.pixel_size
        if 0 <= row < 28 and 0 <= col < 28:
            current = self.image_matrix[row, col]
            updated = int(np.clip(current + (step if event.delta > 0 else -step), 0, 255))
            self.fill_pixel(row, col, hex(updated))
            self.last_action_time = time()
            if not self.checking_inactivity:
                self.checking_inactivity = True
                self.after(10, self._check_idle)

    def clear_canvas(self, *args, **kwargs):
        self.delete('all')
        self.draw_grid()
        self.image_matrix.fill(0)
        self.callback()

    def set_pen(self, size=None, color=None):
        if size is not None:
            self.pen_size = int(size)
        if color is not None:
            self.pen_color = hex(int(color))

    def _check_idle(self):
        if time() - self.last_action_time >= self.inactivity_threshold:
            self.callback(self.matrix)
            self.checking_inactivity = False
        else:
            self.after(10, self._check_idle)

    @property
    def matrix(self):
        return self.image_matrix