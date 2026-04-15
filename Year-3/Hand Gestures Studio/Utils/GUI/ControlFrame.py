import tkinter as tk
import customtkinter as ctk

import cv2 as cv

from Utils.GUI.Data import * 
from Utils.Models import Helper

class ControlFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **DFD[1])
        self.master = master

        self.rowconfigure(index=0, weight=7, uniform=A)
        self.rowconfigure(index=1, weight=1, uniform=A)
        self.columnconfigure(index=0, weight=1, uniform=A)

        self.main_frame = ctk.CTkFrame(self, **DFD[1])
        self.main_frame.grid(row=0, column=0, rowspan=2, sticky='nsew')

        self.main_frame.rowconfigure(index=0, weight=3, uniform=A)
        self.main_frame.rowconfigure(index=1, weight=5, uniform=A)
        self.main_frame.rowconfigure(index=2, weight=2, uniform=A)
        self.main_frame.columnconfigure(index=0, weight=1, uniform=A)

        #! ---------- ---------- ---------- ---------- ----------

        self.main_frame_01 = ctk.CTkFrame(self.main_frame, **DFD[0])
        self.main_frame_01.grid(row=0, column=0, padx=10, pady=(10, 5), sticky='nsew')
        
        self.main_frame_01.rowconfigure(index=(0, 1), weight=1, uniform=A)
        self.main_frame_01.columnconfigure(index=(0, 1), weight=1, uniform=A)

        self.camera_btn = ctk.CTkButton(self.main_frame_01, text='Open Camera', command=self._open_camera, **DBD)
        self.camera_btn.grid(row=0, column=0, padx=(10, 5), pady=(10, 5), sticky='se')

        self.detect_btn = ctk.CTkButton(self.main_frame_01, text='Open Detector', command=self._open_detector, state=DIS, **DBD)
        self.detect_btn.grid(row=0, column=1, padx=(5, 10), pady=(10, 5), sticky='sw')
        
        self.settings_btn = ctk.CTkButton(self.main_frame_01, text='Settings', command=self.show_settings_frame, **DBD)
        self.settings_btn.grid(row=1, column=0, columnspan=2, padx=10, pady=(5, 10), sticky='new')
        
        #! ---------- ---------- ---------- ---------- ----------
        
        self.main_frame_02 = ctk.CTkFrame(self.main_frame, **DFD[0])
        self.main_frame_02.grid(row=1, column=0, padx=10, pady=5, sticky='nsew')
        
        self.main_frame_02.rowconfigure(index=(0, 2), weight=2, uniform=A)
        self.main_frame_02.rowconfigure(index=1, weight=3, uniform=A)
        self.main_frame_02.columnconfigure(index=(0, 1), weight=1, uniform=A)

        self.activate_model_btn = ctk.CTkButton(self.main_frame_02, text='Activate Model', command=None, state=DIS, **DBD)
        self.activate_model_btn.grid(row=0, column=0, columnspan=2, padx=10, pady=(10, 5), sticky='nsew')

        self.has_prediction = False

        fr_1 = ctk.CTkFrame(self.main_frame_02, **DFD[1])
        fr_1.grid(row=1, column=0, columnspan=2, padx=10, pady=2.5, sticky='nsew')
        fr_1.rowconfigure(index=0, weight=1, uniform=A)
        fr_1.columnconfigure(index=(0, 1), weight=1, uniform=A)

        self.prediction_lbl = ctk.CTkLabel(fr_1, text=f'●', fg_color='#101010', corner_radius=7.5, font=('Consolas', 16, 'bold'))
        self.prediction_lbl.grid(row=0, column=0, padx=(10, 5), pady=10, sticky='nsew')

        self.confidence_lbl = ctk.CTkLabel(fr_1, text=f'●', fg_color='#101010', corner_radius=7.5, font=('Consolas', 16, 'bold'))
        self.confidence_lbl.grid(row=0, column=1, padx=(5, 10), pady=10, sticky='nsew')

        self.save_model_btn = ctk.CTkButton(self.main_frame_02, text='Save', command=None, state=DIS, **DBD)
        self.save_model_btn.grid(row=2, column=1, padx=(5, 10), pady=(5, 10), sticky='nsew')

        fr_2 = ctk.CTkFrame(self.main_frame_02, **DFD[1])
        fr_2.grid(row=2, column=0, padx=(10, 5), pady=(5, 10), sticky='nsew')
        fr_2.rowconfigure(index=0, weight=1, uniform=A)
        fr_2.columnconfigure(index=0, weight=1, uniform=A)

        self.set_smooth = ctk.CTkSlider(fr_2, from_=10, to=30, number_of_steps=20, command=lambda l: setattr(self.master, '__l__', int(l)), **DSD)
        self.set_smooth.grid(row=0, column=0, padx=5, pady=5, sticky='se')

        #! ---------- ---------- ---------- ---------- ----------

        self.main_frame_03 = ctk.CTkFrame(self.main_frame, **DFD[0])
        self.main_frame_03.grid(row=2, column=0, padx=10, pady=(5, 10), sticky='nsew')

        self.main_frame_03.rowconfigure(index=0, weight=1, uniform=A)
        self.main_frame_03.columnconfigure(index=(0, 1), weight=1, uniform=A)

        self.restart_btn = ctk.CTkButton(self.main_frame_03, text='Restart', command=self.master.restart, **DBD)
        self.restart_btn.grid(row=0, column=0, padx=(10, 5), pady=10, sticky='ew')

        self.exit_btn = ctk.CTkButton(self.main_frame_03, text='Exit App', command=self.master.exit, **DBD)
        self.exit_btn.grid(row=0, column=1, padx=(5, 10), pady=10, sticky='ew')
        
    #! ---------- ---------- ---------- ---------- ---------- ---------- ---------- ---------- ---------- ----------
    
        self.back_btn = ctk.CTkButton(self, text='Back', command=None, **DBD)
        
        self.main_frame_grid = {'row':0, 'column':0, 'rowspan':2, 'sticky':'nsew'}
        self.sub_frames_grid = {'row':0, 'column':0, 'pady':(0, 5), 'sticky':'nsew'}
    
    #! ---------- ---------- ---------- ---------- ---------- ---------- ---------- ---------- ---------- ----------

        self.settings_frame = ctk.CTkFrame(self, **DFD[1])

        self.settings_frame.rowconfigure(index=(0, 4), weight=3, uniform=A)
        self.settings_frame.rowconfigure(index=(1, 2, 3), weight=2, uniform=A)
        self.settings_frame.columnconfigure(index=0, weight=1, uniform=A)

        self.camera_settings_btn = ctk.CTkButton(self.settings_frame, text='Camera  Settings', width=175, command=self.show_camera_frame, **DBD)
        self.camera_settings_btn.grid(row=1, column=0, padx=10, pady=(10, 0))

        self.detector_settings_btn = ctk.CTkButton(self.settings_frame, text='Detector  Settings', width=175, command=self.show_detector_frame, **DBD)
        self.detector_settings_btn.grid(row=2, column=0, padx=10, pady=5)

        ctk.CTkButton(self.settings_frame, text='', width=175, state=DIS, **DBD).grid(row=3, column=0, padx=10, pady=(0, 10))
        self.import_export_btn = ctk.CTkSegmentedButton(self.settings_frame, values=['  Import  ', '  Export  '],
                                 fg_color='#8B0000', selected_color='#8B0000', selected_hover_color='#008000',
                                 unselected_color='#8B0000', unselected_hover_color='#008000', bg_color='#8B0000',
                                 command=lambda todo: self.import_settings() if todo == '  Import  ' else self.export_settings(),
                                 )
        self.import_export_btn.grid(row=3, column=0, padx=10, pady=(0, 10))

        self.dynamic_labels = {}

        #! ---------- ---------- ---------- ---------- ----------
        
        self.camera_settings_frame = ctk.CTkScrollableFrame(self,
                                                            fg_color='#050505',
                                                            scrollbar_fg_color='#050505',
                                                            scrollbar_button_color='#101010',
                                                            scrollbar_button_hover_color='#151515')

        self.camera_settings = {
            'brightness': 0,
            'contrast': 1,
            'saturation': 1,
            'exposure': 0,
            'gamma': 1,
            'hue': 0
        }

        self.camera_sliders = {
            'Brightness': ctk.CTkSlider(self.camera_settings_frame, from_=-255, to=255,
                command=lambda value: self.update_camera('brightness', value), **DSD),
            'Contrast': ctk.CTkSlider(self.camera_settings_frame, from_=0.1, to=5,
                command=lambda value: self.update_camera('contrast', value), **DSD),
            'Saturation': ctk.CTkSlider(self.camera_settings_frame, from_=0.1, to=5,
                command=lambda value: self.update_camera('saturation', value), **DSD),
            'Exposure': ctk.CTkSlider(self.camera_settings_frame, from_=-255, to=255,
                command=lambda value: self.update_camera('exposure', value), **DSD),
            'Gamma': ctk.CTkSlider(self.camera_settings_frame, from_=0.1, to=2.5,
                command=lambda value: self.update_camera('gamma', value), **DSD),
            'Hue': ctk.CTkSlider(self.camera_settings_frame, from_=-180, to=180,
                command=lambda value: self.update_camera('hue', value), **DSD),
        }

        self.camera_settings_frame.rowconfigure(index=tuple(range(len(self.camera_sliders) * 2 + 1)), weight=1, uniform=A)
        self.camera_settings_frame.columnconfigure(index=(0, 1), weight=1, uniform=A)

        camera_keys = list(self.camera_sliders.keys())
        camera_slds = list(self.camera_sliders.values())
        for i in range(len(self.camera_sliders)):
            ctk.CTkLabel(self.camera_settings_frame, text=camera_keys[i], text_color='#efefef').grid(row=2 * i, column=0, padx=(20, 0), pady=(5, 0), sticky='sw')
            self.dynamic_labels[camera_keys[i]] = ctk.CTkLabel(self.camera_settings_frame, text='', text_color='#efefef')
            self.dynamic_labels[camera_keys[i]].grid(row=2 * i, column=1, padx=(5, 15), pady=(5, 0), sticky='se')
            camera_slds[i].grid(row=2 * i + 1, column=0, columnspan=2, padx=(15, 10), pady=(0, 10), sticky='new')
    
        self.default_camera_btn =  ctk.CTkButton(self.camera_settings_frame, text='Defaults', state=DIS, command=self.apply_camera_defaults, **DBD)
        self.default_camera_btn.grid(row=len(self.camera_sliders) * 2, column=0, columnspan=2, padx=(5, 0), pady=(0, 10), sticky='ns')

        #! ---------- ---------- ---------- ---------- ----------
        
        self.detector_settings_frame = ctk.CTkFrame(self, **DFD[1])

        self.detector_settings_tabs = ctk.CTkTabview(self.detector_settings_frame, **DTVD)
        self.detector_settings_tabs.pack(fill='both', expand=True)
        
        for tab in ['  Base  ', '  Method  ', '  Draw  ']:
            self.detector_settings_tabs.add(tab)

        self.detector_base_frame = self.detector_settings_tabs.tab('  Base  ')
        self.detector_method_frame = self.detector_settings_tabs.tab('  Method  ')
        self.detector_draw_frame = self.detector_settings_tabs.tab('  Draw  ')

        self.detector_settings = {
            'base': {
                'static_mode': False,
                'number_of_hands': 2,
                'complexity': 1,
                'detection_confidence': 0.5,
                'tracking_confidence': 0.5,
            },
            'method': {
                'draw': {
                    'draw_landmarks': True,
                    'draw_bounding_box': False,
                    'landmarks_color': (255, 255, 255),
                    'landmarks_thickness': 2,
                    'connections_color': (0, 0, 0),
                    'connections_thickness': 2,
                    'bounding_box_color': (0, 0, 0),
                    'bounding_box_thickness': 2,
                    'padding': 15,
                },
                'output_size': 8,   # x28
                'padding': 15,
                'output_shape': 2,  # ['None', 'Border', 'Square']
                'flip': True,
            },
            'sample_size': 100,
            }

        self.detector_sliders = {
            'base': {
                'Complexity': ctk.CTkSlider(self.detector_base_frame, from_=0, to=1, number_of_steps=1,
                    command=lambda value: self.update_detector('Complexity', int(value)), **DSD),
                'Number of Hands': ctk.CTkSlider(self.detector_base_frame, from_=1, to=4, number_of_steps=3,
                    command=lambda value: self.update_detector('Number of Hands', int(value)), **DSD),
                'Detection Confidence': ctk.CTkSlider(self.detector_base_frame, from_=0.01, to=0.99,
                    command=lambda value: self.update_detector('Detection Confidence', round(value, 2)), **DSD),
                'Tracking Confidence': ctk.CTkSlider(self.detector_base_frame, from_=0.01, to=0.99,
                    command=lambda value: self.update_detector('Tracking Confidence', round(value, 2)), **DSD),
            },
            'method': {
                'Padding': ctk.CTkSlider(self.detector_method_frame, from_=0, to=50,
                    command=lambda value: self.update_detector('Padding', value), **DSD),
                'Output Size': ctk.CTkSlider(self.detector_method_frame, from_=1, to=10, number_of_steps=9,
                    command=lambda value: self.update_detector('Output Size', value), **DSD),
                'Output Shape': ctk.CTkSlider(self.detector_method_frame, from_=0, to=2, number_of_steps=2,
                    command=lambda value: self.update_detector('Output Shape', value), **DSD),
            },
            'Sample Size': ctk.CTkSlider(self.detector_method_frame, from_=1, to=100,
                    command=lambda value: self.update_detector('Sample Size', value), **DSD),
        }

        #! ---------- ---------- ---------- ---------- ----------
        
        detector_base_keys = list(self.detector_sliders['base'].keys())
        detector_base_slds = list(self.detector_sliders['base'].values())

        self.detector_base_frame.rowconfigure(index=tuple(range(len(detector_base_keys) * 2 + 2)), weight=1, uniform=A)
        self.detector_base_frame.columnconfigure(index=(0, 1), weight=1, uniform=A)

        row = 0
        for i in range(len(detector_base_keys)):
            label = ctk.CTkLabel(self.detector_base_frame, text=detector_base_keys[i], text_color='#efefef')
            label.grid(row=row, column=0, columnspan=2, padx=(15, 5), pady=(5, 0), sticky='sw')
            self.dynamic_labels[detector_base_keys[i]] = ctk.CTkLabel(self.detector_base_frame, text='', text_color='#efefef')
            self.dynamic_labels[detector_base_keys[i]].grid(row=row, column=1, padx=(5, 15), pady=(5, 0), sticky='se')
            detector_base_slds[i].grid(row=row + 1, column=0, rowspan=2, columnspan=2, padx=10, pady=(5, 10), sticky='new')
            row += 2

        self.update_base_btn = ctk.CTkButton(self.detector_base_frame, text='Update', state=DIS, command=self.update_detector_base, **DBD)
        self.update_base_btn.grid(row=row, column=0, rowspan=2, padx=(15, 5), pady=(5, 0), sticky='sew')

        self.default_base_btn = ctk.CTkButton(self.detector_base_frame, text='Defaults', state=DIS, command=lambda: self.apply_detector_defaults('base'), **DBD)
        self.default_base_btn.grid(row=row, column=1, rowspan=2, padx=(5, 15), pady=(5, 0), sticky='sew')

        #! ---------- ---------- ---------- ---------- ----------

        detector_method_keys = list(self.detector_sliders['method'].keys()) + ['Sample Size']
        detector_method_slds = list(self.detector_sliders['method'].values()) + [self.detector_sliders['Sample Size']]

        self.detector_method_frame.rowconfigure(index=tuple(range(len(detector_method_keys) * 2 + 2)), weight=1, uniform=A)
        self.detector_method_frame.columnconfigure(index=(0, 1), weight=1, uniform=A)

        row = 0
        for i in range(len(detector_method_keys)):
            label = ctk.CTkLabel(self.detector_method_frame, text=detector_method_keys[i], text_color='#efefef')
            label.grid(row=row, column=0, columnspan=2, padx=(15, 5), pady=(5, 0), sticky='sw')
            self.dynamic_labels[detector_method_keys[i]] = ctk.CTkLabel(self.detector_method_frame, text='', text_color='#efefef')
            self.dynamic_labels[detector_method_keys[i]].grid(row=row, column=1, padx=(5, 15), pady=(5, 0), sticky='se')
            detector_method_slds[i].grid(row=row + 1, column=0, rowspan=2, columnspan=2, padx=10, pady=(5, 10), sticky='new')
            row += 2

        self.default_method_btn = ctk.CTkButton(self.detector_method_frame, text='Defaults', state=DIS, command=lambda: self.apply_detector_defaults('method'), **DBD)
        self.default_method_btn.grid(row=row, column=0, rowspan=2, columnspan=2, padx=15, pady=(5, 0), sticky='sew')

        #! ---------- ---------- ---------- ---------- ----------

        self.detector_draw_frame.rowconfigure(index=0, weight=3, uniform='A')
        self.detector_draw_frame.rowconfigure(index=1, weight=4, uniform='A')
        self.detector_draw_frame.columnconfigure(index=0, weight=1, uniform='A')

        self.detector_draw_frame_01 = ctk.CTkFrame(self.detector_draw_frame, **DFD[1])
        self.detector_draw_frame_01.grid(row=0, column=0, padx=10, pady=(10, 5), sticky='nsew')

        self.detector_draw_frame_01.rowconfigure((0, 1), weight=1, uniform=A)
        self.detector_draw_frame_01.columnconfigure(0, weight=1, uniform=A)

        self.draw_lm = ctk.BooleanVar(value=True)
        self.lm_check = ctk.CTkCheckBox(self.detector_draw_frame_01, command=self.update_draw, variable=self.draw_lm, text='  Landmarks', **DCBD)
        self.lm_check.grid(row=0, column=0, padx=15, pady=(10, 5), sticky='nw')

        self.draw_bb = ctk.BooleanVar(value=False)
        self.bb_check = ctk.CTkCheckBox(self.detector_draw_frame_01, command=self.update_draw, variable=self.draw_bb, text='  Bounding Box', **DCBD)
        self.bb_check.grid(row=1, column=0, padx=15, pady=(5, 10), sticky='sw')

        self.detector_draw_frame_02 = ctk.CTkFrame(self.detector_draw_frame, **DFD[1])
        self.detector_draw_frame_02.grid(row=1, column=0, padx=10, pady=(5, 10), sticky='nsew')

        self.detector_draw_frame_02.rowconfigure(index=(0, 1, 2), weight=1, uniform=A)
        self.detector_draw_frame_02.columnconfigure(index=0, weight=4, uniform=A)
        self.detector_draw_frame_02.columnconfigure(index=(1, 2), weight=1, uniform=A)

        self.r_sld = ctk.CTkSlider(self.detector_draw_frame_02, command=self.update_draw, **{**C_SLD, 'button_color': '#8B0000'})
        self.r_sld.grid(row=1, column=0, padx=(10, 5), pady=10, sticky='ew')

        self.g_sld = ctk.CTkSlider(self.detector_draw_frame_02, command=self.update_draw, **{**C_SLD, 'button_color': '#008B00'})
        self.g_sld.grid(row=2, column=0, padx=(10, 5), pady=10, sticky='ew')

        self.b_sld = ctk.CTkSlider(self.detector_draw_frame_02, command=self.update_draw, **{**C_SLD, 'button_color': '#00008B'})
        self.b_sld.grid(row=3, column=0, padx=(10, 5), pady=10, sticky='ew')

        self.t_sld = ctk.CTkSlider(self.detector_draw_frame_02, command=self.update_draw, orientation=VRT, **T_SLD)
        self.t_sld.grid(row=1, column=1, rowspan=3, padx=5, pady=5, sticky='ns')

        self.s_sld = ctk.CTkSlider(self.detector_draw_frame_02, orientation=VRT, **S_SLD)
        self.s_sld.grid(row=1, column=2, rowspan=3, padx=5, pady=25, sticky='ns')

        #! ---------- ---------- ---------- ---------- ----------

        self.apply_camera_defaults()
        self.apply_detector_defaults()

    def update_prediction(self, pred, conf):
        self.has_prediction = True
        fg = '#008000' if conf >= 75 else '#8B0000' if conf <= 50 else 'orange'
        self.prediction_lbl.configure(text=f'{pred}', fg_color=fg)
        self.confidence_lbl.configure(text=f'{conf:.2f}', fg_color=fg)

    def remove_prediction(self):
        if self.has_prediction:
            self.prediction_lbl.configure(text='●', fg_color='#101010')
            self.confidence_lbl.configure(text='●', fg_color='#101010')

    def update_camera(self, label, value):
        self.camera_settings[label] = value
        if label in ['brightness', 'exposure', 'hue']:
            self.dynamic_labels[label.capitalize()].configure(text=f'{"+" if value > 0 else ''}{int(value)}')
        else:
            self.dynamic_labels[label.capitalize()].configure(text=f'{round(value, 2)}')
        if self.default_camera_btn._state == DIS:
            self.enable(self.default_camera_btn)

    def apply_camera_settings(self, image):
        if self.camera_settings['brightness'] != 0:
            image = cv.add(image, self.camera_settings['brightness'])
        if self.camera_settings['contrast'] != 1.0:
            image = cv.convertScaleAbs(image, alpha=self.camera_settings['contrast'], beta=0)
        if self.camera_settings['gamma'] != 1 or self.camera_settings['exposure'] != 0:
            image = cv.convertScaleAbs(image, alpha=self.camera_settings['gamma'], beta=self.camera_settings['exposure'])
        if self.camera_settings['saturation'] != 1.0 or self.camera_settings['hue'] != 0:
            image = cv.cvtColor(image, cv.COLOR_BGR2HSV)
            image[:, :, 1] = cv.multiply(image[:, :, 1], self.camera_settings['saturation'])
            image[:, :, 0] = (image[:, :, 0] + self.camera_settings['hue']) % 180
            image = cv.cvtColor(image, cv.COLOR_HSV2BGR)
        return image

    def apply_camera_defaults(self):
        self.camera_settings = {
            'brightness': 0,
            'contrast': 1,
            'saturation': 1,
            'exposure': 0,
            'gamma': 1,
            'hue': 0
        }
        for label, slider in self.camera_sliders.items():
            value = self.camera_settings[label.lower()]
            slider.set(value)
            self.update_camera(label, value)
        self.disable(self.default_camera_btn)

    def update_detector(self, label, value):
        if label in ['Complexity', 'Number of Hands', 'Detection Confidence', 'Tracking Confidence']:
            self.detector_settings['base'][label.replace(' ', '_').lower()] = value
            self.dynamic_labels[label].configure(text=f'{value}')
            if self.default_base_btn._state == DIS:
                self.disable(self.default_base_btn)
            if self.update_base_btn._state == DIS:
                self.enable(self.update_base_btn, self.default_base_btn)
        else:
            if label == 'Padding':
                value = round(value)
                self.detector_settings['method']['padding'] = round(value)
                self.dynamic_labels[label].configure(text=f'{value} Pixels')
                self.detector_settings['method']['draw']['padding'] = value
            elif label == 'Output Size':
                value = 28 * round(value)
                self.detector_settings['method']['output_size'] = value
                self.dynamic_labels[label].configure(text=f'{value}x{value}')
            elif label == 'Output Shape':
                value = ['None', 'Border', 'Square'][int(value)]
                self.detector_settings['method']['output_shape'] = value
                self.dynamic_labels[label].configure(text=f'{value}')
            elif label == 'Sample Size':
                value = 10 * round(value)
                self.detector_settings['sample_size'] = value
                self.dynamic_labels[label].configure(text=f'{value} Images')

            if self.default_method_btn._state == DIS:
                self.enable(self.default_method_btn)

    def update_detector_base(self):
        self.master.update_detector(self.detector_settings['base'])
        self.disable(self.update_base_btn)

    def apply_detector_defaults(self, base_or_method=None):
        if base_or_method == 'base':
            settings = {'static_mode': False,
                        'number_of_hands': 1,
                        'complexity': 1,
                        'detection_confidence': 0.5,
                        'tracking_confidence': 0.5,
                }
            for label, slider in self.detector_sliders['base'].items():
                value = settings[label.lower().replace(' ', '_')]
                slider.set(value)
                self.update_detector(label, value)
    
            self.disable(self.default_base_btn, self.update_base_btn)
            self.update_detector_base()
        
        elif base_or_method == 'method':
            settings = {'draw': {
                            'draw_landmarks': True,
                            'draw_bounding_box': False,
                            'landmarks_color': (255, 255, 255), # Fixed
                            'landmarks_thickness': 2,
                            'connections_color': (0, 0, 0),
                            'connections_thickness': 2,
                            'bounding_box_color': (0, 0, 0),
                            'bounding_box_thickness': 2,
                            'padding': 15,
                        },
                        'output_size': 8,
                        'padding': 15,
                        'output_shape': 2,
                        'flip': True,
                }
            for label, slider in self.detector_sliders['method'].items():
                value = settings[label.lower().replace(' ', '_')]
                slider.set(value)
                self.update_detector(label, value)

            self.draw_lm.set(True)
            self.draw_bb.set(False)
            for sld in [self.r_sld, self.g_sld, self.b_sld, self.s_sld]:
                sld.set(0)
            self.t_sld.set(2)

            self.detector_sliders['Sample Size'].set(10)
            self.update_detector('Sample Size', 10)
            self.disable(self.default_method_btn)
        else:
            self.apply_detector_defaults('base')
            self.apply_detector_defaults('method')

    def update_draw(self, *_, **__):
        R = int(self.r_sld.get())
        G = int(self.g_sld.get())
        B = int(self.b_sld.get())
        T = int(self.t_sld.get())

        S = self.s_sld.get()
        if S == 0:
            self.detector_settings['method']['draw']['connections_color'] = (B, G, R)
            self.detector_settings['method']['draw']['connections_thickness'] = T
        elif S == 1:
            self.detector_settings['method']['draw']['landmarks_color'] = (B, G, R)
            self.detector_settings['method']['draw']['landmarks_thickness'] = T
        elif S == 2:
            self.detector_settings['method']['draw']['bounding_box_color'] = (B, G, R)
            self.detector_settings['method']['draw']['bounding_box_thickness'] = T
        else:
            self.detector_settings['method']['draw']['connections_color'] = (B, G, R)
            self.detector_settings['method']['draw']['connections_thickness'] = T
            self.detector_settings['method']['draw']['landmarks_color'] = (B, G, R)
            self.detector_settings['method']['draw']['landmarks_thickness'] = T
            self.detector_settings['method']['draw']['bounding_box_color'] = (B, G, R)
            self.detector_settings['method']['draw']['bounding_box_thickness'] = T

        self.detector_settings['method']['draw']['draw_landmarks'] = self.draw_lm.get()
        self.detector_settings['method']['draw']['draw_bounding_box'] = self.draw_bb.get()

    def _open_camera(self):
        self.master.open_camera()
        self.camera_btn.configure(text='Close Camera', command=self._close_camera, **DBD)
        self.enable(self.detect_btn, *[sld for sld in self.camera_sliders.values()])

    def _close_camera(self):
        self.master.close_camera()
        self.camera_btn.configure(text='Open Camera', command=self._open_camera, **DBD)
        self.disable(self.detect_btn, self.default_camera_btn, *[sld for sld in self.camera_sliders.values()])
        self._close_detector()

    def _open_detector(self):
        self.master.open_detector()
        self.detect_btn.configure(text='Close Detector', command=self._close_detector, **DBD)
        self.enable(
            *[sld for sld in self.detector_sliders['base'].values()],
            *[sld for sld in self.detector_sliders['method'].values()],
            *[self.detector_sliders['Sample Size'], self.update_base_btn, self.default_base_btn],
            *[self.r_sld, self.g_sld, self.b_sld, self.t_sld, self.s_sld, self.lm_check, self.bb_check]
        )
        self.disable(self.update_base_btn, self.default_base_btn)

    def _close_detector(self):
        self.master.close_detector()
        self.detect_btn.configure(text='Open Detector', command=self._open_detector, **DBD)
        self.disable(
            *[sld for sld in self.detector_sliders['base'].values()],
            *[sld for sld in self.detector_sliders['method'].values()],
            *[self.detector_sliders['Sample Size'], self.update_base_btn, self.default_base_btn],
            *[self.r_sld, self.g_sld, self.b_sld, self.t_sld, self.s_sld, self.lm_check, self.bb_check]
        )


    def show_settings_frame(self):
        self.main_frame.grid_forget()
        self.settings_frame.grid(**self.sub_frames_grid)
        self.back_btn.configure(command=self.back_to_main)
        self.back_btn.grid(row=1, column=0, pady=(5, 10), sticky='ns')

    def back_to_main(self):
        self.settings_frame.grid_forget()
        self.main_frame.grid(row=0, column=0, rowspan=2, sticky='nsew')
        self.back_btn.grid_forget()

    def show_camera_frame(self):
        self.settings_frame.grid_forget()
        self.camera_settings_frame.grid(**self.sub_frames_grid)
        self.back_btn.configure(command=lambda: self.back_to_settings(self.camera_settings_frame))

    def show_detector_frame(self):
        self.settings_frame.grid_forget()
        self.detector_settings_frame.grid(**self.sub_frames_grid)
        self.back_btn.configure(command=lambda: self.back_to_settings(self.detector_settings_frame))

    def back_to_settings(self, frame):
        frame.grid_forget()
        self.settings_frame.grid(**self.sub_frames_grid)
        self.back_btn.configure(command=self.back_to_main)

    def import_settings(self):
        json = Helper.import_settings()
        if json:
            self.camera_settings = json['camera_settings']
            self.detector_settings = json['detector_settings']
            # self.preprocessing_settings = json['preprocessing_settings']

            for label, slider in self.camera_sliders.items():
                value = self.camera_settings[label.lower()]
                slider.set(value)
                self.update_camera(label, value)

            self.master.update_detector(self.detector_settings['base'])
            self.disable(self.update_base_btn)
            self.import_export_btn.set(None)

    def export_settings(self):
        self.import_export_btn.set(None)
        return Helper.export_settings(
            camera_settings=self.camera_settings,
            detector_settings=self.detector_settings,
            # preprocessing_settings=self.preprocessing_settings
        )

    def enable(self, *wids):
        for wid in wids:
            wid.configure(state=NRM)

    def disable(self, *wids):
        for wid in wids:
            wid.configure(state=DIS)