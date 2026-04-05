# pip install numpy customtkinter

import numpy as np
import tkinter as tk
import customtkinter as ctk

A, X, Y, XY = ('A', 'ew', 'ns', 'nsew')
NRM, DIS, CNT = ('normal', 'disabled', 'center')

C0, C1, C2, C3 = (
    '#101010',
    '#FFFFFF',
    '#004030',
    '#D4A019',
)

DSFD = {
    'fg_color': '#101010',
    'scrollbar_fg_color': '#101010',
    'scrollbar_button_color': '#151515',
    'scrollbar_button_hover_color': '#202020'
}

class Primes(ctk.CTk):
    def __init__(self, numbers_range: int=1000, line_step: int=10, hide_numbers: bool=False):
        super().__init__(fg_color=C0)

        self.n = min(max(int(numbers_range), 100), 10_000)
        self.l = min(max(int(line_step), 10), 30)
        self.show = not hide_numbers

        self.start_up()
        self.mainloop()

    def start_up(self):
        self.geometry(f'{900}x{600}')

        self.primes = self.find_primes(self.n)
        self.title(
            f'Prime Numbers Visualization | [{sum(len(l) for l in self.primes)}] Prime Numbers Found Within [{self.n}].')
        
        self.numbers_frame = ctk.CTkScrollableFrame(self, **DSFD)
        self.numbers_frame.pack(padx=(10, 0), pady=10, fill='both', expand=True)
        
        self.numbers_frame.rowconfigure(index=len(self.primes), weight=1, uniform=A)
        self.numbers_frame.columnconfigure(index=tuple(range(self.l)), weight=1, uniform=A)        
        
        for i in range(len(self.primes)):
            for j in range(self.l):
                if j + i*self.l >= self.n:
                    return
                canvas = tk.Canvas(self.numbers_frame, background=self.color(array=self.primes[i], key=j + i*self.l), highlightthickness=0, height=25)
                canvas.grid(row=i, column=j, padx=5, pady=5, sticky=X)
                if self.show:
                    canvas.create_text(12.5, 12.5, text=str(j + i*self.l), fill=C1, anchor=CNT)

    def find_primes(self, n: int) -> list: #ToDo: `Sieve of Eratosthenes` Algorithm.
        is_prime = [True for _ in range(n+1)]
        is_prime[0] = is_prime[1] = False

        for p in range(2, int(np.sqrt(n)) + 1):
            if is_prime[p]:
                for multiple in range(p * p, n + 1, p):
                    is_prime[multiple] = False
      
        primes = [num for num, prime in enumerate(is_prime) if prime]
        primes = [[prime for prime in primes if start <= prime < start + self.l] for start in range(0, n, self.l)]

        return primes

    def search(self, array: list, key: int) -> int: #ToDo: `Binary Search` Algorithm.
        L, R = 0, len(array) - 1
        while L <= R:
            M = (L + R) // 2
            if array[M] == key:
                return M
            elif array[M] < key:
                L = M + 1
            else:
                R = M - 1

        return -1

    def color(self, array: list, key: int) -> str:
        return (C3 if self.search(array, key) != -1 else C2)

Primes(numbers_range=1000, line_step=25, hide_numbers=False)
