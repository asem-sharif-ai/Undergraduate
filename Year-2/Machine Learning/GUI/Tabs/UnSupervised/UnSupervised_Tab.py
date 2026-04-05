
import tkinter as tk, tkinter.ttk as ttk, customtkinter as ctk

from GUI.Data import *
from GUI.Tabs.UnSupervised.Models.KMeans_Tab import *

class UnSupervisedTab(ctk.CTkFrame):
    def __init__(self, parent, dataset, assign_clusters_function):
        super().__init__(master=parent)
        self.pack(expand=True, fill=BOTH)
        self.tabs = ctk.CTkTabview(self, fg_color=FRAME_DEFAULT_COLOR)
        self.tabs.pack(padx=10, pady=(0, 10), expand=True, fill=BOTH)

        self.dataframe = dataset
        self.assign_clusters_function = assign_clusters_function

        for t in UNSUPERVISED_TABS:
            self.tabs.add(t)

        self.k_means_frame = KMeansTab(self.tabs.tab(K_MEANS), dataset=self.dataframe,
                                       destroy_command=self.destroy_k_means,
                                       assign_clusters_function=self.assign_clusters_function)

    def destroy_k_means(self):
        self.k_means_frame.destroy()
        self.k_means_frame = KMeansTab(self.tabs.tab(K_MEANS), dataset=self.dataframe,
                                       destroy_command=self.destroy_k_means,
                                       assign_clusters_function=self.assign_clusters_function)

    def refresh(self, new_dataframe):
        self.dataframe = new_dataframe
        self.k_means_frame.refresh(new_dataframe)