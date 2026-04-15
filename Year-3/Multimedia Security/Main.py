import tkinter as tk
import customtkinter as ctk

from GUI import *

ctk.set_appearance_mode('system')
ctk.set_default_color_theme(r'GUI/Theme.json')

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.setup()
        self.build()

    def setup(self):
        self.title('Multimedia Security Project')
        self.geometry(f'{1000}x{550}')
        self.minsize(1000, 550)

        self.rowconfigure(index=(0, 1, 2), weight=1, uniform='a')
        self.columnconfigure(index=(0, 2), weight=2, uniform='a')
        self.columnconfigure(index=1, weight=1, uniform='a')

    def build(self):
        self.pre_frame = ctk.CTkFrame(self)
        self.pre_frame.grid(row=1, column=1, padx=10, pady=10, sticky='nsew')

        self.pre_frame.rowconfigure(index=(0, 1, 2, 3, 4), weight=1, uniform='a')
        self.pre_frame.columnconfigure(index=0, weight=1, uniform='a')

        self.image_btn = ctk.CTkButton(self.pre_frame, text='Image', command=lambda: self.show_frame('Image'))
        self.image_btn.grid(row=1, column=0)

        self.video_btn = ctk.CTkButton(self.pre_frame, text='Video', command=lambda: self.show_frame('Video'))
        self.video_btn.grid(row=2, column=0)

        self.audio_btn = ctk.CTkButton(self.pre_frame, text='Audio', command=lambda: self.show_frame('Audio'))
        self.audio_btn.grid(row=3, column=0)

        self.frames = {'Image': ImageFrame(self), 'Video': VideoFrame(self), 'Audio': AudioFrame(self)}
        self.image_frame = self.frames['Image']
        self.video_frame = self.frames['Video']
        self.audio_frame = self.frames['Audio']

    def show_frame(self, title:str):
        if title == 'Image':
            valid = self.image_frame.import_image()
        elif title == 'Video':
            valid = self.video_frame.import_video()
        elif title == 'Audio':
            valid = True
        if valid:
            self.pre_frame.grid_forget()
            self.frames[title].grid(row=0, column=0, rowspan=3, columnspan=3, padx=10, pady=10, sticky='nsew')
            self.frames[title].build()

    def back(self, current_frame):
        current_frame.grid_forget()
        self.pre_frame.grid(row=1, column=1, padx=10, pady=10, sticky='nsew')

    def close(self):
        self.destroy()

    def reset(self):
        for wid in self.winfo_children():
            wid.destroy()
        self.setup()
        self.build()

    def write(self, box, text:str, clear:bool=True, disable:bool=True):
        if isinstance(box, ctk.CTkEntry):
            box.configure(state='normal')
            if clear: box.delete(0, 'end')
            box.insert(0, text)
            if disable: box.configure(state='disabled')
        elif isinstance(box, ctk.CTkTextbox):
            box.configure(state='normal')
            if clear: box.delete('1.0', 'end')
            box.insert('end', text)
            if disable: box.configure(state='disabled')

    def enable(self, *wids):
        for wid in wids:
            wid.configure(state='normal')

    def disable(self, *wids):
        for wid in wids:
            wid.configure(state='disabled')

    @staticmethod
    def Run():
        self = App()
        self.mainloop()
