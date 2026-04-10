import tkinter as tk
import customtkinter as ctk

from tkinter.filedialog import askopenfilename as import_file

from Tool.GUI import *

ctk.set_appearance_mode('system')
ctk.set_default_color_theme('blue')

DESCRIPTION = '''
This is a cryptography tool designed for educational purposes.
Developed by Asem Al-Sharif in April 2025.
The tool is intended to assist students and developers in understanding core cryptographic concepts and preparing data for secure deployment and further study.
It features a collection of basic encryption algorithms and provides functionality to save encrypted messages (ciphers) and their corresponding outputs.
'''[1:-1]

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.setup()
        self.build()

    def setup(self):
        self.title('Cryptography Tool')
        self.geometry(f'{1000}x{500}')
        self.resizable(False, False)

        self.rowconfigure(index=(0, 2), weight=4, uniform='a')
        self.rowconfigure(index=(1, 3), weight=3, uniform='a')
        self.columnconfigure(index=0, weight=2, uniform='a')
        self.columnconfigure(index=1, weight=1, uniform='a')

        self.METHODS = [
            'Symmetric  :: AES',
            'Symmetric  :: DES',
            'Asymmetric :: RSA',
            'Stream     :: RC4',
            'Hash       :: MD5',
            'Hash       :: SHA3',
            # 'Digital    :: RSA',
            # 'Blind      :: RSA',
        ]

    def build(self):
        self.input_box = ctk.CTkTextbox(self, wrap='word')
        self.input_box.grid(row=0, column=0, rowspan=2, padx=(10, 5), pady=(10, 5), sticky='nsew')
        
        self.output_box = ctk.CTkTextbox(self, wrap='word', state='disabled')
        self.output_box.grid(row=2, column=0, rowspan=2, padx=(10, 5), pady=(5, 10), sticky='nsew')
        
        self.resize_font(None, None, True)
        # self.input_box.bind('<Button-2>', lambda _: self.resize_font(None, None, True))
        # self.output_box.bind('<Button-2>', lambda _: self.resize_font(None, None, True))
        # self.input_box.bind('<MouseWheel>', lambda e: self.resize_font(e.delta, 'Input'))
        # self.output_box.bind('<MouseWheel>', lambda e: self.resize_font(e.delta, 'Output'))

        self.methods_frames = {
            'Symmetric' : SymmetricFrame(self),
            'Asymmetric': AsymmetricFrame(self),
            'Stream'    : StreamFrame(self),
            'Hash'      : HashFrame(self),
            # 'Digital'   : HashFrame(self),
            # 'Blind'     : HashFrame(self),
        }

        self.methods_frames['Symmetric'].grid(row=0, column=1, rowspan=3, padx=(5, 10), pady=(10, 5), sticky='nsew')
        
        self.control_frame = ctk.CTkFrame(self)
        self.control_frame.grid(row=3, column=1, rowspan=1, padx=(5, 10), pady=(5, 10), sticky='nsew')
        
        self.control_frame.rowconfigure(index=(0, 1), weight=1, uniform='a')
        self.control_frame.columnconfigure(index=(0, 1, 2, 3), weight=1, uniform='a')

        self.current_method = ctk.CTkEntry(self.control_frame, state='disabled', font=('Courier New', 12, 'bold'))
        self.current_method.grid(row=0, column=0, columnspan=2, padx=(10, 5), pady=(10, 5), sticky='nsew')
        self.current_method.bind('<MouseWheel>', lambda e: self.change_method('Next' if e.delta < 0 else 'Back'))

        self.back_btn = ctk.CTkButton(self.control_frame, text='◂', font=('TkDefaultFont', 25), command=lambda: self.change_method(action='Back'))
        self.back_btn.grid(row=1, column=0, padx=(10, 2), pady=(5, 10), sticky='nsew')
        
        self.next_btn = ctk.CTkButton(self.control_frame, text='▸', font=('TkDefaultFont', 25), command=lambda: self.change_method(action='Next'))
        self.next_btn.grid(row=1, column=1, padx=(7, 5), pady=(5, 10), sticky='nsew')
        
        self.import_btn = ctk.CTkButton(self.control_frame, text='Import File', command=self.import_input)
        self.import_btn.grid(row=0, column=2, columnspan=2, padx=(5, 10), pady=(10, 5), sticky='nsew')
        
        self.reset_btn = ctk.CTkButton(self.control_frame, text='Reset Session', command=self.reset)
        self.reset_btn.grid(row=1, column=2, columnspan=2, padx=(5, 10), pady=(5, 10), sticky='nsew')

        self.change_method()
        self.write(DESCRIPTION, is_input=True)

    def read(self, is_input:bool = True):
        return (self.input_box if is_input else self.output_box).get('1.0', 'end-1c').strip()

    def write(self, text:str, clear:bool = True, is_input:bool = False):
        box = self.input_box if is_input else self.output_box

        box.configure(state='normal')
        if clear:
            box.delete('1.0', 'end')
        box.insert('end', text)
        if not is_input:
            box.configure(state='disabled')

    def change_method(self, action:str = 'None'):
        self.current_method.configure(state='normal')
        self.current_method.delete(0, 'end')

        forget_frame = self.method.split()[0]
        if action == 'None':
            self.method_idx = 0
        elif action == 'Back':
            self.method_idx = (self.method_idx - 1) % len(self.METHODS)
        elif action == 'Next':
            self.method_idx = (self.method_idx + 1) % len(self.METHODS)

        self.current_method.insert(0, self.method)
        self.current_method.configure(state='disabled')
        
        if forget_frame != (show_frame := self.method.split()[0]):
            self.methods_frames[forget_frame].grid_forget()
            self.methods_frames[show_frame].grid(row=0, column=1, rowspan=3, padx=(5, 10), pady=(10, 5), sticky='nsew')
        
        if (method := self.method.split()[0]) == 'Symmetric':
            self.methods_frames[method].set_mode(self.method.split()[-1])

    def import_input(self):
        file_path = import_file(
            title='Import Input File',
            filetypes=[('Text Files', '*.txt')]
        )
        if file_path:
            with open(file_path, 'r', encoding='utf-8') as file:
                self.write(file.read(), clear=True, is_input=True)
                self.write('')
                self.tell_action(None)

    def reset(self):
        for wid in self.winfo_children():
            wid.destroy()
        self.setup()
        self.build()

    def tell_action(self, action: str):
        frames = {
            'AES' : self.methods_frames['Symmetric'],
            'DES' : self.methods_frames['Symmetric'],
            'RSA' : self.methods_frames['Asymmetric'],
            'RC4' : self.methods_frames['Stream'],
            'MD5' : self.methods_frames['Hash'],
            'SHA3': self.methods_frames['Hash'],
        }
        if action is None:
            for frame in set(frames.values()):
                frame.export_btn.configure(state='disabled')
        else:
            for frame in set(frames.values()):
                frame.export_btn.configure(state='normal' if frame == frames[action] else 'disabled')
        
    def resize_font(self, delta, target, reset=False):
        if reset:
            self.input_font_size  = 14
            self.output_font_size = 14
            self.input_box.configure(font=('TkDefaultFont', self.input_font_size))
            self.output_box.configure(font=('TkDefaultFont', self.output_font_size))
            return
        if target == 'Input':
            self.input_font_size += 1 if delta > 0 else -1
            self.input_font_size = max(14, min(48, self.input_font_size))
            self.input_box.configure(font=('TkDefaultFont', self.input_font_size))
        elif target == 'Output':
            self.output_font_size += 1 if delta > 0 else -1
            self.output_font_size = max(14, min(48, self.output_font_size))
            self.output_box.configure(font=('TkDefaultFont', self.output_font_size))

    def fill(self, entry, text:str):
        entry.configure(state='normal')
        entry.delete(0, 'end')
        entry.insert(0, text)
        entry.configure(state='disabled')

    def enable(self, *wids):
        for wid in wids:
            wid.configure(state='normal')

    def disable(self, *wids):
        for wid in wids:
            wid.configure(state='disabled')

    @property
    def method(self):
        return self.METHODS[getattr(self, 'method_idx', 0)]

    @staticmethod
    def Run():
        self = App()
        self.mainloop()