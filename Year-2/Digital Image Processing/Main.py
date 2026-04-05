import tkinter as tk
import customtkinter as ctk

from tkinter.filedialog import (askopenfilename   as import_file,
                                asksaveasfilename as export_file)

from PIL import (Image,
                 ImageTk,
                 ImageFilter,
                 ImageEnhance)

from time      import sleep as wait
from typing    import Literal
from threading import Thread

from Functions import *
from Utils.GUI.Frames import (ImageCanvas,
                              SideBar,
                              ToolBox,
                              MessagesPanel,
                              EntryBar,
                              BrowseButton,
                              VarifyButton,
                              LiveBar)

ctk.set_appearance_mode(APP_MODE)
ctk.set_default_color_theme(CLR_MODE)

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title(APP_TITLE)
        self.geometry(f'{self.winfo_screenwidth()}x{self.winfo_screenheight()}')

        # self.geometry(APP_GEOMETRY)

        self.init_grid()
        self.init_screen()
        self.init_default_values()
        self.init_image_default_values()

#! ---------- Create Objects ---------- ---------- ---------- ---------- ---------- ---------- ---------- ---------- ----------

    def init_screen(self):
        self.entry_bar      = EntryBar(self, self.varify_entry)
        self.browse_btn     = BrowseButton(self, self.browse_entry)
        self.varify_btn     = VarifyButton(self, self.varify_entry)
        self.messages_panel = MessagesPanel(self)
        
        self.tool_box       = ToolBox(self, plot_function            = self.plot_histogram,
                                            greyscale_function       = self.convert_greyscale,
                                            rotate_function          = self.get_set_rotate_value,
                                            transform_axis_function  = self.get_transform_axis_value,
                                            zoom_function            = self.get_zoom_value,
                                            brightness_function      = self.get_brightness_value,
                                            saturation_function      = self.get_saturation_value,
                                            contrast_function        = self.get_contrast_value,
                                            resolution_function      = self.get_resolution_value,
                                            noise_function           = self.get_noise_value,
                                            blur_function            = self.get_blur_value,
                                            appearance_mode_function = self.set_appearance_mode,
                                            export_function          = self.export_image,
                                            restart_function         = self.restart,
                                            reset_function           = self.reset,
                                            set_as_main_function     = self.set_as_main
                                        )

        self.side_bar       = SideBar(self, send_msg_function                = self.send_msg,
                                            point_operations_function        = self.get_point_operation_command,
                                            point_operations_adv_function    = self.get_point_operation_adv_command,
                                            gamma_command_function           = self.get_gamma_value,
                                            histogram_command_function       = self.get_histogram_operation_value, 
                                            plot_histogram_command_function  = self.plot_histogram_operation,
                                            neighborhood_operations_function = self.get_neighborhood_operation_command,
                                            edge_detection_function          = self.get_edge_detection_command,
                                            thresholding_function            = self.get_thresholding_command,
                                            morphology_function              = self.get_morphology_command
                                            )

        self.status_bar = LiveBar(self)

    #! ---------- Delete Objects (Reset / Restart) ---------- ---------- ---------- ----------

    def del_screen(self):
        for object in [self.entry_bar, self.browse_btn, self.varify_btn, self.messages_panel, self.tool_box, self.side_bar]:
            object.grid_forget()

#! ---------- Init Grid & Default Values ---------- ---------- ---------- ---------- ---------- ---------- ---------- ---------- ----------

    def init_grid(self):
        self.minsize(600, 400)
        self.rowconfigure(index=(0, 2), weight=4, uniform=A)
        self.rowconfigure(index=(1, 3), weight=1, uniform=A)
        self.columnconfigure(index=(0, 2), weight=1, uniform=A)
        self.columnconfigure(index=1, weight=4, uniform=A)

    def init_default_values(self):
        self.numerical_values = {
            TRANSFORM_AXIS: DEFAULT_VALUES[TRANSFORM_AXIS],
            ROTATE        : DEFAULT_VALUES[ROTATE],
            ZOOM          : DEFAULT_VALUES[ZOOM],
            BRIGHTNESS    : DEFAULT_VALUES[BRIGHTNESS],
            SATURATION    : DEFAULT_VALUES[SATURATION],
            CONTRAST      : DEFAULT_VALUES[CONTRAST],
            RESOLUTION    : DEFAULT_VALUES[RESOLUTION],
            NOISE         : DEFAULT_VALUES[NOISE],
            BLUR          : DEFAULT_VALUES[BLUR],

            HISTOGRAM_OPERATION : DEFAULT_VALUES[HISTOGRAM_OPERATION],

            POINT_OPERATION     : None,
            POINT_OPERATION_ADV : None,
            NEIGHBORHOOD_OPERATION: None,
            
            GAMMA         : None,

            THRESHOLDING  : DEFAULT_VALUES[THRESHOLDING],
            EDGE_DETECTION: DEFAULT_VALUES[EDGE_DETECTION],

            MORPHOLOGY    : None,
        }

        self.logistic_values = {
            GREYSCALE     : False,

            POINT_OPERATION    : False,
            POINT_OPERATION_ADV: False,
            NEIGHBORHOOD_OPERATION: False,

            GAMMA         : False,
            THRESHOLDING  : False,

            EDGE_DETECTION: False,
            MORPHOLOGY: False,

        }

        self.image_before_histogram_operation = None

    def init_image_default_values(self):
        self.image        = self.original_image = self.import_path = self.image_canvas = None
        self.image_height = self.canvas_height  = self.image_width = self.canvas_width = 0

#! ---------- UI Functions I ---------- ---------- ---------- ---------- ---------- ---------- ---------- ---------- ----------

    def set_appearance_mode(self, new_mode):
        ctk.set_appearance_mode(new_mode)
        self.send_msg(msg_type=MSG, msg_text=MSG_BANK[MSG]['Mode'])
        if self.image_canvas is not None:
            self.image_canvas.config(bg=CANVAS_CLR[new_mode])

    #! ---------- Get Entry Path ---------- ---------- ---------- ----------

    def browse_entry(self):
        path = import_file(filetypes=IMPORT_FILE_TYPES)
        if path in NULL_ENTRY:
            self.send_msg(msg_type=ERR, msg_text=MSG_BANK[ERR]['Import'])
        else:
            self.entry_bar.delete(first_index=0, last_index=tk.END)
            self.entry_bar.insert(index=0, string=path)

    def varify_entry(self, _event=None):
        try:
            path = self.entry_bar.entry_bar_var.get().strip()
            Image.open(path)
        except:
            self.send_msg(msg_type=ERR, msg_text=MSG_BANK[ERR]['Invalid Path'])
            self.set_entry_field(guide=NO)
        else:
            self.send_msg(msg_type=MSG, msg_text=MSG_BANK[MSG]['Valid Path'])
            self.set_entry_field(guide=OK)
            self.import_path = path
            self.init_image()

    def set_entry_field(self, guide):
        if guide == OK:
            self.varify_btn.configure(border_color=GRN)
            self.browse_btn.configure(border_color=GRN)
            self.entry_bar.configure(border_color=GRN)
            Thread(target=self.set_entry_field, args=(SET, )).start()
        elif guide == NO:
            self.entry_bar.configure(border_color=RED)
            self.varify_btn.configure(border_color=RED)
            self.browse_btn.configure(border_color=RED)
            self.entry_bar.delete(0, tk.END)
            Thread(target=self.set_entry_field, args=(OFF, )).start()
        elif guide == SET:
            self.entry_bar.delete(0, tk.END)
            self.entry_bar.insert(index=0, string=self.import_path)
            self.varify_btn.configure(state=DIS)
            self.browse_btn.configure(state=DIS)
            self.entry_bar.configure(state=DIS, text_color=TXT_CLR_DIS)
            Thread(target=self.set_entry_field, args=(OFF, )).start()
        elif guide == OFF:
            wait(WAIT_TIME)
            self.entry_bar.configure(border_color=ENTRY_BD)
            self.varify_btn.configure(border_color=ENTRY_BD)
            self.browse_btn.configure(border_color=ENTRY_BD)

#! ---------- Init The Image ---------- ---------- ---------- ---------- ---------- ---------- ---------- ---------- ----------

    def ensure_image_mode(self):
        if self.original_image.mode not in IMG_MODES:
            old_mode = self.original_image.mode
            if self.original_image.mode == RGBA:
                self.original_image = self.original_image.convert(RGB)
            else:
                self.original_image = self.original_image.convert(L)
            self.send_msg(msg_type=ERR, msg_text=MSG_BANK[ERR]['Converted'].replace('$$', old_mode).replace('$', self.original_image.mode))
        if self.original_image.mode == L:
            self.side_bar.object_01.channel_entry.delete(0, tk.END)
            self.side_bar.object_01.channel_entry.insert(0, L)
            self.side_bar.object_01.channel_entry.configure(state=READ_ONLY)


    def init_image(self):
        self.original_image = Image.open(self.import_path)
        self.ensure_image_mode()
        self.image = self.original_image
        self.image_canvas = ImageCanvas(self, self.resize_image)
    
    def re_init_image(self):
        try:
            self.image_canvas.delete(ALL)
        finally:
            self.resized_image = self.image.resize((int(self.image_width), int(self.image_height)))
            self.rotated_image = self.resized_image.rotate(self.numerical_values[ROTATE], expand=True)
            self.image_tk = ImageTk.PhotoImage(self.rotated_image)
            self.image_canvas.create_image(self.canvas_width // 2, self.canvas_height // 2, image=self.image_tk)   

    def del_image(self):
        if self.image_canvas is not None:
            self.image_canvas.delete(ALL)
            self.image_canvas.grid_forget()

    #! ---------- Resize Image For Canvas ---------- ---------- ---------- ----------

    def resize_image(self, event): # Tracing the window configurations
        self.image_ratio = self.image.size[0] / self.image.size[1]
        self.canvas_ratio = event.width / event.height
        self.image_height, self.image_width = self.image.size[0], self.image.size[1]    
        self.canvas_height, self.canvas_width = event.height, event.width
        
        if self.canvas_ratio > self.image_ratio:
            self.image_height = event.height
            self.image_width = int(self.image_height * self.image_ratio)
        else:
            self.image_height = int(self.image_width / self.image_ratio)
            self.image_width = event.width
        
        self.re_init_image()
        
#! ---------- UI Functions II ---------- ---------- ---------- ---------- ---------- ---------- ---------- ---------- ----------

    def send_msg(self, msg_type, msg_text):
        if msg_type == ERR:
            self.messages_panel.configure(state=NRM, border_color=RED, text_color=RED)
            self.messages_panel.insert(index=tk.END, text=f'>> {msg_text}\n\n')
            self.messages_panel.configure(state=DIS)
        elif msg_type == MSG:
            self.messages_panel.configure(state=NRM, border_color=GRN, text_color=GRN)
            self.messages_panel.insert(index=tk.END, text=f'>> {msg_text}\n\n')
            self.messages_panel.configure(state=DIS)
        else:
            self.messages_panel.configure(state=NRM, border_color=ENTRY_BD, text_color=TXT_CLR)
            self.messages_panel.insert(index=tk.END, text=f'>> {msg_text}\n\n')
            self.messages_panel.configure(state=DIS)
        Thread(target=self.reset_widget, args=(self.messages_panel, )).start()

    def highlight(self, color: Literal['red', 'green'], *widgets_args):
        for widget in widgets_args:
            if isinstance(widget, ctk.CTkButton):
                widget.configure(fg_color=color, hover_color=color)
            elif isinstance(widget, ctk.CTkTextbox):
                widget.configure(border_color=color)
            elif isinstance(widget, ctk.CTkFrame):
                widget.configure(border_color=color)
            elif isinstance(widget, ctk.CTkScrollableFrame):
                widget.configure(scrollbar_button_color=color, scrollbar_button_hover_color=color)
            elif isinstance(widget, ctk.CTkProgressBar):
                widget.configure(progress_color=color)

        Thread(target=self.reset_widget, args=widgets_args).start()

    def reset_widget(self, *widgets_args):
        wait(WAIT_TIME)
        for widget in widgets_args:
            if isinstance(widget, ctk.CTkButton):
                widget.configure(fg_color=BTN_FG, hover_color=BTN_HOVER)
            elif isinstance(widget, ctk.CTkTextbox):
                widget.configure(border_color=MSG_BOX_BD, text_color=TXT_CLR)
            elif isinstance(widget, ctk.CTkFrame):
                widget.configure(border_color=FRAME_DEFAULT_COLOR)
            elif isinstance(widget, ctk.CTkScrollableFrame):
                widget.configure(scrollbar_button_color=SCROLLBAR_DEFAULT_COLOR, scrollbar_button_hover_color=SCROLLBAR_HOVER_DEFAULT)
            elif isinstance(widget, ctk.CTkProgressBar):
                widget.configure(progress_color=BLU)

#! ---------- Getting Tool Box Commands ---------- ---------- ---------- ---------- ---------- ---------- ---------- ---------- ----------

    def plot_histogram(self):
        try:
            Histogram(self.image)
        except:
            self.send_msg(msg_type=ERR, msg_text=MSG_BANK[ERR]['Histogram'])
        else:
            self.send_msg(msg_type=MSG, msg_text=MSG_BANK[MSG]['Histogram'])

    def convert_greyscale(self):
        self.logistic_values[GREYSCALE] = True
        self.edit_image()

    def get_set_rotate_value(self, value):
        self.numerical_values[ROTATE] = 360 - int(value) if value != 'None' else 0
        self.edit_image()

    def get_zoom_value(self, value):
        self.numerical_values[ZOOM] = value
        self.edit_image()

    def get_transform_axis_value(self, value):
        self.numerical_values[TRANSFORM_AXIS] = value
        self.edit_image()

    def get_brightness_value(self, value):
        self.numerical_values[BRIGHTNESS] = value
        self.edit_image()

    def get_saturation_value(self, value): 
        self.numerical_values[SATURATION] = value
        self.edit_image()
    
    def get_contrast_value(self, value):
        self.numerical_values[CONTRAST] = value
        self.edit_image()
    
    def get_resolution_value(self, value):
        self.numerical_values[RESOLUTION] = max(value, 0.01)
        self.edit_image()
        
    def get_noise_value(self, value):
        self.numerical_values[NOISE] = value
        self.edit_image()
    
    def get_blur_value(self, value):
        self.numerical_values[BLUR] = value
        self.edit_image()

    def get_point_operation_command(self, operation, channel, factor):
        self.numerical_values[POINT_OPERATION] = (operation, channel, factor)
        self.logistic_values[POINT_OPERATION] = True
        self.edit_image()

    def get_point_operation_adv_command(self, sub_path, operation):
        try:
            self.sub_image = Image.open(sub_path).convert(self.image.mode)
        except:
            self.send_msg(msg_type=ERR, msg_text=MSG_BANK[ERR]['No Image'])
        else:
            self.numerical_values[POINT_OPERATION_ADV] = (self.sub_image, operation)
            self.logistic_values[POINT_OPERATION_ADV] = True
            self.edit_image()

    def get_gamma_value(self, value):
        self.numerical_values[GAMMA] = value
        self.logistic_values[GAMMA] = True
        self.edit_image()

    def get_histogram_operation_value(self, value):
        self.numerical_values[HISTOGRAM_OPERATION] = value
        self.edit_image()

    def get_neighborhood_operation_command(self, filter, size):
        self.numerical_values[NEIGHBORHOOD_OPERATION] = (filter, size)
        self.logistic_values[NEIGHBORHOOD_OPERATION] = True
        self.edit_image()

    def get_thresholding_command(self, mode, size):
        self.numerical_values[THRESHOLDING] = (mode, size)
        self.logistic_values[THRESHOLDING] = True
        self.edit_image()
        
    def get_edge_detection_command(self, algorithm):
        self.numerical_values[EDGE_DETECTION] = algorithm
        self.logistic_values[EDGE_DETECTION] = True
        self.edit_image()

    def get_morphology_command(self, method):
        self.numerical_values[MORPHOLOGY] = method
        self.logistic_values[MORPHOLOGY] = True        
        self.edit_image()

#! ---------- Executing Commands ---------- ---------- ---------- ---------- ---------- ---------- ---------- ---------- ----------

    def zoom(self):
        if self.numerical_values[ZOOM] != 0:
            new_width  = max(self.image.width -1 * (self.numerical_values[ZOOM] * self.image_ratio), 0)
            new_height = max(self.image.height-1 *  self.numerical_values[ZOOM]                    , 0)
            left = (self.image.width  // 2) - (new_width  // 2)
            top  = (self.image.height // 2) - (new_height // 2)
            right = left + new_width
            bottom = top + new_height
            self.image = self.image.crop((left, top, right, bottom))

    def axis_transform(self):
        if self.numerical_values[TRANSFORM_AXIS] == 'X':
            self.image = self.image.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
        elif self.numerical_values[TRANSFORM_AXIS] == 'Y':
            self.image = self.image.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
        elif self.numerical_values[TRANSFORM_AXIS] == 'XY':
            self.image = self.image.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
            self.image = self.image.transpose(Image.Transpose.FLIP_TOP_BOTTOM)

    def brightness(self):
        self.image = ImageEnhance.Brightness(self.image).enhance(self.numerical_values[BRIGHTNESS])

    def saturation(self):
        self.image = ImageEnhance.Color(self.image).enhance(self.numerical_values[SATURATION])

    def contrast(self):
        self.image = self.image.filter(ImageFilter.UnsharpMask(self.numerical_values[CONTRAST]))

    def resolution(self):
        self.image = self.image.resize((int(self.image_width  * self.numerical_values[RESOLUTION]),
                                        int(self.image_height * self.numerical_values[RESOLUTION])))

    def noise(self):
        self.image = Noise(self.image, self.numerical_values[NOISE])

    def blur(self):
        self.image = self.image.filter(ImageFilter.GaussianBlur(self.numerical_values[BLUR]))

    def greyscale(self):
        try:
            self.image = self.image.convert('L')
        except: 
            self.send_msg(msg_type=ERR, msg_text=MSG_BANK[ERR]['No Image'])
        else:
            self.tool_box.convertions_frame.greyscale_btn.configure(state=DIS)

    def point_operation(self):
        self.image = point_operations_manager(image=self.image, info=self.numerical_values[POINT_OPERATION])

    def point_operation_adv(self):
        self.image = point_operations_adv_manager(image=self.image, info=self.numerical_values[POINT_OPERATION_ADV])

    def gamma_correction(self):
        self.image = gamma_correction_manager(self.image, self.numerical_values[GAMMA])

    def histogram_operation(self):
        self.image_before_histogram_operation = self.image
        self.image = histogram_operations_manager(self.image, self.numerical_values[HISTOGRAM_OPERATION])
        for btn in [self.side_bar.object_02.plot_histogram_operation_btn, self.side_bar.object_02.disable_histogram_operation_btn]:
            btn.configure(state=NRM)

    def plot_histogram_operation(self):
        if self.image_before_histogram_operation: # Not None
            histogram_operations_plot_manager(self.image_before_histogram_operation, self.numerical_values[HISTOGRAM_OPERATION])
        
    def neighborhood_operation(self):
        self.image = neighborhood_operations_manager(image=self.image, info=self.numerical_values[NEIGHBORHOOD_OPERATION])

    def edge_detection(self):
        self.image = edge_detection_manager(self.image, info=self.numerical_values[EDGE_DETECTION])
        self.side_bar.object_04.edge_detection_apply_btn.configure(state=DIS)
        if self.side_bar.object_04.already_enhanced:
            self.side_bar.object_04.edge_detection_enhance_btn.configure(state=DIS)
        else:
            self.side_bar.object_04.edge_detection_enhance_btn.configure(state=NRM)

    def thresholding(self):
        self.image = thresholding_manager(image=self.image, info=self.numerical_values[THRESHOLDING])

    def morphology(self):
        self.image = morphology_manager(image=self.image, operation=self.numerical_values[MORPHOLOGY])

    #! ---------- Apply Changes ---------- ---------- ---------- ----------

    def apply_view_status_changes(self):
        if not self.numerical_values[ZOOM] == DEFAULT_VALUES[ZOOM]:
            self.zoom()
        if not self.numerical_values[TRANSFORM_AXIS] == DEFAULT_VALUES[TRANSFORM_AXIS]:
            self.axis_transform()
        # `re_init_image` in `edit_image` function does the rotation.

    def apply_conversion_changes(self):
        if self.logistic_values[GREYSCALE]:
            self.greyscale()
        # if conversion is binarization, most tasks will fail due to unsupported mode.

    def apply_tools_changes(self):
        if not self.numerical_values[BRIGHTNESS] == DEFAULT_VALUES[BRIGHTNESS]:
            self.brightness()
        if not self.numerical_values[SATURATION] == DEFAULT_VALUES[SATURATION]:
            self.saturation()
        if not self.numerical_values[CONTRAST] == DEFAULT_VALUES[CONTRAST]:
            self.contrast()
        if not self.numerical_values[RESOLUTION] == DEFAULT_VALUES[RESOLUTION]:
            self.resolution()
        if not self.numerical_values[NOISE] == DEFAULT_VALUES[NOISE]:
            self.noise()
        if not self.numerical_values[BLUR] == DEFAULT_VALUES[BLUR]:
            self.blur()

    def apply_tasks_changes(self):
        if not self.numerical_values[HISTOGRAM_OPERATION] == DEFAULT_VALUES[HISTOGRAM_OPERATION]:
            self.histogram_operation()

        if self.logistic_values[GAMMA]:
            self.gamma_correction()
        if self.logistic_values[POINT_OPERATION]:
            self.point_operation()
        if self.logistic_values[POINT_OPERATION_ADV]:
            self.point_operation_adv()
        if self.logistic_values[NEIGHBORHOOD_OPERATION]:
            self.side_bar.object_03.load()
            self.neighborhood_operation()
            self.side_bar.object_03.done()
        if self.logistic_values[EDGE_DETECTION]:
            self.edge_detection()
        if self.logistic_values[THRESHOLDING]:
            self.thresholding()
        if self.logistic_values[MORPHOLOGY]:
            self.morphology()

    def edit_image(self):
        if self.original_image is None:
            self.send_msg(msg_type=ERR, msg_text=MSG_BANK[ERR]['No Image'])
        else:
            try:
                self.image = self.original_image
            except:
                self.send_msg(msg_type=ERR, msg_text=MSG_BANK[ERR]['Undefined'])
            else:
                try:   # ToDo: All Functions Here.
                    self.status_bar.load()
                    
                    self.apply_view_status_changes()
                    self.apply_conversion_changes()
                    self.apply_tools_changes()
                    self.apply_tasks_changes()
                    
                    self.re_init_image()
                except:
                    self.send_msg(msg_type=ERR, msg_text='Task Failed.')
                    self.highlight(RED, self.status_bar)
                self.status_bar.done()

    #! ---------- Export Image ---------- ---------- ---------- ----------

    def export_image(self):
        if self.image_canvas is not None:
            try:
                self.export_path = export_file(defaultextension=DEFAULT_EXPORT_TYPE, filetypes=EXPORT_FILE_TYPES)
            except:
                self.send_msg(msg_type=ERR, msg_text=MSG_BANK[ERR]['Export'])
            else:
                try:
                    if extension(self.export_path) in EXPORT_FILE_EXTENTIONS:
                        self.image.save(self.export_path, extension(self.export_path))
                except:
                    self.send_msg(msg_type=ERR, msg_text=MSG_BANK[ERR]['Undefined'])
                else:
                    try:
                        Image.open(self.export_path)
                    except:
                        self.send_msg(msg_type=ERR, msg_text=MSG_BANK[ERR]['Undefined'])
                    else:
                        self.send_msg(msg_type=MSG, msg_text=MSG_BANK[MSG]['Export'])
        else:
            self.send_msg(msg_type=ERR, msg_text=MSG_BANK[ERR]['No Image'])

    #! ---------- Set as Main / Reset / Restart ---------- ---------- ---------- ----------

    def set_as_main(self):
        self.original_image = self.image # Still revertable by reset command
        self.init_default_values()
        self.del_screen()
        self.init_screen()

    def reset(self):
        path = self.import_path
        self.restart()
        self.import_path = path

        if self.import_path is not None:
            try:
                self.init_image()
            except:
                self.send_msg(msg_type=ERR, msg_text='Import Failed')
            else:
                self.set_entry_field(guide=SET)

    def restart(self):
        self.del_image()
        self.del_screen()
        self.init_screen()
        self.init_default_values()
        self.init_image_default_values()

    def Run(self):
        self.mainloop()
