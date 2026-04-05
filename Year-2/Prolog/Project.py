import customtkinter as ctk
from pyswip import Prolog

PATH = r'Project.pl'

MAP = '''
                  .     .                          .                    .      -> UnReachable
a  b  c  d  e  f  g  h  i  j  k  l  m  n  o  p  q  r  s  t  u  v  w  x  y  z
└──┴──┴──┴──┴──┘           └──┴──┴──┴──┴──┘           └──┴──┴──┴──┴──┘         -> Car
            └────────┴────────┴────────┴────────┴────────┘                     -> Train
└──────────────┴──────────────┴──────────────┴──────────────┴──────────────┘   -> Plane
''' [1:-1]

DEFAULTS = {
    'B': {
        'fg_color': '#8B0000',
        'hover_color':'#008000'
    }, 
    'E': {
        'fg_color': '#101010',
        'border_color': '#303030',
        'border_width': 1,
    }, 
    'T': {
       'fg_color': '#101010',
       'border_color': '#303030',
       'border_width': 1,
       'scrollbar_button_color': '#101010',
       'scrollbar_button_hover_color': '#050505',
       'state': 'disabled',
       'font': ('Courier', 15),
       'wrap': 'none',
       'activate_scrollbars': True
    }, 
    'P': {
        'progress_color': '#8B0000',
        'orientation': 'vertical',
        'mode': 'indeterminate',
        'fg_color': 'black',
        'width': 6,
    }
}

class Database(Prolog):
    def __init__(self, path: str=PATH):
        super().__init__()
        self.consult(path)

    def can_travel(self, _from, _to, _by):
        if _by is None:
            output = list(self.query(f'travel({_from}, {_to}).'))
            return f'Travel from `{_from}` to `{_to}`: ' + ('True.\n' if output else 'False.\n')
        else:
            output = list(self.query(f'travel({_from}, {_to}, {_by}).'))
            return f'Travel from `{_from}` to `{_to}` by `{_by}`: ' + ('True.\n' if output else 'False.\n')

    def get_path(self, _from, _to):
        output = list(self.query(f'path({_from}, {_to}, P).'))
        if output:
            paths = f'Paths From `{_from}` to `{_to}`: \n'
            for i, path in enumerate(output):
                for _, steps in path.items():
                    paths += f'   [{i+1}] ' + ', '.join(steps) + '.\n'
            return paths
        else:
            return f'No path found from `{_from}` to `{_to}`.\n'

class App(ctk.CTk):
    def __init__(self):
        super().__init__(fg_color='black')
        self.database = Database()
        
        self.title('Project: Planning a Travel Journey.')
        self.geometry(f'{600}x{400}')
        self.resizable(False, False)
        
        self.rowconfigure(index=0, weight=5, uniform='a')
        self.rowconfigure(index=3, weight=7, uniform='a')
        self.rowconfigure(index=(1, 2), weight=2, uniform='a')
        self.columnconfigure(index=(0, 1, 2, 3), weight=1, uniform='a')

        self.guide_map = ctk.CTkTextbox(self, **DEFAULTS['T'])
        self.guide_map.grid(row=0, column=0, columnspan=4, padx=10, pady=(10, 5), sticky='nsew')
        self.write(self.guide_map, MAP)
        
        self.from_entry = ctk.CTkEntry(self, placeholder_text='From', **DEFAULTS['E'])
        self.from_entry.grid(row=1, column=0, padx=(15, 5), pady=(10, 5), sticky='ew')

        self.to_entry = ctk.CTkEntry(self, placeholder_text='To', **DEFAULTS['E'])
        self.to_entry.grid(row=1, column=1, padx=(5, 15), pady=(10, 5), sticky='ew')

        self.by_entry = ctk.CTkEntry(self, placeholder_text='By  (Optional)', **DEFAULTS['E'])
        self.by_entry.grid(row=2, column=0, padx=(15, 5), pady=(5, 10), sticky='ew')
        
        self.show_database_btn = ctk.CTkButton(self, text='Database', command=self.show_database, **DEFAULTS['B'])
        self.show_database_btn.grid(row=2, column=1, padx=(5, 15), pady=(5, 10), sticky='ew')

        self.can_travel_btn = ctk.CTkButton(self, text='Can Travel', command=self.can_travel, **DEFAULTS['B'])
        self.can_travel_btn.grid(row=1, column=2, padx=(15, 5), pady=(10, 5), sticky='ew')

        self.get_path_btn = ctk.CTkButton(self, text='Get Path', command=self.get_path, **DEFAULTS['B'])
        self.get_path_btn.grid(row=1, column=3, padx=(5, 15), pady=(10, 5), sticky='ew')

        self.query_entry = ctk.CTkEntry(self, placeholder_text='Query', **DEFAULTS['E'])
        self.query_entry.grid(row=2, column=2, padx=(15, 5), pady=(5, 10), sticky='ew')
        self.query_entry.bind('<Return>', lambda _: self.execute_query())

        self.execute_btn = ctk.CTkButton(self, text='Execute Query', command=self.execute_query, **DEFAULTS['B'])
        self.execute_btn.grid(row=2, column=3, padx=(5, 15), pady=(5, 10), sticky='ew')
        
        self.output_box = ctk.CTkTextbox(self, **DEFAULTS['T'])
        self.output_box.grid(row=3, column=0, columnspan=4, padx=10, pady=(5, 10), sticky='nsew')

        for idx in (1, 2):
            x = ctk.CTkProgressBar(self, **DEFAULTS['P'])
            x.grid(row=idx, column=1, columnspan=2, pady=[(15, 0), (0, 15)][idx-1])
            x.start()

        self.mainloop()

    def can_travel(self):
        _from, _to, _by = self.from_entry.get(), self.to_entry.get(), self.by_entry.get()
        if _from and _to:
            self.write(self.output_box, self.database.can_travel(_from, _to, _by if _by else None))
        else:
            self.write(self.output_box, 'You must determine \'From\' and \'To\' at least.')

    def get_path(self):
        _from, _to = self.from_entry.get(), self.to_entry.get()
        if _from and _to:
            self.write(self.output_box, self.database.get_path(_from, _to))
        else:
            self.write(self.output_box, 'You must determine \'From\' and \'To\' of the path.')

    def execute_query(self):
        _query = self.query_entry.get()
        if _query:
            try:
                self.write(self.output_box, list(self.database.query(_query)))
            except Exception as e:
                self.write(self.output_box, e)

    def show_database(self, path=PATH):
        window = ctk.CTkToplevel(fg_color='black')
        window.attributes("-topmost", True)
        window.title('Project Database.')
        window.geometry(f'{300}x{400}')
        window.resizable(False, False)

        textbox = ctk.CTkTextbox(window, **DEFAULTS['T'])
        textbox.pack(padx=10, pady=10, fill='both', expand=True)
        try:
            with open(path, 'r') as file:
                self.write(textbox, file.read())
        except:
            textbox.insert('0.0', f'File `{path}` was not found or an error occurred.')

    def write(self, textbox, text):
        textbox.configure(state='normal')
        textbox.delete(0.0, 'end')
        textbox.insert('end', text)
        textbox.configure(state='disabled')

App()