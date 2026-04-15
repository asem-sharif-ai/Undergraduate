import tkinter as tk
import customtkinter as ctk

class SliderFrame(ctk.CTkFrame):
    def __init__(self, master,
                 label: str,
                 value: str,
                 format: callable = lambda _:_,
                 command: callable = lambda _:_,
                 frame_params: dict = {},
                 label_params: dict = {},
                 slider_params: dict = {},
                 ):
        super().__init__(master, **frame_params)
        
        self.format = format
        self.command = command

        self.rowconfigure(index=0, weight=1, uniform='a')
        self.columnconfigure(index=0, weight=1, uniform='a')

        self.label_lbl = ctk.CTkLabel(self, text=label, **label_params)
        self.label_lbl.grid(row=0, column=0, padx=(15, 0), pady=(10, 5), sticky='nw')
        
        self.value_lbl = ctk.CTkLabel(self, text=value, **label_params)
        self.value_lbl.grid(row=0, column=0, padx=(0, 15), pady=(10, 5), sticky='ne')

        self.slider = ctk.CTkSlider(self, command=self.apply_command, **slider_params)
        self.slider.grid(row=0, column=0, padx=10, pady=(5, 15), sticky='sew')

    def apply_command(self, value):
        self.value_lbl.configure(text=self.format(value))
        self.command(value)

    def set_label(self, title):
        self.label_lbl.configure(text=title)

    def set_value(self, value):
        self.value_lbl.configure(text=value)

    def set_slider(self, value, state:str=None):
        state = self.slider._state if state is None else state
        self.slider.configure(state='normal')
        self.slider.set(value)
        self.slider.configure(state=state)
        
    @property
    def value(self):
        return self.slider.get()
        
class DoubleSliderFrame(ctk.CTkFrame):
    def __init__(self, master,
                 label_1: str,
                 label_2: str,
                 value_1: str,
                 value_2: str,
                 format_1: callable = lambda x: x,
                 format_2: callable = lambda x: x,
                 slider_params_1: dict = {},
                 slider_params_2: dict = {},
                 command: callable = lambda l, r: None,
                 label_params: dict = {},
                 frame_params: dict = {},
                 ):
        super().__init__(master, **frame_params)
        
        self.format_1 = format_1
        self.format_2 = format_2
        self.command = command

        self.rowconfigure(index=0, weight=1, uniform='a')
        self.columnconfigure(index=(0, 1), weight=1, uniform='a')

        self.label_1 = ctk.CTkLabel(self, text=label_1, **label_params)
        self.label_1.grid(row=0, column=0, padx=(15, 0), pady=(10, 5), sticky='nw')
        
        self.value_1 = ctk.CTkLabel(self, text=value_1, **label_params)
        self.value_1.grid(row=0, column=0, padx=(0, 10), pady=(10, 5), sticky='ne')

        self.slider_1 = ctk.CTkSlider(self, command=lambda v:self.apply_command(1, v), **slider_params_1)
        self.slider_1.grid(row=0, column=0, padx=(10, 5), pady=(5, 15), sticky='sew')

        self.label_2 = ctk.CTkLabel(self, text=label_2, **label_params)
        self.label_2.grid(row=0, column=1, padx=(10, 0), pady=(10, 5), sticky='nw')
        
        self.value_2 = ctk.CTkLabel(self, text=value_2, **label_params)
        self.value_2.grid(row=0, column=1, padx=(0, 15), pady=(10, 5), sticky='ne')

        self.slider_2 = ctk.CTkSlider(self, command=lambda v:self.apply_command(2, v), **slider_params_2)
        self.slider_2.grid(row=0, column=1, padx=(5, 10), pady=(5, 15), sticky='sew')

    def apply_command(self, key, value):
        if key == 1:
            self.value_1.configure(text=self.format_1(value))
        elif key == 2:
            self.value_2.configure(text=self.format_2(value))
        self.command(self.slider_1.get(), self.slider_2.get())

    def set_label(self, key: int, title):
        if key == 1:
            self.label_1.configure(text=title)
        elif key == 2:
            self.label_2.configure(text=title)

    def set_value(self, key: int, value):
        if key == 1:
            self.value_1.configure(text=value)
        elif key == 2:
            self.value_2.configure(text=value)

    def set_slider(self, key: int, value, state: str = None):
        if key == 1:
            slider = self.slider_1
        elif key == 2:
            slider = self.slider_2
        state = slider._state if state is None else state
        slider.configure(state='normal')
        slider.set(value)
        slider.configure(state=state)

    @property
    def values(self):
        return self.slider_1.get(), self.slider_2.get()

class HexColorEntry(ctk.CTkEntry):
    def __init__(self, master, initial_color='#1A1A1A', **kwargs):
        super().__init__(master, **kwargs)

        self._default_fg = self._fg_color
        self._vcmd = self.register(self._validate_input)
        self.configure(validate='key', validatecommand=(self._vcmd, '%P'))

        self.insert(0, initial_color)
        self._check_update()

        self.bind('<KeyRelease>', self._check_update)

    def _validate_input(self, value):
        return (
            value.startswith('#') and
            all(c in '0123456789abcdefABCDEF' for c in value[1:]) and
            len(value) <= 7
        )

    def _check_update(self, event=None):
        hex_code = self.get()
        if len(hex_code) == 7:
            try:
                self.configure(fg_color=hex_code)
            except:
                self.configure(fg_color=self._default_fg)
        else:
            self.configure(fg_color=self._default_fg)

    def set_hex(self, hex_value: str):
        if self._validate_input(hex_value):
            self.delete(0, tk.END)
            self.insert(0, hex_value)
            self._check_update()

    def get_hex(self):
        hex_code = self.get()
        if self._validate_input(hex_code) and len(hex_code) == 7:
            return hex_code
        return '#FFFFFF'

    def get_rgb(self):
        hex_code = self.get_hex()
        if self._validate_input(hex_code) and len(hex_code) == 7:
            try:
                return (
                    int(hex_code[1:3], 16),
                    int(hex_code[3:5], 16),
                    int(hex_code[5:7], 16)
                )
            except:
                return None
        return None
