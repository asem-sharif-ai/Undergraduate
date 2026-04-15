import customtkinter as ctk
from tkinter.filedialog import askopenfilename as import_file, asksaveasfilename as export_file

import json
from threading import Thread

from Methods.Audio import (
    read_audio, record_audio,
    play_audio, plot_audio,
    get_properties, format_properties,
    export_audio,
    embed, extract
)
from GUI.Utils import SliderFrame

class AudioFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.rowconfigure(index=(0, 1), weight=1, uniform='a')
        self.columnconfigure(index=0, weight=1, uniform='a')

    def build(self):
        self.import_frame = ctk.CTkFrame(self)
        self.import_frame.grid(row=0, column=0, padx=10, pady=(10, 5), sticky='nsew')

        self.import_frame.rowconfigure(index=0, weight=1, uniform='a')
        self.import_frame.columnconfigure(index=0, weight=1, uniform='a')

        self.import_btn = ctk.CTkButton(self.import_frame, text='Import Audio', command=self.import_audio)
        self.import_btn.grid(row=0, column=0)

        self.build_record_frame()

    def build_record_frame(self):
        self.record_frame = ctk.CTkFrame(self)
        self.record_frame.grid(row=1, column=0, padx=10, pady=(5, 10), sticky='nsew')

        self.record_frame.rowconfigure(index=0, weight=1, uniform='a')
        self.record_frame.columnconfigure(index=(0, 1, 2, 3), weight=1, uniform='a')

        self.frame_1 = ctk.CTkFrame(self.record_frame)
        self.frame_1.grid(row=0, column=0, padx=(10, 5), pady=10, sticky='nsew')

        self.frame_1.rowconfigure(index=(0, 1, 2, 3), weight=1, uniform='a')
        self.frame_1.columnconfigure(index=(0, 1), weight=1, uniform='a')
        
        self.duration_frame = SliderFrame(
            master=self.frame_1,
            label='Duration',
            value='15 Seconds',
            format=lambda v: f'{int(v)} Seconds',
            command=lambda *args, **kwargs:None,
            slider_params={'from_': 5, 'to': 60, 'number_of_steps': 55}
        )
        self.duration_frame.grid(row=0, column=0, columnspan=2, padx=10, pady=(10, 0), sticky='nsew')
        self.duration_frame.set_slider(15)

        self.sample_rate_frame = SliderFrame(
            master=self.frame_1,
            label='Sample Rate',
            value='16000 Hz',
            format=lambda v: f'{['8000', '11025', '16000', '22050', '32000', '44100', '48000'][int(v)]} Hz',
            command=lambda *args, **kwargs:None,
            slider_params={'from_': 0, 'to': 6, 'number_of_steps': 6}
        )
        self.sample_rate_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=(10, 0), sticky='nsew')
        self.sample_rate_frame.set_slider(2)

        self.channels_frame = SliderFrame(
            master=self.frame_1,
            label='Channels',
            value='2 Channels',
            format=lambda v: f'{int(v)} {['Channel', 'Channels', 'Channels'][int(v)-1]}',
            command=lambda *args, **kwargs:None,
            slider_params={'from_': 1, 'to': 3, 'number_of_steps': 2}
        )
        self.channels_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=(10, 0), sticky='nsew')
        self.channels_frame.set_slider(2)

        self.record_btn = ctk.CTkButton(self.frame_1, text='Record', command=self.record_audio)
        self.record_btn.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

        self.plot_btn = ctk.CTkButton(self.frame_1, text='Plot', command=self.plot_audio)
        
        self.frame_2 = ctk.CTkFrame(self.record_frame)
        self.frame_2.grid(row=0, column=1, padx=5, pady=10, sticky='nsew')

        self.frame_2.rowconfigure(index=0, weight=3, uniform='a')
        self.frame_2.rowconfigure(index=1, weight=1, uniform='a')
        self.frame_2.columnconfigure(index=0, weight=1, uniform='a')

        self.properties_btn = ctk.CTkButton(self.frame_2, text='Properties', state='disabled', command=self.show_properties_frame)
        self.properties_btn.grid(row=0, column=0, rowspan=2)

        self.properties_entry = ctk.CTkTextbox(self.frame_2, activate_scrollbars=False, font=('Courier New', 14, 'bold'), state='disabled')
        self.save_btn = ctk.CTkButton(self.frame_2, text='Save', command=self.save_properties)

        self.frame_3 = ctk.CTkFrame(self.record_frame)
        self.frame_3.grid(row=0, column=2, padx=5, pady=10, sticky='nsew')

        self.frame_3.rowconfigure(index=0, weight=2, uniform='a')
        self.frame_3.rowconfigure(index=(1, 2), weight=1, uniform='a')
        self.frame_3.columnconfigure(index=(0, 1), weight=1, uniform='a')

        self.watermark_3_btn = ctk.CTkButton(self.frame_3, text='Watermark', state='disabled', command=self.show_watermark_frame)
        self.watermark_3_btn.grid(row=0, column=0, rowspan=3, columnspan=2)

        self.input_entry = ctk.CTkTextbox(self.frame_3, activate_scrollbars=False)
        self.input_entry.bind('<KeyRelease>', lambda _:self.embed_btn.configure(text='Embed', state='normal'))
        self.write(self.input_entry, 'Write down a watermark and click <Embed> to embed.', False)

        self.bit_idx_frame = SliderFrame(
            master=self.frame_3,
            label='Embedding Bit Index',
            value='LSB',
            format=lambda v: f'{['LSB', '1St', '2Nd', '3Rd', '4Th', '5Th', '6Th', 'MSB'][int(v)]}',
            command=lambda _:self.embed_btn.configure(text='Embed', state='normal'),
            slider_params={'from_': 0, 'to': 7, 'number_of_steps': 7}
        )
        self.bit_idx_frame.set_slider(0)

        self.play_btn = ctk.CTkButton(self.frame_3, text='Play', command=self.play_watermarked)
        self.embed_btn = ctk.CTkButton(self.frame_3, text='Embed', command=self.embed)

        self.frame_4 = ctk.CTkFrame(self.record_frame)
        self.frame_4.grid(row=0, column=3, padx=(5, 10), pady=10, sticky='nsew')
        
        self.frame_4.rowconfigure(index=0, weight=6, uniform='a')
        self.frame_4.rowconfigure(index=1, weight=3, uniform='a')
        self.frame_4.rowconfigure(index=2, weight=4, uniform='a')
        self.frame_4.columnconfigure(index=0, weight=1, uniform='a')

        self.watermark_4_btn = ctk.CTkButton(self.frame_4, text='Watermark', state='disabled', command=self.show_watermark_frame)
        self.watermark_4_btn.grid(row=0, column=0, rowspan=2)

        self.output_entry = ctk.CTkTextbox(self.frame_4, activate_scrollbars=False, state='disabled')
        self.length_frame = SliderFrame(
            master=self.frame_4,
            label='Extraction Length',
            value='25 Letters',
            format=lambda v: f'{int(v)} Letters',
            command=self.extract,
            slider_params={'from_': 5, 'to': 250, 'number_of_steps': 245}
        )
        self.length_frame.set_slider(25)

        self.manage_frame = ctk.CTkFrame(self.frame_4)
        self.manage_frame.grid(row=2, column=0, padx=10, pady=(5, 10), sticky='nsew')
        
        self.manage_frame.rowconfigure(index=(0, 1), weight=1, uniform='a')
        self.manage_frame.columnconfigure(index=(0, 1), weight=1, uniform='a')
        
        self.delete_btn = ctk.CTkButton(self.manage_frame, text='Delete', command=self.delete_audio, state='disabled')
        self.delete_btn.grid(row=0, column=0, padx=(10, 5), pady=(10, 5), sticky='nsew')
        
        self.export_btn = ctk.CTkButton(self.manage_frame, text='Export', command=self.export_audio, state='disabled')
        self.export_btn.grid(row=0, column=1, padx=(5, 10), pady=(10, 5), sticky='nsew')
        
        self.back_btn = ctk.CTkButton(self.manage_frame, text='Back', command=lambda: self.master.back(self))
        self.back_btn.grid(row=1, column=0, padx=(10, 5), pady=(5, 10), sticky='nsew')
        
        self.close_btn = ctk.CTkButton(self.manage_frame, text='Close', command=self.master.close)
        self.close_btn.grid(row=1, column=1, padx=(5, 10), pady=(5, 10), sticky='nsew')

    def show_properties_frame(self):
        self.properties_btn.grid_forget()
        self.properties_entry.grid(row=0, column=0, padx=10, pady=(10, 0), sticky='nsew')
        self.save_btn.grid(row=1, column=0, padx=10, pady=10)
 
    def show_watermark_frame(self):
        self.watermark_3_btn.grid_forget()
        self.watermark_4_btn.grid_forget()
        self.input_entry.grid(row=0, column=0, columnspan=2, padx=10, pady=(10, 0), sticky='nsew')
        self.bit_idx_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=(10, 0), sticky='nsew')
        self.play_btn.grid(row=2, column=0, padx=(10, 5), pady=10, sticky='ew')
        self.embed_btn.grid(row=2, column=1, padx=(5, 10), pady=10, sticky='ew')
        self.output_entry.grid(row=0, column=0, padx=10, pady=(10, 10), sticky='nsew')
        self.length_frame.grid(row=1, column=0, padx=10, pady=(0, 5), sticky='nsew')

    def import_audio(self):
        path = import_file(title='Select An Audio', filetypes=[('Audio Files', '*.wav')])
        self.audio_data, sample_rate, channels = read_audio(path)
        self.properties = get_properties(self.audio_data, sample_rate, channels)
        self.watermarked = self.audio_data.copy()
        self.duration_frame.set_value(self.properties['Duration'])
        self.set_sample_rate(sample_rate)
        self.channels_frame.set_value(channels)
        self.channels_frame.set_slider(channels)
        self.sample_rate_frame.slider.configure(state='disabled')
        self.channels_frame.slider.configure(state='disabled')
        self.ready()

    def ready(self):
        duration = self.properties['Duration']
        self.record_btn.configure(text='Play', command=self.play_audio, state='normal')
        self.record_btn.grid_configure(columnspan=1, padx=(10, 5), sticky='ew')
        self.plot_btn.grid(row=3, column=1, padx=(5, 10), pady=10, sticky='ew')
        
        self.duration_frame.slider.configure(from_=1, to=duration, number_of_steps=duration-1, state='normal')
        self.duration_frame.set_slider(duration)
        self.duration_frame.set_value(f'{duration} Seconds')
        for btn in [self.properties_btn, self.watermark_3_btn, self.watermark_4_btn, self.export_btn, self.delete_btn]:
            btn.configure(state='normal')
        self.write(self.properties_entry, format_properties(self.properties))

    def record_audio(self):
        def record():
            self.record_btn.configure(text='Recording...', state='disabled')
            self.duration_frame.slider.configure(state='disabled')
            self.sample_rate_frame.slider.configure(state='disabled')
            self.channels_frame.slider.configure(state='disabled')

            self.audio_data = record_audio(
                int(self.duration_frame.value),
                self.sample_rate,
                int(self.channels_frame.value)
            )
            
            self.properties = get_properties(self.audio_data, self.sample_rate, int(self.channels_frame.value))
            self.watermarked = self.audio_data.copy()
            self.ready()

        Thread(target=record, daemon=True).start()

    def play_audio(self):
        def play():
            if self.audio_data is not None:
                self.record_btn.configure(text='Playing...', state='disabled')
                play_audio(self.audio_data, int(self.duration_frame.value), self.sample_rate)
                self.record_btn.configure(text='Play Audio', state='normal')
        Thread(target=play, daemon=True).start()

    def plot_audio(self):
        plot_audio(self.audio_data, self.sample_rate)

    def save_properties(self):
        path = export_file(
            title='Export Properties',
            initialfile='Properties',
            defaultextension='.json',
            filetypes=[('JSON File', '*.json'), ('Text File', '*.txt')]
        )

        if path:
            if path.endswith('.json'):
                with open(path, 'w') as file:
                    json.dump(self.properties, file, indent=4)
            elif path.endswith('.txt'):
                with open(path, 'w') as file:
                    file.write(format_properties(self.properties))

    def embed(self):
        self.watermarked = embed(self.audio_data, self.read(self.input_entry), int(self.bit_idx_frame.value))
        self.embed_btn.configure(text='Embeded', state='disabled')

    def extract(self, *args, **kwargs):
        self.write(self.output_entry, extract(self.watermarked, int(self.bit_idx_frame.value), int(self.length_frame.value)))

    def play_watermarked(self):
        def play():
            if self.watermarked is not None:
                self.play_btn.configure(text='Playing...', state='disabled')
                play_audio(self.watermarked, int(self.duration_frame.value), self.sample_rate)
                self.play_btn.configure(text='Play', state='normal')
        Thread(target=play, daemon=True).start()

    def delete_audio(self):
        self.record_frame.destroy()
        self.build_record_frame()

    def export_audio(self):
        path = export_file(title='Export Audio', initialfile='Audio', filetypes=[('WAV Audio', '*.wav')])
        if path:
            export_audio(path, self.audio_data, self.sample_rate, int(self.channels_frame.value))

    def read(self, entry):
        return entry.get('1.0', 'end-1c').strip()

    def write(self, entry, text, disable=True):
        entry.configure(state='normal')
        entry.delete('1.0', 'end')
        entry.insert('end', text)
        if disable: entry.configure(state='disabled')

    def set_sample_rate(self, sr: int) -> int:
        if sr in (sample_rates := [8000, 11025, 16000, 22050, 32000, 44100, 48000]):
            idx = sample_rates.index(sr)
        else:
            idx = min(range(len(sample_rates)), key=lambda i: abs(sample_rates[i] - sr))
        self.sample_rate_frame.set_value(sr)
        self.sample_rate_frame.set_slider(idx)

    @property
    def sample_rate(self):
        return [8000, 11025, 16000, 22050, 32000, 44100, 48000][int(self.sample_rate_frame.value)]