
import tkinter as tk, customtkinter as ctk

from GUI.Data      import *
from GUI.Functions import *

from threading import Thread

class PrePreprocessingTab(ctk.CTkFrame):
    def __init__(self, parent, dataset, pre_processing_function):
        super().__init__(master=parent)
        self.pack(expand=True, fill=BOTH, padx=5, pady=(10, 0))
        self.dataframe = dataset
        self.send_task_command = pre_processing_function

        self.rowconfigure(index=(0, 1), weight=1, uniform=A)
        self.columnconfigure(index=(0, 1, 2, 3, 4), weight=1, uniform=A)

#! ----- ----- ----- ----- ----- ----- ----- ----- <<<<< frame_01 >>>>> ----- ----- ----- ----- ----- ----- ----- -----

        self.frame_01 = ctk.CTkFrame(self, fg_color=FRAME_DEFAULT_COLOR)
        self.frame_01.grid(row=0, column=0, rowspan=2, padx=5, pady=5, sticky=STICKY_XY)
        
        self.frame_01.rowconfigure(index=(0, 1, 2), weight=1, uniform=A)
        self.frame_01.columnconfigure(index=0, weight=1, uniform=A)

        self.frame_01_01 = ctk.CTkFrame(self.frame_01, fg_color=DF_FRAME_BG_1)
        self.frame_01_01.grid(row=0, column=0, pady=5, sticky=STICKY_XY)
        self.frame_01_02 = ctk.CTkFrame(self.frame_01, fg_color=DF_FRAME_BG_1)
        self.frame_01_02.grid(row=1, column=0, pady=5, sticky=STICKY_XY)

        self.frame_01_03 = ctk.CTkFrame(self.frame_01, fg_color=DF_FRAME_BG_1)
        self.frame_01_03.grid(row=2, column=0, pady=5, sticky=STICKY_XY)

        for i in [self.frame_01_01, self.frame_01_02, self.frame_01_03]:
            i.rowconfigure(index=(0, 1), weight=1, uniform=A)
            i.columnconfigure(index=(0, 1), weight=1, uniform=A)

#! ----- ----- ----- ----- <<<<< frame_01_01 >>>>> ----- ----- ----- -----

        self.impute_btn = ctk.CTkButton(self.frame_01_01, text='Impute', command=self.impute)

        self.impute_columns_options = ctk.CTkOptionMenu(self.frame_01_01, dynamic_resizing=False,
                                                        values=get_na_cols(dataset), fg_color=MENU_FG, dropdown_fg_color=MENU_FG,
                                                        button_color=MENU_BTN, button_hover_color=MENU_BTN_HVR, dropdown_hover_color=MENU_BTN_HVR)
        self.impute_columns_options.set(COLUMNS)
        
        self.impute_strategy_options = ctk.CTkOptionMenu(self.frame_01_01, dynamic_resizing=False,
                                                    values=IMPUTING_OPTIONS, fg_color=MENU_FG, dropdown_fg_color=MENU_FG,
                                                    button_color=MENU_BTN, button_hover_color=MENU_BTN_HVR, dropdown_hover_color=MENU_BTN_HVR)
        self.impute_strategy_options.set(STRATEGY)

        self.impute_btn.grid(row=0, column=0, columnspan=2, padx=10, pady=(10, 0), sticky=STICKY_X)
        self.impute_columns_options.grid(row=1, column=0, columnspan=1, padx=(10, 5), pady=(0, 10), sticky=STICKY_X)
        self.impute_strategy_options.grid(row=1, column=1, columnspan=1, padx=(5, 10), pady=(0, 10), sticky=STICKY_X)

#! ----- ----- ----- ----- <<<<< frame_01_02 >>>>> ----- ----- ----- -----

        self.fill_na_btn = ctk.CTkButton(self.frame_01_02, text='Fill NA', command=self.fill_na)

        self.fill_na_value_entry = ctk.CTkEntry(self.frame_01_02, placeholder_text='Value')

        self.fill_na_method_option = ctk.CTkOptionMenu(self.frame_01_02, dynamic_resizing=False,
                                                       values=FILL_NA_OPTIONS, fg_color=MENU_FG, dropdown_fg_color=MENU_FG,
                                                       button_color=MENU_BTN, button_hover_color=MENU_BTN_HVR, dropdown_hover_color=MENU_BTN_HVR)
        self.fill_na_method_option.set(METHOD)

        self.fill_na_btn.grid(row=0, column=0, columnspan=2, padx=10, pady=(10, 0), sticky=STICKY_X)
        self.fill_na_value_entry.grid(row=1, column=0, columnspan=1, padx=(10, 5), pady=(0, 10), sticky=STICKY_X)
        self.fill_na_method_option.grid(row=1, column=1, columnspan=1, padx=(5, 10), pady=(0, 10), sticky=STICKY_X)

        self.fill_na_value_entry.bind('<KeyRelease>', self.bind_fill_na_value)

#! ----- ----- ----- ----- <<<<< frame_01_03 >>>>> ----- ----- ----- -----

        self.drop_na_btn = ctk.CTkButton(self.frame_01_03, text='Drop NA', command=self.drop_na)

        self.drop_na_axis_option = ctk.CTkOptionMenu(self.frame_01_03, dynamic_resizing=False,
                                                     values=AXIS_OPTIONS, fg_color=MENU_FG, dropdown_fg_color=MENU_FG,
                                                     button_color=MENU_BTN, button_hover_color=MENU_BTN_HVR, dropdown_hover_color=MENU_BTN_HVR)

        self.drop_na_how_option = ctk.CTkOptionMenu(self.frame_01_03, dynamic_resizing=False,
                                                    values=HOW_OPTIONS, fg_color=MENU_FG, dropdown_fg_color=MENU_FG,
                                                    button_color=MENU_BTN, button_hover_color=MENU_BTN_HVR, dropdown_hover_color=MENU_BTN_HVR)

        self.drop_na_btn.grid(row=0, column=0, columnspan=2, padx=10, pady=(10, 0), sticky=STICKY_X)
        self.drop_na_axis_option.grid(row=1, column=0, columnspan=1, padx=(10, 5), pady=(0, 10), sticky=STICKY_X)
        self.drop_na_how_option.grid(row=1, column=1, columnspan=1, padx=(5, 10), pady=(0, 10), sticky=STICKY_X)

        self.drop_na_how_option.set(HOW)
        self.drop_na_axis_option.set(AXIS)

#! ----- ----- ----- ----- ----- ----- ----- ----- <<<<< frame_02 >>>>> ----- ----- ----- ----- ----- ----- ----- -----

        self.frame_02 = ctk.CTkFrame(self, fg_color=FRAME_DEFAULT_COLOR)
        self.frame_02.grid(row=0, column=1, rowspan=2, padx=5, pady=5, sticky=STICKY_XY)
        
        self.frame_02.rowconfigure(index=(0, 1), weight=1, uniform=A)
        self.frame_02.columnconfigure(index=0, weight=1, uniform=A)
        
        self.frame_02_01 = ctk.CTkFrame(self.frame_02, fg_color=DF_FRAME_BG_1)
        self.frame_02_01.grid(row=0, column=0, pady=5, sticky=STICKY_XY)

        self.frame_02_02 = ctk.CTkFrame(self.frame_02, fg_color=DF_FRAME_BG_1)
        self.frame_02_02.grid(row=1, column=0, pady=5, sticky=STICKY_XY)

        for i in [self.frame_02_01, self.frame_02_02]:
            i.rowconfigure(index=(0, 1, 2), weight=1, uniform=A)
            i.columnconfigure(index=(0, 1), weight=1, uniform=A)

#! ----- ----- ----- ----- <<<<< frame_02_01 >>>>> ----- ----- ----- -----

        self.drop_btn = ctk.CTkButton(self.frame_02_01, text='Drop', command=self.drop)
        
        self.drop_row_entry = ctk.CTkEntry(self.frame_02_01, placeholder_text=f'{ROWS} {self.dataframe.index.max()}')
        self.drop_columns_options = ctk.CTkOptionMenu(self.frame_02_01, dynamic_resizing=False,
                                                      values=dataset.columns, fg_color=MENU_FG, dropdown_fg_color=MENU_FG,
                                                      button_color=MENU_BTN, button_hover_color=MENU_BTN_HVR, dropdown_hover_color=MENU_BTN_HVR)
        self.drop_columns_options.set(COLUMNS)

        self.drop_axis_options = ctk.CTkOptionMenu(self.frame_02_01, dynamic_resizing=False,
                                              values=AXIS_OPTIONS, fg_color=MENU_FG, dropdown_fg_color=MENU_FG,
                                              button_color=MENU_BTN, button_hover_color=MENU_BTN_HVR, dropdown_hover_color=MENU_BTN_HVR)
        self.drop_axis_options.set(AXIS)
        self.drop_value_entry = ctk.CTkEntry(self.frame_02_01, placeholder_text='Where Value')

        self.drop_btn.grid(row=0, column=0, columnspan=2, padx=10, pady=(10, 0), sticky=STICKY_X)
        
        self.drop_row_entry.grid(row=1, column=0, columnspan=1, padx=(10, 5), pady=5, sticky=STICKY_X)
        self.drop_columns_options.grid(row=1, column=1, columnspan=1, padx=(5, 10), pady=5, sticky=STICKY_X)

        self.drop_value_entry.grid(row=2, column=0, columnspan=1, padx=(10, 5), pady=(0, 10), sticky=STICKY_X)
        self.drop_axis_options.grid(row=2, column=1, columnspan=1, padx=(5, 10), pady=(0, 10), sticky=STICKY_X)

#! ----- ----- ----- ----- <<<<< frame_02_02 >>>>> ----- ----- ----- -----

        self.search_btn = ctk.CTkButton(self.frame_02_02, text='Search', command=self.search)
        self.search_btn.grid(row=0, column=0, columnspan=2, padx=10, pady=(10, 0), sticky=STICKY_X)

        self.search_entry = ctk.CTkEntry(self.frame_02_02, placeholder_text='Search Key')
        self.search_entry.grid(row=1, column=0, padx=(10, 5), pady=5, sticky=STICKY_X)
        self.search_entry.bind('<KeyRelease>', self.bind_replace_key)

        self.replace_entry = ctk.CTkEntry(self.frame_02_02, placeholder_text='Replace Key')
        self.replace_entry.grid(row=1, column=1, padx=(5, 10), pady=5, sticky=STICKY_X)
        self.replace_entry.bind('<KeyRelease>', self.bind_replace_key)

        self.replace_btn = ctk.CTkButton(self.frame_02_02, text='Replace', state=DIS, command=self.replace)
        self.replace_btn.grid(row=2, column=0, columnspan=2, padx=10, pady=(0, 10), sticky=STICKY_X)
        
#! ----- ----- ----- ----- ----- ----- ----- ----- <<<<< Messages Frame >>>>> ----- ----- ----- ----- ----- ----- ----- -----

        self.textbox = ctk.CTkTextbox(self, state=DIS, font=FONTS[PRE_PREPROCESSING], wrap='word', activate_scrollbars=True, fg_color=DF_FRAME_BG_1)
        self.textbox.grid(row=0, column=2, rowspan=2, padx=10, pady=10, sticky=STICKY_XY)

        self.check_missing_values(self.dataframe)

#! ----- ----- ----- ----- ----- ----- ----- ----- <<<<< frame_03 >>>>> ----- ----- ----- ----- ----- ----- ----- -----

        self.frame_03 = ctk.CTkFrame(self, fg_color=FRAME_DEFAULT_COLOR)
        self.frame_03.grid(row=0, column=3, rowspan=2, columnspan=2, padx=5, pady=5, sticky=STICKY_XY)
        
        self.frame_03.rowconfigure(index=(0, 1, 2), weight=1, uniform=A)
        self.frame_03.columnconfigure(index=(0, 1), weight=1, uniform=A)

        self.frame_03_01 = ctk.CTkFrame(self.frame_03, fg_color=DF_FRAME_BG_1)
        self.frame_03_01.grid(row=0, column=0, padx=(0, 5), pady=5, sticky=STICKY_XY)
        self.frame_03_01.rowconfigure(index=(0, 1), weight=1, uniform=A)
        self.frame_03_01.columnconfigure(index=(0, 1), weight=1, uniform=A)

        self.frame_03_02 = ctk.CTkFrame(self.frame_03, fg_color=DF_FRAME_BG_1)
        self.frame_03_02.grid(row=0, column=1, padx=(5, 0), pady=5, sticky=STICKY_XY)
        self.frame_03_02.rowconfigure(index=(0, 1), weight=1, uniform=A)
        self.frame_03_02.columnconfigure(index=(0, 1), weight=1, uniform=A)

        self.frame_03_03 = ctk.CTkFrame(self.frame_03, fg_color=DF_FRAME_BG_1)
        self.frame_03_03.grid(row=1, column=0, columnspan=2, padx=0, pady=5, sticky=STICKY_XY)
        self.frame_03_03.rowconfigure(index=(0, 1), weight=1, uniform=A)
        self.frame_03_03.columnconfigure(index=(0, 1, 2, 3), weight=1, uniform=A)

        self.frame_03_04 = ctk.CTkFrame(self.frame_03, fg_color=DF_FRAME_BG_1)
        self.frame_03_04.grid(row=2, column=0, columnspan=2, padx=0, pady=5, sticky=STICKY_XY)
        self.frame_03_04.rowconfigure(index=(0, 1), weight=1, uniform=A)
        self.frame_03_04.columnconfigure(index=(0, 1, 2, 3), weight=1, uniform=A)

#! ----- ----- ----- ----- <<<<< frame_03_01 >>>>> ----- ----- ----- -----

        self.encode_btn = ctk.CTkButton(self.frame_03_01, text='Encode', command=self.encode)
        self.encode_btn.grid(row=0, column=0, columnspan=2, padx=10, pady=(10, 0), sticky=STICKY_X)

        self.encoder_options = ctk.CTkOptionMenu(self.frame_03_01, dynamic_resizing=False,
                                                 values=ENCODERS, fg_color=MENU_FG, dropdown_fg_color=MENU_FG,
                                                 button_color=MENU_BTN, button_hover_color=MENU_BTN_HVR, dropdown_hover_color=MENU_BTN_HVR)
        self.encoder_options.set(ENCODER)
        self.encoder_options.grid(row=1, column=0, padx=(10, 5), pady=(0, 10), sticky=STICKY_X)

        self.encode_column_options = ctk.CTkOptionMenu(self.frame_03_01, dynamic_resizing=False,
                                                       values=dataset.columns, fg_color=MENU_FG, dropdown_fg_color=MENU_FG,
                                                       button_color=MENU_BTN, button_hover_color=MENU_BTN_HVR, dropdown_hover_color=MENU_BTN_HVR)
        self.encode_column_options.set(COLUMNS)
        self.encode_column_options.grid(row=1, column=1, padx=(5, 10), pady=(0, 10), sticky=STICKY_X)
        self.not_encoded_columns = dataset.columns
        self.encoded_columns = []

#! ----- ----- ----- ----- <<<<< frame_03_02 >>>>> ----- ----- ----- -----

        self.scale_btn = ctk.CTkButton(self.frame_03_02, text='Scale', command=self.scale)
        self.scale_btn.grid(row=0, column=0, columnspan=2, padx=10, pady=(10, 0), sticky=STICKY_X)

        self.scaler_options = ctk.CTkOptionMenu(self.frame_03_02, dynamic_resizing=False,
                                                values=SCALERS, fg_color=MENU_FG, dropdown_fg_color=MENU_FG,
                                                button_color=MENU_BTN, button_hover_color=MENU_BTN_HVR, dropdown_hover_color=MENU_BTN_HVR)
        self.scaler_options.set(SCALER)
        self.scaler_options.grid(row=1, column=0, padx=(10, 5), pady=(0, 10), sticky=STICKY_X)

        self.scale_label_options = ctk.CTkOptionMenu(self.frame_03_02, dynamic_resizing=False,
                                                     values=dataset.columns, fg_color=MENU_FG, dropdown_fg_color=MENU_FG,
                                                     button_color=MENU_BTN, button_hover_color=MENU_BTN_HVR, dropdown_hover_color=MENU_BTN_HVR)
        self.scale_label_options.set(EXCLUDE)
        self.scale_label_options.grid(row=1, column=1, padx=(5, 10), pady=(0, 10), sticky=STICKY_X)
        self.used_scalers = []
        self.unused_scalers = [i for i in SCALERS if i not in self.used_scalers]

#! ----- ----- ----- ----- <<<<< frame_03_03 >>>>> ----- ----- ----- -----

        self.resolve_imbalance_btn = ctk.CTkButton(self.frame_03_03, text='Resolve Imbalance', state=DIS, command=self.resolve_imbalance)
        self.resolve_imbalance_btn.grid(row=0, column=0, columnspan=2, padx=10, pady=(10, 0), sticky=STICKY_X)

        self.resolve_method_options = ctk.CTkOptionMenu(self.frame_03_03, dynamic_resizing=False, state=DIS,
                                               values=BALANCING_METHODS, fg_color=MENU_FG, dropdown_fg_color=MENU_FG,
                                               button_color=MENU_BTN, button_hover_color=MENU_BTN_HVR, dropdown_hover_color=MENU_BTN_HVR)
        self.resolve_method_options.set(METHOD)
        self.resolve_method_options.grid(row=1, column=2, columnspan=2, padx=10, pady=(0, 10), sticky=STICKY_X)

        self.label_options = ctk.CTkOptionMenu(self.frame_03_03, dynamic_resizing=False, command=lambda _:self.submit_label_btn.configure(state=NRM),
                                               values=dataset.columns, fg_color=MENU_FG, dropdown_fg_color=MENU_FG,
                                               button_color=MENU_BTN, button_hover_color=MENU_BTN_HVR, dropdown_hover_color=MENU_BTN_HVR)
        self.label_options.set(LABEL)
        self.label_options.grid(row=0, column=3, padx=(5, 10), pady=(10, 0), sticky=STICKY_X)

        self.submit_label_btn = ctk.CTkButton(self.frame_03_03, text='Submit Label', state=DIS, command=self.submit_label)
        self.submit_label_btn.grid(row=0, column=2, padx=(10, 5), pady=(10, 0), sticky=STICKY_X)

        self.check_balance_btn = ctk.CTkButton(self.frame_03_03, text='Check', command=self.check_balance)
        self.check_balance_btn.grid(row=1, column=0, padx=(10, 5), pady=(0, 10), sticky=STICKY_X)

        self.plot_classes_btn = ctk.CTkButton(self.frame_03_03, text='Plot', command=self.plot_classes)
        self.plot_classes_btn.grid(row=1, column=1, padx=(5, 10), pady=(0, 10), sticky=STICKY_X)

#! ----- ----- ----- ----- <<<<< frame_03_04 >>>>> ----- ----- ----- -----

        self.select_features_btn = ctk.CTkButton(self.frame_03_04, text='Select', command=self.select_features)
        self.select_features_btn.grid(row=0, column=0, padx=(10, 5), pady=(10, 0), sticky=STICKY_X)

        self.rfe_rank_btn = ctk.CTkButton(self.frame_03_04, text='RFE Ranking', command=self.show_rfe_rank)
        self.rfe_rank_btn.grid(row=0, column=1, padx=(5, 10), pady=(10, 0), sticky=STICKY_X)

        self.sub_model_options = ctk.CTkOptionMenu(self.frame_03_04, dynamic_resizing=False, values=SUB_MODELS, fg_color=MENU_FG, dropdown_fg_color=MENU_FG,
                                                   button_color=MENU_BTN, button_hover_color=MENU_BTN_HVR, dropdown_hover_color=MENU_BTN_HVR)
        self.sub_model_options.grid(row=1, column=0, columnspan=2, padx=10, pady=(0, 10), sticky=STICKY_X)
        self.sub_model_options.set(SUB_MODEL)

        self.analyse_components_btn = ctk.CTkButton(self.frame_03_04, text='Analyse', command=self.analyse_components)
        self.analyse_components_btn.grid(row=0, column=2, padx=(10, 5), pady=(10, 0), sticky=STICKY_X)

        self.pca_info_btn = ctk.CTkButton(self.frame_03_04, text='PCA Information', command=self.show_pca_info)
        self.pca_info_btn.grid(row=0, column=3, padx=(5, 10), pady=(10, 0), sticky=STICKY_X)

        self.n_entry = ctk.CTkEntry(self.frame_03_04, placeholder_text='N Features/Components')
        self.n_entry.grid(row=1, column=2, columnspan=2, padx=10, pady=(0, 10), sticky=STICKY_X)

#! ----- ----- ----- ----- <<<<< frame_03_05 >>>>> ----- ----- ----- -----

    def submit_label(self):
        label_column = self.label_options.get()
        if not label_column == LABEL:
            self.label_options.configure(state=DIS)
            self.submit_label_btn.configure(state=DIS, text='Submitted')
            self.scale_label_options.set(label_column)
            self.scale_label_options.configure(state=DIS)
            self.send_task_command(task=LABEL, _label_column=label_column)
        else:
            self.write('Determine The Dataset Label.')

    def impute(self):
        column = self.impute_columns_options.get()
        strategy = self.impute_strategy_options.get()
        if strategy == STRATEGY:
            self.write('Determine The Imputing Strategy.')
        if column == COLUMNS:
            self.write('Determine The Imputing Column.')
        
        if strategy != STRATEGY and column != COLUMNS:
            strategy = strategy.lower().replace(' ', '_')
            self.send_task_command(task=IMPUTE, _column=column, _strategy=strategy)

    def drop_na(self):
        axis = self.drop_na_axis_option.get()
        how = self.drop_na_how_option.get()
        if axis == AXIS:
            self.write("Determine Drop Axis.")
        if how == HOW:
            self.write("Determine Drop Method.")
        if axis != AXIS and how != HOW:
            self.send_task_command(task=DROP_NA, _axis=int(axis), _how=how.lower())

    def fill_na(self):
        value = self.fill_na_value_entry.get()
        method = self.fill_na_method_option.get()
        if not method == METHOD:
            if method == B_FILL: 
                method = 'bfill'
            elif method == F_FILL: 
                method = 'ffill'

            self.send_task_command(task=FILL_NA, _method=method, _value=None)
        elif not value == '':
            self.send_task_command(task=FILL_NA, _value=set_dtype(value), _method=None)
        else:
            self.write('Determine Filling Value Or Method')

    def drop(self):
        row_index = self.drop_row_entry.get()
        column_name = self.drop_columns_options.get()
        value = self.drop_value_entry.get()
        axis = self.drop_axis_options.get()
        if not column_name == COLUMNS:
            if self.label_options.get() == column_name:
                self.write('Can Not Drop Label Column.')
            else:
                self.send_task_command(task=DROP_COL, _column_name=column_name)
        if not row_index == '':
            self.send_task_command(task=DROP_ROW, _row_index=row_index)
        if not value == '' and not axis == AXIS:
            if value.isdigit(): value = float(value)
            self.send_task_command(task=DROP_VAL, _value=value, _axis=int(axis))

    def search(self):
        key = set_dtype(self.search_entry.get())
        self.write(search(self.dataframe, key))

    def replace(self):
        old = set_dtype(self.search_entry.get())
        new = set_dtype(self.replace_entry.get())
        self.send_task_command(task=REPLACE_VAL, _old=old, _new=new)

    def encode(self):
        column = self.encode_column_options.get()
        encoder = self.encoder_options.get()
        if column == COLUMNS:
            self.write('Determine Encoding Column.')
        if encoder == ENCODER:
            self.write('Determine Encoding Type.')

        if column != COLUMNS and encoder != ENCODER:
            self.send_task_command(task=ENCODE, _column=column, _encoder=encoder)

    def scale(self):
        label = self.scale_label_options.get()
        scaler = self.scaler_options.get()
        if label == EXCLUDE:
            self.write('Determine Scaling Type.')
        if scaler == SCALER:
            self.write('Determine Scaling Type.')

        if label != EXCLUDE and scaler != SCALER:
            self.send_task_command(task=SCALE, _label_column=label, _scaler=scaler)

    def resolve_imbalance(self):
        label = self.label_options.get()
        method = self.resolve_method_options.get()
        if label == LABEL:
            self.write('Determine The Dataset Label.')
        if method == METHOD:
            self.write('Determine A Resolving Method.')
        if label != LABEL and method != METHOD:
            self.send_task_command(task=RESOLVE_IMBALANCE, _label_column=label, _resolve_method=method)

    def check_balance(self):
        label = self.label_options.get()
        if not label == LABEL:
            if len(np.unique(self.dataframe[label])) <= 10:
                balanced, skew = check_balance(self.dataframe, label)
                if balanced:
                    self.write('Dataset Is Balanced.')
                else:
                    self.write(f'Not Balanced, Skewed Towards `{skew}` Class.')
                    self.resolve_imbalance_btn.configure(state=NRM)
                    self.resolve_method_options.configure(state=NRM)
            else:
                self.write('Dataset Does Not Look Like a Classification Dataset Or The Column Selected As Label Is Not The Actual Label.')
        else:
            self.write('Determine The Dataset Label.')

    def plot_classes(self):
        label = self.label_options.get()
        if not label == LABEL:
            if len(np.unique(self.dataframe[label])) <= 10:
                plot_classes(self.dataframe, label)
            else:
                self.write('Dataset Does Not Look Like a Classification Dataset Or The Column Selected As Label Is Not The Actual Label.')
        else:
            self.write('Determine The Dataset Label.')

    def select_features(self):
        label = self.label_options.get()
        sub_model = self.sub_model_options.get()
        n_features = self.n_entry.get()
        if label == LABEL:
            self.write('Determine The Dataset Label.')
        if not self.confirm_n_entry(n_features):
            self.write('Invalid `N` Entry For Selected Fratures.')
        if sub_model == SUB_MODEL:
            self.write('Determine A Sub Model.')

        if label != LABEL and self.confirm_n_entry(n_features) and sub_model != SUB_MODEL:
            self.write(f'Selecting Top {n_features} Features.')
            Thread(target=self.__select_features, args=(label, sub_model, n_features, )).start()

    def __select_features(self, label, sub_model, n_features):
        self.rfe_pca_state(DIS)
        self.send_task_command(task=SELECT_FEATURES, _label_column=label, _sub_model=sub_model, _n_features=int(n_features))
        self.rfe_pca_state(NRM)
        self.write('RFE Task Completed Successfully.')

    def show_rfe_rank(self):
        Thread(target=self.__show_rfe_ranks, daemon=True).start()

    def __show_rfe_ranks(self):
        label = self.label_options.get()
        sub_model = self.sub_model_options.get()
        if label == LABEL:
            self.write('Determine The Dataset Label.')
        if sub_model == SUB_MODEL:
            self.write('Determine A Sub Model.')
        if label != LABEL and sub_model != SUB_MODEL:
            self.write(f'Analyzing Features Rankings Using {sub_model}...')
            self.rfe_pca_state(DIS)
            try:
                self.write(features_rank_message(self.dataframe, label, sub_model))
            except Exception as e:
                self.write(f'RFE Task Failed Due To {e.__class__.__name__}.')
            self.rfe_pca_state(NRM)

    def analyse_components(self):
        label = self.label_options.get()
        n_components = self.n_entry.get()
        if label == LABEL:
            self.write('Determine The Dataset Label.')
        if not self.confirm_n_entry(n_components):
            self.write('Invalid `N` Entry For Selected Components.')

        if label != LABEL and self.confirm_n_entry(n_components):
            self.write(f'Analysing Dataset To {n_components} Principal Components...')
            Thread(target=self.__analyse_components, args=(label, n_components, )).start()

    def __analyse_components(self, label, n_components):
        self.rfe_pca_state(DIS)
        self.send_task_command(task=ANALYSE_COMPONENTS, _label_column=label, _n_components=int(n_components))
        self.rfe_pca_state(NRM)
        self.write('PCA Task Completed Successfully.')

    def show_pca_info(self):
        label = self.label_options.get()
        if label == LABEL:
            self.write('Determine The Dataset Label.')
        if label != LABEL:
            self.write('Analyzing Principal Components...')
            try:
                msg, plt = principal_components_message(self.dataframe, label)
                self.write(msg)
                plt.show()
            except Exception as e:
                self.write(f'PCA Task Failed Due To {e.__class__.__name__}.')

    def rfe_pca_state(self, state):
        if state == DIS:        
            self.rfe_rank_btn.configure(state=DIS)
            self.sub_model_options.configure(state=DIS)
            self.select_features_btn.configure(state=DIS)
            self.analyse_components_btn.configure(state=DIS)
            self.pca_info_btn.configure(state=DIS)
            self.n_entry.configure(state=DIS)
        elif state == NRM:
            self.rfe_rank_btn.configure(state=NRM)
            self.sub_model_options.configure(state=NRM)
            self.select_features_btn.configure(state=NRM)
            self.analyse_components_btn.configure(state=NRM)
            self.pca_info_btn.configure(state=NRM)
            self.n_entry.configure(state=NRM)

    def confirm_n_entry(self, n):
        return n.isdigit() and 1<= int(n) <= len(self.dataframe.columns)-1

    def write(self, text, clear: bool=False):
        if clear: self.clear()
        self.textbox.configure(state=NRM)
        self.textbox.insert(tk.END, text=f'{text}\n\n')
        self.textbox.configure(state=DIS)

    def bind_fill_na_value(self, _):
        self.fill_na_method_option.set(METHOD)
        self.fill_na_method_option.configure(button_color=MENU_BTN_HVR)
        self.fill_na_value_entry.configure(border_color=MENU_BTN_HVR)

    def bind_fill_na_method(self, _):
        self.fill_na_value_entry.delete(0, END)
        self.fill_na_method_option.configure(button_color=MENU_BTN_HVR)
        self.fill_na_value_entry.configure(border_color=MENU_BTN_HVR)

    def bind_replace_key(self, _):
        if self.replace_entry.get() != '':
            self.replace_btn.configure(state=NRM)
        else:
            self.replace_btn.configure(state=DIS)

    def just_dropped(self):
        self.drop_row_entry.delete(0, END)
        self.drop_axis_options.set(AXIS)
        self.drop_row_entry.configure(placeholder_text=f'{ROWS} {self.dataframe.index.max()}')
        self.drop_columns_options.set(COLUMNS)
        self.drop_columns_options.configure(values=self.dataframe.columns)
        self.impute_columns_options.set(COLUMNS)
        self.impute_columns_options.configure(values=get_na_cols(self.dataframe))
        self.scale_label_options.configure(values=self.dataframe.columns)
        self.label_options.configure(values=self.dataframe.columns)
        self.pop_encoded_column(self.dataframe, 'Label', '')

    def just_balanced(self):
        self.resolve_imbalance_btn.configure(text='Imbalance Resolved', state=DIS)
        self.resolve_method_options.configure(state=DIS)

    def just_encoded(self):
        self.encode_column_options.set(COLUMNS)
        self.encoder_options.set(ENCODER)
        self.encode_column_options.configure(values=self.not_encoded_columns)

    def pop_used_scaler(self, scaler):
        if scaler and scaler not in self.used_scalers:
            self.used_scalers.append(scaler)
        self.unused_scalers = [i for i in SCALERS if i not in self.used_scalers]

        _text, _state = ('All Scaled', DIS) if self.unused_scalers == [] else ('Scale', NRM)
        self.scale_btn.configure(state=_state, text=_text)
        # self.scale_label_options.configure(state=_state)
        self.scaler_options.configure(values=self.unused_scalers, state=_state)
        self.scaler_options.set(SCALER)

    def pop_encoded_column(self, new_dataframe, encoder, encoded_column):        
        if encoder == 'Label':
            if encoded_column != '':
                self.encoded_columns.append(encoded_column)
        else:
            self.encoded_columns.extend([col for col in new_dataframe.columns if col.startswith(f'{encoded_column}_')])
        self.not_encoded_columns = [col for col in new_dataframe.columns if col not in self.encoded_columns]

        _text, _state = ('All Encoded', DIS) if self.not_encoded_columns == [] else ('Encode', NRM)
        self.encode_btn.configure(state=_state, text=_text)
        for i in [self.encode_btn, self.encode_column_options, self.encoder_options]:
            i.configure(state=_state)

    def check_missing_values(self, new_dataframe):
        rows = count_na(new_dataframe, 1)
        cols = count_na(new_dataframe, 0)
        self.write(text=f'Dataset Has: \n- {cols} NA Cloumns. \n- {rows} NA Rows.')

        for i in [self.impute_btn, self.impute_columns_options, self.impute_strategy_options,
                    self.fill_na_btn, self.fill_na_value_entry, self.fill_na_method_option, 
                    self.drop_na_btn, self.drop_na_axis_option, self.drop_na_how_option]:
            i.configure(state=NRM if (rows or cols) else DIS)

    def refresh(self, new_dataframe):
        self.dataframe = new_dataframe
        self.just_dropped()
        self.just_encoded()