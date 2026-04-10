import json
import tkinter as tk
import customtkinter as ctk
from datetime import datetime

from Tool.Methods.Stream import *

class StreamFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.rowconfigure(index=(0, 1), weight=1, uniform='a')
        self.columnconfigure(index=0, weight=1, uniform='a')

        self.cipher_frame = ctk.CTkFrame(self)
        self.cipher_frame.grid(row=0, column=0, padx=10, pady=(10, 5), sticky='nsew')

        self.cipher_frame.rowconfigure(index=(0, 1, 2), weight=1, uniform='a')
        self.cipher_frame.columnconfigure(index=(0, 1), weight=1, uniform='a')

        self.key_ent = ctk.CTkEntry(self.cipher_frame, placeholder_text='Key', font=('Courier New', 14, 'bold'))
        self.key_ent.grid(row=0, column=0, columnspan=2, padx=10, pady=7.5, ipady=2, sticky='ew')
        self.fill(self.key_ent, 'SecretKey')

        self.format_opt = ctk.CTkSegmentedButton(self.cipher_frame, values=['Decimal', 'Octal', 'Hexadecimal', 'Binary', 'Bytes'])
        self.format_opt.grid(row=1, column=0, columnspan=2, padx=10, pady=7.5, ipady=2, sticky='ew')
        self.format_opt.set('Bytes')

        self.save_btn = ctk.CTkButton(self.cipher_frame, text='Save Key', command=self.save_key)
        self.save_btn.grid(row=2, column=0, padx=(10, 5), pady=(5, 10))

        self.load_btn = ctk.CTkButton(self.cipher_frame, text='Load Key', command=self.load_key)
        self.load_btn.grid(row=2, column=1, padx=(5, 10), pady=(5, 10))

        self.usage_frame = ctk.CTkFrame(self)
        self.usage_frame.grid(row=1, column=0, padx=10, pady=(5, 10), sticky='nsew')

        self.usage_frame.rowconfigure(index=(0, 1), weight=1, uniform='a')
        self.usage_frame.columnconfigure(index=0, weight=1, uniform='a')
        
        self.apply_btn = ctk.CTkButton(self.usage_frame, text='Apply', command=self.apply)
        self.apply_btn.grid(row=0, column=0, padx=10, pady=(30, 0))

        self.export_btn = ctk.CTkButton(self.usage_frame, text='Export', command=self.export, state='disabled')
        self.export_btn.grid(row=1, column=0, padx=10, pady=(0, 30))

    def export(self):
        now = datetime.now()
        file_path = tk.filedialog.asksaveasfilename(
            initialfile=f'RS4-Output-[{now.day}.{now.month}.{now.year}.{now.hour}.{now.minute}].txt',
            defaultextension='.txt',
            filetypes=[('Text files', '*.txt')],
            title='Save Output As'
        )
        if file_path:
            with open(file_path, 'w') as file:
                file.write(self.master.read(False))

    def apply(self):
        try:
            self.master.write(
                RC4(
                    key=self.key,
                    data=self.master.read(),
                    output_format=self.format_opt.get()
                )
            )
            self.master.tell_action('RC4')
        except Exception as e:
            self.master.write(e)

    def save_key(self):
        now = datetime.now()
        file_path = tk.filedialog.asksaveasfilename(
            initialfile=f'RC4-Key-[{now.day}.{now.month}.{now.year}.{now.hour}.{now.minute}].json',
            defaultextension='.json',
            filetypes=[('JSON files', '*.json')],
            title='Save Cipher'
        )

        if file_path:
            with open(file_path, 'w') as file:
                json.dump({
                'Key': self.key,
            }, file, indent=4)

    def load_key(self):
        file_path = tk.filedialog.askopenfilename(
            filetypes=[('JSON files', '*.json')],
            title='Load Cipher'
        )

        if file_path:
            with open(file_path, 'r') as file:
                data = json.load(file)
                self.fill(self.key_ent, f'{data['Key']}')

    def fill(self, entry, text:str):
        entry.delete(0, 'end')
        entry.insert(0, text)

    @property
    def key(self):
        return self.key_ent.get()