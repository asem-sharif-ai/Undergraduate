import tkinter as tk
import customtkinter as ctk
from tkinter.filedialog import askopenfilename as import_file, asksaveasfilename as export_file

import os
import cv2
import json
from PIL import Image, ImageTk
from threading import Thread

from GUI.Utils import SliderFrame

from Methods.Video import (
    validate, get_properties, format_properties,
    VideoFileClip,
    apply_dct_watermark, apply_dwt_watermark,
    export_video
)

from Methods.Image import binarize

class VideoFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.rowconfigure(index=(0, 1), weight=1, uniform='a')
        self.columnconfigure(index=(0, 2), weight=1, uniform='a')
        self.columnconfigure(index=1, weight=2, uniform='a')

    def build(self):
        self.canvas = tk.Canvas(self, bg='black', highlightthickness=1, highlightbackground='#303030')
        self.canvas.grid(row=0, column=1, padx=5, pady=(10, 5), sticky='nsew')

        self.after(50, self.show_frame)
        self.canvas.bind('<Configure>', self.show_frame)

        self.build_right_frame()
        self.build_left_frame()
        self.build_main_frame()
        
        self.after(50, self.write_info)
        
    def write_info(self):
        def write():
            if not hasattr(self, 'properties'):
                self.properties = get_properties(self.video_path, self.video_capture)
            self.write(self.info_box, format_properties(self.properties))
            self.save_info_btn.configure(state='normal')
        Thread(target=write, daemon=True).start()

    def build_left_frame(self):
        self.left_frame = ctk.CTkFrame(self)
        self.left_frame.grid(row=0, column=0, padx=(10, 5), pady=(10, 5), sticky='nsew')
        
        self.left_frame.rowconfigure(index=0, weight=5, uniform='a')
        self.left_frame.rowconfigure(index=1, weight=1, uniform='a')
        self.left_frame.columnconfigure(index=0, weight=1, uniform='a')
        
        self.info_box = ctk.CTkTextbox(self.left_frame, wrap='none', state='disabled',
                                       activate_scrollbars=False, font=('Courier New', 14, 'bold'))
        self.info_box.grid(row=0, column=0, padx=10, pady=(10, 5), sticky='nsew')

        self.save_info_btn = ctk.CTkButton(self.left_frame, text='Save', state='disabled', command=self.save_properties)
        self.save_info_btn.grid(row=1, column=0, padx=10, pady=(5, 10))

    def build_right_frame(self):
        self.right_frame = ctk.CTkFrame(self)
        self.right_frame.grid(row=0, column=2, padx=(5, 10), pady=(10, 5), sticky='nsew')
        
        self.right_frame.rowconfigure(index=0, weight=3, uniform='a')
        self.right_frame.rowconfigure(index=1, weight=6, uniform='a')
        self.right_frame.rowconfigure(index=2, weight=4, uniform='a')
        self.right_frame.columnconfigure(index=(0, 1), weight=1, uniform='a')

        self.play_frame = ctk.CTkFrame(self.right_frame)
        self.play_frame.grid(row=0, column=0, columnspan=2, padx=10, pady=(10, 0), sticky='nsew')

        self.play_frame.rowconfigure(index=0, weight=2, uniform='a')
        self.play_frame.rowconfigure(index=1, weight=1, uniform='a')
        self.play_frame.columnconfigure(index=(0, 1), weight=1, uniform='a')

        self.play_btn = ctk.CTkButton(self.play_frame, text='▶ Play', command=self.play_video)
        self.play_btn.grid(row=0, column=0, padx=(10, 5), pady=(10, 5), sticky='nsew')

        self.stop_btn = ctk.CTkButton(self.play_frame, text='■ Stop', command=self.stop_video, state='disabled')
        self.stop_btn.grid(row=0, column=1, padx=(5, 10), pady=(10, 5), sticky='nsew')

        self.play_bar = ctk.CTkProgressBar(self.play_frame)
        self.play_bar.grid(row=1, column=0, columnspan=2, padx=10, pady=(5, 10), sticky='ew')
        self.play_bar.set(0)

        self.extract_frame = ctk.CTkFrame(self.right_frame)
        self.extract_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=(10, 5), sticky='nsew')

        self.extract_frame.rowconfigure(index=(0, 1, 2), weight=1, uniform='a')
        self.extract_frame.columnconfigure(index=0, weight=1, uniform='a')

        self.extract_vid_btn = ctk.CTkButton(self.extract_frame, text='Extract Video', command=self.extract_video)
        self.extract_vid_btn.grid(row=0, column=0, rowspan=2, padx=10, pady=(0, 10))

        self.extract_aud_btn = ctk.CTkButton(self.extract_frame, text='Extract Audio', command=self.extract_audio)
        self.extract_aud_btn.grid(row=1, column=0, rowspan=2, padx=10, pady=(10, 0))

        self.manage_frame = ctk.CTkFrame(self.right_frame)
        self.manage_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=(5, 10), sticky='nsew')
        self.manage_frame.rowconfigure(index=(0, 1), weight=1, uniform='a')
        self.manage_frame.columnconfigure(index=(0, 1), weight=1, uniform='a')

        self.export_btn = ctk.CTkButton(self.manage_frame, text='Export', command=self.export_video)
        self.export_btn.grid(row=0, column=0, columnspan=2, padx=10, pady=(10, 5), sticky='ew')

        self.back_btn = ctk.CTkButton(self.manage_frame, text='Back', command=lambda: self.master.back(self))
        self.back_btn.grid(row=1, column=0, padx=(10, 5), pady=(5, 10), sticky='nsew')

        self.close_btn = ctk.CTkButton(self.manage_frame, text='Close', command=self.master.close)
        self.close_btn.grid(row=1, column=1, padx=(5, 10), pady=(5, 10), sticky='nsew')

    def build_main_frame(self):
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.grid(row=1, column=0, columnspan=3, padx=10, pady=(5, 10), sticky='nsew')

        self.main_frame.rowconfigure(index=(0, 1), weight=1, uniform='a')
        self.main_frame.columnconfigure(index=(0, 1, 2, 3), weight=1, uniform='a')

        self.display_frame = ctk.CTkFrame(self.main_frame)
        self.display_frame.grid(row=0, column=0, rowspan=2, padx=10, pady=10, sticky='nsew')

        self.display_frame.rowconfigure(index=(0, 2), weight=1, uniform='a')
        self.display_frame.rowconfigure(index=1, weight=2, uniform='a')
        self.display_frame.columnconfigure(index=(0, 2), weight=1, uniform='a')
        self.display_frame.columnconfigure(index=1, weight=5, uniform='a')
    
        frame = ctk.CTkFrame(self.display_frame)
        frame.grid(row=1, column=1, sticky='nsew')

        frame.rowconfigure(index=(0, 1, 2), weight=1, uniform='a')
        frame.columnconfigure(index=0, weight=1, uniform='a')

        self.display_var = ctk.StringVar(value='SRC')

        self.main_radio = ctk.CTkRadioButton(frame, text='View Source Video', value='SRC', variable=self.display_var,
                                             font=('Segoe UI', 12, 'bold'), command=self.set_default_source)
        self.main_radio.grid(row=0, column=0, padx=10, pady=10, sticky='nsw')

        self.dct_radio = ctk.CTkRadioButton(frame, text='Discrete Cosine Transform', value='HCT', variable=self.display_var,
                                            state='disabled', font=('Segoe UI', 12, 'bold'), command=self.set_default_source)
        self.dct_radio.grid(row=1, column=0, padx=10, pady=10, sticky='nsw')

        self.dwt_radio = ctk.CTkRadioButton(frame, text='Discrete Wavelet Transform', value='HWT', variable=self.display_var,
                                            state='disabled', font=('Segoe UI', 12, 'bold'), command=self.set_default_source)
        self.dwt_radio.grid(row=2, column=0, padx=10, pady=10, sticky='nsw')

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

        self.dct_alpha_frame = SliderFrame(
            master=self.dct_wm_frame,
            label='Alpha',
            value='10.0 α',
            format=lambda v: f'{float(v):.1f} α',
            command=lambda *args, **kwargs: self.dct_wm_btn.configure(state='normal', text='Embed'),
            slider_params={'from_': 1, 'to': 30, 'number_of_steps': 58}
        )
        self.dct_alpha_frame.set_slider(10)

        self.dwt_alpha_frame = SliderFrame(
            master=self.dwt_wm_frame,
            label='Alpha',
            value='10.0 α',
            format=lambda v: f'{float(v):.1f} α',
            command=lambda *args, **kwargs: self.dwt_wm_btn.configure(state='normal', text='Embed'),
            slider_params={'from_': 1, 'to': 30, 'number_of_steps': 58}
        )
        self.dwt_alpha_frame.set_slider(10)

    def set_default_source(self):
        self.video_src = {
            'SRC': self.video_capture,
            'HCT': self.video_capture,
            'HWT': self.video_capture
        }[self.display_var.get()]

    def show_method_frame(self, name):
        if name == 'DCT':
            self.dct_wm_btn.configure(text='Embed', command=self.apply_dct_watermark)
            self.dct_wm_btn.grid_configure(row=2, rowspan=1, pady=(5, 15))
            self.dct_alpha_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=(10, 0), sticky='nsew')

        elif name == 'DWT':
            self.dwt_wm_btn.configure(text='Embed', command=self.apply_dwt_watermark)
            self.dwt_wm_btn.grid_configure(row=2, rowspan=1, pady=(5, 15))
            self.dwt_alpha_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=(10, 0), sticky='nsew')

    def load_watermark(self, show=True):
        try:
            path = import_file(title='Select An Image', filetypes=[('Image Files', '*.jpg;*.jpeg;*.png;*.webp;*.tiff')])
            watermark = Image.open(path).convert('L')
            self.wm_path = path
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

                for btn in [self.dct_wm_btn, self.dwt_wm_btn]:
                    btn.configure(state='normal')
            else:
                return True

    def apply_dct_watermark(self):
        def apply():
            self.dct_wm_btn.configure(state='disabled', text='Embedding...')
            self.dct_video = apply_dct_watermark(self.video_path, self.wm_path, self.dct_alpha_frame.value)
            self.dct_radio.configure(state='normal')
            self.dct_wm_btn.configure(text='Embeded')
        Thread(target=apply, daemon=True).start()

    def apply_dwt_watermark(self):
        def apply():
            self.dwt_wm_btn.configure(state='disabled', text='Embedding...')
            self.dwt_video = apply_dwt_watermark(self.video_path, self.wm_path, self.dwt_alpha_frame.value)
            self.dwt_radio.configure(state='normal')
            self.dwt_wm_btn.configure(text='Embeded')
        Thread(target=apply, daemon=True).start()

    def binarize_watermark(self, *args, **kwargs):
        self.wm_display_image = binarize(self.wm_original_image, self.threshold, 'L')
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

    def remove_watermark(self):
        self.wm_display_image = None
        self.main_frame.destroy()
        self.build_main_frame()
        self.show_image()

    def reset_watermark(self):
        self.wm_display_image = self.wm_original_image
        self.wm_threshold_frame.set_value('---')
        self.wm_threshold_frame.set_slider(128)
        self.show_watermark()

    def extract_audio(self):
        path = export_file(title='Extract Audio', initialfile=f'{self.name}-[Audio]', defaultextension='.wav', filetypes=[('WAV File', '*.wav')])
        if path:
            clip = VideoFileClip(self.video_path)
            clip.audio.write_audiofile(path)

    def extract_video(self):
        path = export_file(
            title='Extract Video',
            initialfile=f'{self.name}-[Video]',
            defaultextension='.mkv',
            filetypes=[('MKV File', '*.mkv')]
        )
        if path:
            clip = VideoFileClip(self.video_path)
            clip = clip.without_audio()
            clip.write_videofile(path, codec='libx264')

    def export_video(self):
        path = export_file(title='Save Watermarked Video As', initialfile=f'Video-[{self.display_var.get()}]', defaultextension='.png',
        filetypes=[('MP4 Video', '*.mp4'), ('MKV Video', '*.mkv'), ('AVI Video', '*.avi')])

        if path:
            export_video(path, self.video_src)

    def play_video(self):
        self.play_btn.configure(text='■ Pause', command=self.pause_video)
        self.stop_btn.configure(state='normal')
        self.paused = False
        self.update_frame()

    def pause_video(self):
        self.paused = True
        self.play_btn.configure(text='▶ Play', command=self.play_video)

    def stop_video(self):
        self.play_btn.configure(text='▶ Play', command=self.play_video)
        self.stop_btn.configure(state='disabled')
        self.frame_idx = 0
        self.play_bar.set(0)
        self.paused = True
        self.show_frame()

    def show_frame(self, event=None, video_src=None, frame_idx=None):
        video_src = self.video_src if video_src is None else video_src
        frame_idx = self.frame_idx if frame_idx is None else max(0, min(frame_idx, self.frames_len))

        video_src.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
        ret, frame = video_src.read()

        if not ret:
            return

        image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
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

    def update_frame(self):
        if not self.paused:
            if self.frame_idx <= self.frames_len:
                self.show_frame()
                self.frame_idx += 1
                self.play_bar.set(self.frame_idx / self.frames_len)
                self.after(5, self.update_frame)
            else:
                self.stop_video()

    def import_video(self):
        try:
            path = import_file(title='Select A Video', filetypes=[('Video Files', '*.mp4;*.mkv')])
            if not path:
                return False

            cap, success = validate(path)
            if not success:
                return False
        except:
            return False
        else:
            self.video_capture = cap
            self.video_path    = path
            self.paused        = False

            self.video_src = cap
            self.frame_idx = 0
            self.dct_video = None
            self.dwt_video = None
            
            return True

    def save_properties(self):
        path = export_file(
            title='Export Properties',
            initialfile=f'{os.path.splitext(os.path.basename(self.video_path))[0]}-[Properties]',
            defaultextension='.json',
            filetypes=[('JSON File', '*.json'), ('Text File', '*.txt')]
        )

        if path:
            if path.endswith('.json'):
                with open(path, 'w') as file:
                    json.dump(self.properties, file, indent=4)
            elif path.endswith('.txt'):
                with open(path, 'w') as file:
                    file.write(format_properties(self.properties))

    def write(self, entry, text, disable=True):
        entry.configure(state='normal')
        entry.delete('1.0', 'end')
        entry.insert('end', text)
        if disable: entry.configure(state='disabled')

    def close(self):
        try:
            if getattr(self, 'video_capture', None) is not None:
                self.video_capture.release()
        except Exception as e:
            print(f'Error releasing video: {e}')

    @property
    def frames_len(self):
        return self.properties['Video']['Frame_Count']

    @property
    def name(self):
        return os.path.splitext(os.path.basename(self.video_path))[0]

    @property
    def threshold(self):
        return int(self.wm_threshold_frame.value)