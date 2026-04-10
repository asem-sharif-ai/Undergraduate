import json
import tkinter as tk
import customtkinter as ctk
from datetime import datetime

from Tool.Methods.Symmetric import *

class SymmetricFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.rowconfigure(index=(0, 1), weight=1, uniform='a')
        self.columnconfigure(index=0, weight=1, uniform='a')

        self.cipher_frame = ctk.CTkFrame(self)
        self.cipher_frame.grid(row=0, column=0, padx=10, pady=(10, 5), sticky='nsew')

        self.cipher_frame.rowconfigure(index=(0, 1, 2, 3), weight=1, uniform='a')
        self.cipher_frame.columnconfigure(index=(0, 1), weight=1, uniform='a')

        ctk.CTkLabel(self.cipher_frame, text='Key').grid(row=0, column=0, padx=(15, 0), pady=(5, 10), sticky='nw')
        self.key_lbl = ctk.CTkLabel(self.cipher_frame, text=f'{16} Bytes ')
        self.key_lbl.grid(row=0, column=0, padx=(0, 10), pady=(5, 10), sticky='ne')

        self.key_sld = ctk.CTkSlider(self.cipher_frame, from_=16, to=32, number_of_steps=2,command=self.update_key)
        self.key_sld.grid(row=0, column=0, padx=(10, 5), pady=(25, 0), sticky='ew')
        self.key_sld.set(24)

        ctk.CTkLabel(self.cipher_frame, text='Mode').grid(row=0, column=1, padx=(10, 0), pady=(5, 10), sticky='nw')
        self.mode_lbl = ctk.CTkLabel(self.cipher_frame, text=f'CBC')
        self.mode_lbl.grid(row=0, column=1, padx=(0, 15), pady=(5, 10), sticky='ne')

        self.mode_sld = ctk.CTkSlider(self.cipher_frame, from_=0, to=2, number_of_steps=2,
                        command=lambda k: self.mode_lbl.configure(text=f'{['CBC', 'CFB', 'OFB'][int(k)]}'))
        self.mode_sld.grid(row=0, column=1, padx=(5, 10), pady=(25, 0), sticky='ew')
        self.mode_sld.set(0)

        self.key_ent = ctk.CTkEntry(self.cipher_frame, state='disabled', font=('Courier New', 14, 'bold'))
        self.key_ent.grid(row=1, column=0, columnspan=2, padx=10, pady=7.5, sticky='nsew')

        self.iv_ent = ctk.CTkEntry(self.cipher_frame, state='disabled', font=('Courier New', 14, 'bold'))
        self.iv_ent.grid(row=2, column=0, columnspan=2, padx=10, pady=7.5, sticky='nsew')

        self.save_btn = ctk.CTkButton(self.cipher_frame, text='Save Cipher', command=self.save_cipher)
        self.save_btn.grid(row=3, column=0, padx=(10, 5), pady=(5, 10))

        self.load_btn = ctk.CTkButton(self.cipher_frame, text='Load Cipher', command=self.load_cipher)
        self.load_btn.grid(row=3, column=1, padx=(5, 10), pady=(5, 10))

        self.usage_frame = ctk.CTkFrame(self)
        self.usage_frame.grid(row=1, column=0, padx=10, pady=(5, 10), sticky='nsew')

        self.usage_frame.rowconfigure(index=(0, 1, 2), weight=1, uniform='a')
        self.usage_frame.columnconfigure(index=0, weight=1, uniform='a')
        
        self.encrypt_btn = ctk.CTkButton(self.usage_frame, text='Encrypt', command=self.encrypt)
        self.encrypt_btn.grid(row=0, column=0, padx=10, pady=(20, 0))

        self.decrypt_btn = ctk.CTkButton(self.usage_frame, text='Decrypt', command=self.decrypt)
        self.decrypt_btn.grid(row=1, column=0, padx=10, pady=10)

        self.export_btn = ctk.CTkButton(self.usage_frame, text='Export', command=self.export, state='disabled')
        self.export_btn.grid(row=2, column=0, padx=10, pady=(0, 20))

        self.update_key(24)

    def encrypt(self):
        try:
            self.master.write(
                encrypt(
                    algorithm=self.method,
                    mode=self.mode,
                    key=self.key,
                    iv=self.iv,
                    plaintext=self.master.read()
                )
            )
            self.master.tell_action(self.method)
        except Exception as e:
            self.master.write(e)

    def decrypt(self):
        try:
            self.master.write(
                decrypt(
                    algorithm=self.method,
                    mode=self.mode,
                    key=self.key,
                    iv=self.iv,
                    ciphertext=self.master.read()
                )
            )
            self.master.tell_action(self.method)
        except Exception as e:
            self.master.write(e)

    def save_cipher(self):
        now = datetime.now()
        file_path = tk.filedialog.asksaveasfilename(
            initialfile=f'{self.method}-Cipher-[{now.day}.{now.month}.{now.year}.{now.hour}.{now.minute}].json',
            defaultextension='.json',
            filetypes=[('JSON files', '*.json')],
            title='Save Cipher'
        )

        if file_path:
            with open(file_path, 'w') as file:
                json.dump({
                    'Method': self.method,
                    'Key': decode(self.key),
                    'IV' : decode(self.iv),
                    'Len': int(self.key_sld.get()) if self.method != 'DES' else 8,
                    'Mode': ['CBC', 'CFB', 'OFB'][int(self.mode_sld.get())],
                    }, file, indent=4)

    def load_cipher(self):
        file_path = tk.filedialog.askopenfilename(
            filetypes=[('JSON files', '*.json')],
            title='Load Cipher'
        )

        if file_path:
            with open(file_path, 'r') as file:
                data = json.load(file)
            if data['Method'] == self.method:
                self.key = encode(data['Key'])
                self.iv = encode(data['IV'])
                
                self.key_sld.set(data['Len'] if data['Method'] != 'DES' else 24)
                self.key_lbl.configure(text=f'{data['Len']} Bytes')
                
                self.mode_lbl.configure(text=data['Mode'])
                self.mode_sld.set(['CBC', 'CFB', 'OFB'].index(data['Mode']))
                
                self.fill(self.key_ent, f'Key: `{decode(self.key)}`')
                self.fill(self.iv_ent, f'IV : `{decode(self.iv)}`')
                
                for wid in [self.key_sld, self.mode_sld, self.save_btn, self.load_btn]:
                    wid.configure(state='disabled')

    def export(self):
        now = datetime.now()
        file_path = tk.filedialog.asksaveasfilename(
            initialfile=f'{self.method}-Output-[{now.day}.{now.month}.{now.year}.{now.hour}.{now.minute}].txt',
            defaultextension='.txt',
            filetypes=[('Text files', '*.txt')],
            title='Save Output As'
        )

        if file_path:
            with open(file_path, 'w') as file:
                file.write(self.master.read(False))

    def update_key(self, len):
        self.key_lbl.configure(text=f'{int(len)} Bytes ')
        self.key, self.iv = generate_key(int(len)), generate_iv(self.method)
        self.fill(self.key_ent, f'Key: `{decode(self.key)}`')
        self.fill(self.iv_ent, f'IV : `{decode(self.iv)}`')

    def set_mode(self, mode):
        self.key_sld.set(24)
        if mode == 'DES':
            self.key_lbl.configure(text='8 Bytes')
            self.key_sld.configure(state='disabled')
            self.update_key(8)
        else:
            self.key_lbl.configure(text='24 Bytes')
            self.key_sld.configure(state='normal')
            self.update_key(24)

    def fill(self, entry, text:str):
        entry.configure(state='normal')
        entry.delete(0, 'end')
        entry.insert(0, text)
        entry.configure(state='disabled')

    @property
    def mode(self):
        return ['CBC', 'CFB', 'OFB'][int(self.mode_sld.get())]

    @property
    def method(self):
        return self.master.METHODS[getattr(self.master, 'method_idx', 0)].split()[-1]