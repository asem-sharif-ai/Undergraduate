# pip install numpy customtkinter

import numpy as np
import customtkinter as ctk

from time import sleep
from threading import Thread

NRM, DIS = ('normal', 'disabled')
A, X, Y, XY = ('A', 'ew', 'ns', 'nsew')

C0, C1, C2, C3, C4, C5 = (
    '#101010',
    '#1A1A1A',
    "#E6E6E6",
    '#004030',
    "#62897B",
    '#D4A019',
)

class App(ctk.CTk):
    def __init__(self):
        super().__init__(fg_color=C0)

        self.title('Algorithms Visualization')

        self.get_data()
        self.mainloop()

    def get_data(self):
        self.geometry(f'{400}x{125}')
        self.resizable(False, False)
        
        self.pre_screen_frame = ctk.CTkFrame(self, fg_color=C0)
        self.pre_screen_frame.pack(fill='both', expand=True)
        
        self.pre_screen_frame.rowconfigure(index=(0, 1), weight=1, uniform=A)
        self.pre_screen_frame.columnconfigure(index=(0, 1), weight=1, uniform=A)
        
        self.data_type_btn = ctk.CTkSegmentedButton(self.pre_screen_frame,
                                                    fg_color=C0,
                                                    selected_color=C3, 
                                                    unselected_color=C1, 
                                                    selected_hover_color=C4, 
                                                    unselected_hover_color=C4,
                                                    values=['Range', 'Random'],
                                                    height=35,
            )

        self.data_type_btn.grid(row=0, column=0, padx=(20, 10), pady=(10, 0), sticky=X)
        self.data_type_btn.set('Range')

        self.size_slider = ctk.CTkSlider(self.pre_screen_frame,
                                         from_=10, to=90,
                                         progress_color=C3,
                                         fg_color=C1,
                                         button_color=C3,
                                         button_hover_color=C4
                                         )
        
        self.size_slider.grid(row=0, column=1, padx=(10, 20), pady=(10, 0), sticky=X)
        self.size_slider.set(50)

        self.start_btn = ctk.CTkButton(self.pre_screen_frame, text='Start', fg_color=C3, hover_color=C4, command=self.start)
        self.start_btn.grid(row=1, column=0, columnspan=2, padx=20, pady=(0, 10), sticky=X)

    def start(self):
        size = round(self.size_slider.get())
        if self.data_type_btn.get() == 'Range':
            self.data = list(range(0, 251, 250 // size))
        else:
            self.data = [i for i in np.random.choice(list(range(0, 251, 1)), size=size, replace=False)]

        self.n = len(self.data)
        self.range = list(range(self.n))
        self.min, self.max = np.min(self.data), np.max(self.data)
        self.scale = lambda x: 0.05 + ((x - self.min) / (self.max - self.min)) * 0.9
        self.unscale = lambda y: self.min + ((y - 0.05) / 0.9) * (self.max - self.min)
        self.exist = lambda: np.random.choice(self.data)

        self.set_screen()

    def set_screen(self):
        self.pre_screen_frame.destroy()

        self.geometry(f'{1250}x{750}')
        self.resizable(True, True)

        self.rowconfigure(index=0, weight=4, uniform=A)
        self.rowconfigure(index=1, weight=1, uniform=A)
        self.columnconfigure(index=0, weight=1, uniform=A)
        
        self.bars_frame = ctk.CTkFrame(self, fg_color=C0)
        self.bars_frame.grid(row=0, column=0, padx=10, pady=5, sticky=XY)
        
        self.bars_frame.rowconfigure(index=0, weight=1, uniform=A)
        self.bars_frame.columnconfigure(index=self.range, weight=1, uniform=A)
        
        self.buttons_frame = ctk.CTkFrame(self, fg_color=C0)
        self.buttons_frame.grid(row=1, column=0, sticky=XY)

        self.buttons_frame.rowconfigure(index=0, weight=1, uniform=A)
        self.buttons_frame.columnconfigure(index=(0, 1, 2), weight=1, uniform=A)

        #! ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- 
        
        self.search_frame = ctk.CTkFrame(self.buttons_frame, fg_color=C0)
        self.search_frame.grid(row=0, column=0, padx=(10, 0), pady=5, sticky=XY)

        self.search_frame.rowconfigure(index=(0, 1, 2), weight=1, uniform=A)
        self.search_frame.columnconfigure(index=(0, 1), weight=1, uniform=A)

        self.search_entry = ctk.CTkEntry(self.search_frame, fg_color=C1, placeholder_text='Search Key  |  `Restart`')
        self.search_entry.grid(row=0, column=0, columnspan=2, sticky=XY, padx=10, pady=(10, 5))
        self.search_entry.bind('<KeyRelease>', self.bind_entry)

        self.linear_search_btn = ctk.CTkButton(self.search_frame, text='Linear Search', state=DIS, command=self.linear_search, fg_color=C3, hover_color=C4)
        self.linear_search_btn.grid(row=1, column=0, sticky=X, padx=(10, 5), pady=5)
        
        self.jump_search_btn = ctk.CTkButton(self.search_frame, text='Jump Search', state=DIS, command=self.jump_search, fg_color=C3, hover_color=C4)
        self.jump_search_btn.grid(row=1, column=1, sticky=X, padx=(5, 10), pady=5)

        self.binary_search_btn = ctk.CTkButton(self.search_frame, text='Binary Search', state=DIS, command=self.binary_search, fg_color=C3, hover_color=C4)
        self.binary_search_btn.grid(row=2, column=0, sticky=X, padx=(10, 5), pady=(5, 10))
        
        self.ternary_search_btn = ctk.CTkButton(self.search_frame, text='Ternary Search', state=DIS, command=self.ternary_search, fg_color=C3, hover_color=C4)
        self.ternary_search_btn.grid(row=2, column=1, sticky=X, padx=(5, 10), pady=(5, 10))

        #! ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- 
        
        self.terminal = ctk.CTkTextbox(self.buttons_frame, wrap='word', font=('Courier', 15), state=DIS, fg_color=C1)
        self.terminal.grid(row=0, column=1, padx=10, pady=10, sticky=XY)
        
        self.show_data()
        
        #! ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- 
        
        self.sort_frame = ctk.CTkScrollableFrame(self.buttons_frame, fg_color=C0, scrollbar_button_color=C1)
        self.sort_frame.grid(row=0, column=2, padx=(0, 0), pady=5, sticky=XY)

        self.sort_frame.rowconfigure(index=(0, 1, 2, 3, 4), weight=1, uniform=A)
        self.sort_frame.columnconfigure(index=(0, 1), weight=1, uniform=A)

        self.merge_sort_btn = ctk.CTkButton(self.sort_frame, text='Merge Sort', command=self.merge_sort, fg_color=C3, hover_color=C4)
        self.merge_sort_btn.grid(row=0, column=0, sticky=X, padx=(10, 5), pady=5)
        
        self.quick_sort_btn = ctk.CTkButton(self.sort_frame, text='Quick Sort', command=self.quick_sort, fg_color=C3, hover_color=C4)
        self.quick_sort_btn.grid(row=0, column=1, sticky=X, padx=(5, 10), pady=5)

        self.insertion_sort_btn = ctk.CTkButton(self.sort_frame, text='Insertion Sort', command=self.insertion_sort, fg_color=C3, hover_color=C4)
        self.insertion_sort_btn.grid(row=1, column=0, sticky=X, padx=(10, 5), pady=5)
        
        self.selection_sort_btn = ctk.CTkButton(self.sort_frame, text='Selection Sort', command=self.selection_sort, fg_color=C3, hover_color=C4)
        self.selection_sort_btn.grid(row=1, column=1, sticky=X, padx=(5, 10), pady=5)
        
        self.bubble_sort_btn = ctk.CTkButton(self.sort_frame, text='Bubble Sort', command=self.bubble_sort, fg_color=C3, hover_color=C4)
        self.bubble_sort_btn.grid(row=2, column=0, sticky=X, padx=(10, 5), pady=5)

        self.heao_sort_btn = ctk.CTkButton(self.sort_frame, text='Heap Sort', command=self.heap_sort, fg_color=C3, hover_color=C4)
        self.heao_sort_btn.grid(row=2, column=1, sticky=X, padx=(5, 10), pady=5)

        self.shuffle_btn = ctk.CTkButton(self.sort_frame, text='Shuffle', command=self.shuffle, fg_color=C3, hover_color=C4)
        self.shuffle_btn.grid(row=3, column=0, columnspan=2, sticky=X, padx=(10, 10), pady=5)

        self.sort_btn = ctk.CTkButton(self.sort_frame, text='Sort', command=self.sort, fg_color=C3, hover_color=C4)
        self.sort_btn.grid(row=4, column=0, sticky=X, padx=(10, 5), pady=(5, 10))

        self.reverse_btn = ctk.CTkButton(self.sort_frame, text='Reverse', command=self.reverse, fg_color=C3, hover_color=C4)
        self.reverse_btn.grid(row=4, column=1, sticky=X, padx=(5, 10), pady=(5, 10))

    def show_data(self):
        self.write(' '.join(f'{int(num):03d}' for num in sorted(self.data)))

        self.bars = []
        for idx, val in zip(self.range, self.data):
            bar = ctk.CTkProgressBar(self.bars_frame,
                                     progress_color=C3,
                                     fg_color=C0,
                                     corner_radius=0,
                                     orientation='vertical'
                                     )

            bar._canvas.bind('<Button-1>', lambda _, b=bar: self.set_entry(b))
            bar.grid(row=0, column=idx, padx=0.5, sticky=XY)
            bar.set(self.scale(val))
            self.bars.append(bar)

    def update_data(self):
        for idx, bar in zip(self.range, self.bars):
            bar.set(self.scale(self.data[idx]))

    def set_entry(self, bar):
        if self.search_entry._state != DIS:
            value = int(self.unscale(bar.get()))
            self.search_entry.delete(0, ctk.END)
            self.search_entry.insert(0, value)
            self.bind_entry(None)

    def bind_entry(self, _event):
        entry = self.search_entry.get()
        if entry.lower() == 'restart':
            self.bars_frame.destroy()
            self.buttons_frame.destroy()
            self.get_data()

        else:
            self.reset_colors()
            try:
                self.key = int(entry)
            except:
                _state = DIS
            else:
                _state = NRM
                self.color_key()
            finally:
                for btn in [self.linear_search_btn, self.jump_search_btn, self.binary_search_btn, self.ternary_search_btn]:
                    btn.configure(state=_state)

    def color_key(self):
        if self.key in self.data:
            self.bars[self.data.index(self.key)].configure(progress_color=C2)

    def manage_buttons(self, state):
        for btn in [self.linear_search_btn, self.jump_search_btn, self.binary_search_btn, self.ternary_search_btn, self.search_entry,
                    self.merge_sort_btn, self.quick_sort_btn, self.insertion_sort_btn, self.selection_sort_btn, self.bubble_sort_btn,
                    self.heao_sort_btn, self.shuffle_btn, self.sort_btn, self.reverse_btn]:
            btn.configure(state=state)
        
    def reset_colors(self):
        for bar in self.bars:
            bar.configure(progress_color=C3)

    def write(self, *texts):
        self.terminal.configure(state=NRM)
        for text in texts:
            self.terminal.insert(ctk.END, text=f'{text}\n')
        self.terminal.configure(state=DIS)

    def linear_search(self):
        def _search():
            self.manage_buttons(state=DIS)
            key = int(self.search_entry.get())
            self.color_key()
            index = -1
            for i in range(self.n):
                if self.data[i] == key:
                    self.bars[i].configure(progress_color=C5)
                    index = i
                    break
                else:
                    self.bars[i].configure(progress_color=C4)            
                sleep(0.05)
            self.write(f'Linear Search: {f"Found at index `{index}`"  if index != -1 else "Not Found."}')
            self.manage_buttons(state=NRM)
            
        self.reset_colors()
        Thread(target=_search, daemon=True).start()

    def jump_search(self):
        def _search():
            self.manage_buttons(state=DIS)
            key = int(self.search_entry.get())
            self.color_key()
            index = -1
            Start, Size = 0, int(np.sqrt(self.n))
            Jump = Start + Size
            while self.data[min(Jump, self.n)-1] < key:
                self.bars[min(Jump, self.n)-1].configure(progress_color=C4)

                Start = Jump
                Jump += Size

                if self.data[min(Jump, self.n)-1] >= key:
                    self.bars[min(Jump, self.n)-1].configure(progress_color=C4)

                if Start >= self.n:
                    break
                    
                sleep(0.2)

            for i in range(Start, min(Jump, self.n)):
                if self.data[i] == key:
                    self.bars[i].configure(progress_color=C5)
                    index = i
                    break
                else:
                    self.bars[i].configure(progress_color=C4)        
                sleep(0.05)
            self.write(f'Jump Search: {f"Found at index `{index}`"  if index != -1 else "Not Found."}')
            self.manage_buttons(state=NRM)

        self.reset_colors()
        Thread(target=_search, daemon=True).start()

    def binary_search(self):
        def _search():
            self.manage_buttons(state=DIS)
            key = int(self.search_entry.get())
            self.color_key()
            index = -1
            Low, High = 0, len(self.data) - 1
            while Low <= High:
                Mid = (Low + High) // 2
                if self.data[Mid] == key:
                    self.bars[Mid].configure(progress_color=C5)
                    index = Mid
                    break
                elif self.data[Mid] > key:
                    High = Mid - 1
                    self.bars[Mid].configure(progress_color=C4)
                else:  # self.data[mid] < key
                    Low = Mid + 1
                    self.bars[Mid].configure(progress_color=C4)

                sleep(0.2)
            self.write(f'Binary Search: {f"Found at index `{index}`"  if index != -1 else "Not Found."}')
            self.manage_buttons(state=NRM)

        self.reset_colors()
        Thread(target=_search, daemon=True).start()

    def ternary_search(self):
        def _search():
            self.manage_buttons(state=DIS)
            key = int(self.search_entry.get())
            self.color_key()
            index = -1
            Low, High = 0, len(self.data) - 1
            while Low <= High:
                TH = (High - Low) // 3
                LowTH = Low + TH    # One Third
                HighTH = High - TH  # Two Thirds

                if self.data[LowTH] == key:
                    self.bars[LowTH].configure(progress_color=C5)
                    index = LowTH
                    break
                elif self.data[HighTH] == key:
                    self.bars[LowTH].configure(progress_color=C4)
                    self.bars[HighTH].configure(progress_color=C5)
                    index = HighTH
                    break
                elif self.data[LowTH] > key:
                    self.bars[LowTH].configure(progress_color=C4)
                    High = LowTH - 1
                elif self.data[HighTH] < key:
                    self.bars[HighTH].configure(progress_color=C4)
                    Low = HighTH + 1
                else:  # self.data[LowTH] < key < self.data[HighTH]
                    self.bars[LowTH].configure(progress_color=C4)
                    self.bars[HighTH].configure(progress_color=C4)
                    Low  = LowTH  + 1
                    High = HighTH - 1
                    
                sleep(0.2)
            self.write(f'Ternary Search: {f"Found at index `{index}`"  if index != -1 else "Not Found."}')
            self.manage_buttons(state=NRM)

        self.reset_colors()
        Thread(target=_search, daemon=True).start()

    def merge_sort(self):
        def _merge(left, right, l, r):
            i = j = k = 0
            while i < len(left) and j < len(right):
                if left[i] < right[j]:
                    self.data[l + k] = left[i]
                    self.bars[l + k].set(self.scale(left[i]))
                    i += 1
                else:
                    self.data[l + k] = right[j]
                    self.bars[l + k].set(self.scale(right[j]))
                    j += 1
                k += 1
                sleep(0.025)

            while i < len(left):
                self.data[l + k] = left[i]
                self.bars[l + k].set(self.scale(left[i]))
                i += 1
                k += 1
                sleep(0.025)

            while j < len(right):
                self.data[l + k] = right[j]
                self.bars[l + k].set(self.scale(right[j]))
                j += 1
                k += 1
                sleep(0.025)

            for idx in range(l, r + 1):
                self.bars[idx].configure(progress_color=C5)

        def _merge_sort(l, r):
            if l < r:
                m = (l + r) // 2
                _merge_sort(l, m)
                _merge_sort(m + 1, r)
                
                left = self.data[l:m + 1]
                right = self.data[m + 1:r + 1]
                
                _merge(left, right, l, r)

        def _sort():
            self.manage_buttons(state=DIS)
            _merge_sort(0, self.n - 1)
            self.manage_buttons(state=NRM)

        self.reset_colors()
        Thread(target=_sort, daemon=True).start()

    def quick_sort(self):
        def _partition(low, high):
            pivot = self.data[high]
            self.bars[high].configure(progress_color=C4)
            i = low - 1

            for j in range(low, high):
                if self.data[j] < pivot:
                    i += 1
                    self.data[i], self.data[j] = self.data[j], self.data[i]
                    self.bars[i].set(self.scale(self.data[i]))
                    self.bars[j].set(self.scale(self.data[j]))
                    
                    self.bars[i].configure(progress_color=C4)
                    sleep(0.025)

            self.data[i + 1], self.data[high] = self.data[high], self.data[i + 1]
            self.bars[i + 1].set(self.scale(self.data[i + 1]))
            self.bars[high].set(self.scale(self.data[high]))
              
            self.bars[i + 1].configure(progress_color=C5)
            self.bars[high].configure(progress_color=C5)
            sleep(0.025)

            return i + 1

        def _quick_sort(low, high):
            if low < high:
                pi = _partition(low, high)
                _quick_sort(low, pi - 1)
                _quick_sort(pi + 1, high)
            else:
                self.bars[high].configure(progress_color=C5)                

        def _sort():
            self.manage_buttons(state=DIS)
            _quick_sort(0, self.n - 1)
            self.manage_buttons(state=NRM)

        self.reset_colors()
        Thread(target=_sort, daemon=True).start()

    def insertion_sort(self):
        def _sort():
            self.manage_buttons(state=DIS)
            for i in range(1, self.n):
                key = self.data[i]
                self.bars[i - 1].configure(progress_color=C5)
                j = i - 1
                while j >= 0 and key < self.data[j]:
                    self.data[j + 1] = self.data[j]
                    self.bars[j + 1].set(self.scale(self.data[j + 1]))
                    self.bars[j].set(self.scale(key))

                    self.bars[j + 1].configure(progress_color=C3 if j > i else C5)
                    self.bars[j].configure(progress_color=C4)

                    sleep(0.05)
                    j -= 1

                self.data[j + 1] = key
                self.bars[j + 1].set(self.scale(self.data[j + 1]))
                self.bars[j + 1].configure(progress_color=C5)

            self.manage_buttons(state=NRM)
            
        self.reset_colors()
        Thread(target=_sort, daemon=True).start()

    def selection_sort(self):
        def _sort():
            self.manage_buttons(state=DIS)

            for i in range(0, self.n):
                min_index = i
                self.bars[i].configure(progress_color=C5)
                for j in range(i+1, self.n):
                    self.bars[j].configure(progress_color=C4)
                    if self.data[j] < self.data[min_index]:
                        self.bars[j].configure(progress_color=C5)
                        self.bars[min_index].configure(progress_color=C4)
                        min_index = j
                    sleep(0.025)

                self.data[i], self.data[min_index] = self.data[min_index], self.data[i]
                self.bars[i].configure(progress_color=C5)
                
                self.bars[i].set(self.scale(self.data[i]))
                self.bars[min_index].set(self.scale(self.data[min_index]))

                for z in range(i+1, self.n):
                    self.bars[z].configure(progress_color=C3)

                sleep(0.05)

            self.manage_buttons(state=NRM)
        
        self.reset_colors()
        Thread(target=_sort, daemon=True).start()

    def bubble_sort(self):
        def _sort():
            self.manage_buttons(state=DIS)
    
            for i in range(self.n):
                for j in range(0, self.n - i - 1):
                    if j > 0:
                        self.bars[j - 1].configure(progress_color=C3)

                    self.bars[j].configure(progress_color=C4)
                    self.bars[j + 1].configure(progress_color=C4)
                    
                    if self.data[j] > self.data[j + 1]:
                        self.bars[j].configure(progress_color=C5)
                        
                        self.data[j], self.data[j + 1] = self.data[j + 1], self.data[j]
                        self.bars[j].set(self.scale(self.data[j]))
                        self.bars[j + 1].set(self.scale(self.data[j + 1]))

                        sleep(0.025)
                        self.bars[j].configure(progress_color=C4)
                        self.bars[j + 1].configure(progress_color=C5)
                    else:
                        self.bars[j + 1].configure(progress_color=C5)

                    sleep(0.025)

                if i == self.n - 1:
                    self.bars[0].configure(progress_color=C5)
                else:
                    self.bars[self.n - i - 2].configure(progress_color=C3)
    
            self.manage_buttons(state=NRM)
        
        self.reset_colors()
        Thread(target=_sort, daemon=True).start()
        
    def heap_sort(self):
        def heapify(n, i):
            largest = i
            l = 2 * i + 1
            r = 2 * i + 2

            if l < n and self.data[i] < self.data[l]:
                largest = l

            if r < n and self.data[largest] < self.data[r]:
                largest = r

            if largest != i:
                self.bars[i].configure(progress_color=C5)
                self.bars[largest].configure(progress_color=C5)

                self.data[i], self.data[largest] = self.data[largest], self.data[i]
                self.bars[i].set(self.scale(self.data[i]))
                self.bars[largest].set(self.scale(self.data[largest]))

                sleep(0.025)

                self.bars[i].configure(progress_color=C4)
                self.bars[largest].configure(progress_color=C4)

                heapify(n, largest)

        def _sort():
            self.manage_buttons(state=DIS)

            for i in range(self.n // 2 - 1, -1, -1):
                heapify(self.n, i)

            for i in range(self.n - 1, 0, -1):
                self.bars[i].configure(progress_color=C5)
                self.bars[0].configure(progress_color=C5)

                self.data[i], self.data[0] = self.data[0], self.data[i]
                self.bars[i].set(self.scale(self.data[i]))
                self.bars[0].set(self.scale(self.data[0]))

                sleep(0.025)

                self.bars[i].configure(progress_color=C5)
                self.bars[0].configure(progress_color=C5)

                heapify(i, 0)

            self.manage_buttons(state=NRM)

        self.reset_colors()
        Thread(target=_sort, daemon=True).start()

    def shuffle(self):
        np.random.shuffle(self.data)
        self.reset_colors()
        self.update_data()
        self.bind_entry(None)

    def sort(self):
        self.data = sorted(self.data, reverse=False)
        self.reset_colors()
        self.update_data()
        self.bind_entry(None)

    def reverse(self):
        self.data = sorted(self.data, reverse=True)
        self.reset_colors()
        self.update_data()
        self.bind_entry(None)


if __name__ == '__main__':
    App()