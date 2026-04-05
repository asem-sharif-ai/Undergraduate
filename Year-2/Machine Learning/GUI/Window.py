import tkinter as tk, customtkinter as ctk

from GUI.Data import *

from GUI.Tabs.PreProcessing.PreProcessing_Tab import *
from GUI.Tabs.Supervised.Supervised_Tab import *
from GUI.Tabs.UnSupervised.UnSupervised_Tab import *
from GUI.Tabs.Additional.Log_Tab import *

#! ----- ----- ----- ----- ----- ----- ----- ----- <<<<< Workspace Frame >>>>> ----- ----- ----- ----- ----- ----- ----- -----

class WorkspaceFrame(ctk.CTkFrame):
    def __init__(self, parent, dataset, **kwargs):
        super().__init__(master=parent)
        self.grid(row=1, column=0, rowspan=1, columnspan=1, padx=10, pady=10, sticky=STICKY_XY)
        self.tabs = ctk.CTkTabview(self, fg_color=FRAME_DEFAULT_COLOR)
        self.tabs.pack(padx=10, pady=(0, 10), expand=True, fill=BOTH)
        _self = self.tabs

        for operation in MAIN_MENU_TABS:
            _self.add(operation)

        self.pre_preprocessing_tab = PrePreprocessingTab(_self.tab(PRE_PREPROCESSING), dataset=dataset, pre_processing_function=kwargs.get('pre_processing_function', None))

        self.supervised_tab = SupervisedFrame(_self.tab(SUPERVISED), dataset=dataset)

        self.unsupervised_tab = UnSupervisedTab(_self.tab(UNSUPERVISED), dataset=dataset, assign_clusters_function=kwargs.get('assign_clusters_function', None))

        self.log_tab = LogTab(_self.tab(LOG_TAB), **kwargs)

    def refresh(self, new_dataframe):
        self.pre_preprocessing_tab.refresh(new_dataframe)
        self.supervised_tab.refresh(new_dataframe)
        self.unsupervised_tab.refresh(new_dataframe)

#! ----- ----- ----- ----- ----- ----- ----- ----- <<<<< Dataset Frame >>>>> ----- ----- ----- ----- ----- ----- ----- -----

class DatasetFrame(ttk.Treeview):
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
        self.columnconfigure(index=1, weight=1, uniform=A)

    def style_tree(self):
        self.style = ttk.Style()
        self.style.theme_use(THEME)
        self.style.configure(TREE, font=FONTS['Font'], anchor=CENTER, foreground=WHT, fieldbackground=DF_FRAME_BG_1,
                                   cellpadding=20, bd=0, highlightthickness=0)
        
        self.style.configure(TREE_HEAD, font=FONTS['Bold'], background=DF_FRAME_BG_1, foreground=WHT)
        self.style.map(TREE, background=[(SELECTED, DF_FRAME_BG_3)], foreground=[(SELECTED, BLK)])

        self.tag_configure(ODD , background=DF_FRAME_BG_1)
        self.tag_configure(EVEN, background=DF_FRAME_BG_2)

    def insert_data(self):
        self[COLS] = [NULL] + self.columns
        self[SHOW] = HEAD
        
        self.heading(NULL, text=NULL, anchor=CENTER)
        self.column(NULL, width=50, anchor=CENTER)

        for col in self.columns:
            self.heading(col, text=col, anchor=CENTER)
            self.column(col, width=150, anchor=CENTER)

        for i, row in self.dataframe.iterrows():
            values = [i] + [row[col] for col in self.columns]
            self.insert(NULL, END, values=values, tags=([EVEN, ODD][i % 2], ))

    def init_tree(self):
        h_scroll_bar = ctk.CTkScrollbar(self, orientation=HRZ, fg_color=DF_FRAME_BG_1, button_color=DF_FRAME_BG_2, command=self.xview)
        v_scroll_bar = ctk.CTkScrollbar(self, orientation=VRT, fg_color=DF_FRAME_BG_1, button_color=DF_FRAME_BG_2, command=self.yview)
        self.configure(xscrollcommand=h_scroll_bar.set, yscrollcommand=v_scroll_bar.set)

        self.grid(row=0, column=0, columnspan=1, padx=10, pady=10, sticky=STICKY_XY)
        h_scroll_bar.grid(row=2, column=0, columnspan=3, sticky=STICKY_X)
        v_scroll_bar.grid(row=0, column=2, rowspan=2, sticky=STICKY_Y)

#! ----- ----- ----- ----- ----- ----- ----- ----- <<<<< Pre Screen Frame >>>>> ----- ----- ----- ----- ----- ----- ----- -----

class PreScreenFrame(ctk.CTkFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(master=parent)
        self.grid(row=0, column=0, rowspan=2, columnspan=1, sticky=STICKY_XY)

        self.rowconfigure(index=0, weight=1, uniform=A)
        self.columnconfigure(index=1, weight=1, uniform=A)

        self.import_btn = ctk.CTkButton(self, text='Import Dataset', command=kwargs.get('import_function', None))
        self.import_btn.grid(row=0, column=1, padx=5, pady=5)
