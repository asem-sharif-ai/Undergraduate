import tkinter as tk
import customtkinter as ctk

import math
import pandas as pd

from threading import Thread

from Utils.GUI.Data import * 
from Utils.Models import CNN, Helper, Tracker

class ModelFrame(ctk.CTkFrame):
    def __init__(self, master, dataset: pd.DataFrame, label: str):
        super().__init__(master, **DFD[1])
        self.master = master
        self.dataset = dataset
        self.label = label
        self.has_loaded_model = False
        self.main_is_viewed = False

        self.view_pre()

    def view_pre(self):
        self.pre_frame = ctk.CTkFrame(self, **DFD[1])
        self.pre_frame.pack(fill='both', expand=True)

        self.pre_frame.rowconfigure(index=(0, 3), weight=5, uniform=A)
        self.pre_frame.rowconfigure(index=(1, 2), weight=2, uniform=A)
        self.pre_frame.columnconfigure(index=0, weight=1, uniform=A)

        self.import_model_btn = ctk.CTkButton(self.pre_frame, text='Import Model', width=175, command=Thread(target=self.import_model, daemon=True).start, **DBD)
        self.import_model_btn.grid(row=1, column=0, padx=10, pady=10)

        self.generate_model_btn = ctk.CTkButton(self.pre_frame, text='Generate Model', width=175, command=self.view_main, **DBD)
        self.generate_model_btn.grid(row=2, column=0, padx=10, pady=10)

        self.init_main()

    #! ----- ----- Generate Model ----- ----- ----- ----- ----- ----- ----- -----

    def init_main(self):
        self.main_frame = ctk.CTkFrame(self, **DFD[1])
        self.main_frame.rowconfigure(index=0, weight=11, uniform=A)
        self.main_frame.rowconfigure(index=1, weight=5, uniform=A)
        self.main_frame.columnconfigure(index=(0, 1), weight=1, uniform=A)

        #! ----- Model Base Frame ----- ----- ----- -----

        self.base_frame = ctk.CTkFrame(self.main_frame, **DFD[0])
        self.base_frame.grid(row=0, column=0, rowspan=2, padx=(10, 5), pady=10, sticky='nsew')

        self.base_frame.rowconfigure(index=tuple(range(7)), weight=1, uniform=A)
        self.base_frame.columnconfigure(index=(0, 1), weight=1, uniform=A)

        fr_1 = ctk.CTkFrame(self.base_frame, **DFD[1])
        fr_1.grid(row=0, column=0, columnspan=2, padx=10, pady=(10, 5), sticky='nsew')
        fr_1.rowconfigure(index=0, weight=1, uniform=A)
        fr_1.columnconfigure(index=0, weight=1, uniform=A)

        self.dataset_lbl = ctk.CTkLabel(fr_1, text=f'', font=('Lucida Console', 12, 'bold'))
        self.dataset_lbl.grid(row=0, column=0, padx=(5, 10), pady=5, sticky='nsw')

        ctk.CTkLabel(self.base_frame, text='Complexity').grid(row=1, column=0, rowspan=2, padx=(10, 5), pady=0, sticky='nw')
        self.complexity_lbl = ctk.CTkLabel(self.base_frame, text='3')
        self.complexity_lbl.grid(row=1, column=0, padx=(5, 10), pady=0, sticky='ne')
        self.complexity_sld = ctk.CTkSlider(self.base_frame, from_=1, to=5, number_of_steps=4,
                                        command=lambda n: self.complexity_lbl.configure(text=f'{int(n)}'), **DSD)
        self.complexity_sld.grid(row=1, column=0, padx=5, pady=(0, 5), sticky='sew')
        self.complexity_sld.set(3)

        fr_2 = ctk.CTkFrame(self.base_frame, **DFD[1])
        fr_2.grid(row=1, column=1, padx=10, pady=5, sticky='nsew')
        fr_2.rowconfigure(index=0, weight=1, uniform=A)
        fr_2.columnconfigure(index=0, weight=1, uniform=A)

        self.use_generator = False
        self.generator_option = ctk.CTkRadioButton(fr_2, text='  Use Generator',
                                                   variable=ctk.IntVar(value=0),
                                                   command=self.handle_use_generator, **DRBD)
        self.generator_option.grid(row=0, column=0, padx=10, pady=5, ipadx=2.5, sticky='nsew')

        ctk.CTkLabel(self.base_frame, text='Batch Size').grid(row=2, column=0, rowspan=2, padx=(10, 5), pady=0, sticky='nw')
        self.batch_lbl = ctk.CTkLabel(self.base_frame, text='32')
        self.batch_lbl.grid(row=2, column=0, padx=(5, 10), pady=0, sticky='ne')
        self.batch_sld = ctk.CTkSlider(self.base_frame, from_=1, to=8, number_of_steps=7,
                                        command=lambda n: self.batch_lbl.configure(text=f'{int(2 ** n)}'), **DSD)
        self.batch_sld.grid(row=2, column=0, padx=5, pady=(0, 5), sticky='sew')
        self.batch_sld.set(5)

        ctk.CTkLabel(self.base_frame, text='Test Size').grid(row=2, column=1, rowspan=2, padx=(10, 5), pady=0, sticky='nw')
        self.test_lbl = ctk.CTkLabel(self.base_frame, text='0.10')
        self.test_lbl.grid(row=2, column=1, padx=(5, 10), pady=0, sticky='ne')
        self.test_sld = ctk.CTkSlider(self.base_frame, from_=0.05, to=0.25,
                                        command=lambda n: self.test_lbl.configure(text=f'{n:.2f}'), **DSD)
        self.test_sld.grid(row=2, column=1, padx=5, pady=(0, 5), sticky='sew')
        self.test_sld.set(0.1)

        fr_3 = ctk.CTkFrame(self.base_frame, **DFD[1])
        fr_3.grid(row=3, column=0, columnspan=2, padx=10, pady=0, sticky='nsew')
        fr_3.rowconfigure(index=0, weight=1, uniform=A)
        fr_3.columnconfigure(index=0, weight=1, uniform=A)

        self.init_btn = ctk.CTkButton(fr_3, text='Initialize Model', state=DIS, command=self.init_model, **DBD)
        self.init_btn.grid(row=0, column=0, padx=7.5, pady=7.5, sticky='nsew')

        self.compile_btn = ctk.CTkButton(self.base_frame, text='Compile', state=DIS, command=self.compile_model, **DBD)
        self.compile_btn.grid(row=4, column=0, padx=(10, 5), pady=(10, 5), sticky='nsew')

        ctk.CTkLabel(self.base_frame, text='Learning Rate').grid(row=4, column=1, rowspan=2, padx=(10, 0), pady=2.5, sticky='nw')
        self.lr_lbl = ctk.CTkLabel(self.base_frame, text='0.0010')
        self.lr_lbl.grid(row=4, column=1, padx=(0, 10), pady=2.5, sticky='ne')
        self.lr_sld = ctk.CTkSlider(self.base_frame, from_=0.0001, to=0.1,
                                        command=lambda n: self.lr_lbl.configure(text=f'{n:.4f}'), **DSD)
        self.lr_sld.grid(row=4, column=1, padx=5, pady=2.5, sticky='sew')
        self.lr_sld.set(0.01)

        self.train_btn = ctk.CTkButton(self.base_frame, text='Train', state=DIS, command=self.train_model, **DBD)
        self.train_btn.grid(row=5, column=0, padx=(10, 5), pady=7, ipady=1, sticky='nsew')

        ctk.CTkLabel(self.base_frame, text='Epochs').grid(row=5, column=1, rowspan=2, padx=(10, 0), pady=2.5, sticky='nw')
        self.epochs_lbl = ctk.CTkLabel(self.base_frame, text='10')
        self.epochs_lbl.grid(row=5, column=1, padx=(0, 10), pady=2.5, sticky='ne')
        self.epochs_sld = ctk.CTkSlider(self.base_frame, from_=1, to=25, number_of_steps=24,
                                        command=lambda n: self.epochs_lbl.configure(text=f'{int(n)}'), **DSD)
        self.epochs_sld.grid(row=5, column=1, padx=5, pady=2.5, sticky='sew')
        self.epochs_sld.set(10)

        self.evaluate_btn = ctk.CTkButton(self.base_frame, text='Evaluate', state=DIS, command=self.evaluate_model, **DBD)
        self.evaluate_btn.grid(row=6, column=0, columnspan=2, padx=10, pady=(5, 10), sticky='nsew')

        #! ----- Train / Test Frame ----- ----- ----- -----

        self.train_frame = ctk.CTkFrame(self.main_frame, **DFD[0])
        self.train_frame.grid(row=0, column=1, padx=(5, 10), pady=(10, 5), sticky='nsew')

        self.font = ('Consolas', 14, 'bold')

        self.train_frame.rowconfigure(index=0, weight=2, uniform='a')
        self.train_frame.rowconfigure(index=1, weight=5, uniform='a')
        self.train_frame.columnconfigure(index=0, weight=1, uniform='a')

        fr_1 = ctk.CTkFrame(self.train_frame, **DFD[1])
        fr_1.grid(row=0, column=0, padx=10, pady=(10, 0), sticky='nsew')
        fr_1.rowconfigure(index=(0, 1), weight=1, uniform=A)
        fr_1.columnconfigure(index=(0, 1), weight=1, uniform=A)

        ctk.CTkLabel(fr_1, text='Epoch', font=self.font).grid(row=0, column=0, padx=(10, 5), pady=(10, 0), sticky='w')
        self.current_epoch_lbl = ctk.CTkLabel(fr_1, text=f'-', font=self.font)
        self.current_epoch_lbl.grid(row=0, column=0, padx=(5, 10), pady=(10, 0), sticky='e')

        ctk.CTkLabel(fr_1, text='Batch', font=self.font).grid(row=0, column=1, padx=(10, 5), pady=(10, 0), sticky='w')
        self.current_batch_lbl = ctk.CTkLabel(fr_1, text=f'-', font=self.font)
        self.current_batch_lbl.grid(row=0, column=1, padx=(5, 10), pady=(10, 0), sticky='e')

        self.process_bar = ctk.CTkProgressBar(fr_1, **DPBD)
        self.process_bar.set(0)
        self.process_bar.grid(row=1, column=0, columnspan=2, padx=10, pady=(5, 10), sticky='ew')

        fr_2 = ctk.CTkFrame(self.train_frame, **DFD[1])
        fr_2.grid(row=1, column=0, padx=10, pady=10, sticky='nsew')
        fr_2.rowconfigure(index=(0, 1, 2, 3), weight=1, uniform=A)
        fr_2.columnconfigure(index=(0, 1, 2), weight=1, uniform=A)

        ctk.CTkLabel(fr_2, text='Accuracy', font=self.font).grid(row=0, column=1, padx=(10, 5), pady=(10, 5), sticky='ew')
        ctk.CTkLabel(fr_2, text='Loss', font=self.font).grid(row=0, column=2, padx=(5, 10), pady=(10, 5), sticky='ew')

        ctk.CTkLabel(fr_2, text='Training', font=self.font).grid(row=1, column=0, padx=10, pady=(2.5, 7.5), sticky='w')
        self.training_accuracy_lbl = ctk.CTkLabel(fr_2, text=f'-', font=self.font)
        self.training_accuracy_lbl.grid(row=1, column=1, padx=(10, 5), pady=(2.5, 7.5), sticky='ew')
        self.training_loss_lbl = ctk.CTkLabel(fr_2, text=f'-', font=self.font)
        self.training_loss_lbl.grid(row=1, column=2, padx=(5, 10), pady=(2.5, 7.5), sticky='ew')

        ctk.CTkLabel(fr_2, text='Validation', font=self.font).grid(row=2, column=0, padx=10, pady=(0, 5), sticky='w')
        self.validation_accuracy_lbl = ctk.CTkLabel(fr_2, text=f'-', font=self.font)
        self.validation_accuracy_lbl.grid(row=2, column=1, padx=(10, 5), pady=(0, 5), sticky='ew')
        self.validation_loss_lbl = ctk.CTkLabel(fr_2, text=f'-', font=self.font)
        self.validation_loss_lbl.grid(row=2, column=2, padx=(5, 10), pady=(0, 5), sticky='ew')

        ctk.CTkLabel(fr_2, text='Evaluation', font=self.font).grid(row=3, column=0, padx=10, pady=(2.5, 10), sticky='w')
        self.evaluation_accuracy_lbl = ctk.CTkLabel(fr_2, text=f'-', font=self.font)
        self.evaluation_accuracy_lbl.grid(row=3, column=1, padx=(10, 5), pady=(2.5, 10), sticky='ew')
        self.evaluation_loss_lbl = ctk.CTkLabel(fr_2, text=f'-', font=self.font)
        self.evaluation_loss_lbl.grid(row=3, column=2, padx=(5, 10), pady=(2.5, 10), sticky='ew')

        #! ----- Evaluation Frame ----- ----- ----- -----

        self.eval_frame = ctk.CTkFrame(self.main_frame, **DFD[0])
        self.eval_frame.grid(row=1, column=1, padx=(5, 10), pady=(5, 10), sticky='nsew')

        self.eval_frame.rowconfigure(index=(0, 1), weight=1, uniform=A)
        self.eval_frame.columnconfigure(index=(0, 1, 2, 3, 4, 5), weight=1, uniform=A)

        self.confusion_btn = ctk.CTkButton(self.eval_frame, text='Confusion Matrix', state=DIS, command=self.plot_confusion, **DBD)
        self.confusion_btn.grid(row=0, column=0, columnspan=3, padx=(10, 5), pady=(10, 5), sticky='nsew')

        self.accuracy_vs_loss_btn = ctk.CTkButton(self.eval_frame, text='Accuracy VS Loss', state=DIS, command=self.plot_accuracy_vs_loss, **DBD)
        self.accuracy_vs_loss_btn.grid(row=0, column=3, columnspan=3, padx=(5, 10), pady=(10, 5), sticky='nsew')

        self.summary_btn = ctk.CTkButton(self.eval_frame, text='Summary', state=DIS, command=self.summary, **DBD)
        self.summary_btn.grid(row=1, column=0, columnspan=2, padx=(10, 5), pady=(5, 10), sticky='nsew')

        self.roc_auc_btn = ctk.CTkButton(self.eval_frame, text='ROC-AUC', state=DIS, command=self.plot_roc_auc, **DBD)
        self.roc_auc_btn.grid(row=1, column=2, columnspan=2, padx=5, pady=(5, 10), sticky='nsew')

        self.overview_btn = ctk.CTkButton(self.eval_frame, text='Overview', state=DIS, command=self.overview, **DBD)
        self.overview_btn.grid(row=1, column=4, columnspan=2, padx=(5, 10), pady=(5, 10), sticky='nsew')

    def view_main(self, cnn=None):
        self.setup_model(cnn)
        self.pre_frame.pack_forget()
        self.main_frame.pack(fill='both', expand=True)
        self.main_is_viewed = True
        self.validate_data()

    def init_model(self):
        complexity = int(self.complexity_sld.get())
        batch_size = int(2 ** self.batch_sld.get())
        test_size = round(self.test_sld.get(), 3)
        try:
            self.cnn = CNN(
                complexity=complexity,
                dataset=self.dataset,
                label=self.label,
                writer=self.master.write
            )
            self.cnn.load_data(
                test_size=test_size,
                batch_size=batch_size,
                use_generator=self.use_generator
            )
        except Exception as e:
            self.master.write(f'{e.__class__.__name__}')
        else:
            self.disable(self.init_btn, self.complexity_sld, self.generator_option, self.test_sld, self.batch_sld,
                         self.master.data_section.remove_btn)
            self.master.data_section.disable_labeling()
            self.enable(self.compile_btn, self.lr_sld)

    def compile_model(self):
        learning_rate = round(self.lr_sld.get(), 4)
        try:
            self.cnn.compile(learning_rate=learning_rate)
        except Exception as e:
            self.master.write(f'{e.__class__.__name__}')
        else:
            self.disable(self.compile_btn, self.lr_sld)
            self.enable(self.train_btn, self.epochs_sld)

    def train_model(self):
        self.epochs = int(self.epochs_sld.get())
        self.batch_size = 2 ** int(self.batch_sld.get())
        self.training_batches = math.ceil(len(self.cnn.x_train) / self.batch_size)
        self.val_eval_batches = math.ceil(len(self.cnn.x_test) / self.batch_size)
        try:
            self.is_training = True
            self.disable(self.train_btn, self.epochs_sld)
            Thread(target=self.cnn.train, kwargs={'epochs':self.epochs, 'callbacks':[Tracker(self.update_process)]}, daemon=True).start()
        except Exception as e:
            self.master.write(f'{e.__class__.__name__}')

    def evaluate_model(self):
        def evaluate():
            self.cnn.evaluate(callbacks=[Tracker(self.update_process)])
            self.current_batch_lbl.configure(text=f'[{self.val_eval_batches}/{self.val_eval_batches}]')
            self.process_bar.set(1)
            self.ready()
        try:
            Thread(target=evaluate, daemon=True).start()
        except Exception as e:
            self.master.write(f'{e.__class__.__name__}')

    def update_process(self, *_, **kwargs):
        if 'epoch' in kwargs:
            self.current_epoch_lbl.configure(text=f'[{kwargs['epoch']+1}/{self.epochs}]')
            self.process_bar.configure(progress_color='#8B0000')

        if 'training_batch' in kwargs:
            self.current_batch_lbl.configure(text=f'[{kwargs['training_batch']+1}/{self.training_batches}]')
            self.process_bar.set((kwargs['training_batch']+1)/self.training_batches)
        if 'training_accuracy' in kwargs:
            self.training_accuracy_lbl.configure(text=f'{kwargs['training_accuracy'] * 100:.2f}')
        if 'training_loss' in kwargs:
            self.training_loss_lbl.configure(text=f'{kwargs['training_loss']:.3f}')

        if 'val_eval_batch' in kwargs:
            self.current_batch_lbl.configure(text=f'[{kwargs['val_eval_batch']+1}/{self.val_eval_batches}]')
            self.process_bar.set((kwargs['val_eval_batch']+1)/self.val_eval_batches)

        if self.is_training:
            if 'val_eval' in kwargs:
                self.process_bar.set(0)
                self.process_bar.configure(progress_color='orange')
            if 'val_eval_accuracy' in kwargs:
                self.validation_accuracy_lbl.configure(text=f'{kwargs['val_eval_accuracy'] * 100:.2f}')
            if 'val_eval_loss' in kwargs:
                self.validation_loss_lbl.configure(text=f'{kwargs['val_eval_loss']:.3f}')
        else:
            if 'val_eval' in kwargs:
                self.process_bar.set(0)
                self.process_bar.configure(progress_color='#008000')
            if 'val_eval_accuracy' in kwargs:
                self.evaluation_accuracy_lbl.configure(text=f'{kwargs['val_eval_accuracy'] * 100:.2f}')
            if 'val_eval_loss' in kwargs:
                self.evaluation_loss_lbl.configure(text=f'{kwargs['val_eval_loss']:.3f}')

        if 'stats' in kwargs:
            self.cnn._catch_stats(kwargs['stats'])
            self.process_bar.configure(progress_color='orange')
            self.evaluate_btn.configure(state=NRM)
            self.is_training = False

        if 'evaluation_accuracy' in kwargs:
            self.evaluation_accuracy_lbl.configure(text=f'{kwargs['evaluation_accuracy'] * 100:.2f}')
        if 'evaluation_loss' in kwargs:
            self.evaluation_loss_lbl.configure(text=f'{kwargs['evaluation_loss']:.3f}')
        if 'evaluation_batch' in kwargs:
            self.current_batch_lbl.configure(text=f'[{kwargs['evaluation_batch']+1}/{self.val_eval_batches}]')
            self.process_bar.set((kwargs['evaluation_batch']+1)/self.val_eval_batches)

    def ready(self):
        self.master.cnn = self.cnn
        self.process_bar.configure(progress_color='#008000')
        self.disable(self.evaluate_btn)
        self.master.control_section.activate_model_btn.configure(command=self.activate_model, state=NRM)
        self.master.control_section.save_model_btn.configure(state=NRM, command=self.export_model)

        self.enable(
            self.confusion_btn,
            self.accuracy_vs_loss_btn,
            self.summary_btn,
            self.roc_auc_btn,
            self.overview_btn,
        )

    def activate_model(self):
        self.master.cnn_is_activated = True
        self.master.control_section.activate_model_btn.configure(text='De-Activate Model', command=self.deactivate_model)
        self.enable(self.master.control_section.set_smooth)

    def deactivate_model(self):
        self.master.cnn_is_activated = False
        self.master.control_section.activate_model_btn.configure(text='Activate Model', command=self.activate_model)
        self.disable(self.master.control_section.set_smooth)
        self.master.control_section.remove_prediction()

    def plot_confusion(self):
        self.cnn.plot_confusion_matrix()

    def plot_accuracy_vs_loss(self):
        self.cnn.plot_loss_and_accuracy()

    def plot_roc_auc(self):
        self.cnn.plot_roc_auc()

    def overview(self):
        self.cnn.overview()

    def summary(self):
        self.cnn.summary()

    def validate_data(self):
        if self.main_is_viewed:
            if self.has_loaded_model:
                self.dataset_lbl.configure(
                    text=f'Dataset: Valid: `{self.label}`, [{(d := int(math.sqrt(len(self.dataset.columns) - 1)))}x{d}].'
                ); return

            if Helper.validate_dataset(self.dataset, self.label, self.master.write):
                self.dataset_lbl.configure(
                    text=f'Dataset: Valid: `{self.label}`, [{(d := int(math.sqrt(len(self.dataset.columns) - 1)))}x{d}].'
                )
                do = self.enable
            else:
                self.dataset_lbl.configure(text='Dataset: Invalid.')
                do = self.disable
            
            do(self.init_btn, self.complexity_sld, self.generator_option, self.test_sld, self.batch_sld)

    def import_model(self):
        instance, model = Helper.get_instance_and_model()
        if instance:
            try:
                cnn = CNN.load(instance, model)
                self.view_main(cnn)
                self.master.update_data_section(cnn.dataset)
                self.master.data_section.disable_labeling()
                self.disable(self.master.data_section.remove_btn)
                self.master.data_section.disable_labeling()
            except:
                self.master.write('Undefined error occurred while loading the model.')

    def setup_model(self, cnn: CNN):
        if cnn is not None:
            self.cnn = cnn
            self.cnn.write = self.master.write
            self.dataset = cnn.dataset
            self.label = cnn.label
            batch = math.ceil(len(cnn.x_test) / cnn.batch_size)
            self.current_batch_lbl.configure(text=f'[{batch}/{batch}]')
    
            self.process_bar.set(1)
            self.process_bar.configure(progress_color='#008000')
            self.current_epoch_lbl.configure(text=f'[{cnn.epochs}/{cnn.epochs}]')
            self.training_accuracy_lbl.configure(text=f'{cnn.stats['Training Accuracy'][-1]*100:.2f}')
            self.training_loss_lbl.configure(text=f'{cnn.stats['Validation Loss'][-1]:.3f}')
            self.validation_accuracy_lbl.configure(text=f'{cnn.stats['Validation Accuracy'][-1]*100:.2f}')
            self.validation_loss_lbl.configure(text=f'{cnn.stats['Validation Loss'][-1]:.3f}')
            self.evaluation_accuracy_lbl.configure(text=f'{cnn.accuracy:.2f}')
            self.evaluation_loss_lbl.configure(text=f'{cnn.loss:.3f}')

            self.complexity_lbl.configure(text=f'{cnn.complexity}')
            self.complexity_sld.set(cnn.complexity)
            
            if cnn.use_generator:
                self.handle_use_generator()

            self.batch_lbl.configure(text=f'{cnn.batch_size}')
            self.batch_sld.set(math.log2(cnn.batch_size))

            self.test_lbl.configure(text=f'{cnn.test_size:.2f}')
            self.test_sld.set(cnn.test_size)

            self.lr_lbl.configure(text=f'{cnn.learning_rate:.4f}')
            self.lr_sld.set(cnn.learning_rate)

            self.epochs_lbl.configure(text=f'{cnn.epochs}')
            self.epochs_sld.set(cnn.epochs)
        
            self.disable(self.complexity_sld, self.generator_option, self.batch_sld, self.test_sld, self.init_btn)
            self.has_loaded_model = True
            self.ready()

    def export_model(self):
        dir = Helper.get_directory(True)
        if dir:
            try:
                self.cnn.save(dir, f'Model-[{Helper.time()}]')
            except Exception as e:
                self.master.write(f'{e.__class__.__name__}')

    def destroy_model(self):
        self.main_frame.destroy()
        self.init_main()
        self.enable(self.import_model_btn)
        self.has_loaded_model = False
        self.master.data_section.remove_dataset()
        self.pre_frame.pack(fill='both', expand=True)

    def handle_use_generator(self):
        self.use_generator = not self.use_generator
        self.generator_option.configure(fg_color='#008B00' if self.use_generator else '#8B0000')

    def enable(self, *wids):
        for wid in wids:
            wid.configure(state=NRM)

    def disable(self, *wids):
        for wid in wids:
            wid.configure(state=DIS)