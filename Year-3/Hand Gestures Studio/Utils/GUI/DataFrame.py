import tkinter as tk, tkinter.ttk as ttk
import customtkinter as ctk

import pandas as pd

from Utils.GUI.Data import * 
from Utils.Models import Helper

class DataTable(ttk.Treeview):
    def __init__(self, master, dataset: pd.DataFrame):
        super().__init__(master)
        self.dataframe = dataset
        self.columns = list(dataset.columns)

        self.init_grid()
        self.style_tree()
        self.insert_data()
        self.init_tree()

    def init_grid(self):
        self.rowconfigure(index=0, weight=10, uniform=A)
        self.rowconfigure(index=1, weight=1, uniform=A)
        self.columnconfigure(index=0, weight=10, uniform=A)

    def style_tree(self):
        self.style = ttk.Style()
        self.style.theme_use('alt')
        self.style.configure('Treeview', font=('Segoe UI', 10), anchor='center', foreground=WHT, fieldbackground='#101010', bd=0, highlightthickness=0)
        
        self.style.configure('Treeview.Heading', font=('Segoe UI', 10, 'bold'), background='#101010', foreground=WHT)
        self.style.map('Treeview', background=[('selected', '#151515')], foreground=[('selected', BLK)])

        self.tag_configure('odd' , background='#101010')
        self.tag_configure('even', background='#151515')

    def insert_data(self):
        self['columns'] = [''] + self.columns
        self['show'] = 'headings'
        
        self.heading('', text='', anchor='center')
        self.column('', width=50, anchor='center')

        for col in self.columns:
            self.heading(col, text=col, anchor='center')
            self.column(col, width=150, anchor='center')

        for i, row in self.dataframe.iterrows():
            values = [i] + [row[col] for col in self.columns]
            self.insert('', 'end', values=values, tags=(['even', 'odd'][i % 2], ))

    def init_tree(self):
        bar = ctk.CTkScrollbar(self, orientation=HRZ, fg_color='#101010', button_color='#151515', hover=False, command=self.xview)
        bar.grid(row=2, column=0, columnspan=3, sticky='ew')
        self.configure(xscrollcommand=bar.set)


class DataFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, **DFD[1])
        self.master = master
        self.write = self.master.write

        self.rowconfigure(index=(0, 3), weight=5, uniform=A)
        self.rowconfigure(index=(1, 2), weight=2, uniform=A)
        self.columnconfigure(index=0, weight=1, uniform=A)

        self.init_main_page()

    def init_main_page(self):
        self.import_data_btn = ctk.CTkButton(self, text='Import Dataset', width=175, command=self.import_dataset, **DBD)
        self.import_data_btn.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

        self.generate_data_btn = ctk.CTkButton(self, text='Generate Dataset', width=175, command=self.generate_dataset, **DBD)
        self.generate_data_btn.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

        self.dataset = None
        self.label = None

        self.bars = []
        self.captured_bars = []

        self.captured = 0
        self.capturing = False
        self.capturing_key = None

    def import_dataset(self, filename=None):
        data, info = Helper.import_dataset(filename)
        if data is None:
            return
        if not isinstance(data, Exception):
            self.dataset = data
            self.columns = list(data.columns)
            self.master.update_data(dataset=data)

            self.import_data_btn.destroy()
            self.generate_data_btn.destroy()

            self.dataset_table = DataTable(self, Helper.get_brief(data))
            self.dataset_table.grid(row=0, column=0, rowspan=3, padx=10, pady=10, sticky='nsew')

            self.rowconfigure(index=3, weight=4, uniform=A)

            self.btns_frame = ctk.CTkFrame(self, **DFD[0])
            self.btns_frame.grid(row=3, column=0, padx=10, pady=(0, 10), sticky='nsew')

            self.btns_frame.rowconfigure(index=(0, 1), weight=1, uniform=A)
            self.btns_frame.columnconfigure(index=(0, 1), weight=1, uniform=A)

            self.label_options = ctk.CTkOptionMenu(self.btns_frame, values=self.columns, command=self.set_label, **DMD)
            self.label_options.grid(row=0, column=0, columnspan=2, padx=10, pady=(10, 5), sticky='sew')
            self.label_options.set('Determine Dataset Label')
            self.enable_labeling()

            self.info_btn = ctk.CTkButton(self.btns_frame, text='Data Info', command=lambda: self.write(info), **DBD)
            self.info_btn.grid(row=1, column=0, padx=(10, 5), pady=(5, 10), sticky='ne')

            self.remove_btn = ctk.CTkButton(self.btns_frame, text='Remove Data', command=self.remove_dataset, **DBD)
            self.remove_btn.grid(row=1, column=1, padx=(5, 10), pady=(5, 10), sticky='nw')
            
            self.master.model_section.import_model_btn.configure(state=DIS)
        else:
            self.write(data.__class__.__name__)

    def set_label(self, label):
        self.label = label
        self.master.update_data(label=label)

    def search_columns(self):
        window = ctk.CTkInputDialog(title='Determine Dataset Label', text='Search For Label Column', **DIDD)
        column = window.get_input()
        if column is not None:
            if column in self.dataset.columns:
                self.set_label(column)
            else:
                self.write(f'Givin label column `{column}` was not found.')

    def scroll_columns(self, event):
        step = 1 if event.delta > 0 else -1
        self.label = self.columns[(self.columns.index(self.label if self.label else self.columns[-1]) + step) % len(self.columns)]
        self.label_options.set(self.label)
        self.set_label(self.label)

    def enable_labeling(self):
        self.label_options.configure(state=NRM)
        self.label_options.bind('<Button-2>', lambda _: self.write(self.columns))
        self.label_options.bind('<Button-3>', lambda _: self.search_columns())
        self.label_options.bind('<MouseWheel>', self.scroll_columns)

    def disable_labeling(self):
        self.label_options.configure(state=DIS)
        self.label_options.unbind('<Button-2>')
        self.label_options.unbind('<Button-3>')
        self.label_options.unbind('<MouseWheel>')

    def remove_dataset(self):
        self.dataset_table.destroy()
        self.btns_frame.destroy()
        self.rowconfigure(index=3, weight=5, uniform=A)
        self.init_main_page()
        self.master.update_data(remove=True)
        self.master.model_section.import_model_btn.configure(state=NRM)
        
    def generate_dataset(self):
        self.import_data_btn.destroy()
        self.generate_data_btn.destroy()

        self.rowconfigure(index=3, weight=3, uniform=A)

        self.signs_frame = ctk.CTkScrollableFrame(self, **DSFD)
        self.signs_frame.grid(row=0, column=0, rowspan=3, columnspan=2, padx=10, pady=(10, 5), sticky='nsew')

        self.add_sign_btn = ctk.CTkButton(self.signs_frame, text='Add Sign', command=self.add, **DBD)
        self.add_sign_btn.pack(padx=10, pady=10, expand=True, fill='x')

        self.export_btn = ctk.CTkButton(self, text='Export Dataset', width=175, command=self.export_dataset, state=DIS, **DBD)
        self.export_btn.grid(row=3, column=0, columnspan=2, padx=10, pady=(5, 10))

        self.dataset = {}
        self.add()
        
    def add(self): # store as [frame, entry, capture_btn, delete_btn]
        frame = ctk.CTkFrame(self.signs_frame, **DFD[1])
        
        frame.rowconfigure(index=0, weight=1, uniform=A)        
        frame.columnconfigure(index=(0, 1, 2), weight=1, uniform=A)        

        entry = ctk.CTkEntry(frame, placeholder_text='Letter', **DED)
        entry.grid(row=0, column=0, padx=(10, 5), pady=10, sticky='ew')

        capture_btn = ctk.CTkButton(frame, text='Capture', command=lambda: self.start_capturing(entry), state=NRM if self.master.detecting else DIS, **DBD)
        capture_btn.grid(row=0, column=1, padx=5, pady=10, sticky='ew')

        delete_btn = ctk.CTkButton(frame, text='Delete', command=lambda: self.delete(frame), **DBD)
        delete_btn.grid(row=0, column=2, padx=(5, 10), pady=10, sticky='ew')

        self.bars.append([frame, entry, capture_btn, delete_btn])
        frame.pack(before=self.add_sign_btn, expand=True, fill='both', padx=10, pady=(10, 5))

        self.bars[0][3].configure(state=NRM if len(self.bars) > 1 else DIS)

    def delete(self, frame):
        for bar in self.bars:
            if bar[0] == frame:
                if bar in self.captured_bars:
                    self.captured_bars.remove(bar)
                if key := bar[1].get():
                    self.dataset.pop(key, None)
                self.bars.remove(bar)
                frame.destroy()

        self.bars[0][3].configure(state=DIS if len(self.bars) == 1 else NRM)

        if len(self.dataset) < 2:
            self.export_btn.configure(state=DIS)

    def start_capturing(self, entry):
        key = entry.get()
        if key:
            if key not in self.dataset.keys():
                self.dataset[key] = []
            self.capturing = True
            self.capturing_key = key

            for bar in self.bars:
                if bar[1] == entry:
                    bar[1].configure(state=DIS)
                    bar[2].configure(state=DIS, fg_color='orange')
                    bar[3].configure(state=DIS)
                    self.captured_bars.append(bar)
                else:
                    for wid in bar[1:]:
                        wid.configure(state=DIS)
        else:
            self.write('Can not refer to an empty string key.')

    def capture(self, hand_image, sample_size):
        if self.captured < sample_size:
            self.dataset[self.capturing_key].append(hand_image)
            self.captured += 1
        else:
            self.capturing = False
            self.capturing_key = None
            self.captured = 0

            for bar in self.bars:
                if bar in self.captured_bars:
                    bar[1].configure(state=DIS)
                    bar[2].configure(state=DIS, fg_color='#8B0000')
                    bar[3].configure(state=NRM)
                else:
                    for wid in bar[1:]:
                        wid.configure(state=NRM)
            if len(self.dataset) >= 2 and self.export_btn._state == DIS:
                self.export_btn.configure(state=NRM)

            if len(self.bars) > 1:
                self.bars[0][3].configure(state=NRM)
            else:
                self.bars[0][3].configure(state=DIS)

    def export_dataset(self):
        filename = Helper.export_dataset(self.dataset, shape=self.master.control_section.detector_settings['method']['output_size'])
        if filename:
            self.master.update_data_section(filename)
