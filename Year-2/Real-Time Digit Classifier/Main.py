import os
import numpy as np
import customtkinter as ctk

from typing import Literal
from threading import Thread

from Canvas import *

ctk.set_appearance_mode('dark')
ctk.set_default_color_theme('dark-blue')

def to_ar(value):
    return str(value).translate(str.maketrans('0123456789.', '٠١٢٣٤٥٦٧٨٩٫'))

class App(ctk.CTk):
    def __init__(self, lang:str|Literal['AR', 'EN']):
        super().__init__()

        self.lang = lang[:2].upper()
        self.setup()
        self.build()
        self.model()
        self.after(25, self.update_output)

    def setup(self):
        self.title('Real-Time Digit Classifier - MNIST [AR | EN]')
        
        self.geometry(f'{800}x{600}')
        self.resizable(False, False)

        self.rowconfigure(index=0, weight=7, uniform='a')
        self.rowconfigure(index=1, weight=2, uniform='a')
        self.columnconfigure(index=0, weight=1, uniform='a')
        
        self.vector = None

    def build(self):
        self.frame_1 = ctk.CTkFrame(self)
        self.frame_1.grid(row=0, column=0, padx=10, pady=(10, 5), sticky='nsew')
        
        self.canvas = Canvas(self.frame_1, pixel_size=15, callback=self.update_output)
        self.canvas.place(relx=0.5, rely=0.5, anchor='center')

        self.frame_2 = ctk.CTkFrame(self)
        self.frame_2.grid(row=1, column=0, padx=10, pady=(5, 10), sticky='nsew')

        self.frame_2.rowconfigure(index=1, weight=3, uniform='a')
        self.frame_2.rowconfigure(index=(0, 2), weight=1, uniform='a')
        self.frame_2.columnconfigure(index=(list(range(10))), weight=1, uniform='a')

        self.lbls = [] # [1, 2, 3, ...]
        self.bars = [] # [ctk.CTkProgressBar, ...]
        self.conf = [] # [confidence, ...]

        for i in range(10):
            number_lbl = ctk.CTkLabel(self.frame_2, text=i, font=('Consolas', 15))
            number_lbl.grid(row=0, column=i, sticky='nsew', padx=5, pady=(5, 2))

            confidence_bar = ctk.CTkProgressBar(self.frame_2, orientation='vertical')
            confidence_bar.grid(row=1, column=i, sticky='ns', padx=5, pady=2)
            confidence_bar.set(0)

            confidence_lbl = ctk.CTkLabel(self.frame_2, text=f'--.--%', font=('Consolas', 15))
            confidence_lbl.grid(row=2, column=i, sticky='nsew', padx=5, pady=(2, 5))

            self.lbls.append(number_lbl)
            self.bars.append(confidence_bar)
            self.conf.append(confidence_lbl)

    def switch_lang(self, _event):
        self.lang = {'AR': 'EN', 'EN': 'AR'}.get(self.lang)
        self.canvas.deactivate()
        self.clear_output()
        self.model()

    def animate_loading(self, lbl, n):
        if getattr(self, 'loaded', False):
            lbl.configure(text=f'{self.lang} Model Loaded.')
            self.after(2000, lbl.destroy)
            self.after(2500, self.canvas.activate)
            [self.lbls[i].configure(text=i if self.lang.startswith('E') else to_ar(i)) for i in range(10)]
            return

        lbl.configure(text=f'Loading {self.lang} Model{"." * n}')
        self.after(500, lambda: self.animate_loading(lbl, (n + 1) % 4))

    def model(self):
        loading_lbl = ctk.CTkLabel(
            self.canvas,
            text='Loading Model...',
            font=('Consolas', 18, 'bold')
        )
        loading_lbl.place(relx=0.5, rely=0.5, anchor='center')

        if not (isinstance(self.lang, str) and self.lang in ['AR', 'EN']):
            loading_lbl.configure(text=f'Invalid mode `{self.lang}` ≠ [`AR`|`EN`].')
            return
        else:
            if not os.path.exists(os.path.join('Models', f'{self.lang}.keras')):
                loading_lbl.configure(text='Model was not found.')
                return
        
        # self.lang = {'AR':'Arabic', 'EN':'English'}[self.lang.upper()]

        def load_model():
            from Models import load, preprocess
            self.CNN = load(lang=self.lang)
            self.vector = lambda matrix: self.CNN.predict(preprocess(matrix), verbose=0)[0]
            
            self.loaded = True

            self.title(f'MNIST {self.lang} Model')
            self.canvas.bind('<Button-2>', self.switch_lang)

        self.animate_loading(loading_lbl, 1)
        Thread(target=load_model, daemon=True).start()

    def update_output(self, matrix: np.ndarray=None):
        if matrix is None:
            self.clear_output()
            return

        if self.vector is not None:
            vector = self.vector(matrix)
            vector = [round(i, 2) for i in vector]

            if self.lang == 'EN':
                vector_txt = [f'{v * 100:05.2f}%' for v in vector]
            else:
                vector_txt = [to_ar(f'{v * 100:05.2f}%') for v in vector]

            for i, v in enumerate(vector):
                self.bars[i].set(v)
                self.bars[i].configure(progress_color=self.color(v))
                self.conf[i].configure(text=vector_txt[i])

    def clear_output(self):
        if hasattr(self, 'bars'):
            for i in range(10):
                self.bars[i].set(0)
                self.bars[i].configure(progress_color=self.color(0))
                self.conf[i].configure(text='--.--%')

    def color(self, value):
        return f'#{int(255 * (1 - value)) :02X}{int(255 * value):02X}{0:02X}'

    @staticmethod
    def Run(lang:str|Literal['AR', 'EN']):
            self = App(lang)
            self.mainloop()