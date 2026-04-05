
import tkinter as tk, customtkinter as ctk

from GUI.Data      import *
from GUI.Functions import *

from threading import Thread

class LogTab(ctk.CTkFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(master=parent)
        self.pack(expand=True, fill=BOTH)

        self.rowconfigure(index=0, weight=4, uniform=A)
        self.rowconfigure(index=1, weight=1, uniform=A)
        self.columnconfigure(index=(0, 1), weight=1, uniform=A)
        
        self.log_index = 1

        self.guide_panel = ctk.CTkTextbox(self, state=DIS, border_width=BD_WDH, border_color=BD_CLR, font=FONTS['Bold +'], activate_scrollbars=True)
        self.guide_panel.grid(row=0, column=0, padx=10, pady=(5, 0), sticky=STICKY_XY)
        
        self.log_panel = ctk.CTkTextbox(self, state=DIS, border_width=BD_WDH, border_color=BD_CLR, font=FONTS['Bold +'], activate_scrollbars=True)
        self.log_panel.grid(row=0, column=1, padx=10, pady=(5, 0), sticky=STICKY_XY)

        self.lower_frame = ctk.CTkFrame(self, fg_color=TXT_FG, border_color=TXT_BD, border_width=BD_WDH)
        self.lower_frame.grid(row=1, column=0, columnspan=2, padx=5, pady=5)
        
        self.lower_frame.rowconfigure(index=0, weight=1, uniform=A)
        self.lower_frame.columnconfigure(index=list(range(5)), weight=1, uniform=A)

        self.undo_btn = ctk.CTkButton(self.lower_frame, text='Undo', state=DIS, command=kwargs.get('undo_function', None))
        self.undo_btn.grid(row=0, column=0, padx=10, pady=10)

        self.redo_btn = ctk.CTkButton(self.lower_frame, text='Redo', state=DIS, command=kwargs.get('redo_function', None))
        self.redo_btn.grid(row=0, column=1, padx=10, pady=10)

        self.export_btn = ctk.CTkButton(self.lower_frame, text='Export Dataset', command=kwargs.get('export_function', None))
        self.export_btn.grid(row=0, column=2, padx=10, pady=10)

        self.reset_btn = ctk.CTkButton(self.lower_frame, text='Reset Session', command=kwargs.get('reset_function', None))
        self.reset_btn.grid(row=0, column=3, padx=10, pady=10)

        self.restart_btn = ctk.CTkButton(self.lower_frame, text='Restart Session', command=kwargs.get('restart_function', None))
        self.restart_btn.grid(row=0, column=4, padx=10, pady=10)

        self.guide_panel.configure(state=NRM)
        self.guide_panel.insert(index=END, text=GUIDE_MESSAGE)
        self.guide_panel.configure(state=DIS)

    def update_log(self, msg_type, msg_text):
        if msg_type == ERR:
            self.log_panel.configure(state=NRM, border_color=RED)
            self.log_panel.insert(index=tk.END, text=f'{self.log_index} >> {msg_text}\n\n')
            self.log_panel.configure(state=DIS)
        elif msg_type == MSG:
            self.log_panel.configure(state=NRM, border_color=GRN)
            self.log_panel.insert(index=tk.END, text=f'{self.log_index} >> {msg_text}\n\n')
            self.log_panel.configure(state=DIS)
        else:
            self.log_panel.configure(state=NRM, border_color=BD_CLR)
            self.log_panel.insert(index=tk.END, text=f'{self.log_index} >> {msg_text}\n\n')
            self.log_panel.configure(state=DIS)
        self.log_index += 1
        Thread(target=self.reset_border).start()

    def reset_border(self):
        wait()
        self.log_panel.configure(border_color=BD_CLR)
