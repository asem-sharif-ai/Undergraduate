import tkinter as tk
import customtkinter as ctk

from tkinter.filedialog import askopenfilename as import_file

from PIL import Image, ImageTk

from threading import Thread

from Functions  import *
from Utils.GUI.Data import *

class PointOperationsFrame(ctk.CTkTabview):
    def __init__(self, master, send_msg_function,
                               send_operation_data_function,
                               send_advanced_data_function):

        super().__init__(master, height=250, fg_color=FRAME_DEFAULT_COLOR)
        self.pack(padx=10, pady=(5, 10), expand=True, fill=BOTH)

        self.send_msg = send_msg_function
        self.send_operation_data = send_operation_data_function
        self.send_advanced_data = send_advanced_data_function

    #! ---------- ---------- ---------- ---------- ---------- 

        self.add(SIMPLE)

        self.tab(SIMPLE).rowconfigure(index=(0, 1, 2, 3), weight=1, uniform=A)
        self.tab(SIMPLE).columnconfigure(index=0, weight=1, uniform=A)
        self.tab(SIMPLE).columnconfigure(index=1, weight=1, uniform=A)

        self.operation_entry = ctk.CTkEntry(self.tab(SIMPLE), placeholder_text=POINT_OPERATION, fg_color=MSG_BOX_FG, border_color=ENTRY_BD, border_width=BORDER_WIDTH)
        self.operation_entry.grid(row=0, column=0, columnspan=2, padx=(10, 10), pady=(10, 10), sticky=NSEW)
        self.operation_entry.bind(KEY_RELEASE, self.check_operation)
        
        self.channel_entry = ctk.CTkEntry(self.tab(SIMPLE), placeholder_text='RGB', fg_color=MSG_BOX_FG, border_color=ENTRY_BD, border_width=BORDER_WIDTH)
        self.channel_entry.grid(row=1, column=0, columnspan=1, padx=(10, 10), pady=(10, 10), sticky=NSEW)
        self.channel_entry.bind(KEY_RELEASE, self.check_channel)

        self.factor_entry = ctk.CTkEntry(self.tab(SIMPLE), placeholder_text='128', fg_color=MSG_BOX_FG, border_color=ENTRY_BD, border_width=BORDER_WIDTH)
        self.factor_entry.grid(row=1, column=1, columnspan=1, padx=(10, 10), pady=(10, 10), sticky=NSEW)
        self.factor_entry.bind(KEY_RELEASE, self.check_factor)

        self.apply_btn = ctk.CTkButton(self.tab(SIMPLE), text='Apply', command=self.send_command)
        self.apply_btn.grid(row=2, column=0, columnspan=2, padx=(10, 10), pady=(10, 10), sticky=NSEW)

        self.plot_btn = ctk.CTkButton(self.tab(SIMPLE), text='Plot IO-LUT', state=DIS, command=self.plot_operation_lut)
        self.plot_btn.grid(row=3, column=0, columnspan=2, padx=(10, 10), pady=(10, 10), sticky=NSEW)

    #! ---------- ---------- ---------- ---------- ---------- 

        self.add(ADVANCED)
        
        self.tab(ADVANCED).rowconfigure(index=(0, 1, 2, 3), weight=1, uniform=A)
        self.tab(ADVANCED).columnconfigure(index=0, weight=1, uniform=A)
        self.tab(ADVANCED).columnconfigure(index=1, weight=1, uniform=A)

        self.adv_operation_entry = ctk.CTkEntry(self.tab(ADVANCED), placeholder_text='`?` For Help.', fg_color=MSG_BOX_FG, border_color=ENTRY_BD, border_width=BORDER_WIDTH)
        self.adv_operation_entry.grid(row=0, column=0, columnspan=2, padx=(10, 10), pady=(10, 10), sticky=NSEW)
        self.adv_operation_entry.bind(KEY_RELEASE, self.adv_check_operation)

        self.canvas = tk.Canvas(self.tab(ADVANCED), width=100, height=50, highlightthickness=0, background=FRAME_DEFAULT_COLOR[1])
        self.canvas.grid(row=1, column=0, rowspan=2, columnspan=2, padx=(10, 10), pady=(10, 10), sticky=NSEW)

        self.adv_import_btn = ctk.CTkButton(self.tab(ADVANCED), text='Import', command=self.adv_get_sub_image)
        self.adv_import_btn.grid(row=3, column=0, columnspan=1, padx=(10, 10), pady=(10, 10), sticky=NSEW)

        self.adv_apply_btn = ctk.CTkButton(self.tab(ADVANCED), text='Apply', state=DIS, command=self.adv_send_command)
        self.adv_apply_btn.grid(row=3, column=1, columnspan=1, padx=(10, 10), pady=(10, 10), sticky=NSEW)

    #! ---------- ---------- ---------- ---------- ---------- 

    def check_operation(self, _event):
        if self.operation_entry.get() == '?':
            self.operation_entry.delete(0, tk.END)
            self.send_msg(msg_type=ERR, msg_text = POINT_OPERATIONS_LIST)
        if self.operation_entry.get().endswith(';'):
            op = self.operation_entry.get()[:-1]
            self.operation_entry.delete(0, tk.END)
            self.operation_entry.insert(0, fill_operation_name(text=op, options=POINT_OPERATIONS_LIST))

        if self.confirm(self.operation_entry.get(), OPR):
            self.operation_entry.configure(border_color=GRN)
        else:
            self.operation_entry.configure(border_color=RED)

        if self.operation_entry.get() in NULL_ENTRY:
            self.operation_entry.configure(border_color=ENTRY_BD)

        if self.channel_entry.get().upper() == RGB and self.operation_entry.get().lower() in [ELIMINATE, SWAP]:
            self.apply_btn.configure(state=DIS)
        elif len(self.channel_entry.get()) == 1 and self.operation_entry.get().lower() == SWAP:
            self.apply_btn.configure(state=DIS)
        else:
            self.apply_btn.configure(state=NRM)

    #! ---------- ---------- ---------- ---------- ---------- 

    def check_channel(self, _event):
        if self.channel_entry.get() == '?':
            self.send_msg(msg_type=ERR, msg_text = CHANNELS_LIST)
            
        if self.confirm(self.channel_entry.get(), CHN):
            self.channel_entry.configure(border_color=GRN)
        else:
            self.channel_entry.configure(border_color=RED)

        if self.channel_entry.get() in NULL_ENTRY:
            self.channel_entry.configure(border_color=ENTRY_BD)

        if self.channel_entry.get().upper() == RGB and self.operation_entry.get().lower() in [ELIMINATE, SWAP]:
            self.apply_btn.configure(state=DIS)
        elif len(self.channel_entry.get()) == 1 and self.operation_entry.get().lower() == SWAP:
            self.apply_btn.configure(state=DIS)
        else:
            self.apply_btn.configure(state=NRM)

    #! ---------- ---------- ---------- ---------- ---------- 

    def check_factor(self, _event):
        if self.factor_entry.get() == '?':
            self.send_msg(msg_type=ERR, msg_text = '[0 : 255]')

        if self.confirm(self.factor_entry.get(), FAC):
            self.factor_entry.configure(border_color=GRN)
        else:
            self.factor_entry.configure(border_color=RED)

        if self.factor_entry.get() in NULL_ENTRY:
            self.factor_entry.configure(border_color=ENTRY_BD)

    def confirm(self, value, jop):
        if value not in NULL_ENTRY:
            if jop == FAC:
                return value.isdigit() and 0 <= int(value) <= 255
            elif jop == CHN:
                return value.upper() in CHANNELS_LIST
            elif jop == OPR:
                return clean(value) in POINT_OPERATIONS_LIST or is_expression(value)
        return False

    def send_command(self):
        operation = self.operation_entry.get()
        channel = self.channel_entry.get().upper()
        factor = self.factor_entry.get()

        if is_expression(operation):
            self.plot_btn.configure(state=NRM)
            return self.send_operation_data(operation, channel=RGB, factor=0)
        else:
            operation = clean(operation)
            if not self.confirm(operation, OPR):
                self.operation_entry.configure(border_color=RED)
            if not self.confirm(channel, CHN):
                self.channel_entry.configure(border_color=RED)
            if not self.confirm(factor, FAC):
                self.factor_entry.configure(border_color=RED)

            if (self.confirm(operation, OPR) and self.confirm(channel, CHN) and self.confirm(factor, FAC)):
                self.operation_entry.configure(border_color=GRN)
                self.channel_entry.configure(border_color=GRN)
                self.factor_entry.configure(border_color=GRN)
                self.plot_btn.configure(state=NRM)
                self.send_operation_data(operation, channel, factor)
            else:
                self.plot_btn.configure(state=DIS)

    def plot_operation_lut(self):
        self.send_command()
        try:
            if is_expression(self.operation_entry.get()):
                plot_point_operations_LUT(self.operation_entry.get(), factor=0)
            else:
                plot_point_operations_LUT(clean(self.operation_entry.get()), int(self.factor_entry.get()))
        except: pass

    #! ---------- ---------- ---------- ---------- ---------- 

    def adv_check_operation(self, _event):
        if self.adv_operation_entry.get() == '?':
            self.adv_operation_entry.delete(0, tk.END)
            self.send_msg(msg_type=ERR, msg_text = ADVANCED_POINT_OPERATIONS_LIST)
        if self.adv_operation_entry.get().endswith(';'):
            op = self.adv_operation_entry.get()[:-1]
            self.adv_operation_entry.delete(0, tk.END)
            self.adv_operation_entry.insert(0, fill_operation_name(text=op, options=ADVANCED_POINT_OPERATIONS_LIST))

        if clean(self.adv_operation_entry.get()) in ADVANCED_POINT_OPERATIONS_LIST:
            self.adv_operation_entry.configure(border_color=GRN)
        else:
            self.adv_operation_entry.configure(border_color=RED)
        if self.adv_operation_entry.get() in NULL_ENTRY:
            self.adv_operation_entry.configure(border_color=ENTRY_BD)

    def adv_get_sub_image(self):
        self.sub_image_path = import_file(filetypes=IMPORT_FILE_TYPES)
        if self.sub_image_path:
            image = Image.open(self.sub_image_path)
            image_ratio = image.width / image.height
            canvas_ratio = self.canvas.winfo_width() / self.canvas.winfo_height()
            if image_ratio > canvas_ratio:
                new_width = self.canvas.winfo_width()
                new_height = int(new_width / image_ratio)
            else:
                new_height = self.canvas.winfo_height()
                new_width = int(new_height * image_ratio)
            resized_image = image.resize((new_width, new_height))
            photo = ImageTk.PhotoImage(resized_image)
            self.canvas.create_image(self.canvas.winfo_width() // 2, self.canvas.winfo_height() // 2, anchor=tk.CENTER, image=photo)
            self.canvas.image = photo
            self.adv_apply_btn.configure(state=NRM)

    def adv_send_command(self):
        operation = clean(self.adv_operation_entry.get())
        try:
            Image.open(self.sub_image_path)
        except:
            self.send_msg(msg_type=ERR, msg_text='Invalid Sub Image Path')
        else:
            if operation in ADVANCED_POINT_OPERATIONS_LIST:
                self.send_advanced_data(sub_path=self.sub_image_path, operation=operation)
            else:
                self.adv_operation_entry.configure(border_color=RED)
                self.send_msg(msg_type=ERR, msg_text='Invalid Operation')

#! ---------- ---------- ---------- ---------- ---------- ---------- ---------- ---------- ---------- ----------

class GammaHistogramFrame(ctk.CTkTabview):
    def __init__(self, master, send_msg_function, gamma_function, histogram_function, plot_histogram_function):
        self.send_gamma_value = gamma_function
        self.send_histogram_value = histogram_function
        self.plot_histogram_operations = plot_histogram_function

        super().__init__(master, fg_color=FRAME_DEFAULT_COLOR, height=100)
        self.pack(padx=10, pady=(5, 10), expand=True, fill='x')

        self.add(HISTOGRAM)
        self.add(GAMMA)
        
        for _tab in [self.tab(GAMMA), self.tab(HISTOGRAM)]:
            _tab.rowconfigure(index=(0, 1), weight=1, uniform=A)
            _tab.columnconfigure(index=0, weight=1, uniform=A)
            _tab.columnconfigure(index=1, weight=1, uniform=A)

        self.gamma_entry = ctk.CTkEntry(self.tab(GAMMA), placeholder_text='λ', fg_color=MSG_BOX_FG, border_width=BORDER_WIDTH, border_color=ENTRY_BD)
        self.gamma_entry.grid(row=0, column=0, columnspan=1, padx=(10, 10), pady=(10, 10), sticky=NSEW)
        self.gamma_entry.bind(KEY_RELEASE, self.check_gamma_entry)

        self.apply_gamma_btn = ctk.CTkButton(self.tab(GAMMA), text='Apply', state=DIS, command=self.send_gamma)
        self.apply_gamma_btn.grid(row=0, column=1, columnspan=1, padx=(10, 10), pady=(10, 10), sticky=NSEW)
        
        self.disable_gamma_btn = ctk.CTkButton(self.tab(GAMMA), text='Disable', state=DIS, command=self.disable_gamma)
        self.disable_gamma_btn.grid(row=1, column=0, columnspan=1, padx=(10, 10), pady=(10, 10), sticky=NSEW)

        self.plot_gamma_btn = ctk.CTkButton(self.tab(GAMMA), text='Plot', state=DIS, command=self.plot_gamma)
        self.plot_gamma_btn.grid(row=1, column=1, columnspan=1, padx=(10, 10), pady=(10, 10), sticky=NSEW)

        self.histogram_operations_btn = ctk.CTkSegmentedButton(self.tab(HISTOGRAM), values=HISTOGRAM_OPERATIONS, command=self.send_histogram_value)
        self.histogram_operations_btn.grid(row=0, column=0, rowspan=1, columnspan=2, padx=(10, 10), pady=(10, 10), sticky=NSEW)

        self.disable_histogram_operation_btn = ctk.CTkButton(self.tab(HISTOGRAM), state=DIS, text='Disable', command=self.disable_histogram_operations)
        self.disable_histogram_operation_btn.grid(row=1, column=0, columnspan=1, padx=(10, 10), pady=(10, 10), sticky=NSEW)

        self.plot_histogram_operation_btn = ctk.CTkButton(self.tab(HISTOGRAM), state=DIS, text='Plot', command=self.plot_histogram_operations)
        self.plot_histogram_operation_btn.grid(row=1, column=1, columnspan=1, padx=(10, 10), pady=(10, 10), sticky=NSEW)

    def check_gamma_entry(self, _event=None):
        if not self.confirm_gamma():
            if not self.gamma_entry.get().strip(): 
                self.gamma_entry.configure(border_color=ENTRY_BD)
            else:
                self.gamma_entry.configure(border_color=RED)
            self.apply_gamma_btn.configure(state=DIS)
            self.plot_gamma_btn.configure(state=DIS)
            self.disable_gamma_btn.configure(state=DIS)
        else:
            self.gamma_entry.configure(border_color=GRN)
            self.apply_gamma_btn.configure(state=NRM)

    def confirm_gamma(self):
        gamma_statement = self.gamma_entry.get().strip()
        try:
            self.gamma_value = float(gamma_statement)
            return 0 < self.gamma_value <= 10
        except:
            return False

    def send_gamma(self):
        if self.confirm_gamma():
            self.send_gamma_value(self.gamma_value)
            self.plot_gamma_btn.configure(state=NRM)
            self.disable_gamma_btn.configure(state=NRM)

    def disable_gamma(self):
        self.send_gamma_value(1)
        self.gamma_entry.delete(0, tk.END)
        self.check_gamma_entry()

    def plot_gamma(self):
        plot_gamma_correction_LUT(gamma_value=self.gamma_value)

    def disable_histogram_operations(self):
        self.send_histogram_value(DEFAULT_VALUES[HISTOGRAM_OPERATION])
        self.histogram_operations_btn.set(None)
        self.disable_histogram_operation_btn.configure(state=DIS)
        self.plot_histogram_operation_btn.configure(state=DIS)
    
#! ---------- ---------- ---------- ---------- ---------- ---------- ---------- ---------- ---------- ----------

class NeighborhoodOperationsFrame(ctk.CTkTabview):
    def __init__(self, master, send_msg_function, neighborhood_operations_function):

        self.send_data = neighborhood_operations_function
        self.send_msg = send_msg_function

        super().__init__(master, height=100, fg_color=FRAME_DEFAULT_COLOR)
        self.pack(padx=10, pady=(5, 10), expand=True, fill=BOTH)

    #! ---------- ---------- ---------- ---------- ---------- 

        self.add(NEIGHBORHOOD_OPERATION)

        self.tab(NEIGHBORHOOD_OPERATION).rowconfigure(index=(0, 1), weight=1, uniform=A)
        self.tab(NEIGHBORHOOD_OPERATION).columnconfigure(index=0, weight=1, uniform=A)
        self.tab(NEIGHBORHOOD_OPERATION).columnconfigure(index=1, weight=1, uniform=A)

        self.filter_name_entry = ctk.CTkEntry(self.tab(NEIGHBORHOOD_OPERATION), placeholder_text='Filter Mode', fg_color=MSG_BOX_FG, border_width=BORDER_WIDTH, border_color=ENTRY_BD)
        self.filter_name_entry.grid(row=0, column=0, columnspan=2, padx=(10, 10), pady=(10, 10), sticky=NSEW)
        self.filter_name_entry.bind(KEY_RELEASE, self.check_filter)
        self.filter_name_entry.bind(KEY_RELEASE, self.check_info)

        self.filter_info_entry = ctk.CTkEntry(self.tab(NEIGHBORHOOD_OPERATION), placeholder_text='L or W', fg_color=MSG_BOX_FG, border_width=BORDER_WIDTH, border_color=ENTRY_BD)
        self.filter_info_entry.grid(row=1, column=0, columnspan=1, padx=(10, 10), pady=(10, 10), sticky=NSEW)
        self.filter_info_entry.bind(KEY_RELEASE, self.check_info)
        self.filter_info_entry.bind(KEY_RELEASE, self.check_filter)

        self.apply_btn = ctk.CTkButton(self.tab(NEIGHBORHOOD_OPERATION), text='Apply', command=self.apply)
        self.apply_btn.grid(row=1, column=1, columnspan=1, padx=(10, 10), pady=(10, 10), sticky=NSEW)

    #! ---------- ---------- ---------- ---------- ---------- 

    def load(self):
        self.apply_btn.configure(state=DIS)
        self.filter_info_entry.configure(state=READ_ONLY)
        self.filter_name_entry.configure(state=READ_ONLY)

    def done(self):
        self.apply_btn.configure(state=NRM)
        self.filter_info_entry.configure(state=NRM)
        self.filter_name_entry.configure(state=NRM)

    def apply(self):
        filter_name = self.filter_name_entry.get()
        filter_info = self.filter_info_entry.get()

        if not self.confirm(filter_name, FLT):
            self.filter_name_entry.configure(border_color=RED)
        if not self.confirm(filter_info, INF):
            self.filter_info_entry.configure(border_color=RED)

        if self.confirm(filter_name, FLT) and self.confirm(filter_info, INF):
            Thread(target=self.send_data, args=(filter_name, filter_info, ), daemon=True).start()

    def check_filter(self, _event=None):
        if self.filter_name_entry.get() == '?':
            self.filter_name_entry.delete(0, tk.END)
            self.send_msg(msg_type=ERR, msg_text=NEIGHBORHOOD_OPERATIONS_LIST)
        if self.filter_name_entry.get().endswith(';'):
            op = self.filter_name_entry.get()[:-1]
            self.filter_name_entry.delete(0, tk.END)
            self.filter_name_entry.insert(0, fill_operation_name(text=op, options=NEIGHBORHOOD_OPERATIONS_LIST))

        if self.confirm(self.filter_name_entry.get(), FLT):
            self.filter_name_entry.configure(border_color=GRN)
        else:
            self.filter_name_entry.configure(border_color=RED)

        if self.filter_name_entry.get() in NULL_ENTRY:
            self.filter_name_entry.configure(border_color=ENTRY_BD)

    def check_info(self, _event=None):
        if self.filter_info_entry.get() == '?':
            self.send_msg(msg_type=ERR, msg_text=PASS_FILTERS)

        if self.confirm(self.filter_info_entry.get(), INF):
            self.filter_info_entry.configure(border_color=GRN)
        else:
            self.filter_info_entry.configure(border_color=RED)

        if self.filter_info_entry.get() in NULL_ENTRY:
            self.filter_info_entry.configure(border_color=ENTRY_BD)

    def confirm(self, value, jop):
        if value not in NULL_ENTRY:
            if jop == INF:
                try:
                    size = int(value)
                    return 2 <= size <= 20
                except:
                    try:
                        filter = value.upper().split()[0]
                        weight = int(value.upper().split()[1])
                    except:
                        return filter in PASS_FILTERS
                    else:
                        return filter in PASS_FILTERS[:-1] and 1 <= weight <= 10
            elif jop == FLT:
                value = value.strip().lower()
                if value.startswith(RANK):
                    try:
                        rank = int(value.strip().split()[-1])
                        size = int(self.filter_info_entry.get())
                    except:
                        return False
                    else:
                        return 0 < rank <= size**2
                elif value.startswith(OUTLIER):
                    try:
                        threshold = int(value.strip().split()[-1])
                    except:
                        return False
                    else:
                        return 0 < threshold <= 255
                else:
                    return value in NEIGHBORHOOD_OPERATIONS_LIST
        return False

    #! ---------- ---------- ---------- ---------- ---------- 

class EdgeDetectionFrame(ctk.CTkTabview):
    def __init__(self, master, send_msg_function, edge_detection_function):

        self.send_msg = send_msg_function
        self.send_edge_detection_data = edge_detection_function

        super().__init__(master, height=100, fg_color=FRAME_DEFAULT_COLOR)
        self.pack(padx=10, pady=(5, 10), expand=True, fill=BOTH)

        self.add(EDGE_DETECTION)

    #! ---------- ---------- ---------- ---------- ---------- 
        
        self.tab(EDGE_DETECTION).rowconfigure(index=(0, 1), weight=1, uniform=A)
        self.tab(EDGE_DETECTION).columnconfigure(index=0, weight=1, uniform=A)
        self.tab(EDGE_DETECTION).columnconfigure(index=1, weight=1, uniform=A)

        self.edge_detection_options = ctk.CTkOptionMenu(self.tab(EDGE_DETECTION), command=self.handle_edge_detection_options,
                                                     values=EDGE_FILTERS, fg_color=MSG_BOX_FG, dropdown_fg_color=MSG_BOX_FG,
                                                     button_color=ENTRY_BD, button_hover_color=MSG_BOX_FG, dropdown_hover_color=ENTRY_BD)
        self.edge_detection_options.grid(row=0, column=0, rowspan=1, columnspan=2, padx=(10, 10), pady=(10, 10), sticky=NSEW)
        self.edge_detection_options.set(EDGE_FILTERS_LIST_TITLE)

        self.edge_detection_apply_btn = ctk.CTkButton(self.tab(EDGE_DETECTION), text='Apply', command=self.__send_edge_detection_data)
        self.edge_detection_apply_btn.grid(row=1, column=0, columnspan=1, padx=(10, 10), pady=(10, 10), sticky=NSEW)

        self.edge_detection_enhance_btn = ctk.CTkButton(self.tab(EDGE_DETECTION), text='Enhance', state=DIS, command=self.enhance)
        self.edge_detection_enhance_btn.grid(row=1, column=1, columnspan=1, padx=(10, 10), pady=(10, 10), sticky=NSEW)

        self.enhance_option = False
        self.already_enhanced = False

    #! ---------- ---------- ---------- ---------- ---------- 

    def handle_edge_detection_options(self, _value):
        self.edge_detection_options.configure(button_color=ENTRY_BD)
        self.edge_detection_apply_btn.configure(state=NRM)
        self.edge_detection_enhance_btn.configure(state=DIS)
        self.enhance_option = False
        self.already_enhanced = False

    def enhance(self):
        if not self.already_enhanced:
            self.enhance_option = True
            self.__send_edge_detection_data()
            self.already_enhanced = True

    def __send_edge_detection_data(self):
        if self.edge_detection_options.get() == EDGE_FILTERS_LIST_TITLE:
            self.edge_detection_options.configure(button_color=RED)
        else:
            Thread(target=self.send_edge_detection_data, args=((self.edge_detection_options.get(), self.enhance_option), ), daemon=True).start()

#! ---------- ---------- ---------- ---------- ---------- ---------- ---------- ---------- ---------- ----------

class ThresholdingFrame(ctk.CTkTabview):
    def __init__(self, master, send_msg_function, thresholding_function):

        self.send_msg = send_msg_function
        self.send_thresholding_data = thresholding_function

        super().__init__(master, height=100, fg_color=FRAME_DEFAULT_COLOR)
        self.pack(padx=10, pady=(5, 10), expand=True, fill=BOTH)

        self.add(THRESHOLDING_TAB)

        self.tab(THRESHOLDING_TAB).rowconfigure(index=(0, 1), weight=1, uniform=A)
        self.tab(THRESHOLDING_TAB).columnconfigure(index=0, weight=1, uniform=A)
        self.tab(THRESHOLDING_TAB).columnconfigure(index=1, weight=1, uniform=A)

        self.thresholding_options = ctk.CTkOptionMenu(self.tab(THRESHOLDING_TAB), command=self.handle_int_entry,
                                                     values=THRESHOLDING_OPTIONS_LIST, fg_color=MSG_BOX_FG, dropdown_fg_color=MSG_BOX_FG,
                                                     button_color=ENTRY_BD, button_hover_color=MSG_BOX_FG, dropdown_hover_color=ENTRY_BD)
        self.thresholding_options.grid(row=0, column=0, rowspan=1, columnspan=2, padx=(10, 10), pady=(10, 10), sticky=NSEW)
        self.thresholding_options.set(THRESHOLDING_LIST_TITLE)

        self.thresholding_int_entry = ctk.CTkEntry(self.tab(THRESHOLDING_TAB), placeholder_text='', fg_color=MSG_BOX_FG, border_width=BORDER_WIDTH, border_color=ENTRY_BD)
        self.thresholding_int_entry.grid(row=1, column=0, columnspan=1, padx=(10, 10), pady=(10, 10), sticky=NSEW)
        self.thresholding_int_entry.bind(KEY_RELEASE, self.check_entry_value)

        self.thresholding_apply_btn = ctk.CTkButton(self.tab(THRESHOLDING_TAB), text='Apply', command=self.apply_thresholding)
        self.thresholding_apply_btn.grid(row=1, column=1, columnspan=1, padx=(10, 10), pady=(10, 10), sticky=NSEW)


    def handle_int_entry(self, mode):
        self.check_entry_value()
        self.check_entry_placeholder_text(mode)
        self.thresholding_options.configure(button_color=ENTRY_BD)

    def check_entry_value(self, _event=None):
        if self.confirm_int():
            self.thresholding_int_entry.configure(border_color=GRN)
        else:
            self.thresholding_int_entry.configure(border_color=RED)
            
        if self.thresholding_int_entry.get() in NULL_ENTRY:
            self.thresholding_int_entry.configure(border_color=ENTRY_BD)

    def check_entry_placeholder_text(self, mode):
        if self.thresholding_int_entry.get() in NULL_ENTRY:
            entry = self.thresholding_int_entry
            if mode == THRESHOLDING_OPTIONS_LIST[0]:
                entry.configure(placeholder_text='TH')
            elif mode == THRESHOLDING_OPTIONS_LIST[1]:
                entry.configure(placeholder_text='L H C')
            elif mode == THRESHOLDING_OPTIONS_LIST[2]:
                entry.configure(placeholder_text='N')
            elif mode in THRESHOLDING_OPTIONS_LIST[3:]:
                entry.configure(placeholder_text='L')
            else:
                entry.configure(placeholder_text='')

    def confirm_mode(self):
        return not self.thresholding_options.get() == THRESHOLDING_LIST_TITLE
    
    def confirm_int(self):
        value = self.thresholding_int_entry.get()
        mode = self.thresholding_options.get()
        if value not in NULL_ENTRY:
            if mode == THRESHOLDING_OPTIONS_LIST[0]:
                try:
                    info = int(value)
                    return 0 < info < 255
                except:
                    return value.lower() in THRESHOLDS
            elif mode == THRESHOLDING_OPTIONS_LIST[1]:
                try:
                    i = tuple(int(i) for i in value.split())
                    return i[0] < i[1] < 255 and i[2] in [0, 1]
                except:
                    return False
            else:
                try:
                    info = int(value)
                    return 2 <= info <= 20
                except:
                    return False
        return False

    def apply_thresholding(self):
        if not self.confirm_mode():
            self.thresholding_options.configure(button_color=RED)
        if not self.confirm_int():
            self.thresholding_int_entry.configure(border_color=RED)

        if self.confirm_mode() and self.confirm_int():
            Thread(target=self.send_thresholding_data, args=(self.thresholding_options.get(), self.thresholding_int_entry.get()), daemon=True).start()

#! ---------- ---------- ---------- ---------- ---------- ---------- ---------- ---------- ---------- ----------

class MorphologyFrame(ctk.CTkTabview):
    def __init__(self, master, send_msg_function, morphology_function):

        self.send_msg = send_msg_function
        self.send_morphology_data = morphology_function

        super().__init__(master, height=100, fg_color=FRAME_DEFAULT_COLOR)
        self.pack(padx=10, pady=(5, 10), expand=True, fill=BOTH)

        self.add(MORPHOLOGY)

        self.tab(MORPHOLOGY).rowconfigure(index=(0, 1), weight=1, uniform=A)
        self.tab(MORPHOLOGY).columnconfigure(index=0, weight=1, uniform=A)
        self.tab(MORPHOLOGY).columnconfigure(index=1, weight=1, uniform=A)

        self.morphology_options = ctk.CTkOptionMenu(self.tab(MORPHOLOGY), dynamic_resizing=False,
                                                     values=MORPHOLOGY_LIST, fg_color=MSG_BOX_FG, dropdown_fg_color=MSG_BOX_FG,
                                                     button_color=ENTRY_BD, button_hover_color=MSG_BOX_FG, dropdown_hover_color=ENTRY_BD)
        self.morphology_options.grid(row=0, column=0, rowspan=1, columnspan=2, padx=(10, 10), pady=(10, 10), sticky=NSEW)
        self.morphology_options.set(MORPHOLOGY_LIST_TITLE)

        self.morphology_apply_btn = ctk.CTkButton(self.tab(MORPHOLOGY), text='Apply', command=self.apply)
        self.morphology_apply_btn.grid(row=1, column=1, columnspan=2, padx=(10, 10), pady=(10, 10), sticky=NSEW)

    def apply(self):
        method = self.morphology_options.get()
        if method != MORPHOLOGY_LIST_TITLE:
            self.send_morphology_data(method)