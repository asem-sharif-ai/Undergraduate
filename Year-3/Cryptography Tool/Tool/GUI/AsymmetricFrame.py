import json
import tkinter as tk
import customtkinter as ctk
from datetime import datetime

from Tool.Methods.Asymmetric import *

class AsymmetricFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.rowconfigure(index=(0, 1), weight=1, uniform='a')
        self.columnconfigure(index=0, weight=1, uniform='a')

        self.cipher_frame = ctk.CTkFrame(self)
        self.cipher_frame.grid(row=0, column=0, padx=10, pady=(10, 5), sticky='nsew')

        self.cipher_frame.rowconfigure(index=(0, 1, 2, 3), weight=1, uniform='a')
        self.cipher_frame.columnconfigure(index=(0, 1), weight=1, uniform='a')

        ctk.CTkLabel(self.cipher_frame, text='Key Size').grid(row=0, column=0, padx=(15, 0), pady=(5, 10), sticky='nw')
        self.size_lbl = ctk.CTkLabel(self.cipher_frame, text=f'{2048} Bits ')
        self.size_lbl.grid(row=0, column=1, padx=(0, 10), pady=(5, 10), sticky='ne')

        self.size_sld = ctk.CTkSlider(self.cipher_frame, from_=0, to=3, number_of_steps=3,command=self.update_keys)
        self.size_sld.grid(row=0, column=0, columnspan=2, padx=10, pady=(25, 0), sticky='ew')
        self.size_sld.set(1)

        self.pub_ent = ctk.CTkEntry(self.cipher_frame, state='disabled', font=('Courier New', 14, 'bold'))
        self.pub_ent.grid(row=1, column=0, columnspan=2, padx=10, pady=7.5, sticky='nsew')

        self.prv_ent = ctk.CTkEntry(self.cipher_frame, state='disabled', font=('Courier New', 14, 'bold'))
        self.prv_ent.grid(row=2, column=0, columnspan=2, padx=10, pady=7.5, sticky='nsew')

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

        self.update_keys(1)

    def encrypt(self):
        try:
            self.master.write(
                encrypt(
                    public_key=self.keys[0],
                    plaintext=self.master.read()
                )
            )
            self.master.tell_action('RSA')
        except Exception as e:
            self.master.write(e)

    def decrypt(self):
        try:
            self.master.write(
                decrypt(
                    private_key=self.keys[1],
                    ciphertext=self.master.read()
                )
            )
            self.master.tell_action('RSA')
        except Exception as e:
            self.master.write(e)

    def save_cipher(self):
        now = datetime.now()
        file_path = tk.filedialog.asksaveasfilename(
            initialfile=f'RSA-Cipher-[{now.day}.{now.month}.{now.year}.{now.hour}.{now.minute}].json',
            defaultextension='.json',
            filetypes=[('JSON files', '*.json')],
            title='Save Cipher'
        )

        if file_path:
            with open(file_path, 'w') as file:
                json.dump({
                'Key_Size': [1024, 2048, 3072, 4096][int(self.size_sld.get())],
                'Public_Key': self.keys[0].export_key('PEM').decode('utf-8'),
                'Private_Key': self.keys[1].export_key('PEM').decode('utf-8')
            }, file, indent=4)

    def load_cipher(self):
        file_path = tk.filedialog.askopenfilename(
            filetypes=[('JSON files', '*.json')],
            title='Load Cipher'
        )

        if file_path:
            with open(file_path, 'r') as file:
                data = json.load(file)
                
            self.size_lbl.configure(text=f'{data["Key_Size"]} Bits')
            self.size_sld.set([1024, 2048, 3072, 4096].index(data['Key_Size']))
            self.size_sld.configure(state='disabled')
            
            self.keys = setup_keys((data['Public_Key'], data['Private_Key']))
            pub, prv = format_keys(self.keys)
            self.fill(self.pub_ent, f'Public : `{pub}`')
            self.fill(self.prv_ent, f'Private: `{prv}`')
            
            for wid in [self.size_sld, self.load_btn, self.save_btn]:
                wid.configure(state='disabled')

    def export(self):
        now = datetime.now()
        file_path = tk.filedialog.asksaveasfilename(
            initialfile=f'RSA-Output-[{now.day}.{now.month}.{now.year}.{now.hour}.{now.minute}].txt',
            defaultextension='.txt',
            filetypes=[('Text files', '*.txt')],
            title='Save Output As'
        )

        if file_path:
            with open(file_path, 'w') as file:
                file.write(self.master.read(False))

    def update_keys(self, step):
        size = [1024, 2048, 3072, 4096][int(step)]
        if size != getattr(self, 'key_size', 1024):
            self.size_lbl.configure(text=f'{int(size)} Bits ')
            self.keys = generate_keys(size)
            pub, prv = format_keys(self.keys)
            self.fill(self.pub_ent, f'Public : `{pub}`')
            self.fill(self.prv_ent, f'Private: `{prv}`')
            self.key_size = size

    def fill(self, entry, text:str):
        entry.configure(state='normal')
        entry.delete(0, 'end')
        entry.insert(0, text)
        entry.configure(state='disabled')