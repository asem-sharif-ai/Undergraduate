import tkinter as tk
import customtkinter as ctk

from tkinter.filedialog import askopenfilename as import_file, asksaveasfilename as export_file

import pandas as pd

from copy import deepcopy

from GUI.Data   import *
from GUI.Window import *

from Workspace.PreProcessing.PreProcessing import * 

ctk.set_appearance_mode(APP_MODE)
ctk.set_default_color_theme(CLR_MODE)

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title(APP_TITLE)

        self.init_grid()
        self.init_pre_screen()

    def pre_processing(self, task, **kwargs):
        if task == DROP_COL:
            column_name = kwargs.get('_column_name', None)
            try:
                self.dataset = drop_column(dataframe=self.dataset, _column_name=column_name)
            except Exception as e:
                self.write_task(ERR, f'Dropping `{column_name}` Failed Due To {e.__class__.__name__}.')
            else:
                self.write_task(MSG, f'Column `{column_name}` Dropped Successfully.')

        elif task == DROP_ROW:
            row_index = kwargs.get('_row_index', None)
            try:
                self.dataset = drop_row(dataframe=self.dataset, _row_index=row_index)
            except Exception as e:
                self.write_task(ERR, f'Dropping `{row_index}` Failed Due To {e.__class__.__name__}.')
            else:
                self.write_task(MSG, f'Row `{row_index}` Dropped Successfully.')

        elif task == DROP_VAL:
            value = kwargs.get('_value', None)
            axis = kwargs.get('_axis', None)
            try:
                self.dataset = drop_value(dataframe=self.dataset, _value=value, _axis=axis)
            except Exception as e:
                self.write_task(ERR, f'Dropping `{value}` Based On Axis {axis} Failed Due To {e.__class__.__name__}.')
            else:
                self.write_task(MSG, f'Dropped `{value}` Based On Axis {axis} Successfully.')

        elif task == REPLACE_VAL:
            old = kwargs.get('_old', None)
            new = kwargs.get('_new', None)
            try:
                self.dataset = replace_value(dataframe=self.dataset, _old=old, _new=new)
            except Exception as e:
                self.write_task(ERR, f'Replacing `{old}` With {new} Failed Due To {e.__class__.__name__}.')
            else:
                self.write_task(MSG, f'Replaced `{old}` With {new} Successfully.')

        elif task == DROP_NA:
            axis = kwargs.get('_axis', None)
            how = kwargs.get('_how', None)
            try:
                self.dataset = drop_na(dataframe=self.dataset, _axis=axis, _how=how)
            except Exception as e:
                self.write_task(ERR, f'Dropping NA Of Axis `{axis} For {how}` Failed Due To {e.__class__.__name__}.')
            else:
                self.write_task(MSG, f'Dropped NA Of Axis `{axis} For {how}` Successfully.')
    
        elif task == FILL_NA:
            value = kwargs.get('_value', None)
            method = kwargs.get('_method', None)
            try:
                self.dataset = fill_na(dataframe=self.dataset, _method=method, _value=value)
            except Exception as e:
                self.write_task(ERR, f'Filling NA With `{value if value else method}` Failed Due To {e.__class__.__name__}.')
            else:
                self.write_task(MSG, f'Filled NA With `{value if value else method}` Successfully.')
    
        elif task == IMPUTE:
            column = kwargs.get('_column', None)
            strategy = kwargs.get('_strategy', None)
            try:
                self.dataset = impute(dataframe=self.dataset, _column=column, _strategy=strategy)
            except Exception as e:
                self.write_task(ERR, f'Imputing Missing Values Of `{column}` with `{strategy}` Failed Due To {e.__class__.__name__}.')
            else:
                self.write_task(MSG, f'Imputed Missing Values Of `{column}` with `{strategy}` Successfully.')
    
        elif task == ENCODE:
            column = kwargs.get('_column', None)
            encoder = kwargs.get('_encoder', None)
            try:
                self.dataset = encode(dataframe=self.dataset, _column=column, _encoder=encoder)
                self.workspace_frame.pre_preprocessing_tab.pop_encoded_column(self.dataset, encoder, column)
            except Exception as e:
                self.write_task(ERR, f'Encoding `{column}` with `{encoder}` Failed Due To {e.__class__.__name__}.')
            else:
                self.write_task(MSG, f'Encoded `{column}` with `{encoder}` Successfully.')
                self.log[ENCODE][self.log[INDEX]] = (encoder, column)

        elif task == SCALE:
            label_column = kwargs.get('_label_column', None)
            scaler = kwargs.get('_scaler', None)
            try:
                self.dataset = scale(dataframe=self.dataset, _label_column=label_column, _scaler=scaler)
                self.workspace_frame.pre_preprocessing_tab.pop_used_scaler(scaler)
            except Exception as e:
                self.write_task(ERR, f'Scaling `{[i for i in self.dataset.columns if i != label_column]}` With `{scaler} Scaler` Failed Due To {e.__class__.__name__}.')
            else:
                self.write_task(MSG, f'Scaled `{[i for i in self.dataset.columns if i != label_column]}` With `{scaler} Scaler` Successfully.')
                self.log[SCALE][self.log[INDEX]] = scaler
    
        elif task == RESOLVE_IMBALANCE:
            label_column = kwargs.get('_label_column', None)
            resolve_method = kwargs.get('_resolve_method', None)
            try:
                self.dataset = resolve_imbalance(dataframe=self.dataset, _label_column=label_column, _resolve_method=resolve_method)
                self.workspace_frame.pre_preprocessing_tab.just_balanced()
            except Exception as e:
                self.write_task(ERR, f'Resolving Label `{label_column}` Imbalance With `{resolve_method} Method` Failed Due To {e.__class__.__name__}.')
            else:
                self.write_task(MSG, f'Resolved Label `{label_column}` Imbalance With `{resolve_method} Method` Successfully.')
                self.log[BALANCE] = (self.log[INDEX], resolve_method)

        elif task == SELECT_FEATURES:
            label_column = kwargs.get('_label_column', None)
            sub_model = kwargs.get('_sub_model', None)
            n_features = kwargs.get('_n_features', None)
            try:
                self.dataset = select_features(dataframe=self.dataset, _label_column=label_column, _sub_model=sub_model, _n_features=n_features)
            except Exception as e:
                self.write_task(ERR, f'Selecting `{n_features}` Features By `{sub_model}` Failed Due To {e.__class__.__name__}.')
            else:
                self.write_task(MSG, f'Selected `{n_features}` Features By `{sub_model}` Successfully.')

        elif task == ANALYSE_COMPONENTS:
            label_column = kwargs.get('_label_column', None)
            n_components = kwargs.get('_n_components', None)
            try:
                self.dataset = analyse_principal_components(dataframe=self.dataset, _label_column=label_column, _n_components=n_components)
            except Exception as e:
                self.write_task(ERR, f'Analysing To `{n_components}` Principal Components Failed Due To {e.__class__.__name__}.')
            else:
                self.write_task(MSG, f'Analysed To `{n_components}` Principal Components Successfully.')

        elif task == LABEL: # Submit Label -> All Supervised Models
            label_column = kwargs.get('_label_column', None)
            self.write_task(MSG, f'Label `{label_column}` Submitted.')
            _ = self.workspace_frame.supervised_tab
            for tab in [_.decision_tree_frame,
                        _.random_forest_frame,
                        _.support_vector_machine_frame,
                        _.neural_network_frame,
                        _.k_nearest_neighbors_frame]:
                tab.label_options.set(label_column)
                tab.label_options.configure(state=DIS)

            self.log[LABEL] = (self.log[INDEX], label_column)

        if task in [DROP_COL, DROP_ROW, DROP_VAL, REPLACE_VAL, DROP_NA, FILL_NA, IMPUTE, ENCODE]:
            self.workspace_frame.pre_preprocessing_tab.check_missing_values(self.dataset)
            self.log[NAN].append(self.log[INDEX])

        self.update_log()
        self.update_app()

    def assign_clusters(self, new_dataframe):
        self.dataset = new_dataframe
        self.update_log()
        self.update_app()

    def update_app(self):
        self.dataset_frame.destroy()
        self.dataset_frame = DatasetFrame(self, dataset=self.dataset)
        self.workspace_frame.refresh(new_dataframe=self.dataset)

#! -----------------------------------------------------------------------

    def init_pre_screen(self):
        self.pre_screen_frame = PreScreenFrame(self, import_function=self.import_dataset)

    def import_dataset(self):
        path = import_file(title=CSV_IMPORT_LABEL, filetypes=CSV_FILES)
        try:
            if path.lower().endswith('.csv'):
                pd.read_csv(path)
            else:
                pd.read_excel(path)
        except Exception as e:
            print(f'Undefined `{e.__class__.__name__}` Error Occured While Importing Dataset, Import Failed.')
        else:
            self.path = path
            self.init_main_screen()

    def init_main_screen(self):
        self.pre_screen_frame.destroy()
        self.init_workspace()

    def init_workspace(self):
        self.dataset = pd.read_csv(self.path)

        self.log = {
            DATASET : [deepcopy(self.dataset)],
            INDEX   : 0,
            LABEL   : (-1, None),   # (index, label)

            NAN     : [],           # [index, ...]
            SCALE   : {},           # {index: scaler, index: scaler}
            ENCODE  : {},           # {index: (encoder, column), ...}
            BALANCE : (-1, None),   # (index, method)
        }

        self.dataset_frame = DatasetFrame(self, dataset=self.dataset)
        self.workspace_frame = WorkspaceFrame(self, dataset=self.dataset,
                                              pre_processing_function=self.pre_processing, assign_clusters_function=self.assign_clusters,
                                              reset_function=self.reset, restart_function=self.restart, export_function=self.export_dataset,
                                              undo_function=self.undo, redo_function=self.redo)

    def export_dataset(self):
        path = export_file(title=CSV_EXPORT_LABEL, filetypes=CSV_FILES)
        if path:
            try:
                self.dataset.to_csv(f'{path}.csv', index=False)
            except:
                self.write_task(ERR, f'Undefined Error Occured While Exporting Dataset, Export Failed.')
            else:
                self.write_task(MSG, f'Dataset Exported Successfully At `{path}`.')
        else:
                self.write_task(ERR, f'Export Cancelled Or Failed, Export Failed.')

#! -----------------------------------------------------------------------

    def del_workspace(self):
        self.dataset_frame.destroy()
        self.workspace_frame.destroy()

    def del_main_screen(self):
        self.del_workspace()
        self.init_pre_screen()

    def init_grid(self):
        self.window = {HEIGHT:self.winfo_screenheight(), WIDTH:self.winfo_screenwidth()}
        self.geometry(f'{self.window[WIDTH] // 2}x{self.window[HEIGHT] // 2}')
        self.minsize(self.window[WIDTH] // 2, self.window[HEIGHT] // 2)
        self.rowconfigure(index=0, weight=2, uniform=A)
        self.rowconfigure(index=1, weight=3, uniform=A)
        self.columnconfigure(index=0, weight=6, uniform=A)

#! -----------------------------------------------------------------------

    def write_task(self, type, text):
        self.workspace_frame.log_tab.update_log(msg_text=text, msg_type=type)
        if type == ERR:
            self.workspace_frame.tabs.set(LOG_TAB)

    def update_log(self):
        if self.log[INDEX] != len(self.log[DATASET]) - 1:
            self.log[DATASET] = self.log[DATASET][: self.log[INDEX] + 1]
            self.workspace_frame.log_tab.redo_btn.configure(state=DIS)

        if self.log[INDEX] > self.log[LABEL][0]:
            self.log[LABEL] = (-1, None)
        if self.log[INDEX] > self.log[BALANCE][0]:
            self.log[BALANCE] = (-1, None)

        for key in [key for key in self.log[SCALE] if key > self.log[INDEX]]:
            self.log[SCALE].pop(key)
        for key in [key for key in self.log[ENCODE] if key > self.log[INDEX]]:
            self.log[ENCODE].pop(key)

        for idx in [idx for idx in self.log[NAN] if idx > self.log[INDEX]]:
            self.log[NAN].remove(idx)

        self.log[DATASET].append(deepcopy(self.dataset))
        self.log[INDEX] += 1
        self.workspace_frame.log_tab.undo_btn.configure(state=NRM)

    def undo(self):
        self.log[INDEX] -= 1
        self.dataset = self.log[DATASET][self.log[INDEX]]

        _pre = self.workspace_frame.pre_preprocessing_tab

        if self.log[INDEX] in self.log[ENCODE]:
            if self.log[ENCODE][self.log[INDEX]][0] == LABEL:
                _pre.encoded_columns.remove(self.log[ENCODE][self.log[INDEX]][1])
            else:
                _pre.encoded_columns = list(
                    filter(lambda col: not col.startswith(self.log[ENCODE][self.log[INDEX]][1]),
                    _pre.encoded_columns)
                )
            _pre.pop_encoded_column(self.dataset, 'Label', '')

        elif self.log[INDEX] == self.log[LABEL][0]:
            _pre.submit_label_btn.configure(text='Submit Label')
            _pre.label_options.configure(state=NRM)
            _pre.label_options.set(LABEL)
            _pre.scale_label_options.configure(state=NRM)
            _pre.scale_label_options.set(EXCLUDE)
            
            _models = self.workspace_frame.supervised_tab
            for tab in [_models.decision_tree_frame,
                        _models.random_forest_frame,
                        _models.support_vector_machine_frame,
                        _models.neural_network_frame,
                        _models.k_nearest_neighbors_frame]:
                tab.label_options.configure(state=NRM)
                tab.label_options.set(LABEL)

        elif self.log[INDEX] == self.log[BALANCE][0]:
            _pre.resolve_method_options.configure(state=NRM)
            _pre.resolve_method_options.set(METHOD)
            _pre.resolve_imbalance_btn.configure(state=NRM, text='Resolve Imbalance')

        elif self.log[INDEX] in self.log[SCALE]:
            _pre.used_scalers.remove(self.log[SCALE][self.log[INDEX]])
            _pre.pop_used_scaler('')

        elif self.log[INDEX] in self.log[NAN]:
            _pre.check_missing_values(self.dataset)

        self.workspace_frame.log_tab.log_index -= 1
        self.write_task(type=MSG, text='Undo.')
        self.workspace_frame.log_tab.log_index -= 1

        self.workspace_frame.log_tab.redo_btn.configure(state=NRM)
        if self.log[INDEX] == 0:
            self.workspace_frame.log_tab.undo_btn.configure(state=DIS)

        self.update_app()

    def redo(self):
        self.log[INDEX] += 1
        self.dataset = self.log[DATASET][self.log[INDEX]]
        
        _pre = self.workspace_frame.pre_preprocessing_tab

        if self.log[INDEX] -1 in self.log[ENCODE]:
            if self.log[ENCODE][self.log[INDEX] - 1][0] == LABEL:
                _pre.encoded_columns.append(self.log[ENCODE][self.log[INDEX] - 1][1])
            else:
                _pre.encoded_columns.extend(
                    [col for col in self.dataset.columns if col.startswith(f'{self.log[ENCODE][self.log[INDEX] - 1][1]}_')]
                    )
            _pre.pop_encoded_column(self.dataset, 'Label', '')

        elif self.log[INDEX] -1 == self.log[LABEL][0]:
            _pre.submit_label_btn.configure(text='Submitted', state=DIS)
            _pre.label_options.configure(state=DIS)
            _pre.label_options.set(self.log[LABEL][1])

            _pre.scale_label_options.configure(state=DIS)
            _pre.scale_label_options.set(self.log[LABEL][1])

            _models = self.workspace_frame.supervised_tab
            for tab in [_models.decision_tree_frame,
                        _models.random_forest_frame,
                        _models.support_vector_machine_frame,
                        _models.neural_network_frame,
                        _models.k_nearest_neighbors_frame]:
                tab.label_options.set(self.log[LABEL][1])
                tab.label_options.configure(state=DIS)

        elif self.log[INDEX] -1 == self.log[BALANCE][0]:
            _pre.resolve_method_options.set(self.log[BALANCE][1])
            _pre.just_balanced()

        elif self.log[INDEX] -1 in self.log[SCALE]:
            _pre.pop_used_scaler(self.log[SCALE][self.log[INDEX]])

        elif self.log[INDEX] -1 in self.log[NAN]:
            _pre.check_missing_values(self.dataset)


        self.write_task(type=MSG, text='Redo.')
        self.workspace_frame.log_tab.log_index += 1

        self.workspace_frame.log_tab.undo_btn.configure(state=NRM)
        if self.log[INDEX] == len(self.log[DATASET]) - 1:
            self.workspace_frame.log_tab.redo_btn.configure(state=DIS)

        self.update_app()

    def reset(self):
        self.del_workspace()
        self.init_workspace()

    def restart(self):
        del self.dataset
        self.del_main_screen()

    @staticmethod
    def run():
        self = App()
        self.mainloop()