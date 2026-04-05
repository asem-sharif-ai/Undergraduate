import tkinter as tk, tkinter.ttk as ttk, customtkinter as ctk

from GUI.Data      import *
from GUI.Functions import *

from threading import Thread
from Workspace.UnSupervised.KMeans import *
from itertools import permutations
from re import match


class KMeansTab(ctk.CTkFrame):
    def __init__(self, parent, dataset, destroy_command, assign_clusters_function):
        super().__init__(master=parent)
        self.pack(expand=True, fill=BOTH, padx=5, pady=(25, 0))

        self.dataset = dataset
        self.destroy_command = destroy_command
        self.assign_clusters_as_main = assign_clusters_function

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

        self.frame_01_01.rowconfigure(index=(0, 1, 2, 3, 4), weight=1, uniform=A)
        self.frame_01_01.columnconfigure(index=(0, 1), weight=1, uniform=A)

        self.frame_01_02.rowconfigure(index=(0, 1, 2, 3, 4), weight=1, uniform=A)
        self.frame_01_02.columnconfigure(index=(0, 1), weight=1, uniform=A)

        self.frame_01_03.rowconfigure(index=0, weight=1, uniform=A)
        self.frame_01_03.columnconfigure(index=(0, 1, 2, 3), weight=1, uniform=A)

#! ----- ----- ----- ----- ----- ----- ----- ----- <<<<< frame_01_01 >>>>> ----- ----- ----- ----- ----- ----- ----- -----

        self.algorithm_options = ctk.CTkOptionMenu(self.frame_01_01, dynamic_resizing=False, command=None,
                                               values=K_ALGORITHMS, fg_color=MENU_FG, dropdown_fg_color=MENU_FG,
                                               button_color=MENU_BTN, button_hover_color=MENU_BTN_HVR, dropdown_hover_color=MENU_BTN_HVR)
        self.algorithm_options.grid(row=0, column=0, padx=(10, 5), pady=(10, 5), sticky=STICKY_X)
        self.algorithm_options.set(ALGORITHM)

        self.init_options = ctk.CTkOptionMenu(self.frame_01_01, dynamic_resizing=False, command=None,
                                               values=K_INITS, fg_color=MENU_FG, dropdown_fg_color=MENU_FG,
                                               button_color=MENU_BTN, button_hover_color=MENU_BTN_HVR, dropdown_hover_color=MENU_BTN_HVR)
        self.init_options.grid(row=0, column=1, padx=(5, 10), pady=(10, 5), sticky=STICKY_X)
        self.init_options.set(INIT)

        self.n_clusters_entry = ctk.CTkEntry(self.frame_01_01, placeholder_text='N Clusters')
        self.n_clusters_entry.grid(row=1, column=0, padx=(10, 5), pady=5, sticky=STICKY_X)

        self.n_init_entry = ctk.CTkEntry(self.frame_01_01, placeholder_text='N Init `auto`')
        self.n_init_entry.grid(row=1, column=1, padx=(5, 10), pady=5, sticky=STICKY_X)
        
        self.max_iterations_entry =  ctk.CTkEntry(self.frame_01_01, placeholder_text='Maximum Iteraions')
        self.max_iterations_entry.grid(row=2, column=0, padx=(10, 5), pady=5, sticky=STICKY_X)
    
        self.tolerance_entry = ctk.CTkEntry(self.frame_01_01, placeholder_text='Tolerance')
        self.tolerance_entry.grid(row=2, column=1, padx=(5, 10), pady=5, sticky=STICKY_X)

        self.label_name_entry = ctk.CTkEntry(self.frame_01_01, placeholder_text='Label Column')
        self.label_name_entry.grid(row=3, column=0, padx=(10, 5), pady=5, sticky=STICKY_X)

        self.random_state_entry = ctk.CTkEntry(self.frame_01_01, placeholder_text='Random State')
        self.random_state_entry.grid(row=3, column=1, padx=(5, 10), pady=5, sticky=STICKY_X)

        self.varify_model_btn = ctk.CTkButton(self.frame_01_01, text='Varify Requirements | Inititalize Model ', command=self.varify_model)
        self.varify_model_btn.grid(row=4, column=0, columnspan=2, padx=10, pady=(5, 10), sticky=STICKY_X)

#! ----- ----- ----- ----- ----- ----- ----- ----- <<<<< frame_01_02 >>>>> ----- ----- ----- ----- ----- ----- ----- -----

        self.show_data_btn = ctk.CTkButton(self.frame_01_02, text='Data Information', state=DIS, command=self.show_data_info)
        self.show_data_btn.grid(row=0, column=0, columnspan=2, padx=10, pady=(10, 5), sticky=STICKY_X)

        self.fit_model_btn = ctk.CTkButton(self.frame_01_02, text='Fit Model', state=DIS, command=self.fit_model)
        self.fit_model_btn.grid(row=1, column=0, padx=(10, 5), pady=5, sticky=STICKY_X)

        self.plot_k_elbow_btn = ctk.CTkButton(self.frame_01_02, text='K-Elbow', state=DIS, command=self.plot_k_elbow)
        self.plot_k_elbow_btn.grid(row=1, column=1, padx=(5, 10), pady=5, sticky=STICKY_X)

        self.plot_clusters_btn = ctk.CTkButton(self.frame_01_02, text='Plot Clusters', state=DIS, command=self.plot_clusters)
        self.plot_clusters_btn.grid(row=2, column=0, padx=(10, 5), pady=5, sticky=STICKY_X)

        self.plot_clusters_axis = ctk.CTkOptionMenu(self.frame_01_02, dynamic_resizing=False, state=DIS,
                                                       values=[], fg_color=MENU_FG, dropdown_fg_color=MENU_FG,
                                                       button_color=MENU_BTN, button_hover_color=MENU_BTN_HVR, dropdown_hover_color=MENU_BTN_HVR)
        self.plot_clusters_axis.grid(row=2, column=1, padx=(5, 10), pady=5, sticky=STICKY_X)
        self.plot_clusters_axis.set(PLOT_AXIS)

        self.assign_clusters_btn = ctk.CTkButton(self.frame_01_02, text='Assign Clusters', state=DIS, command=self.assign_clusters)
        self.assign_clusters_btn.grid(row=3, columnspan=2, padx=10, pady=5, sticky=STICKY_X)

        self.destroy_model_btn = ctk.CTkButton(self.frame_01_02, text='Destroy Model', state=DIS, command=self.destroy_command)
        self.destroy_model_btn.grid(row=4, column=0, columnspan=2, padx=10, pady=(5, 10), sticky=STICKY_X)

#! ----- ----- ----- ----- ----- ----- ----- ----- <<<<< frame_01_03 >>>>> ----- ----- ----- ----- ----- ----- ----- -----

        self.btn_01 = ctk.CTkButton(self.frame_01_03, text='Inertia', state=DIS, command=self.show_inertia)
        self.btn_01.grid(row=0, column=0, padx=(10, 5), pady=5, sticky=STICKY_X)

        self.btn_02 = ctk.CTkButton(self.frame_01_03, text='Silhouette', state=DIS, command=self.show_silhouette)
        self.btn_02.grid(row=0, column=1, padx=5, pady=5, sticky=STICKY_X)

        self.btn_03 = ctk.CTkButton(self.frame_01_03, text='Davies-Bouldin', state=DIS, command=self.show_davies_bouldin)
        self.btn_03.grid(row=0, column=2, padx=5, pady=5, sticky=STICKY_X)

        self.btn_04 = ctk.CTkButton(self.frame_01_03, text='Calinski & Harabasz', state=DIS, command=self.show_calinski_harabasz)
        self.btn_04.grid(row=0, column=3, padx=(5, 10), pady=5, sticky=STICKY_X)

#! ----- ----- ----- ----- ----- ----- ----- ----- <<<<< Functions >>>>> ----- ----- ----- ----- ----- ----- ----- -----

    def show_data_info(self):
        self.write(self.model.dataframe_info)

    def plot_clusters(self):
        choice = self.plot_clusters_axis.get()
        if choice != PLOT_AXIS:
            matches = match(r"\('([^']*)',\s*'([^']*)'(?:,\s*'([^']*)')?\)", choice)
            x = matches.group(1)
            y = matches.group(2)
            z = matches.group(3) if matches.group(3) else None
            self.model.plot_clusters(x, y, z)

    def plot_k_elbow(self):
        self.write('Appling K-Elbow Algorithm...')
        Thread(target=self.model.grid_search).start()

    def fit_model(self):
        self.write('Fitting Model...')
        try:
            self.model.cluster()
        except Exception as e:
            self.write(f'Fitting Model Failed Due To {e.__class__.__name__}')
        else:
            self.write(f'Model Has Been Fitted Successfully.')
            self.fit_model_btn.configure(state=DIS)
            for i in [self.assign_clusters_btn, self.plot_clusters_btn, self.plot_clusters_axis, self.plot_k_elbow_btn,
                      self.btn_01, self.btn_02, self.btn_03, self.btn_04]:
                i.configure(state=NRM)

    def assign_clusters(self):
        try:
            self.model.assign_clusters()
            self.assign_clusters_as_main(self.model.dataframe)
        except Exception as e:
            self.write(f'Some Error Occured While Updating Dataset: {e.__class__.__name__}')
        else:
            self.write(f'Dataset Updated With Cluster `{self.model.label_column}` Column.')
            self.assign_clusters_btn.configure(state=DIS)

    def show_inertia(self):
        self.write(f'Inertia Score: {self.model.inertia}')

    def show_silhouette(self):
        self.write(f'Silhouette Score: {self.model.silhouette}')

    def show_davies_bouldin(self):
        self.write(f'Davies Bouldin Score: {self.model.davies_bouldin}')

    def show_calinski_harabasz(self):
        self.write(f'Calinski And Harabasz Score: {self.model.calinski_harabasz}')

    def write(self, text):
        self.messages_textbox.configure(state=NRM)
        self.messages_textbox.insert(tk.END, text=f'{text}\n\n')
        self.messages_textbox.configure(state=DIS)

    def varify_model(self):
        n_clusters     = self.n_clusters_entry.get()
        init           = self.init_options.get()
        n_init         = self.n_init_entry.get()
        max_iterations = self.max_iterations_entry.get()
        algorithm      = self.algorithm_options.get()
        label_name     = self.label_name_entry.get()
        random_state   = self.random_state_entry.get()
        tolerance      = self.tolerance_entry.get()
        all_ok = True

        if n_clusters == '':
            self.write('Determine The Number Of Clusters.')
            all_ok = False
        else:
            try:
                if not 2 <= int(n_clusters): raise
            except:
                self.write('Invalid Entry For The Number Of Clusters.')
                all_ok = False

        if algorithm == ALGORITHM:
            algorithm = 'LLOYD'
            self.algorithm_options.set(algorithm)

        if init == INIT:
            init = 'K-Means++'
            self.init_options.set(init)

        if n_init == '':
            n_init = 'auto'
            self.n_init_entry.insert(0, n_init)
        elif n_init.lower() != 'auto':
            try:
                int(n_init)
            except:
                self.write('Invalid Entry For N Init.')
                all_ok = False

        if max_iterations == '':
            max_iterations = '300'
            self.max_iterations_entry.insert(0, max_iterations)
        else:
            try:
                int(max_iterations)
            except:
                self.write('Invalid Entry For Max Iterations.')
                all_ok = False

        if label_name == '':
            label_name = 'cluster'
            self.label_name_entry.insert(0, label_name)

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

        if tolerance == '':
            tolerance = '0.0'
            self.tolerance_entry.insert(0, tolerance)
        else:
            try:
                if not 0.00 <= float(tolerance) <= 0.50:
                    self.tolerance_entry.delete(0, END)
                    tolerance = np.clip(float(tolerance), 0.00, 0.50)
                    self.tolerance_entry.insert(0, str(tolerance))
            except:
                self.write('Invalid Entry For The Min Impurity.')
                all_ok = False

        if all_ok:
            self.write('Model Specifications Are Varified, Initializing Model.')
            try:
                self.model = KMeans_Model(dataframe=self.dataset, 
                                          n_clusters=int(n_clusters),
                                          algorithm=algorithm.lower(),
                                          init=init.lower(),
                                          n_init=int(n_init) if n_init.isdigit() else 'auto',
                                          max_iter=int(max_iterations), 
                                          tol=float(tolerance),
                                          label_column=label_name,
                                          random_state=int(random_state),
                                          )
            except:
                self.write('Some Error Occured While Initializing The Model.')
            else:
                self.write('Model Initialization Task Completed Successfully.')
                for i in [self.show_data_btn, self.fit_model_btn, self.plot_k_elbow_btn, self.destroy_model_btn]:
                    i.configure(state=NRM)

                for i in [self.n_clusters_entry, self.n_init_entry, self.max_iterations_entry, self.algorithm_options, self.init_options,
                          self.label_name_entry, self.random_state_entry, self.tolerance_entry, self.varify_model_btn]:
                    i.configure(state=DIS)
                self.plot_clusters_axis.configure(values=[str(i) for n in (2, 3) for i in permutations(self.dataset.columns, n)])

    def refresh(self, new_dataframe):
        self.dataset = new_dataframe