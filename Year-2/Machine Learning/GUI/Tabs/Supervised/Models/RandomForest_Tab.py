
import tkinter as tk, customtkinter as ctk

from GUI.Data import *
from GUI.Functions import *

from Workspace.Supervised.RandomForest import * 

class RandomForestTab(ctk.CTkFrame):
    def __init__(self, parent, dataset, destroy_command):
        super().__init__(master=parent)
        self.pack(expand=True, fill=BOTH, padx=5, pady=(25, 0))

        self.dataset = dataset
        self.destroy_command = destroy_command

        self.rowconfigure(index=(0, 1, 2), weight=1, uniform=A)
        self.columnconfigure(index=(0, 1, 2, 3), weight=1, uniform=A)

#! ----- ----- ----- ----- ----- ----- ----- ----- <<<<< Sub Frames >>>>> ----- ----- ----- ----- ----- ----- ----- -----

        self.frame_01_01 = ctk.CTkFrame(self, fg_color=DF_FRAME_BG_1)
        self.frame_01_01.grid(row=0, column=0, rowspan=3, pady=(0, 0), padx=(0, 5), sticky=STICKY_XY)

        self.frame_01_02 = ctk.CTkFrame(self, fg_color=DF_FRAME_BG_1)
        self.frame_01_02.grid(row=0, column=1, rowspan=3, pady=(0, 0), padx=5, sticky=STICKY_XY)

        self.frame_01_03 = ctk.CTkFrame(self, fg_color=DF_FRAME_BG_1)
        self.frame_01_03.grid(row=2, column=2, columnspan=2, padx=(5, 0), pady=(5, 0), sticky=STICKY_XY)

        self.messages_textbox = ctk.CTkTextbox(self, state=DIS, font=FONTS[TERMINL], wrap='none', activate_scrollbars=True, fg_color=DF_FRAME_BG_1)
        self.messages_textbox.grid(row=0, column=2, rowspan=2, columnspan=2, padx=(5, 0), pady=(0, 5), sticky=STICKY_XY)

        self.frame_01_01.rowconfigure(index=(0, 1, 2, 3, 4, 5), weight=1, uniform=A)
        self.frame_01_01.columnconfigure(index=(0, 1), weight=1, uniform=A)

        self.frame_01_02.rowconfigure(index=(0, 1, 2, 3, 4), weight=1, uniform=A)
        self.frame_01_02.columnconfigure(index=(0, 1), weight=1, uniform=A)

        self.frame_01_03.rowconfigure(index=0, weight=1, uniform=A)
        self.frame_01_03.columnconfigure(index=(0, 1, 2, 3), weight=1, uniform=A)

#! ----- ----- ----- ----- ----- ----- ----- ----- <<<<< frame_01_01 >>>>> ----- ----- ----- ----- ----- ----- ----- -----

        self.model_type_btn = ctk.CTkSegmentedButton(self.frame_01_01, values=[CLASSIFICATION, REGRESSION], command=self.bind_model_type)
        self.model_type_btn.grid(row=0, column=0, columnspan=2, padx=10, pady=(10, 5), sticky=STICKY_X)
        self.model_type_btn.set(CLASSIFICATION)

        self.label_options = ctk.CTkOptionMenu(self.frame_01_01, dynamic_resizing=False, command=None,
                                               values=dataset.columns, fg_color=MENU_FG, dropdown_fg_color=MENU_FG,
                                               button_color=MENU_BTN, button_hover_color=MENU_BTN_HVR, dropdown_hover_color=MENU_BTN_HVR)
        self.label_options.grid(row=1, column=0, padx=(10, 5), pady=5, sticky=STICKY_X)
        self.label_options.set(LABEL)

        self.data_split_options = ctk.CTkOptionMenu(self.frame_01_01, dynamic_resizing=False, command=None,
                                               values=DATA_SPLIT_METHODS, fg_color=MENU_FG, dropdown_fg_color=MENU_FG,
                                               button_color=MENU_BTN, button_hover_color=MENU_BTN_HVR, dropdown_hover_color=MENU_BTN_HVR)
        self.data_split_options.grid(row=1, column=1, padx=(5, 10), pady=5, sticky=STICKY_X)
        self.data_split_options.set(DATA_SPLIT_METHOD)

        self.criterion_options = ctk.CTkOptionMenu(self.frame_01_01, dynamic_resizing=False,
                                                       values=CLS_CRITERIONS, fg_color=MENU_FG, dropdown_fg_color=MENU_FG,
                                                       button_color=MENU_BTN, button_hover_color=MENU_BTN_HVR, dropdown_hover_color=MENU_BTN_HVR)
        self.criterion_options.grid(row=2, column=0, padx=(10, 5), pady=5, sticky=STICKY_X)
        self.criterion_options.set(CRITERION)

        self.n_estimators_entry = ctk.CTkEntry(self.frame_01_01, placeholder_text='N Estimators')
        self.n_estimators_entry.grid(row=2, column=1, padx=(5, 10), pady=5, sticky=STICKY_X)

        self.test_size_entry = ctk.CTkEntry(self.frame_01_01, placeholder_text='Test Size')
        self.test_size_entry.grid(row=3, column=0, padx=(10, 5), pady=5, sticky=STICKY_X)

        self.random_state_entry = ctk.CTkEntry(self.frame_01_01, placeholder_text='Random State')
        self.random_state_entry.grid(row=3, column=1, padx=(5, 10), pady=5, sticky=STICKY_X)

        self.max_depth_entry = ctk.CTkEntry(self.frame_01_01, placeholder_text='Maximum Depth')
        self.max_depth_entry.grid(row=4, column=0, padx=(10, 5), pady=5, sticky=STICKY_X)

        self.min_impurity_entry = ctk.CTkEntry(self.frame_01_01, placeholder_text='Minimum Impurity')
        self.min_impurity_entry.grid(row=4, column=1, padx=(5, 10), pady=5, sticky=STICKY_X)

        self.varify_model_btn = ctk.CTkButton(self.frame_01_01, text='Varify Requirements | Inititalize Model', command=self.varify_model)
        self.varify_model_btn.grid(row=5, column=0, columnspan=2, padx=10, pady=(5, 10), sticky=STICKY_X)

#! ----- ----- ----- ----- ----- ----- ----- ----- <<<<< frame_01_02 >>>>> ----- ----- ----- ----- ----- ----- ----- -----

        self.split_data_btn = ctk.CTkButton(self.frame_01_02, text='Split Data', state=DIS, command=self.split_data)
        self.split_data_btn.grid(row=0, column=0, columnspan=2, padx=10, pady=(10, 5), sticky=STICKY_X)

        self.train_model_btn = ctk.CTkButton(self.frame_01_02, text='Train Model', state=DIS, command=self.train_model)
        self.train_model_btn.grid(row=1, column=0, padx=(10, 5), pady=5, sticky=STICKY_X)

        self.test_model_btn = ctk.CTkButton(self.frame_01_02, text='Test Model', state=DIS, command=self.test_model)
        self.test_model_btn.grid(row=1, column=1, padx=(5, 10), pady=5, sticky=STICKY_X)


        self.plot_tree_btn = ctk.CTkButton(self.frame_01_02, text='Plot Tree', state=DIS, command=self.plot_tree)
        self.plot_tree_btn.grid(row=2, column=0, columnspan=1, padx=(10, 5), pady=5, sticky=STICKY_X)

        self.plot_tree_indecies = ctk.CTkOptionMenu(self.frame_01_02, dynamic_resizing=False, state=DIS,
                                                       values=[], fg_color=MENU_FG, dropdown_fg_color=MENU_FG,
                                                       button_color=MENU_BTN, button_hover_color=MENU_BTN_HVR, dropdown_hover_color=MENU_BTN_HVR)
        self.plot_tree_indecies.grid(row=2, column=1, columnspan=1, padx=(5, 10), pady=5, sticky=STICKY_X)
        self.plot_tree_indecies.set(TREE_INDEX)

        self.report_or_variance_btn = ctk.CTkButton(self.frame_01_02, text='Classification Report', state=DIS, command=self.write_model_report)
        self.report_or_variance_btn.grid(row=3, column=0, padx=(10, 5), pady=5, sticky=STICKY_X)

        self.confusion_or_regression_btn = ctk.CTkButton(self.frame_01_02, text='Confusion Matrix', state=DIS, command=self.plot_confusion_matrix)
        self.confusion_or_regression_btn.grid(row=3, column=1, padx=(5, 10), pady=5, sticky=STICKY_X)
        
        self.destroy_model_btn = ctk.CTkButton(self.frame_01_02, text='Destroy Model', state=DIS, command=self.destroy_command)
        self.destroy_model_btn.grid(row=4, column=0, columnspan=2, padx=10, pady=(5, 10), sticky=STICKY_X)

#! ----- ----- ----- ----- ----- ----- ----- ----- <<<<< frame_01_03 >>>>> ----- ----- ----- ----- ----- ----- ----- -----

        self.btn_01 = ctk.CTkButton(self.frame_01_03, text='Accuracy Score', state=DIS, command=self.show_accuracy)
        self.btn_01.grid(row=0, column=0, padx=(10, 5), pady=5, sticky=STICKY_X)

        self.btn_02 = ctk.CTkButton(self.frame_01_03, text='Precision Score', state=DIS, command=self.show_precision)
        self.btn_02.grid(row=0, column=1, padx=5, pady=5, sticky=STICKY_X)

        self.btn_03 = ctk.CTkButton(self.frame_01_03, text='Recall Score', state=DIS, command=self.show_recall)
        self.btn_03.grid(row=0, column=2, padx=5, pady=5, sticky=STICKY_X)

        self.btn_04 = ctk.CTkButton(self.frame_01_03, text='F1 Score', state=DIS, command=self.show_f1)
        self.btn_04.grid(row=0, column=3, padx=(5, 10), pady=5, sticky=STICKY_X)

#! ----- ----- ----- ----- ----- ----- ----- ----- <<<<< Functions >>>>> ----- ----- ----- ----- ----- ----- ----- -----

    def split_data(self):
        try:
            self.model.split_data()
        except:
            self.write('Some Error Occured While Splitting The Data.')
        else:
            self.split_data_btn.grid_forget()
            self.train_data_btn = ctk.CTkButton(self.frame_01_02, text='Train Data', command=self.train_data_info)
            self.train_data_btn.grid(row=0, column=0, padx=(10, 5), pady=(10, 5), sticky=STICKY_X)
            self.test_data_btn = ctk.CTkButton(self.frame_01_02, text='Test Data', command=self.test_data_info)
            self.test_data_btn.grid(row=0, column=1, padx=(5, 10), pady=(10, 5), sticky=STICKY_X)
            self.train_model_btn.configure(state=NRM)

    def train_data_info(self):
        self.write(self.model.train_data_info)

    def test_data_info(self):
        self.write(self.model.test_data_info)

    def write_model_report(self):
        self.write(f'Decision Tree Classification Report: \n{self.model.report}')

    def train_model(self):
        self.write('Training Model...')
        try:
            self.model.train()
        except Exception as e:
            self.write(f'Training Model Failed Due To {e.__class__.__name__}')
        else:
            self.write(f'Model Has Been Trained Successfully.')
            self.train_model_btn.configure(state=DIS)
            self.test_model_btn.configure(state=NRM)

    def test_model(self):
        self.write('Testing Model...')
        try:
            self.model.test()
        except Exception as e:
            self.write(f'Testing Model Failed Due To {e.__class__.__name__}')
        else:
            self.write(f'Model Has Been Tested Successfully.')
            self.test_model_btn.configure(state=DIS)
            for i in [self.report_or_variance_btn, self.plot_tree_btn, self.plot_tree_indecies, self.confusion_or_regression_btn,
                      self.btn_01, self.btn_02, self.btn_03, self.btn_04]:
                i.configure(state=NRM)

    def plot_tree(self):
        index = self.plot_tree_indecies.get()
        if not index == INDEX:
            self.model.plot_tree(i=int(index))
        else:
            self.write('Determine A Tree Index.')

#! ----- ----- ----- ----- ----- ----- ----- ----- <<<<< Classifier >>>>> ----- ----- ----- ----- ----- ----- ----- -----

    def plot_confusion_matrix(self):
        self.write(CONFUSION_MATRIX)
        self.model.plot_confusion_matrix()

    def show_accuracy(self):
        self.write(f'Accuracy Score: {self.model.accuracy} | {round(self.model.accuracy, 3) * 100}%')

    def show_precision(self):
        self.write(f'Precision Score: {self.model.precision} | {round(self.model.precision, 3) * 100}%')

    def show_recall(self):
        self.write(f'Recall Score: {self.model.precision} | {round(self.model.precision, 3) * 100}%')

    def show_f1(self):
        self.write(f'F1 Score: {self.model.f1} | {round(self.model.f1, 3) * 100}%')

#! ----- ----- ----- ----- ----- ----- ----- ----- <<<<< Regressor >>>>> ----- ----- ----- ----- ----- ----- ----- -----

    def show_explained_variance(self):
        self.write(f'Explained Variance: {self.model.explained_variance:.03f} / 1')

    def plot_regression(self):
        self.model.plot_regression()

    def show_mean_abs(self):
        self.write(f'Mean Absolute Error: {self.model.mean_absolute:.03f}%')

    def show_mean_sqr(self):
        self.write(f'Mean Squared Error: {self.model.mean_squared:.03f}%')

    def show_root_mean_sqr(self):
        self.write(f'Root Mean Squared Error: {self.model.root_mean_squared:.03f}%')

    def show_r2(self):
        self.write(f'R2 Score: {self.model.r2:.03f}%')

    def write(self, text):
        self.messages_textbox.configure(state=NRM)
        self.messages_textbox.insert(tk.END, text=f'{text}\n\n')
        self.messages_textbox.configure(state=DIS)

    def varify_model(self):
        model_type   = self.model_type_btn.get()
        criterion    = self.criterion_options.get()
        n_estimators = self.n_estimators_entry.get()
        label        = self.label_options.get()
        data_split   = self.data_split_options.get()
        test_size    = self.test_size_entry.get()
        random_state = self.random_state_entry.get()
        max_depth    = self.max_depth_entry.get()
        min_impurity = self.min_impurity_entry.get()
        all_ok, warning = True, False

        if model_type not in [CLASSIFICATION, REGRESSION]:
            self.write('Determine The Model Type.')
            all_ok = False

        if label == LABEL:
            self.write('Determine The Dataset Label.')
            all_ok = False
        elif model_type == CLASSIFICATION and len(np.unique(self.dataset[label])) > 10:
            self.write('The Determined Label Has More Than 10 Instances, Which May Not Be The Actual Label For A Classification Task.')
            warning = not warning
        elif model_type == REGRESSION and len(np.unique(self.dataset[label])) <= 10:
            self.write('The Determined Label Has Less Than 10 Instances, Which May Not Be The Actual Label For A Regression Task.')
            warning = not warning

        if data_split == DATA_SPLIT_METHOD:
            data_split = 'Holdout'
            self.data_split_options.set(data_split)

        if criterion == CRITERION:
            if model_type in [CLASSIFICATION, REGRESSION]:
                criterion = 'Gini' if model_type == CLASSIFICATION else 'Squared Error'
                self.criterion_options.set(criterion)
            else:
                self.write('Determine A Model Criterion.')

        if n_estimators == '':
            n_estimators = '100'
            self.n_estimators_entry.insert(0, n_estimators)
        else:
            try:
                if not 2 <= int(n_estimators):
                    self.n_estimators_entry.delete(0, END)
                    n_estimators = np.min(int(n_estimators), 2)
                    self.n_estimators_entry.insert(0, str(n_estimators))
            except:
                self.write('Invalid Entry For Tree N Estimators.')
                all_ok = False

        if test_size == '':
            test_size = '0.25'
            self.test_size_entry.insert(0, test_size)
        else:
            try:
                if not 0.05 <= float(test_size) <= 0.50:
                    self.test_size_entry.delete(0, END)
                    test_size = np.clip(float(test_size), 0.05, 0.50)
                    self.test_size_entry.insert(0, str(test_size))
            except:
                self.write('Invalid Entry For The Test Size.')
                all_ok = False

        if random_state == '':
            random_state = '42'
            self.random_state_entry.insert(0, random_state)
        else:
            try:
                if not 0 <= int(random_state) <= RND:
                    self.random_state_entry.delete(0, END)
                    random_state = np.clip(int(random_state), 0, RND)
                    self.random_state_entry.insert(0, str(random_state))
            except:
                self.write('Invalid Entry For The Random State.')
                all_ok = False

        if max_depth == '':
            max_depth = 'None'
            self.max_depth_entry.insert(0, max_depth)
        elif max_depth != 'None':
            try:
                if not 2 < int(max_depth):
                    self.max_depth_entry.delete(0, END)
                    max_depth = np.max(max_depth, 2)
                    self.max_depth_entry.insert(0, str(max_depth))
            except:
                self.write('Invalid Entry For The Max Depth.')
                all_ok = False

        if min_impurity == '':
            min_impurity = '0.0'
            self.min_impurity_entry.insert(0, min_impurity)
        else:
            try:
                if not 0.00 <= float(min_impurity) <= 0.50:
                    self.min_impurity_entry.delete(0, END)
                    min_impurity = np.clip(float(min_impurity), 0.00, 0.50)
                    self.min_impurity_entry.insert(0, str(min_impurity))
            except:
                self.write('Invalid Entry For The Min Impurity.')
                all_ok = False

        if all_ok and not warning:
            self.write('Model Specifications Are Varified, Initializing Model.')
            try:
                if model_type == CLASSIFICATION:
                    self.model = RandomForestModel_Classifier(dataframe=self.dataset,
                                                              label_column=label,
                                                              criterion=criterion.lower().replace(' ', '_'),
                                                              n_estimators=int(n_estimators),
                                                              random_state=int(random_state),
                                                              max_depth=int(max_depth) if max_depth != 'None' else None,
                                                              min_impurity_decrease=float(min_impurity),
                                                              split_method=data_split,
                                                              test_size=float(test_size)
                                                              )
                else:
                    self.model = RandomForestModel_Regressor(dataframe=self.dataset,
                                                             label_column=label,
                                                             criterion=criterion.lower().replace(' ', '_'),
                                                             n_estimators=int(n_estimators),
                                                             random_state=int(random_state),
                                                             max_depth=int(max_depth) if max_depth != 'None' else None,
                                                             min_impurity_decrease=float(min_impurity),
                                                             split_method=data_split,
                                                             test_size=float(test_size)
                                                             )
            except:
                self.write('Some Error Occured While Initializing The Model.')
            else:
                self.write('Model Initialization Task Completed Successfully.')
                for i in [self.split_data_btn, self.destroy_model_btn]:
                    i.configure(state=NRM)

                for i in [self.model_type_btn, self.criterion_options, self.n_estimators_entry, self.label_options, self.data_split_options,
                          self.test_size_entry, self.random_state_entry, self.max_depth_entry, self.min_impurity_entry, self.varify_model_btn]:
                    i.configure(state=DIS)
                self.plot_tree_indecies.configure(values=[str(i) for i in list(range(int(n_estimators)))])

    def bind_model_type(self, model_type):
        if model_type == CLASSIFICATION:
            self.criterion_options.set(CRITERION)
            self.criterion_options.configure(values=CLS_CRITERIONS)

            self.btn_01.configure(text='Accuracy Score', command=self.show_accuracy)
            self.btn_02.configure(text='Precision Score', command=self.show_precision)
            self.btn_03.configure(text='Recall Score', command=self.show_recall)
            self.btn_04.configure(text='F1 Score', command=self.show_f1)

            self.confusion_or_regression_btn.configure(text='Confusion Matrix', command=self.plot_confusion_matrix)
            self.report_or_variance_btn.configure(text='Classification Report', command=self.write_model_report)

        elif model_type == REGRESSION:
            self.criterion_options.set(CRITERION)
            self.criterion_options.configure(values=REG_CRITERIONS)

            self.btn_01.configure(text='MAE', command=self.show_mean_abs)
            self.btn_02.configure(text='MSE', command=self.show_mean_sqr)
            self.btn_03.configure(text='RMSE', command=self.show_root_mean_sqr)
            self.btn_04.configure(text='R2', command=self.show_r2)

            self.confusion_or_regression_btn.configure(text='Plot Regression', command=self.plot_regression)
            self.report_or_variance_btn.configure(text='Explained Variance', command=self.show_explained_variance)

    def refresh(self, new_dataframe):
        self.dataset = new_dataframe
        self.label_options.configure(values=self.dataset.columns)