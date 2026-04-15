import tkinter as tk
import customtkinter as ctk
from tkinter.filedialog import askopenfilename as import_file, asksaveasfilename as export_file

from PIL import Image, ImageTk

from GUI.Utils import (SliderFrame, DoubleSliderFrame, HexColorEntry)

from Methods.Image import (
    binarize,
    apply_geometric_attacks,
    apply_text_watermark,
    apply_overlay_watermark, embed_lsb_watermark,
    embed_dct_watermark, embed_dct_text, extract_dct_text,
    embed_dwt_watermark, embed_dwt_text, extract_dwt_text,
)

class ImageFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.rowconfigure(index=(0, 1), weight=1, uniform='a')
        self.columnconfigure(index=(0, 2), weight=1, uniform='a')
        self.columnconfigure(index=1, weight=2, uniform='a')

    def build(self):
        self.canvas = tk.Canvas(self, bg='black', highlightthickness=1, highlightbackground='#303030')
        self.canvas.grid(row=0, column=1, padx=5, pady=(10, 5), sticky='nsew')

        self.after(50, self.show_image)
        self.canvas.bind('<Configure>', self.show_image)

        for event in ('<Button-1>', '<Button-3>'):
            self.canvas.bind(event, lambda *args, **kwargs:self.show_image(image=self.original_image))
        for event in ('<ButtonRelease-1>', '<ButtonRelease-3>'):
            self.canvas.bind(event, lambda *args, **kwargs:self.show_image(image=self.display_image))

        self.build_left_frame()
        self.build_right_frame()
        self.build_main_frame()

    def build_left_frame(self):
        self.left_frame = ctk.CTkFrame(self)
        self.left_frame.grid(row=0, column=0, padx=(10, 5), pady=(10, 5), sticky='nsew')
        
        self.left_frame.rowconfigure(index=(0, 1), weight=3, uniform='a')
        self.left_frame.rowconfigure(index=2, weight=7, uniform='a')
        self.left_frame.columnconfigure(index=(0, 1), weight=1, uniform='a')

        self.scale_frame = SliderFrame(
            master=self.left_frame,
            label='Scale',
            value='1.00',
            format=lambda v: f'{float(v):.2f}',
            command=self.apply_geometric_attacks,
            slider_params={'from_': 0.01, 'to': 1, 'number_of_steps': 99}
        )
        self.scale_frame.grid(row=0, column=0, padx=(10, 5), pady=(10, 2.5), sticky='nsew')
        self.scale_frame.set_slider(1)

        self.rotate_frame = SliderFrame(
            master=self.left_frame,
            label='Rotate',
            value='0°',
            format=lambda v: f'{int(v)}°',
            command=self.apply_geometric_attacks,
            slider_params={'from_': -180, 'to': 180, 'number_of_steps': 360}
        )
        self.rotate_frame.grid(row=0, column=1, padx=(5, 10), pady=(10, 2.5), sticky='nsew')

        self.resize_frame = DoubleSliderFrame(
            master=self.left_frame,
            label_1='Width',
            value_1=f'{self.original_image.size[0]}px',
            format_1=lambda v: f'{int(v)}px',
            slider_params_1={'from_': 0.1*self.original_image.size[0], 'to': self.original_image.size[0]},

            label_2='Height',
            value_2=f'{self.original_image.size[1]}px',
            format_2=lambda v: f'{int(v)}px',
            slider_params_2={'from_': 0.1*self.original_image.size[1], 'to': self.original_image.size[1]},

            command=self.apply_geometric_attacks,
        )
        self.resize_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=(5, 5), sticky='nsew')

        self.resize_frame.set_slider(1, self.original_image.size[0])
        self.resize_frame.set_slider(2, self.original_image.size[1])

        self.crop_frame = ctk.CTkFrame(self.left_frame)
        self.crop_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=(2.5, 10), sticky='nsew')

        self.crop_frame.rowconfigure(index=(0, 1), weight=1, uniform='a')
        self.crop_frame.columnconfigure(index=0, weight=1, uniform='a')

        self.crop_frame_1 = DoubleSliderFrame(
            master=self.crop_frame,
            label_1='Start X',
            value_1=f'0%',
            format_1=lambda v: f'{int(v)}%',
            slider_params_1={'from_': 0, 'to': 90, 'number_of_steps': 89},

            label_2='End X',
            value_2=f'100%',
            format_2=lambda v: f'{int(v)}%',
            slider_params_2={'from_': 10, 'to': 100, 'number_of_steps': 89},

            command=self.apply_geometric_attacks,
        )
        self.crop_frame_1.grid(row=0, column=0, padx=10, pady=(10, 5), sticky='nsew')

        self.crop_frame_1.set_slider(1, 0)
        self.crop_frame_1.set_slider(2, 100)

        self.crop_frame_2 = DoubleSliderFrame(
            master=self.crop_frame,
            label_1='Start Y',
            value_1=f'0%',
            format_1=lambda v: f'{int(v)}%',
            slider_params_1={'from_': 0, 'to': 90, 'number_of_steps': 89},

            label_2='End Y',
            value_2=f'100%',
            format_2=lambda v: f'{int(v)}%',
            slider_params_2={'from_': 10, 'to': 100, 'number_of_steps': 89},

            command=self.apply_geometric_attacks,
        )
        self.crop_frame_2.grid(row=1, column=0, padx=10, pady=(5, 10), sticky='nsew')

        self.crop_frame_2.set_slider(1, 0)
        self.crop_frame_2.set_slider(2, 100)

    def build_right_frame(self):
        self.right_frame = ctk.CTkFrame(self)
        self.right_frame.grid(row=0, column=2, padx=(5, 10), pady=(10, 5), sticky='nsew')
        
        self.right_frame.rowconfigure(index=0, weight=2, uniform='a')
        self.right_frame.rowconfigure(index=1, weight=7, uniform='a')
        self.right_frame.rowconfigure(index=2, weight=4, uniform='a')
        self.right_frame.columnconfigure(index=(0, 1, 2), weight=1, uniform='a')

        self.watermark_entry = ctk.CTkEntry(self.right_frame, placeholder_text='Watermark')
        self.watermark_entry.grid(row=0, column=0, columnspan=2, padx=(10, 5), pady=(10, 5), sticky='nsew')

        self.color_entry = HexColorEntry(self.right_frame)
        self.color_entry.grid(row=0, column=2, padx=(5, 10), pady=(10, 5), sticky='nsew')

        self.watermark_entry.bind('<KeyRelease>', self.apply_text_watermark)
        self.color_entry.bind('<KeyRelease>', self.apply_text_watermark)

        self.txt_wm_frame = ctk.CTkFrame(self.right_frame)
        self.txt_wm_frame.grid(row=1, column=0, columnspan=3, padx=10, pady=5, sticky='nsew')

        self.txt_wm_frame.rowconfigure(index=(0, 1), weight=1, uniform='a')
        self.txt_wm_frame.columnconfigure(index=0, weight=1, uniform='a')

        self.txt_wm_frame_1 = DoubleSliderFrame(
            master=self.txt_wm_frame,
            label_1='Index X',
            value_1=f'10%',
            format_1=lambda v: f'{int(v)}%',
            slider_params_1={'from_': 1, 'to': 99, 'number_of_steps': 98},

            label_2='Index Y',
            value_2=f'10%',
            format_2=lambda v: f'{int(v)}%',
            slider_params_2={'from_': 1, 'to': 99, 'number_of_steps': 98},

            command=self.apply_text_watermark,
        )
        self.txt_wm_frame_1.grid(row=0, column=0, padx=10, pady=(10, 5), sticky='nsew')

        self.txt_wm_frame_1.set_slider(1, 10)
        self.txt_wm_frame_1.set_slider(2, 10)

        self.txt_wm_frame_2 = DoubleSliderFrame(
            master=self.txt_wm_frame,
            label_1='Font Size',
            value_1=f'2',
            format_1=lambda v: f'{int(v)}',
            slider_params_1={'from_': 1, 'to': 10, 'number_of_steps': 9},

            label_2='Font Bold',
            value_2=f'2',
            format_2=lambda v: f'{int(v)}',
            slider_params_2={'from_': 1, 'to': 10, 'number_of_steps': 9},

            command=self.apply_text_watermark,
        )
        self.txt_wm_frame_2.grid(row=1, column=0, padx=10, pady=(5, 10), sticky='nsew')

        self.txt_wm_frame_2.set_slider(1, 4)
        self.txt_wm_frame_2.set_slider(2, 4)

        self.manage_frame = ctk.CTkFrame(self.right_frame)
        self.manage_frame.grid(row=2, column=0, columnspan=3, padx=10, pady=(5, 10), sticky='nsew')
        self.manage_frame.rowconfigure(index=(0, 1), weight=1, uniform='a')
        self.manage_frame.columnconfigure(index=(0, 1, 2, 3, 4, 5), weight=1, uniform='a')
        
        change_btn = ctk.CTkButton(self.manage_frame, text='Change', command=self.change_image)
        change_btn.grid(row=0, column=0, columnspan=2, padx=(10, 5), pady=(10, 5), sticky='nsew')
        
        reset_btn = ctk.CTkButton(self.manage_frame, text='Reset', command=self.reset_image)
        reset_btn.grid(row=0, column=2, columnspan=2, padx=6, pady=(10, 5), sticky='nsew')
        
        export_btn = ctk.CTkButton(self.manage_frame, text='Export', command=self.export_image)
        export_btn.grid(row=0, column=4, columnspan=2, padx=(5, 10), pady=(10, 5), sticky='nsew')
        
        back_btn = ctk.CTkButton(self.manage_frame, text='Back', command=lambda: self.master.back(self))
        back_btn.grid(row=1, column=0, columnspan=3, padx=(10, 5), pady=(5, 10), sticky='nsew')
        
        close_btn = ctk.CTkButton(self.manage_frame, text='Close', command=self.master.close)
        close_btn.grid(row=1, column=3, columnspan=3, padx=(5, 10), pady=(5, 10), sticky='nsew')

    def build_main_frame(self):
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.grid(row=1, column=0, columnspan=3, padx=10, pady=(5, 10), sticky='nsew')

        self.main_frame.rowconfigure(index=(0, 1), weight=1, uniform='a')
        self.main_frame.columnconfigure(index=(0, 1, 2, 3), weight=1, uniform='a')

        self.overlay_lsb_wm_frame = ctk.CTkFrame(self.main_frame)
        self.overlay_lsb_wm_frame.grid(row=0, column=0, rowspan=2, padx=10, pady=10, sticky='nsew')

        self.overlay_lsb_wm_frame.rowconfigure(index=(0, 1, 2, 3), weight=1, uniform='a')
        self.overlay_lsb_wm_frame.columnconfigure(index=(0, 1), weight=1, uniform='a')

        self.overlay_wm_btn = ctk.CTkButton(self.overlay_lsb_wm_frame, text='Overlay Watermark', state='disabled', command=lambda:self.show_method_frame('Overlay'))
        self.overlay_wm_btn.grid(row=1, column=0, columnspan=2)

        self.lsb_wm_btn = ctk.CTkButton(self.overlay_lsb_wm_frame, text='LSB Embedding', state='disabled', command=lambda:self.show_method_frame('LSB'))
        self.lsb_wm_btn.grid(row=2, column=0, columnspan=2)

        self.dct_wm_frame = ctk.CTkFrame(self.main_frame)
        self.dct_wm_frame.grid(row=0, column=1, rowspan=2, padx=(5, 7.5), pady=10, sticky='nsew')

        self.dct_wm_frame.rowconfigure(index=(0, 1, 2, 3), weight=1, uniform='a')
        self.dct_wm_frame.columnconfigure(index=(0, 1), weight=1, uniform='a')

        self.dct_wm_btn = ctk.CTkButton(self.dct_wm_frame, text='DCT', state='disabled', command=lambda:self.show_method_frame('DCT'))
        self.dct_wm_btn.grid(row=0, column=0, rowspan=4, columnspan=2)

        self.dwt_wm_frame = ctk.CTkFrame(self.main_frame)
        self.dwt_wm_frame.grid(row=0, column=2, rowspan=2, padx=(7.5, 5), pady=10, sticky='nsew')

        self.dwt_wm_frame.rowconfigure(index=(0, 1, 2, 3), weight=1, uniform='a')
        self.dwt_wm_frame.columnconfigure(index=(0, 1), weight=1, uniform='a')

        self.dwt_wm_btn = ctk.CTkButton(self.dwt_wm_frame, text='DWT', state='disabled', command=lambda:self.show_method_frame('DWT'))
        self.dwt_wm_btn.grid(row=0, column=0, rowspan=4, columnspan=2)

        self.img_wm_frame = ctk.CTkFrame(self.main_frame)
        self.img_wm_frame.grid(row=0, column=3, rowspan=2, padx=10, pady=10, sticky='nsew')

        self.img_wm_frame.rowconfigure(index=0, weight=9, uniform='a')
        self.img_wm_frame.rowconfigure(index=1, weight=4, uniform='a')
        self.img_wm_frame.columnconfigure(index=0, weight=1, uniform='a')

        self.load_wm_btn = ctk.CTkButton(self.img_wm_frame, text='Load Watermark', command=self.load_watermark)
        self.load_wm_btn.grid(row=0, column=0, rowspan=2)

        self.owm_options = ctk.CTkSegmentedButton(self.overlay_lsb_wm_frame, values=['Additive', 'Multiplicative', 'Transparency'], command=self.apply_overlay_watermark)
        
        self.owm_key_frame = SliderFrame(
            master=self.overlay_lsb_wm_frame,
            label='Key Strength / Alpha',
            value='10%',
            format=lambda v: f'{int(v)}%',
            command=self.apply_overlay_watermark,
            slider_params={'from_': 10, 'to': 90, 'number_of_steps': 8}
        )
        self.owm_key_frame.set_slider(10)

        self.channel_options = ctk.CTkSegmentedButton(self.overlay_lsb_wm_frame, values=['R', 'G', 'B', 'H', 'S', 'I', 'L'], command=self.apply_lsb_watermark)
        self.channel_options.set('L')
        if self.original_image.mode == 'L':
            self.channel_options.configure(state='disabled')

        self.lsb_idx_frame = SliderFrame(
            master=self.overlay_lsb_wm_frame,
            label='Embedding Bit Index',
            value='LSB',
            format=lambda v: f'{['LSB', '1St', '2Nd', '3Rd', '4Th', '5Th', '6Th', 'MSB'][int(v)]}',
            command=self.apply_lsb_watermark,
            slider_params={'from_': 0, 'to': 7, 'number_of_steps': 7}
        )
        self.lsb_idx_frame.set_slider(0)

        self.dct_alpha_frame = SliderFrame(
            master=self.dct_wm_frame,
            label='Alpha',
            value='10.0 α',
            format=lambda v: f'{float(v):.1f} α',
            command=lambda *args, **kwargs:None,
            slider_params={'from_': 1, 'to': 30, 'number_of_steps': 58}
        )
        self.dct_alpha_frame.set_slider(10)

        self.dct_block_frame = SliderFrame(
            master=self.dct_wm_frame,
            label='Block Size',
            value='8',
            format=lambda v: f'{int(v)}',
            command=lambda *args, **kwargs:None,
            slider_params={'from_': 4, 'to': 32, 'number_of_steps': 7}
        )
        self.dct_block_frame.set_slider(8)

        self.dct_input_entry = ctk.CTkTextbox(self.dct_wm_frame, activate_scrollbars=False)
        self.dct_output_entry = ctk.CTkTextbox(self.dct_wm_frame, state='disabled')
        
        self.dct_input_entry.bind('<Return>', self.apply_dct_text)
        self.write(self.dct_input_entry, 'Write down a watermark and press <Enter> to embed.', False)
        
        self.dct_length_frame = SliderFrame(
            master=self.dct_wm_frame,
            label='Extraction Length',
            value='---',
            format=lambda v: f'{int(v)} Letter',
            command=self.extract_dct_text,
            slider_params={'from_': 1, 'to': 100, 'number_of_steps': 99}
        )
        self.dct_length_frame.set_slider(10)

        self.dwt_input_entry = ctk.CTkTextbox(self.dwt_wm_frame, activate_scrollbars=False)
        self.dwt_output_entry = ctk.CTkTextbox(self.dwt_wm_frame, state='disabled')
        
        self.dwt_input_entry.bind('<Return>', self.apply_dwt_text)
        self.write(self.dwt_input_entry, 'Write down a watermark and press <Enter> to embed.', False)
        
        self.dwt_length_frame = SliderFrame(
            master=self.dwt_wm_frame,
            label='Extraction Length',
            value='---',
            format=lambda v: f'{int(v)} Letter',
            command=self.extract_dwt_text,
            slider_params={'from_': 1, 'to': 100, 'number_of_steps': 99}
        )
        self.dwt_length_frame.set_slider(10)

        self.dwt_alpha_frame = SliderFrame(
            master=self.dwt_wm_frame,
            label='Alpha',
            value='10.0 α',
            format=lambda v: f'{float(v):.1f} α',
            command=lambda *args, **kwargs:None,
            slider_params={'from_': 1, 'to': 30, 'number_of_steps': 58}
        )
        self.dwt_alpha_frame.set_slider(10)

        self.dwt_level_frame = SliderFrame(
            master=self.dwt_wm_frame,
            label='Level',
            value='1',
            format=lambda v: f'{int(v)}',
            command=lambda *args, **kwargs:None,
            slider_params={'from_': 1, 'to': 3, 'number_of_steps': 2}
        )
        self.dwt_level_frame.set_slider(1)

    def show_method_frame(self, name):
        if name == 'Overlay':
            self.overlay_shown = True
            self.overlay_wm_btn.grid_forget()
            if not getattr(self, 'lsb_shown', False):
                self.lsb_wm_btn.grid_configure(row=2, rowspan=2)
            self.owm_options.grid(row=0, column=0, columnspan=2, padx=10, pady=(15, 0), ipady=2, sticky='ew')
            self.owm_key_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=(0, 10), sticky='nsew')

        elif name == 'LSB':
            self.lsb_shown = True
            self.lsb_wm_btn.grid_forget()
            if not getattr(self, 'overlay_shown', False):
                self.overlay_wm_btn.grid_configure(row=0, rowspan=2)
            self.lsb_idx_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=(10, 0), sticky='nsew')
            self.channel_options.grid(row=3, column=0, columnspan=2, padx=10, pady=(0, 15), ipady=2, sticky='ew')

        elif name == 'DCT':
            self.dct_wm_btn.configure(text='Embed Image', command=self.apply_dct_watermark)
            self.dct_wm_btn.grid_configure(row=1, rowspan=1, pady=(5, 15))
            self.dct_alpha_frame.grid(row=0, column=0, padx=(10, 5), pady=(10, 0), sticky='nsew')
            self.dct_block_frame.grid(row=0, column=1, padx=(5, 10), pady=(10, 0), sticky='nsew')
            
            self.dct_input_entry.grid(row=2, column=0, padx=(10, 5), pady=(0, 10), sticky='nsew')
            self.dct_output_entry.grid(row=2, column=1, padx=(5, 10), pady=(0, 10), sticky='nsew')
            
            self.dct_length_frame.grid(row=3, column=0, columnspan=2, padx=10, pady=(0, 10), sticky='nsew')
            
        elif name == 'DWT':
            self.dwt_wm_btn.configure(text='Embed Image', command=self.apply_dwt_watermark)
            self.dwt_wm_btn.grid_configure(row=1, rowspan=1, pady=(5, 15))
            self.dwt_alpha_frame.grid(row=0, column=0, padx=(10, 5), pady=(10, 0), sticky='nsew')
            self.dwt_level_frame.grid(row=0, column=1, padx=(5, 10), pady=(10, 0), sticky='nsew')

            self.dwt_input_entry.grid(row=2, column=0, padx=(10, 5), pady=(0, 10), sticky='nsew')
            self.dwt_output_entry.grid(row=2, column=1, padx=(5, 10), pady=(0, 10), sticky='nsew')

            self.dwt_length_frame.grid(row=3, column=0, columnspan=2, padx=10, pady=(0, 10), sticky='nsew')
        
    def show_image(self, event=None, image=None):
        image = self.display_image if image is None else image
        if event is not None:
            canvas_w = event.width
            canvas_h = event.height
        else:
            canvas_w = self.canvas.winfo_width()
            canvas_h = self.canvas.winfo_height()
            
        canvas_r = canvas_w / canvas_h

        if canvas_w <= 1 or canvas_h <= 1:
            self.after(25, self.show_image)
            return

        image_w, image_h = image.size
        image_r = image_w / image_h

        if image_r > canvas_r:
            new_w = canvas_w
            new_h = int(new_w / image_r)
        else:
            new_h = canvas_h
            new_w = int(new_h * image_r)

        self.tk_image = ImageTk.PhotoImage(image.resize((new_w, new_h), Image.LANCZOS))
        self.canvas.delete('all')
        self.canvas.create_image(
            canvas_w // 2,
            canvas_h // 2,
            image=self.tk_image,
            anchor='center'
        )
        if getattr(self, 'wm_image', None) is not None:
            self.show_watermark()

    def show_watermark(self, image=None):
        image = image if image is not None else self.wm_display_image
        
        canvas_w = self.wm_canvas.winfo_width()
        canvas_h = self.wm_canvas.winfo_height()
        canvas_r = canvas_w / canvas_h

        if canvas_w <= 1 or canvas_h <= 1:
            self.after(25, self.show_watermark)
            return

        image_w, image_h = image.size
        image_r = image_w / image_h

        if image_r > canvas_r:
            new_w = canvas_w
            new_h = int(new_w / image_r)
        else:
            new_h = canvas_h
            new_w = int(new_h * image_r)

        self.wm_tk_image = ImageTk.PhotoImage(image.resize((new_w, new_h), Image.LANCZOS))
        self.wm_canvas.delete('all')
        self.wm_canvas.create_image(
            canvas_w // 2,
            canvas_h // 2,
            image=self.wm_tk_image,
            anchor='center'
        )

    def load_watermark(self, show=True):
        try:
            path = import_file(title='Select An Image', filetypes=[('Image Files', '*.jpg;*.jpeg;*.png;*.webp;*.tiff')])
            watermark = Image.open(path)
            watermark = watermark.convert(self.original_image.mode)
            self.wm_display_image = watermark
            self.wm_original_image = watermark
        except:
            pass
        else:
            if show:
                self.load_wm_btn.grid_forget()

                self.wm_canvas = tk.Canvas(self.img_wm_frame, bg='black', highlightthickness=1, highlightbackground='#303030')
                self.wm_canvas.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky='nsew')

                self.after(25, self.show_watermark)

                for event in ('<Button-1>', '<Button-3>'):
                    self.wm_canvas.bind(event, lambda *args, **kwargs:self.show_watermark(image=self.wm_original_image))
                for event in ('<ButtonRelease-1>', '<ButtonRelease-3>'):
                    self.wm_canvas.bind(event, lambda *args, **kwargs:self.show_watermark(image=self.wm_display_image))

                self.wm_btns_frame = ctk.CTkFrame(self.img_wm_frame)
                self.wm_btns_frame.grid(row=1, column=0, padx=10, pady=(0, 10), sticky='nsew')

                self.wm_btns_frame.rowconfigure(index=(0, 1), weight=1, uniform='a')
                self.wm_btns_frame.columnconfigure(index=(0, 1, 2), weight=1, uniform='a')

                self.wm_threshold_frame = SliderFrame(
                    master=self.wm_btns_frame,
                    label='Threshold',
                    value='---',
                    format=lambda v: f'{int(v)} <',
                    command=self.binarize_watermark,
                    slider_params={'from_': 1, 'to': 254, 'number_of_steps': 253}
                )
                self.wm_threshold_frame.set_slider(128)
                self.wm_threshold_frame.grid(row=0, column=0, rowspan=2, columnspan=2, padx=(10, 10), pady=10, sticky='nsew')

                self.reset_wm_btn = ctk.CTkButton(self.wm_btns_frame, text='Reset', command=self.reset_watermark)
                self.reset_wm_btn.grid(row=0, column=2, padx=(0, 10), pady=(10, 5), sticky='ew')

                self.remove_wm_btn = ctk.CTkButton(self.wm_btns_frame, text='Remove', command=self.remove_watermark)
                self.remove_wm_btn.grid(row=1, column=2, padx=(0, 10), pady=(5, 10), sticky='ew')

                for btn in [self.overlay_wm_btn, self.lsb_wm_btn, self.dct_wm_btn, self.dwt_wm_btn]:
                    btn.configure(state='normal')
            else:
                return True

    def apply_geometric_attacks(self, *args, **kwargs):
        params = {
            'Scale': round(self.scale_frame.value, 2),
            'Rotate': int(self.rotate_frame.value),
            'Resize': {
                'width': int(self.resize_frame.values[0]),
                'height': int(self.resize_frame.values[1])
                },
            'Crop': {
                'start_x': self.crop_frame_1.values[0],
                'start_y': self.crop_frame_2.values[0],
                'end_x': self.crop_frame_1.values[1],
                'end_y': self.crop_frame_2.values[1]
                },
        }
        self.display_image = apply_geometric_attacks(self.original_image, params)
        self.show_image()

    def apply_text_watermark(self, *args, **kwargs):
        params = {
            'Text': self.watermark_entry.get(),
            'Color': self.color_entry.get_rgb(),
            'X': int(self.txt_wm_frame_1.values[0]),
            'Y': int(self.txt_wm_frame_1.values[1]),
            'Size': int(self.txt_wm_frame_2.values[0]),
            'Bold': int(self.txt_wm_frame_2.values[1]),
        }
        self.display_image = apply_text_watermark(self.original_image, params)
        self.show_image()

    def binarize_watermark(self, *args, **kwargs):
        self.wm_display_image = binarize(self.wm_original_image, self.threshold, self.original_image.mode)
        self.show_watermark()

    def reset_watermark(self):
        self.wm_display_image = self.wm_original_image
        self.wm_threshold_frame.set_value('---')
        self.wm_threshold_frame.set_slider(128)
        self.show_watermark()

    def remove_watermark(self):
        self.wm_display_image = None
        self.main_frame.destroy()
        self.build_main_frame()
        self.show_image()

    def apply_overlay_watermark(self, *args, **kwargs):
        if (method := self.owm_options.get()):
            self.display_image = apply_overlay_watermark(
                self.original_image,
                self.wm_display_image,
                method,
                self.owm_key_frame.value
                )
            self.show_image()

    def apply_lsb_watermark(self, *args, **kwargs):
        self.display_image = embed_lsb_watermark(
            self.original_image,
            self.wm_display_image,
            self.channel_options.get(),
            int(self.lsb_idx_frame.value)
            )
        self.show_image()

    def apply_dct_watermark(self, *args, **kwargs):
        self.display_image = embed_dct_watermark(
            self.original_image,
            self.wm_display_image,
            float(self.dct_alpha_frame.value),
            int(self.dct_block_frame.value)
            )
        self.show_image()
        
    def apply_dct_text(self, *args, **kwargs):
        self.display_image = embed_dct_text(
            self.original_image,
            self.read(self.dct_input_entry),
            float(self.dct_alpha_frame.value),
            int(self.dct_block_frame.value)
        )
        
    def extract_dct_text(self, *args, **kwargs):
        self.write(self.dct_output_entry, extract_dct_text(
            self.display_image,
            self.original_image,
            int(self.dct_block_frame.value),
            int(self.dct_length_frame.value)
            )
        )

    def apply_dwt_watermark(self, *args, **kwargs):
        self.display_image = embed_dwt_watermark(
            self.original_image,
            self.wm_display_image,
            float(self.dwt_alpha_frame.value),
            int(self.dwt_level_frame.value)
            )
        self.show_image()

    def apply_dwt_text(self, *args, **kwargs):
        self.display_image = embed_dwt_text(
            self.original_image,
            self.read(self.dwt_input_entry),
            float(self.dwt_alpha_frame.value),
            int(self.dwt_level_frame.value)
        )

    def extract_dwt_text(self, *args, **kwargs):
        self.write(self.dwt_output_entry, extract_dwt_text(
            self.display_image,
            self.original_image,
            float(self.dwt_alpha_frame.value),
            int(self.dwt_level_frame.value),
            int(self.dwt_length_frame.value)
            )
        )

    def change_image(self):
        valid = self.import_image()
        if valid:
            self.reset_image()

    def reset_image(self):
        self.display_image = self.original_image
        for wid in self.winfo_children():
            wid.destroy()
        self.build()

    def export_image(self):
        path = export_file(title='Export Image', initialfile='Image', defaultextension='.png',
        filetypes=[('PNG Image', '*.png'), ('JPEG Image', '*.jpg'), ('WebP Image', '*.webp'), ('TIFF Image', '*.tiff')])

        if path:
            img_format = {
                'jpg': 'JPEG',
                'jpeg': 'JPEG',
                'png': 'PNG',
                'webp': 'WEBP',
                'tiff': 'TIFF',
            }.get(path.lower().rsplit('.', 1)[-1] if '.' in path else 'png', 'PNG')
            try:
                self.display_image.save(path, format=img_format)
                return True
            except Exception as e:
                return False
        return False

    def import_image(self):
        try:
            path = import_file(title='Select An Image', filetypes=[('Image Files', '*.jpg;*.jpeg;*.png;*.webp;*.tiff')])
            original_image = Image.open(path)
            if original_image.mode not in ('RGB', 'L'):
                original_image = original_image.convert('RGB')
        except:
            return False
        else:
            self.original_image = original_image
            self.display_image = original_image
            self.path = path
            return True

    def read(self, entry):
        return entry.get('1.0', 'end-1c').strip()

    def write(self, entry, text, disable=True):
        entry.configure(state='normal')
        entry.delete('1.0', 'end')
        entry.insert('end', text)
        if disable: entry.configure(state='disabled')

    @property
    def threshold(self):
        return int(self.wm_threshold_frame.value)