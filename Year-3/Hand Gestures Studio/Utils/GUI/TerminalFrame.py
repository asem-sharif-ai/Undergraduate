import tkinter as tk
import customtkinter as ctk

from Utils.GUI.Data import * 
from Utils.Models import Helper

class TerminalFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, **DFD[1])

        self.rowconfigure(index=0, weight=4, uniform=A)
        self.rowconfigure(index=1, weight=1, uniform=A)
        self.columnconfigure(index=0, weight=1, uniform=A)

        #! ----- Terminal ----- ----- ----- -----
        
        self.terminal = ctk.CTkTextbox(self, **DTBD)
        self.terminal.grid(row=0, column=0, padx=10, pady=(10, 5), sticky='nsew')

        #! ----- Control Frame ----- ----- ----- -----

        self.frame = ctk.CTkFrame(self, **DFD[0])
        self.frame.grid(row=1, column=0, padx=(5, 10), pady=10, sticky='nsew')

        self.frame.rowconfigure(index=0, weight=1, uniform=A)
        self.frame.columnconfigure(index=(0, 1, 2, 3), weight=1, uniform=A)
        
        fr_1 = ctk.CTkFrame(self.frame, **DFD[1])
        fr_1.grid(row=0, column=0, padx=(10, 5), columnspan=2, pady=7.5, sticky='nsew')
        
        self.size_sld = ctk.CTkSlider(fr_1, from_=5, to=30, **{**DSD, 'state':NRM}, command=lambda s: self.update_size(int(s)))
        self.size_sld.pack(expand=True, fill='x', padx=5)
        
        self.clear_btn = ctk.CTkButton(self.frame, text='Clear', command=self.clear, **DBD)
        self.clear_btn.grid(row=0, column=2, padx=7.5, pady=7.5, sticky='nsew')

        self.save_btn = ctk.CTkButton(self.frame, text='Save', command=self.save, **DBD)
        self.save_btn.grid(row=0, column=3, padx=(5, 10), pady=7.5, sticky='nsew')

    def update_size(self, size):
        self.terminal.configure(font=(('Courier', size)))

    def clear(self):
        self.terminal.configure(state=NRM)
        self.terminal.delete(0.0, tk.END)
        self.terminal.configure(state=DIS)

    def save(self):
        Helper.export_output(self.terminal.get(1.0, tk.END))
        
    def write(self, text, nn):
        self.terminal.configure(state=NRM)
        self.terminal.insert(tk.END, f'{text}{"\n" * nn}')
        self.terminal.configure(state=DIS)