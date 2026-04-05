import tkinter as tk
import customtkinter as ctk

from Utils.GUI.Data import *
from Utils.GUI.SideBar_SubFrames import *
from Utils.GUI.ToolBox_SubFrames import *

#! ---------- Image Frame ---------- ---------- ---------- ---------- ---------- ---------- ---------- ---------- ----------

class ImageCanvas(tk.Canvas):
    def __init__(self, parent, resize_function):
        super().__init__(master=parent, background=CANVAS_CLR[APP_MODE], highlightthickness=0)
        self.grid(row=0, column=1, rowspan=3, columnspan=1, padx=10, pady=(20, 0), sticky=NSEW)
        self.resize_image = resize_function
        self.bind('<Configure>', self.resize_image)

#! ---------- Sidebare Frame ---------- ---------- ---------- ---------- ---------- ---------- ---------- ---------- ----------

class SideBar(ctk.CTkScrollableFrame):
    def __init__(self, parent,
                 send_msg_function,
                 point_operations_function, point_operations_adv_function,
                 histogram_command_function, plot_histogram_command_function, gamma_command_function,
                 neighborhood_operations_function,
                 edge_detection_function,
                 thresholding_function,
                 morphology_function):

        super().__init__(master=parent, scrollbar_button_color=SCROLLBAR_DEFAULT_COLOR, scrollbar_button_hover_color=SCROLLBAR_HOVER_DEFAULT)
        self.grid(row=0, column=0, rowspan=3, columnspan=1, padx=(10, 0), pady=(20, 0), sticky=NSEW)

        self.object_01 = PointOperationsFrame(self, send_msg_function, point_operations_function, point_operations_adv_function)

        self.object_02 = GammaHistogramFrame(self, send_msg_function, gamma_command_function, histogram_command_function, plot_histogram_command_function)

        self.object_03 = NeighborhoodOperationsFrame(self, send_msg_function, neighborhood_operations_function)

        self.object_04 = EdgeDetectionFrame(self, send_msg_function, edge_detection_function)

        
        self.object_06 = MorphologyFrame(self, send_msg_function, morphology_function)
        
#! ---------- ToolBox Frame ---------- ---------- ---------- ---------- ---------- ---------- ---------- ---------- ----------

class ToolBox(ctk.CTkScrollableFrame):
    def __init__(self, parent,
                 plot_function,
                 greyscale_function,
                 appearance_mode_function, export_function, reset_function, restart_function, set_as_main_function,
                 rotate_function, transform_axis_function, zoom_function,
                 brightness_function, saturation_function, contrast_function, noise_function, blur_function, resolution_function
                ):

        super().__init__(master=parent, scrollbar_button_color=SCROLLBAR_DEFAULT_COLOR, scrollbar_button_hover_color=SCROLLBAR_HOVER_DEFAULT)
        self.grid(row=0, column=2, rowspan=1, columnspan=1, padx=10, pady=(20, 0), sticky=NSEW)

        self.toolbox_tabs = ctk.CTkTabview(self)
        self.toolbox_tabs.pack(padx=(10, 0), fill=BOTH, expand=True)

    #! ---------- Tools Tab ---------- ---------- ---------- ----------
    
        self.toolbox_tabs.add(TOOLS_TAB)
    
        self.histaogram_frame = HistogramFrame(self.toolbox_tabs.tab(TOOLS_TAB), plot_function)
        
        self.convertions_frame = ConvertionsFrame(self.toolbox_tabs.tab(TOOLS_TAB), greyscale_function)
        
        self.segmenteds_frame = SegmentedsFrame(self.toolbox_tabs.tab(TOOLS_TAB), rotate_function,
                                                                                  transform_axis_function,
                                                                                  zoom_function)
        
        self.sliders_frame = SlidersFrame(self.toolbox_tabs.tab(TOOLS_TAB), brightness_function,
                                                                            saturation_function,
                                                                            contrast_function,
                                                                            noise_function,
                                                                            blur_function,
                                                                            resolution_function)

    #! ---------- Settings Tab ---------- ---------- ---------- ----------

        self.toolbox_tabs.add(SETTINGS_TAB)

        self.settings_frame = SettingsFrame(self.toolbox_tabs.tab(SETTINGS_TAB), appearance_mode_function,
                                                                                 export_function,
                                                                                 reset_function,
                                                                                 restart_function,
                                                                                 set_as_main_function)

#! ---------- MessageBox Frame ---------- ---------- ---------- ---------- ---------- ---------- ---------- ---------- ----------

class MessagesPanel(ctk.CTkTextbox):
    def __init__(self, parent):
        super().__init__(master=parent, wrap='none', state=DIS, border_width=BORDER_WIDTH, border_color=MSG_BOX_BD, fg_color=MSG_BOX_FG,
                         scrollbar_button_color=SCROLLBAR_DEFAULT_COLOR, scrollbar_button_hover_color=SCROLLBAR_HOVER_DEFAULT)
        self.grid(row=2, column=2, rowspan=1, columnspan=1, padx=10, sticky=NSEW)

#! ---------- Entry Frame ---------- ---------- ---------- ---------- ---------- ---------- ---------- ---------- ----------

class EntryBar(ctk.CTkEntry):
    def __init__(self, parent, varify_function):
        self.entry_bar_var = ctk.StringVar()
        super().__init__(master=parent,
                         text_color=TXT_CLR, border_color=ENTRY_BD, fg_color=ENTRY_FG, border_width=BORDER_WIDTH, textvariable=self.entry_bar_var)
        self.grid(row=3, column=1, rowspan=1, columnspan=1, padx=10, pady=20, sticky=NSEW)
        self.bind('<Return>', varify_function)

    #! ---------- Varify Button ---------- ---------- ---------- ----------
    
class VarifyButton(ctk.CTkButton):
    def __init__(self, parent, varify_function):        
        super().__init__(master=parent, text='Varify Path', text_color=TXT_CLR, fg_color=ENTRY_FG,
                                                            border_width=BORDER_WIDTH, border_color=ENTRY_BD, text_color_disabled=TXT_CLR_DIS,
                                                            command=varify_function)

        self.grid(row=3, column=2, rowspan=1, columnspan=1, padx=10, pady=20, sticky=NSEW)

    #! ---------- Browse Button ---------- ---------- ---------- ----------
    
class BrowseButton(ctk.CTkButton):
    def __init__(self, parent, browse_function):
        super().__init__(master=parent, text='Browse Image', text_color=TXT_CLR, fg_color=ENTRY_FG, text_color_disabled=TXT_CLR_DIS,
                                                             border_width=BORDER_WIDTH, border_color=ENTRY_BD,
                                                             command=browse_function)
        
        self.grid(row=3, column=0, rowspan=1, columnspan=1, padx=10, pady=20, sticky=NSEW)

#! ---------- Status Bar ---------- ---------- ---------- ---------- ---------- ---------- ---------- ---------- ----------

class LiveBar(ctk.CTkProgressBar):
    def __init__(self, parent):
        super().__init__(master=parent, mode=LOADING_BAR, indeterminate_speed=2, width=15)
        self.grid(row=1, column=2, columnspan=1, padx=20, pady=(5, 5), sticky='ew')

    def load(self):
        self.start()

    def done(self):
        self.stop()