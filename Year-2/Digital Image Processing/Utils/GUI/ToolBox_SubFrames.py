import customtkinter as ctk

from threading import Thread

from Functions  import *
from Utils.GUI.Data import *

#! ---------- ---------- ---------- ---------- ---------- ---------- ---------- ---------- ---------- ----------

class HistogramFrame(ctk.CTkFrame):
    def __init__(self, parent, plot_function):
        super().__init__(master=parent, fg_color=FRAME_DEFAULT_COLOR, border_width=BORDER_WIDTH, border_color=FRAME_DEFAULT_COLOR)
        self.pack(padx=0, pady=10, fill='x', expand=True)

        self.plot_histogram = plot_function

        self.histogram_btn = ctk.CTkButton(self, text='Plot Histogram', command=self.plot_histogram)
        self.histogram_btn.pack(padx=10, pady=10, fill=BOTH, expand=True)

#! ---------- ---------- ---------- ---------- ---------- ---------- ---------- ---------- ---------- ----------

class ConvertionsFrame(ctk.CTkFrame):
    def __init__(self, parent, greyscale_function):
        super().__init__(master=parent, fg_color=FRAME_DEFAULT_COLOR, border_width=BORDER_WIDTH, border_color=FRAME_DEFAULT_COLOR)
        self.pack(padx=0, pady=10, fill='x', expand=True)

        self.convert_greycsale = greyscale_function

        self.greyscale_btn = ctk.CTkButton(self, text='Convert GreyScale', command=self.convert_greycsale)
        self.greyscale_btn.pack(padx=10, pady=10, fill=BOTH, expand=True)

#! ---------- ---------- ---------- ---------- ---------- ---------- ---------- ---------- ---------- ----------

class SegmentedsFrame(ctk.CTkFrame):
    def __init__(self, parent, rotate_function, transform_axis_function, zoom_function):
        super().__init__(master=parent, fg_color=FRAME_DEFAULT_COLOR, border_width=BORDER_WIDTH, border_color=FRAME_DEFAULT_COLOR)
        self.pack(padx=0, pady=10, fill=BOTH, expand=True)

        self.send_rotate_value = rotate_function
        self.send_transform_axis_value = transform_axis_function
        self.send_zoom_value = zoom_function

        self.rotate_btn = ctk.CTkSegmentedButton(self, values=ROTATE_VALUES, fg_color=COLORS['BD'], unselected_color=COLORS['BD'],
                                                 command=self.send_rotate_value)
        self.rotate_btn.set(DEFAULT_VALUES[ROTATE])
        self.rotate_btn.pack(padx=10, pady=10, fill=BOTH, expand=True)
                
        self.transform_axis_btn = ctk.CTkSegmentedButton(self, values=TRANSFORM_AXIS_VALUES, command=self.send_transform_axis_value)
        self.transform_axis_btn.set(DEFAULT_VALUES[TRANSFORM_AXIS])
        self.transform_axis_btn.pack(padx=10, pady=10, fill=BOTH, expand=True)

        ctk.CTkLabel(self, text=ZOOM).pack()
        self.zoom_sld = ctk.CTkSlider(self, from_=-300, to=300, command=self.send_zoom_value)
        self.transform_axis_btn.set(DEFAULT_VALUES[ZOOM])
        self.zoom_sld.pack(padx=5, pady=(0, 10), fill='x', expand=True)
        
#! ---------- ---------- ---------- ---------- ---------- ---------- ---------- ---------- ---------- ----------

class SlidersFrame(ctk.CTkFrame):
    def __init__(self, parent, brightness_function,
                               saturation_function,
                               contrast_function,
                               noise_function,
                               blur_function,
                               resolution_function):
        
        super().__init__(master=parent, fg_color=FRAME_DEFAULT_COLOR, border_width=BORDER_WIDTH, border_color=FRAME_DEFAULT_COLOR)
    
        self.send_brightness_value = brightness_function
        self.send_saturation_value = saturation_function
        self.send_contrast_value   = contrast_function
        self.send_resolution_value = resolution_function
        self.send_noise_value      = noise_function
        self.send_blur_value       = blur_function
    
        self.pack(padx=0, pady=10, fill=BOTH, expand=True)     

        ctk.CTkLabel(self, text=BRIGHTNESS).pack()
        self.brightness_sld = ctk.CTkSlider(self, from_=0, to=5, command=self.send_brightness_value)
        self.brightness_sld.set(DEFAULT_VALUES[BRIGHTNESS])
        self.brightness_sld.pack(padx=5, pady=5, fill='x', expand=True)

        ctk.CTkLabel(self, text=SATURATION).pack()
        self.saturation_sld = ctk.CTkSlider(self, from_=0, to=5, command=self.send_saturation_value)
        self.saturation_sld.set(DEFAULT_VALUES[SATURATION])
        self.saturation_sld.pack(padx=5, pady=5, fill='x', expand=True)

        ctk.CTkLabel(self, text=CONTRAST).pack()
        self.contrast_sld = ctk.CTkSlider(self, from_=0, to=50, command=self.send_contrast_value)
        self.contrast_sld.set(DEFAULT_VALUES[CONTRAST])
        self.contrast_sld.pack(padx=5, pady=5, fill='x', expand=True)

        ctk.CTkLabel(self, text=NOISE).pack()
        self.noise_sld = ctk.CTkSlider(self, from_=-0.5, to=0.5, command=self.send_noise_value)
        self.noise_sld.set(DEFAULT_VALUES[NOISE])
        self.noise_sld.pack(padx=5, pady=5, fill='x', expand=True)

        ctk.CTkLabel(self, text=RESOLUTION).pack()
        self.resolution_sld = ctk.CTkSlider(self, from_=0, to=2, command=self.send_resolution_value)
        self.resolution_sld.set(DEFAULT_VALUES[RESOLUTION])
        self.resolution_sld.pack(padx=5, pady=5, fill='x', expand=True)

        ctk.CTkLabel(self, text=BLUR).pack()
        self.blur_sld = ctk.CTkSlider(self, from_=0, to=50, command=self.send_blur_value)
        self.blur_sld.set(DEFAULT_VALUES[BLUR])
        self.blur_sld.pack(padx=5, pady=(5, 15), fill='x', expand=True)

#! ---------- ---------- ---------- ---------- ---------- ---------- ---------- ---------- ---------- ----------

class SettingsFrame(ctk.CTkFrame):
    def __init__(self, parent,
                       appearance_mode_function,
                       export_function,
                       reset_function,
                       restart_function,
                       set_as_main_function):

        super().__init__(master=parent, fg_color=FRAME_DEFAULT_COLOR, border_width=BORDER_WIDTH, border_color=FRAME_DEFAULT_COLOR)
        self.pack(padx=0, pady=10, fill=BOTH, expand=True)
        
        self.set_appearance_mode = appearance_mode_function
        self.send_export_command = export_function
        self.send_reset_command = reset_function
        self.send_restart_command = restart_function
        self.set_as_main = set_as_main_function

        self.appearance_mode_btn = ctk.CTkSegmentedButton(self, values=APPEARANCE_MODES, command=self.__set_appearance_mode)
        self.appearance_mode_btn.pack(padx=10, pady=(15, 10), fill=BOTH, expand=True)
        self.appearance_mode_btn.set(APPEARANCE_MODES[0])

        self.export_btn = ctk.CTkButton(self, text='Set As Main', command=self.set_as_main)
        self.export_btn.pack(padx=10, pady=10, fill='x', expand=True)

        self.export_btn = ctk.CTkButton(self, text='Export', command=self.send_export_command)
        self.export_btn.pack(padx=10, pady=10, fill='x', expand=True)

        self.reset_btn = ctk.CTkButton(self, text='Reset', command=self.send_reset_command)
        self.reset_btn.pack(padx=10, pady=10, fill='x', expand=True)

        self.restart_btn = ctk.CTkButton(self, text='Restart', command=self.send_restart_command)
        self.restart_btn.pack(padx=10, pady=10, fill='x', expand=True)

    def __set_appearance_mode(self, value):
        self.set_appearance_mode(value.strip())