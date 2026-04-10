import json
import tkinter as tk
import customtkinter as ctk
from datetime import datetime

from Tool.Methods.Hash import generate_hash

class HashFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.export_data = None

        self.rowconfigure(index=(0, 3), weight=5, uniform='a')
        self.rowconfigure(index=(1, 2), weight=2, uniform='a')
        self.columnconfigure(index=0, weight=1, uniform='a')

        self.hash_btn = ctk.CTkButton(self, text='Hash', command=self.hash)
        self.hash_btn.grid(row=1, column=0, padx=10, pady=10)

        self.export_btn = ctk.CTkButton(self, text='Export', command=self.export_hash, state='disabled')
        self.export_btn.grid(row=2, column=0, padx=10, pady=10)

    def hash(self):
        text = self.master.read()
        hasher = self.master.METHODS[self.master.method_idx].split()[-1]
        output = generate_hash(text, hasher)
        self.master.write(output)

        self.master.tell_action(hasher)
        self.export_data = {
            'Input': text,
            'Method': hasher,
            'Hash': output,
        }
        
    def export_hash(self):
        now = datetime.now()
        file_path = tk.filedialog.asksaveasfilename(
            initialfile=f'Hash-[{now.day}.{now.month}.{now.year}.{now.hour}.{now.minute}].json',
            defaultextension='.json',
            filetypes=[('JSON files', '*.json')],
            title='Save hash output'
        )

        if file_path:
            with open(file_path, 'w') as file:
                json.dump(self.export_data, file, indent=4)
