import customtkinter as ctk

from Calculator import *

# Global Fonts
FONT = ('Segoe UI', 13, 'bold')
SEMI = ('Segoe UI', 16, 'bold')
BOLD = ('Segoe UI', 19, 'bold')

# Default App Data
DAD = {'fg_color':'#202020'}

# Default Frame Data
DFD = {'fg_color':'#101010'}

# Output Frame Data
OFD = {'fg_color':'#202020'}

# Default Scrollable Frame Data
DSFD = {
    'fg_color':'#101010', 
    'scrollbar_fg_color':'#101010', 
    'scrollbar_button_color':'#202020', 
    'scrollbar_button_hover_color':'#303030'
}

# Output Scrollable Frame Data
OSFD = {
    'fg_color':'#202020', 
    'scrollbar_fg_color':'#202020', 
    'scrollbar_button_color':'#303030', 
    'scrollbar_button_hover_color':'#404040'
}

# Default Entry Data
DED = {
    'fg_color':'#252525',
    'border_color':'#505050',
    'border_width':2,
    'text_color':'#EEEEEE',
    'placeholder_text_color':'#858585',
    'font':FONT,
}

# Special Entry Data
SED = {
    'fg_color':'#252525',
    'border_color':'#505050',
    'border_width':2,
    'text_color':'#EEEEEE',
    'placeholder_text_color':'#858585',
    'font':('Consolas', 13, 'bold'),
}

# Default Button Data
DBD = {
    'fg_color':'#004080',
    'hover_color':'#002040',
    'text_color':'#EEEEEE',
    'font':FONT,
}

# Cancel Button Data
CBD = {
    'text':'❌',
    'fg_color':'#800000',
    'hover_color':'#400000',
    'text_color':'#EEEEEE',
    'font':FONT,
}

# Special Button Data
SBD = {
    'fg_color':'#008020',
    'hover_color':'#005010',
    'text_color':'#EEEEEE',
    'font':FONT,
}

class LockableEntry(ctk.CTkEntry):
    def __init__(self, master, init_value='', **kwargs):
        super().__init__(master, **kwargs)
        self.init_value = init_value
        self.insert(0, self.init_value)
        self.bind('<Key>', self._block_prefix)
        self.bind('<Button-1>', self._cursor_after_prefix)
        self.bind('<KeyRelease>', self._restore_prefix)

    def _block_prefix(self, event):
        if self.index('insert') < len(self.init_value):
            self.icursor(len(self.init_value))
        if event.keysym in ('BackSpace', 'Delete') and self.index('insert') <= len(self.init_value):
            return 'break'

    def _cursor_after_prefix(self, event):
        if self.index('insert') < len(self.init_value):
            self.icursor(len(self.init_value))

    def _restore_prefix(self, event):
        if not self.get().startswith(self.init_value):
            user_part = self.get_value()
            self.delete(0, 'end')
            self.insert(0, self.init_value + user_part)
            self.icursor(len(self.init_value))

    def get_value(self):
        return self.get()[len(self.init_value):]

    def set_value(self, value):
        self.delete(len(self.init_value), 'end')
        self.insert('end', value)

class OutputFrame(ctk.CTkFrame):
    def __init__(self, master, subjects, terms):
        super().__init__(master, **DFD)
        
        self.subjects = subjects
        self.terms = terms
        
        self.rowconfigure(index=0, weight=3, uniform='a')
        self.rowconfigure(index=1, weight=2, uniform='a')
        self.columnconfigure(index=0, weight=3, uniform='a')
        self.columnconfigure(index=1, weight=2, uniform='a')
        
        self.bars_frame = ctk.CTkScrollableFrame(self, orientation='horizontal', **OSFD)
        self.bars_frame.grid(row=0, column=0, columnspan=2, padx=10, pady=(10, 5), sticky='nsew')
        
        self.result_frame = ctk.CTkFrame(self, **OFD)
        self.result_frame.grid(row=1, column=0, padx=(10, 5), pady=(5, 10), sticky='nsew')
        
        self.desire_frame = ctk.CTkFrame(self, **OFD)
        self.desire_frame.grid(row=1, column=1, padx=(5, 10), pady=(5, 10), sticky='nsew')
        
        self.after(50, self.build)
        self.after(50, self.calculate)
        self.after(50, self.required_for_desired)

    def build(self):
        #* self.subjects is None or list[dict[keys:'Subject', 'Hours', 'Grade', 'Max Grade'], ...]
        #* self.terms is None or list[dict[keys:'Term', 'Hours', 'GPA'], ...]

        self.bars_frame.rowconfigure(index=(0, 2, 3), weight=1, uniform='a')
        self.bars_frame.rowconfigure(index=1, weight=3, uniform='a')
        current_idx = 1
        
        if self.subjects is not None:
            current_idx = len(self.subjects)

            for i in range(len(self.subjects)):
                self.bars_frame.columnconfigure(index=i, weight=1, uniform='a')
                
                value = self.subjects[i]['Grade'] / self.subjects[i]['Max Grade']

                label_1 = ctk.CTkLabel(self.bars_frame, text=f'{self.subjects[i]['Subject']}', font=FONT)
                label_1.grid(row=0, column=i, padx=15, pady=5)

                bar = ctk.CTkProgressBar(self.bars_frame, orientation='vertical', progress_color=colorize(value))
                bar.grid(row=1, column=i, padx=15, pady=5, sticky='ns')
                
                label_3 = ctk.CTkLabel(self.bars_frame, text=f'{value*100:.1f}%', font=FONT)
                label_3.grid(row=2, column=i, padx=15, pady=5)
                
                label_2 = ctk.CTkLabel(self.bars_frame, text=f'{classify(value)}', font=FONT)
                label_2.grid(row=3, column=i, padx=15, pady=5)
                
                OutputFrame.animate_bar(bar, value, grade_label=label_2, percent_label=label_3)
        else:
            label = ctk.CTkLabel(self.bars_frame, text='No Subjects', font=FONT)
            label.grid(row=0, column=0, padx=15, rowspan=4)
        
        sep = ctk.CTkProgressBar(self.bars_frame, orientation='vertical', progress_color='#101010')
        sep.set(1)
        sep.grid(row=0, column=current_idx, rowspan=4, padx=15, pady=5, sticky='ns')

        if self.terms is not None:
            for i in range(len(self.terms)):
                self.bars_frame.columnconfigure(index=current_idx+1+i, weight=1, uniform='a')

                value = self.terms[i]['GPA'] / 4
                
                label_1 = ctk.CTkLabel(self.bars_frame, text=f'{self.terms[i]['Term']}', font=FONT)
                label_1.grid(row=0, column=current_idx+1+i, padx=15, pady=5)
                
                bar = ctk.CTkProgressBar(self.bars_frame, orientation='vertical', progress_color=colorize(value))
                bar.grid(row=1, column=current_idx+1+i, padx=15, pady=5, sticky='ns')
                
                label_3 = ctk.CTkLabel(self.bars_frame, text=f'{self.terms[i]['GPA']:.2f}', font=FONT)
                label_3.grid(row=2, column=current_idx+1+i, padx=15, pady=5)
                
                label_2 = ctk.CTkLabel(self.bars_frame, text=f'{classify(value)}', font=FONT)
                label_2.grid(row=3, column=current_idx+1+i, padx=15, pady=5)

                OutputFrame.animate_bar(bar, value, grade_label=label_2, percent_label=label_3)
        else:
            label = ctk.CTkLabel(self.bars_frame, text='No Terms', font=FONT)
            label.grid(row=0, column=current_idx+1, padx=15, rowspan=4)

    def calculate(self):
        if self.subjects is not None:
            self.gpa, self.hours = GPA.calculate( # list[tuple[int, float, float]] = (Hours, Grade, Max_Grade)
                grades=[(sub['Hours'], sub['Grade'], sub['Max Grade']) for sub in self.subjects],
                return_hours=True
            )
            if self.terms is not None:
                self.gpa = GPA.update( # list[tuple[float, int] = (GPA, Hours)
                    (self.gpa, self.hours), *[(term['GPA'], term['Hours']) for term in self.terms]
                )
                self.hours += sum(term['Hours'] for term in self.terms)
        else:
            if self.terms is not None:
                self.gpa = GPA.update(
                    *[(term['GPA'], term['Hours']) for term in self.terms]
                )
                self.hours = sum(term['Hours'] for term in self.terms)

        self.result_frame.rowconfigure(index=0, weight=3, uniform='a')
        self.result_frame.rowconfigure(index=1, weight=2, uniform='a')
        self.result_frame.columnconfigure(index=0, weight=3, uniform='a')
        self.result_frame.columnconfigure(index=(1, 2, 3), weight=2, uniform='a')

        value = self.gpa / 4

        label_1 = ctk.CTkLabel(self.result_frame, text=f'Overall GPA:', font=BOLD)
        label_1.grid(row=0, column=0, padx=(15, 0), pady=(30, 10), sticky='nsw')

        label_2 = ctk.CTkLabel(self.result_frame, text=f'{self.gpa:.2f}/4.00', font=BOLD)
        label_2.grid(row=0, column=1, padx=7.5, pady=(30, 10), sticky='nsew')

        label_3 = ctk.CTkLabel(self.result_frame, text=f'{value*100:.02f}%', font=BOLD)
        label_3.grid(row=0, column=2, padx=7.5, pady=(30, 10), sticky='nsew')

        label_4 = ctk.CTkLabel(self.result_frame, text=f'{classify(value)}', font=BOLD)
        label_4.grid(row=0, column=3, padx=(0, 15), pady=(30, 10), sticky='ns')

        bar = ctk.CTkProgressBar(self.result_frame, progress_color=colorize(value))
        bar.grid(row=1, column=0, columnspan=4, padx=15, pady=(0, 30), sticky='ew')
        bar.set(value)

        self.animate_gpa(bar=bar, gpa=self.gpa, label_gpa=label_2, label_percent=label_3, label_grade=label_4)

    def required_for_desired(self):
        self.desire_frame.rowconfigure(index=(0, 1, 2), weight=1, uniform='a')
        self.desire_frame.columnconfigure(index=0, weight=14, uniform='a')
        self.desire_frame.columnconfigure(index=1, weight=1, uniform='a')

        self.des_ent = LockableEntry(self.desire_frame, init_value='Desired GPA:   ', **SED)
        self.des_ent.grid(row=0, column=0, padx=10, pady=(10, 0), sticky='ew')

        self.hours_ent = LockableEntry(self.desire_frame, init_value='Within Hours:  ', **SED)
        self.hours_ent.grid(row=1, column=0, padx=10, pady=5, sticky='ew')
        
        self.req_ent = LockableEntry(self.desire_frame, init_value='Required GPA:  ', **SED)
        self.req_ent.grid(row=2, column=0, padx=10, pady=(0, 10), sticky='ew')
        
        self.bar = ctk.CTkProgressBar(self.desire_frame, orientation='vertical', progress_color=colorize(0))
        self.bar.grid(row=0, column=1, rowspan=3, padx=(0, 10), pady=10, sticky='nse')
        self.bar.set(0)

        self.des_ent.bind('<KeyRelease>', lambda event: self.find_required())
        self.hours_ent.bind('<KeyRelease>', lambda event: self.find_required())
        self.req_ent.configure(state='disabled')

    def find_required(self):
        ok = True
        try:
            desired = self.des_ent.get_value()
            if desired:
                if float(desired) > 4.0:
                    raise
            else:
                self.des_ent.configure(border_color=DED['border_color'])
                    
        except:
            self.des_ent.configure(border_color='#AA0000')
            ok = False
        else:
            if desired:
                self.des_ent.configure(border_color='#00AA00')

        try:
            hours = self.hours_ent.get_value()
            if hours:
                if int(hours) <= 0:
                    raise
            else:
                self.hours_ent.configure(border_color=DED['border_color'])
        except:
            self.hours_ent.configure(border_color='#AA0000')
            ok = False
        else:
            if hours:
                self.hours_ent.configure(border_color='#00AA00')

        if '' in (desired, hours):
            self.req_ent.configure(state='normal')
            self.req_ent.set_value('')
            self.req_ent.configure(border_color=DED['border_color'])
            OutputFrame.reverse_gpa(self.bar, 0)
            self.req_ent.configure(state='disabled')
            return

        if ok:
            required = GPA.required_for_desired(
                current_gpa=self.gpa,
                spent_hours=self.hours,
                desired_gpa=float(desired),
                within_hours=int(hours)
            )

            self.req_ent.configure(state='normal')
            if required <= 4 and required >= 0:
                self.req_ent.set_value(f'{required}')
                self.req_ent.configure(border_color=colorize(required/4))
                OutputFrame.animate_gpa(self.bar, required, step=0.04, delay=5)
            else:
                self.req_ent.set_value('Unachievable')
                self.req_ent.configure(border_color=colorize(0))
                OutputFrame.reverse_gpa(self.bar, 0)
            self.req_ent.configure(state='disabled')

    @staticmethod
    def animate_bar(bar, target_value, grade_label=None, percent_label=None, step=0.03, delay=15):
        def update(val=0.0):
            if val >= target_value:
                bar.set(target_value)
                if grade_label:
                    grade_label.configure(text=classify(target_value))
                if percent_label:
                    percent_label.configure(text=f'{target_value*100:.1f}%')
                return

            bar.set(val)
            bar.configure(progress_color=colorize(val))
            if grade_label:
                grade_label.configure(text=classify(val))
            if percent_label:
                percent_label.configure(text=f'{val*100:.1f}%')
            bar.after(delay, update, val + step)
            
        update()

    @staticmethod
    def animate_gpa(bar, gpa, label_gpa=None, label_percent=None, label_grade=None, step=0.03, delay=15):
        target_value = gpa / 4

        def update(val=0.0):
            if val >= target_value:
                bar.set(target_value)
                bar.configure(progress_color=colorize(target_value))
                if label_gpa:
                    label_gpa.configure(text=f'{gpa:.2f}/4.00')
                if label_percent:
                    label_percent.configure(text=f'{target_value * 100:.1f}%')
                if label_grade:
                    label_grade.configure(text=classify(target_value))
                return

            bar.set(val)
            bar.configure(progress_color=colorize(val))
            if label_gpa:
                label_gpa.configure(text=f'{val * 4:.2f}/4.00')
            if label_percent:
                label_percent.configure(text=f'{val * 100:.2f}%')
            if label_grade:
                label_grade.configure(text=classify(val))

            bar.after(delay, update, val + step)

        update()

    @staticmethod
    def reverse_gpa(bar, to_value, step=0.04, delay=10):
        current = bar._determinate_value
        
        def update(val=current):
            if val <= to_value:
                bar.set(to_value)
                bar.configure(progress_color=colorize(to_value))
                return

            bar.set(val)
            bar.configure(progress_color=colorize(val))
            bar.after(delay, update, val - step)

        update()
