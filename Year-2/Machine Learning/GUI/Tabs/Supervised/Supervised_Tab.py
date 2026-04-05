import tkinter as tk, tkinter.ttk as ttk, customtkinter as ctk

from GUI.Data import *

from GUI.Tabs.Supervised.Models.DecisionTree_Tab import *
from GUI.Tabs.Supervised.Models.RandomForest_Tab import *
from GUI.Tabs.Supervised.Models.SupportVectorMachine_Tab import *
from GUI.Tabs.Supervised.Models.NeuralNetwork_Tab import *
from GUI.Tabs.Supervised.Models.KNearestNeighbors_Tab import *

class SupervisedFrame(ctk.CTkFrame):
    def __init__(self, parent, dataset):
        super().__init__(master=parent)
        self.pack(expand=True, fill=BOTH)
        self.tabs = ctk.CTkTabview(self, fg_color=FRAME_DEFAULT_COLOR)
        self.tabs.pack(padx=10, pady=(0, 10), expand=True, fill=BOTH)

        self.dataframe = dataset

        for t in SUPERVISED_TABS:
            self.tabs.add(t)

        self.decision_tree_frame = DecisionTreeTab(self.tabs.tab(DECISION_TREE),
                                                   dataset=self.dataframe,
                                                   destroy_command=self.destroy_decision_tree)

        self.random_forest_frame = RandomForestTab(self.tabs.tab(RANDOM_FOREST),
                                                   dataset=self.dataframe,
                                                   destroy_command=self.destroy_random_forest_tree)

        self.support_vector_machine_frame = SupportVectorMachineTab(self.tabs.tab(SVM),
                                                                    dataset=self.dataframe,
                                                                    destroy_command=self.destroy_support_vector_machine)

        self.neural_network_frame = NeuralNetworkTab(self.tabs.tab(ANN),
                                                     dataset=self.dataframe,
                                                     destroy_command=self.destroy_neural_network)

        self.k_nearest_neighbors_frame = KNearestNeighborsTab(self.tabs.tab(KNN),
                                                     dataset=self.dataframe,
                                                     destroy_command=self.destroy_k_nearest_neighbors)

    def destroy_decision_tree(self):
        self.decision_tree_frame.destroy()
        self.decision_tree_frame = DecisionTreeTab(self.tabs.tab(DECISION_TREE),
                                                   dataset=self.dataframe,
                                                   destroy_command=self.destroy_decision_tree)

    def destroy_random_forest_tree(self):
        self.random_forest_frame.destroy()
        self.random_forest_frame = RandomForestTab(self.tabs.tab(RANDOM_FOREST),
                                                   dataset=self.dataframe,
                                                   destroy_command=self.destroy_random_forest_tree)

    def destroy_support_vector_machine(self):
        self.support_vector_machine_frame.destroy()
        self.support_vector_machine_frame = SupportVectorMachineTab(self.tabs.tab(SVM),
                                                                    dataset=self.dataframe,
                                                                    destroy_command=self.destroy_support_vector_machine)

    def destroy_neural_network(self):
        self.neural_network_frame.destroy()
        self.neural_network_frame = NeuralNetworkTab(self.tabs.tab(ANN),
                                                     dataset=self.dataframe,
                                                     destroy_command=self.destroy_neural_network)

    def destroy_k_nearest_neighbors(self):
        self.k_nearest_neighbors_frame.destroy()
        self.k_nearest_neighbors_frame = KNearestNeighborsTab(self.tabs.tab(KNN),
                                                     dataset=self.dataframe,
                                                     destroy_command=self.destroy_k_nearest_neighbors)

    def refresh(self, new_dataframe):
        self.dataframe = new_dataframe
        for tab in [self.decision_tree_frame, self.random_forest_frame, self.support_vector_machine_frame, 
                    self.neural_network_frame, self.k_nearest_neighbors_frame]:
            tab.refresh(new_dataframe)