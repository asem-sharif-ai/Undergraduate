import numpy as np
import customtkinter as ctk

from Utils.GUI.Data import *

def get_user_matrix():
    app = ctk.CTkToplevel()
    app.attributes('-topmost', True)
    app.title('Set Kernel')
    Matrix = None

    def show_matrix_page(_event=None):
        nonlocal Matrix
        try:
            L = int(L_entry.get())
            if not 2 <= L <= 10: raise
        except:
            L_entry.configure(border_color=RED)
        else:
            app.title(f'{L}x{L} Kernel.')
            L_entry.grid_forget()
            L_btn.grid_forget()

            def check_values():
                nonlocal Matrix
                Matrix = np.zeros((L, L))
                all_ok = True
                for i, row in enumerate(entries):
                    for j, entry in enumerate(row):
                        value = entry.get()
                        try:
                            Matrix[i, j] = float(value) if not value == '' else 1
                            entry.configure(border_color=GRN)
                            if not -10 <= Matrix[i, j] <= 10: raise
                        except:
                            entry.configure(border_color=RED)
                            all_ok = False
                if all_ok:
                    app.destroy()

            app.geometry(f'{L*75}x{L*75}')

            for i in range(L):
                app.rowconfigure(index=i, weight=1, uniform=A)
                app.columnconfigure(index=i, weight=1, uniform=A)

            entries = [[] for _ in range(L)]

            for r in range(L):
                for c in range(L):
                    entry = ctk.CTkEntry(app, width=50, height=25, placeholder_text='1')
                    entry.grid(row=r, column=c, padx=5, pady=5)        
                    entries[r].append(entry)
            
            entries[L//2][L//2].configure(border_color=BLU)
            
            app.rowconfigure(index=L, weight=1, uniform=A)
            apply_btn = ctk.CTkButton(app, text='Apply', command=check_values)
            apply_btn.grid(row=L, column=0, columnspan=L, padx=5, pady=5)

    app.geometry(f'{250}x{75}')
    app.resizable(width=False, height=False)
    
    app.rowconfigure(index=0, weight=1, uniform=A)
    app.columnconfigure(index=(0, 1), weight=1, uniform=A)

    L_entry = ctk.CTkEntry(app, placeholder_text='Kernel Size `L`')
    L_entry.grid(row=0, column=0, padx=(20, 10), pady=5)
    L_entry.bind('<Return>', show_matrix_page)

    L_btn = ctk.CTkButton(app, text='OK', command=show_matrix_page)
    L_btn.grid(row=0, column=1, padx=(10, 20), pady=(0, 0))

    app.wait_window(app)
    return (Matrix if Matrix is not None else np.ones((3, 3)))


def get_structering_element():
    app = ctk.CTkToplevel()
    app.attributes('-topmost', True)
    app.title('Set Structing Element')
    Matrix = None

    def show_matrix_page(_event=None):
        nonlocal Matrix
        try:
            rows = int(rows_entry.get())
            cols = int(cols_entry.get())
            if not (2 <= rows <= 20 and 2 <= cols <= 20):
                raise
        except:
            rows_entry.configure(border_color=RED)
            cols_entry.configure(border_color=RED)
        else:
            app.title(f'{rows}x{cols} Structing Element.')
            for i in [rows_entry, cols_entry, L_btn]:
                i.grid_forget()

            def check_values():
                nonlocal Matrix
                Matrix = np.zeros((rows, cols), dtype=int)
                for i, row in enumerate(checks):
                    for j, var in enumerate(row):
                        Matrix[i, j] = var.get()
                app.destroy()

            app.geometry(f'{cols*75}x{rows*75}')

            for i in range(rows):
                app.rowconfigure(index=i, weight=1, uniform=A)
            for j in range(cols):
                app.columnconfigure(index=j, weight=1, uniform=A)

            checks = [[] for _ in range(rows)]

            for r in range(rows):
                for c in range(cols):
                    var = ctk.IntVar()
                    checkbox = ctk.CTkCheckBox(app, variable=var, text='')
                    checkbox.grid(row=r, column=c, padx=(25, 0), pady=5)
                    checks[r].append(var)

            app.rowconfigure(index=rows, weight=1, uniform=A)
            apply_btn = ctk.CTkButton(app, text='Apply', command=check_values)
            apply_btn.grid(row=rows, column=0, columnspan=cols, padx=5, pady=5)

    app.geometry(f'{350}x{100}')
    app.resizable(width=False, height=False)
    
    app.rowconfigure(index=0, weight=1, uniform=A)
    app.columnconfigure(index=(0, 1, 2), weight=1, uniform=A)

    rows_entry = ctk.CTkEntry(app, placeholder_text='Rows')
    rows_entry.grid(row=0, column=0, padx=(20, 10), pady=5)

    cols_entry = ctk.CTkEntry(app, placeholder_text='Columns')
    cols_entry.grid(row=0, column=1, padx=(10, 10), pady=5)

    L_btn = ctk.CTkButton(app, text='OK', command=show_matrix_page)
    L_btn.grid(row=0, column=2, padx=(10, 20), pady=(0, 0))

    app.wait_window(app)
    return Matrix