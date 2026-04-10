import json
import datetime
import tkinter as tk
import customtkinter as ctk

from Widgets import *

ctk.set_appearance_mode('System')
ctk.set_default_color_theme('blue')

class App(ctk.CTk):
    def __init__(self):
        super().__init__(**DAD)
        self.title('MUFAI GPA Calculator - By Asem Sharif')
        self.geometry(f'{800}x{400}')
        self.resizable(False, False)

        self.subjects = []
        self.terms = []

        self.rowconfigure(index=0, weight=6, uniform='a')
        self.rowconfigure(index=1, weight=1, uniform='a')
        self.columnconfigure(index=0, weight=3, uniform='a')
        self.columnconfigure(index=1, weight=2, uniform='a')

        self.subjects_frame = ctk.CTkScrollableFrame(self, **DSFD)
        self.subjects_frame.grid(row=0, column=0, padx=(10, 5), pady=10, sticky='nsew')

        self.add_sub_btn = ctk.CTkButton(self.subjects_frame, text='➕ Add Subject', command=self.add_subject, **DBD)
        self.add_sub_btn.pack(pady=10)

        self.terms_frame = ctk.CTkScrollableFrame(self, **DSFD)
        self.terms_frame.grid(row=0, column=1, padx=(5, 10), pady=10, sticky='nsew')

        self.add_term_btn = ctk.CTkButton(self.terms_frame, text='➕ Add Term', command=self.add_term, **DBD)
        self.add_term_btn.pack(pady=10)

        self.btns_frame = ctk.CTkFrame(self, **DFD)
        self.btns_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=(0, 10), sticky='nsew')
        
        self.btns_frame.rowconfigure(index=0, weight=1, uniform='a')
        self.btns_frame.columnconfigure(index=(0, 1, 2, 3), weight=1, uniform='a')

        self.load_btn = ctk.CTkButton(self.btns_frame, text='📂 Load', command=self.load_data, **DBD)
        self.load_btn.grid(row=0, column=0)

        self.save_btn = ctk.CTkButton(self.btns_frame, text='💾 Save', command=self.save_date, **DBD)
        self.save_btn.grid(row=0, column=1)

        self.reset_btn = ctk.CTkButton(self.btns_frame, text='⛔️ Reset', command=self.reset_data, **DBD)
        self.reset_btn.grid(row=0, column=2)

        self.calc_btn = ctk.CTkButton(self.btns_frame, text='Σ Calculate', command=self.calculate, **SBD)
        self.calc_btn.grid(row=0, column=3)

        self.add_subject('disabled'); self.add_subject()
        self.add_term('disabled'); self.add_term()

    def add_subject(self, state='normal'):
        frame = ctk.CTkFrame(self.subjects_frame, **DFD)
        frame.rowconfigure(index=0, weight=1, uniform='a')
        frame.columnconfigure(index=(0, 1, 2, 3), weight=2, uniform='a')
        frame.columnconfigure(index=4, weight=1, uniform='a')
        
        sub_idx = len(self.subjects)
        widgets = {'Frame': frame}

        for index, label in enumerate(['Subject', 'Hours', 'Grade', 'Max Grade']):
            ent = ctk.CTkEntry(frame, placeholder_text=label, **DED)
            ent.grid(row=0, column=index, padx=(10, 0), sticky='nsew')
            ent.bind('<KeyRelease>', lambda event, i=sub_idx, l=label:self.bind_subjects(i, l))
            widgets[label] = ent
            
            if state != 'normal':
                ent.insert(0, label)
                ent.configure(state=state, text_color=DED['placeholder_text_color'])
            else:
                if index == 3:
                    ent.insert(0, '100')

        if state == 'normal':
            del_btn = ctk.CTkButton(frame, state=state, command=lambda idx=sub_idx: self.subjects[idx]['Frame'].destroy(), **CBD)
            del_btn.grid(row=0, column=4, padx=(10, 0), sticky='nsew')
            self.subjects.append(widgets)

        frame.pack(before=self.add_sub_btn, padx=(0, 10), pady=(10, 5), expand=True, fill='both')

        return widgets

    def bind_subjects(self, idx, key):
        if key == 'Hours':
            entry = self.subjects[idx][key]
            try:
                if int(entry.get()) < 1 or int(entry.get()) > 99:
                    raise
            except:
                entry.configure(border_color='#AA0000')
                self.subjects[idx]['State'] = False
            else:
                entry.configure(border_color='#00AA00')
                self.subjects[idx]['State'] = True

        elif key in ['Grade', 'Max Grade']:
            entry_1 = self.subjects[idx]['Grade']
            entry_2 = self.subjects[idx]['Max Grade']
            try:
                if float(entry_1.get()) > float(entry_2.get()):
                    raise
            except:
                entry_1.configure(border_color='#AA0000')
                entry_2.configure(border_color='#AA0000')
                self.subjects[idx]['State'] = False
            else:
                entry_1.configure(border_color='#00AA00')
                entry_2.configure(border_color='#00AA00')
                self.subjects[idx]['State'] = True

    def add_term(self, state='normal'):
        frame = ctk.CTkFrame(self.terms_frame, **DFD)
        frame.rowconfigure(index=0, weight=1, uniform='a')
        frame.columnconfigure(index=(0, 1, 2), weight=3, uniform='a')
        frame.columnconfigure(index=3, weight=2, uniform='a')

        term_idx = len(self.terms)
        widgets = {'Frame': frame}

        for index, label in enumerate(['Term', 'Hours', 'GPA']):
            ent = ctk.CTkEntry(frame, placeholder_text=label, **DED)
            ent.grid(row=0, column=index, padx=(10, 0), sticky='nsew')
            ent.bind('<KeyRelease>', lambda event, i=term_idx, l=label:self.bind_terms(i, l))
            widgets[label] = ent
            
            if state != 'normal':
                ent.insert(0, label)
                ent.configure(state=state, text_color=DED['placeholder_text_color'])
            
        if state == 'normal':
            self.terms.append(widgets)
            del_btn = ctk.CTkButton(frame, state=state, command=lambda idx=term_idx: self.terms[idx]['Frame'].destroy(), **CBD)
            del_btn.grid(row=0, column=3, padx=(10, 0), sticky='nsew')

        frame.pack(before=self.add_term_btn, padx=(0, 10), pady=(10, 5), expand=True, fill='both')

        return widgets

    def bind_terms(self, idx, key):
        entry = self.terms[idx][key]
        
        if key == 'Hours':
            try:
                if int(entry.get()) < 1 or int(entry.get()) > 999:
                    raise
            except:
                entry.configure(border_color='#AA0000')
                self.terms[idx]['State'] = False
            else:
                entry.configure(border_color='#00AA00')
                self.terms[idx]['State'] = True

        elif key == 'GPA':
            try:
                if float(entry.get()) > 4.0:
                    raise
            except:
                entry.configure(border_color='#AA0000')
                self.terms[idx]['State'] = False
            else:
                entry.configure(border_color='#00AA00')
                self.terms[idx]['State'] = True

    def load_data(self):
        file_path = tk.filedialog.askopenfilename(
            filetypes=[('JSON Files', '*.json')],
            title='Open Data File'
        )
        if file_path:
            self.reset_data(False)
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            subjects_data, terms_data = data.get('Subjects', []), data.get('Terms', [])

            for item in subjects_data:
                sub = self.add_subject()
                sub['Subject'].insert(0, item.get('Subject', ''))
                sub['Hours'].insert(0, item.get('Hours', ''))
                sub['Grade'].insert(0, item.get('Grade', ''))
                sub['Max Grade'].delete(0, tk.END)
                sub['Max Grade'].insert(0, item.get('Max Grade', ''))

            for item in terms_data:
                term = self.add_term()
                term['Term'].insert(0, item.get('Term', ''))
                term['Hours'].insert(0, item.get('Hours', ''))
                term['GPA'].insert(0, item.get('GPA', ''))
            
            self.after(100, self.read_data)

    def save_date(self):
        subjects_data, terms_data = self.read_data()
        if subjects_data or terms_data:
            file_path = tk.filedialog.asksaveasfilename(
                initialfile=f'Data-[{datetime.datetime.now().strftime('%d.%m.%y-%H.%M')}]',
                defaultextension='.json',
                filetypes=[('JSON Files', '*.json')],
                title='Save Data As'
            )
            if file_path:
                data = {**({'Subjects': subjects_data} if subjects_data else {}), **({'Terms': terms_data} if terms_data else {})}
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=4)

    def reset_data(self, add_one=True):
        for sub in self.subjects:
            sub['Frame'].destroy()
        for term in self.terms:
            term['Frame'].destroy()
        self.subjects = []
        self.terms = []
        
        if add_one:
            self.add_subject()
            self.add_term()

    def read_data(self):
        output = [False, False]

    #! ----- ----- Validate Subjects ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
        subjects = [sub for sub in self.subjects if sub['Frame'].winfo_exists()]

        if subjects:
            for idx, sub in enumerate(subjects):
                if sub['Subject'].get() == '':
                    sub['Subject'].insert(0, f'Subject {idx+1}')

                for lbl in ['Hours', 'Grade', 'Max Grade']:
                    sub[lbl].focus_set()
                    sub[lbl].event_generate('<KeyRelease>')
            else:
                self.focus_set()

            subjects_state = [sub['State'] for sub in subjects]
            if bool(subjects_state) and all(subjects_state):
                output[0] = [{
                    'Subject': sub['Subject'].get(),
                    'Hours': int(sub['Hours'].get()),
                    'Grade': float(sub['Grade'].get()),
                    'Max Grade': float(sub['Max Grade'].get()),
                    } for sub in subjects]
            
        else:
            output[0] = None

    #! ----- ----- Validate Terms ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
        terms = [term for term in self.terms if term['Frame'].winfo_exists()]
        
        if terms:
            for idx, term in enumerate(terms):
                if term['Term'].get() == '':
                    term['Term'].insert(0, f'Term {idx+1}')
                
                for lbl in ['Hours', 'GPA']:
                    term[lbl].focus_set()
                    term[lbl].event_generate('<KeyRelease>')
            else:
                self.focus_set()

            terms_state = [term['State'] for term in terms]
            if bool(terms_state) and all(terms_state):
                output[1] = [{
                    'Term': term['Term'].get(),
                    'Hours': int(term['Hours'].get()),
                    'GPA': float(term['GPA'].get()),
                    } for term in terms]
        else:
            output[1] = None

        return output

    def calculate(self):
        subjects_data, terms_data = self.read_data()
        if False not in [subjects_data, terms_data]: # UI is ready, either subjests, terms, or both are givin
            self.subjects_frame.grid_forget()
            self.terms_frame.grid_forget()

            self.output_frame = OutputFrame(self, subjects_data, terms_data)
            self.output_frame.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky='nsew')

            self.calc_btn.configure(text='⬅ Back', command=self.back)
            for btn in (self.load_btn, self.save_btn, self.reset_btn):
                btn.configure(state='disabled')

    def back(self):
        self.output_frame.destroy()
        self.output_frame = None

        self.subjects_frame.grid(row=0, column=0, padx=(10, 5), pady=10, sticky='nsew')
        self.terms_frame.grid(row=0, column=1, padx=(5, 10), pady=10, sticky='nsew')

        self.calc_btn.configure(text='Calculate', command=self.calculate)
        for btn in (self.load_btn, self.save_btn, self.reset_btn):
            btn.configure(state='normal')

    @staticmethod
    def run():
        app = App()
        app.mainloop()
