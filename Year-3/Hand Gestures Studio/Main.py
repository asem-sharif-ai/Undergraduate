
import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

import tkinter as tk
import customtkinter as ctk

import cv2 as cv
import numpy as np
from PIL import Image, ImageTk

from threading import Thread

from Utils import *

ctk.set_appearance_mode(APP_MODE)
ctk.set_default_color_theme(CLR_MODE)

class App(ctk.CTk):
    def __init__(self):
        super().__init__(**DFD[0])

        self.title(APP_TITLE)

        self.setup()
        self.init_screen()

    def setup(self):
        self.dataset = None
        self.label = None

        self.capturer = None
        self.capturing = False
        self.detector = None
        self.detecting = False

        self.cnn = None
        self.cnn_is_activated = False
        self.__i__ = 0
        self.__l__ = 20

        self.shy = False
        self._dots = 0

        self.preprocess_index  = 0
        self.landmarks_on_blank = False
        self.show_raw_hand_image = False

        self.protocol('WM_DELETE_WINDOW', self.exit)

    def init_screen(self):
        self.geometry(f'{16*85}x{9*85}')
        self.minsize(16*50, 9*50)

        self.rowconfigure(index=(0, 1), weight=1, uniform=A)
        self.columnconfigure(index=0, weight=5, uniform=A)
        self.columnconfigure(index=1, weight=3, uniform=A)
        self.columnconfigure(index=2, weight=2, uniform=A)

    #! ----- ----- Camera | Process Frames ----- ----- ----- ----- ----- ----- ----- -----

        self.main_canvas = tk.Canvas(self, **DCD)
        self.main_canvas.grid(row=0, column=0, padx=(10, 5), pady=(10, 5), sticky='nsew')

        self.side_canvas = tk.Canvas(self, width=400, height=400, **DCD)
        self.side_canvas.grid(row=0, column=1, padx=5, pady=(10, 5), sticky=None)

        self.main_canvas.bind('<Button-1>', lambda _: setattr(self, 'shy', not self.shy))
        self.main_canvas.bind('<Button-3>', lambda _: setattr(self, 'shy', not self.shy))

        self.side_canvas.bind('<Button-1>', lambda _: setattr(self, 'landmarks_on_blank', not self.landmarks_on_blank))
        self.side_canvas.bind('<MouseWheel>', lambda e: setattr(self, 'preprocess_index', (self.preprocess_index + (1 if e.delta > 0 else -1)) % 4))
        self.side_canvas.bind('<ButtonPress-3>', lambda _: setattr(self, 'show_raw_hand_image', True))
        self.side_canvas.bind('<ButtonRelease-3>', lambda _: setattr(self, 'show_raw_hand_image', False))

        self.canvas_text = {self.main_canvas: None, self.side_canvas: None}

        self.update_canvas(self.main_canvas, text='Camera is Disabled')
        self.update_canvas(self.side_canvas, text='Detector is Disabled')

    #! ----- ----- Control Frame ----- ----- ----- ----- ----- ----- ----- -----

        self.control_section = ControlFrame(self)
        self.control_section.grid(row=0, column=2, padx=(5, 10), pady=(10, 5), sticky='nsew')

    #! ----- ----- Main Frame ----- ----- ----- ----- ----- ----- ----- -----

        #! ----- Model Frame ----- ----- ----- -----

        self.model_section = ModelFrame(self, self.dataset, self.label)
        self.model_section.grid(row=1, column=0, padx=(10, 5), pady=(5, 10), sticky='nsew')

        #! ----- Terminal Frame ----- ----- ----- -----

        self.terminal_section = TerminalFrame(self)
        self.terminal_section.grid(row=1, column=1, padx=5, pady=(5, 10), sticky='nsew')

        #! ----- Date Frame ----- ----- ----- -----

        self.data_section = DataFrame(self)
        self.data_section.grid(row=1, column=2, padx=(5, 10), pady=(5, 10), sticky='nsew')

    def open_camera(self, _=None):
        def open():
            self.capturer = cv.VideoCapture(0)
            if not self.capturer.isOpened():
                self.update_canvas(self.main_canvas, text='Error: Camera Process Failed')
                return
            self.capturing = True
            if self.detecting:
                self.enable(*[self.data_section.bars[i][2] for i in range(len(self.data_section.bars))])
            self.refresh_canvas()
        Thread(target=open, daemon=True).start()

    def close_camera(self, _=None):
        def close():
            self.capturing = False
            if self.capturer:
                self.capturer.release()
                self.capturer = None

            self.update_canvas(self.main_canvas, text='Camera is Disabled')
            self.update_canvas(self.side_canvas, text='Detector is Disabled')

            if self.data_section.bars:
                self.disable(*[bar[2] for bar in self.data_section.bars])

        Thread(target=close, daemon=True).start()

    def open_detector(self, _=None):
        self.detecting = True
        self.enable(*[self.data_section.bars[i][2] for i in range(len(self.data_section.bars))])
        if self.cnn is not None:
            self.enable(self.control_section.activate_model_btn)

    def close_detector(self, _=None):
        self.detecting = False
        self.update_canvas(self.side_canvas, text='Detector is Disabled')
        self.disable(*[self.data_section.bars[i][2] for i in range(len(self.data_section.bars))], self.control_section.activate_model_btn)

    def update_detector(self, base):
        if self.detecting:
            self.close_detector()
            self.detector = Detector(**base)
            self.open_detector()
        else:
            self.detector = Detector(**base)

    @property
    def cnn_is_accepting(self): # return True once every __l__ [10:30] calls if cnn_is_activated else False
        self.__i__ = (self.__i__ + 1) % self.__l__
        return self.__i__ == 0 and self.cnn_is_activated

    def predict(self, hand_image):
        hand_image = cv.resize(hand_image, self.cnn.shape)
        prediction, confidence = self.cnn.predict(matrix=hand_image, return_confidence=True, return_decoded=True)
        self.control_section.update_prediction(prediction, confidence)

    def refresh_canvas(self):
        if self.capturing:
            ok, image = self.capturer.read()
            if ok:
                image = self.control_section.apply_camera_settings(image)
                if self.detecting:
                    image, hands = self.detector.detect(
                        image=image,
                        **self.control_section.detector_settings['method'],
                        landmarks_on_blank=self.landmarks_on_blank
                    )
                    if hands:
                        hand_image = Detector.preprocess_image(
                            image=hands[0],
                            index=self.preprocess_index,
                            is_blank=self.landmarks_on_blank
                        )
                        self.clear_canvas(self.side_canvas)
                        self.update_canvas(self.side_canvas, image=hand_image if not self.show_raw_hand_image else hands[0])

                        if self.cnn_is_activated and self.cnn_is_accepting:
                            Thread(target=self.predict, kwargs={'hand_image':hand_image}, daemon=True).start()

                        if self.data_section.capturing:
                            self.data_section.capture(hand_image, self.control_section.detector_settings['sample_size'])
                    else:
                        self.update_canvas(self.side_canvas, text='No Hands Detected')
                        self.control_section.remove_prediction()

                self.update_canvas(
                    self.main_canvas,
                    **{'image': image if self.detecting else cv.cvtColor(image, cv.COLOR_BGR2RGB)} if not self.shy else {'text': self.__dots()}
                )

            self.main_canvas.after(10, self.refresh_canvas)

    def update_canvas(self, canvas, image=None, text=None):
        if image is not None:
            if isinstance(image, np.ndarray):
                image = Image.fromarray(image)

            image_w, image_h = image.size
            canvas_w = canvas.winfo_width()
            canvas_h = canvas.winfo_height()

            scale = min(canvas_w / image_w, canvas_h / image_h)
            width, height = int(image_w * scale), int(image_h * scale)
            
            image = ImageTk.PhotoImage(image.resize((width, height), Image.Resampling.LANCZOS))

            self.clear_canvas(self.main_canvas)
            canvas.create_image(
                (canvas_w - width) // 2, 
                (canvas_h - height) // 2, 
                image=image, 
                anchor=tk.NW
            )

            if canvas == self.main_canvas:
                self.camera_feed = image
            else:
                self.hand_feed = image
        else:
            canvas.delete('all')
            try:
                self.canvas_text[canvas].destroy()
                self.canvas_text[canvas] = None
            except:
                pass
            finally:
                if text is not None:
                    canvas_text = tk.Label(canvas, text=text, font=('Courier', 15), fg='#000000', bg='white')
                    canvas_text.place(relx=0.5, rely=0.5, anchor='center')
                    self.canvas_text[canvas] = canvas_text

    def clear_canvas(self, canvas):
        return self.update_canvas(canvas)

    def update_data_section(self, filename):
        self.data_section.destroy()
        self.data_section = DataFrame(self)
        self.data_section.grid(row=1, column=2, padx=(5, 10), pady=(5, 10), sticky='nsew')
        self.data_section.import_dataset(filename)

    def update_data(self, dataset=None, label=None, remove=False):
        if dataset is not None or remove:
            self.dataset = dataset
            self.model_section.dataset = dataset
        if label is not None or remove:
            self.label = label
            self.model_section.label = label
        self.model_section.validate_data()

    def restart(self):
        for i in [self.main_canvas, self.side_canvas, self.data_section, self.model_section, self.control_section]:
            i.destroy()
        self.setup()
        self.init_screen()

    def exit(self):
        self.close_camera()
        self.destroy()

    def write(self, text, clear=False, nn=2):
        if clear:
            self.terminal_section.clear()
        self.terminal_section.write(text, nn=nn)

    def enable(self, *wids):
        for wid in wids:
            wid.configure(state=NRM)

    def disable(self, *wids):
        for wid in wids:
            wid.configure(state=DIS)

    def __dots(self):
        self._dots = (self._dots % 100) + 1
        return '●'*(((self._dots - 1) // 20) + 1)

    @staticmethod
    def run():
        app = App()
        app.mainloop()
