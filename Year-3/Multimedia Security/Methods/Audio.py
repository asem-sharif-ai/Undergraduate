import wave
import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
from scipy.io import wavfile

def read_audio(path: str) -> tuple[np.ndarray, int, int]:
    sample_rate, audio_data = wavfile.read(path)

    if audio_data.dtype != np.int16:
        if np.issubdtype(audio_data.dtype, np.floating):
            audio_data = (audio_data * 32767).astype(np.int16)
        else:
            audio_data = audio_data.astype(np.int16)

    if audio_data.ndim == 1:
        audio_data = np.expand_dims(audio_data, axis=1)

    channels = audio_data.shape[1]

    return audio_data, sample_rate, channels

def record_audio(duration: float, sample_rate: int, channels: int) -> np.ndarray:
    audio_data = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=channels, dtype=np.int16)
    sd.wait()
    return audio_data

def play_audio(audio_data: np.ndarray, duration: int, sample_rate: int) -> None:
    sd.play(audio_data[:int(int(duration) * int(sample_rate))], samplerate=sample_rate)
    sd.wait()

def plot_audio(audio_data: np.ndarray, sample_rate: int) -> None:
    time_axis = np.linspace(0, audio_data.shape[0] / sample_rate, audio_data.shape[0])

    plt.style.use('dark_background')
    plt.figure('Audio Waveform', figsize=(12, 6))
    if audio_data.ndim == 1 or audio_data.shape[1] == 1:
        plt.plot(time_axis, audio_data.squeeze(), color='r', label='Channel 1')
    else:
        for ch in range(min(audio_data.shape[1], 3)):
            plt.plot(time_axis, audio_data[:, ch], color=[(220/255, 0, 0), (170/255, 0, 0), (120/255, 0, 0)][ch], label=f'Channel {ch + 1}')

    plt.title('Audio Waveform')
    plt.xlabel('Time')
    plt.ylabel('Amplitude')
    plt.legend()
    plt.grid(True, color='gray', linestyle='--', alpha=0.3)
    plt.tight_layout()
    plt.show()

def get_properties(audio_data: np.ndarray, sample_rate: int, channels: int) -> dict:
    return {
        'Duration': int(len(audio_data) / sample_rate),
        'Sample_Rate': sample_rate,
        'Channels': channels,
        'Bit_Depth': audio_data.dtype.itemsize * 8,
        'Total_Samples': audio_data.size,
        'Peak_Amplitude': int(np.max(np.abs(audio_data))),
        'RMS_Amplitude': float(np.sqrt(np.mean(np.square(audio_data.astype(np.float32))))),
        'Mean_Amplitude': float(np.mean(audio_data)),
        'Min_Amplitude': int(np.min(audio_data)),
        'Max_Amplitude': int(np.max(audio_data))
    }

def format_properties(properties: dict) -> str:
    return f'''Audio Properties:
    - Duration       : {properties['Duration']} Seconds
    - Sample Rate    : {properties['Sample_Rate']} Hz
    - Channels       : {properties['Channels']}
    - Bit Depth      : {properties['Bit_Depth']} Bits
    - Total Samples  : {properties['Total_Samples']}
    - Peak Amplitude : {properties['Peak_Amplitude']}
    - RMS Amplitude  : {properties['RMS_Amplitude']:.2f}
    - Mean Amplitude : {properties['Mean_Amplitude']:.2f}
    - Min Amplitude  : {properties['Min_Amplitude']}
    - Max Amplitude  : {properties['Max_Amplitude']}'''

def export_audio(path: str, audio_data: np.ndarray, sample_rate: int, channels: int):
    with wave.open(f'{path}.wav', 'wb') as file:
        file.setnchannels(channels)
        file.setsampwidth(2)
        file.setframerate(sample_rate)
        file.writeframes(audio_data.tobytes())

def embed(audio: np.ndarray, watermark: str, bit_idx: int) -> np.ndarray:
    audio = audio.flatten()
    
    watermark_bits = np.unpackbits(np.frombuffer(watermark.encode('utf-8'), dtype=np.uint8))
    if len(watermark_bits) > len(audio):
        raise ValueError('Watermark too long for the audio at given bit index.')

    watermarked_audio = audio.copy()
    for i, bit in enumerate(watermark_bits):
        watermarked_audio[i] = (watermarked_audio[i] & ~(1 << bit_idx)) | (bit << bit_idx)
    
    return watermarked_audio

def extract(audio: np.ndarray, bit_idx: int, length: int) -> str:
    audio = audio.flatten()
    bits = [(audio[i] >> bit_idx) & 1 for i in range(length * 8)]
    bytes_array = np.packbits(np.array(bits, dtype=np.uint8))
    return bytes_array.tobytes().decode('utf-8', errors='ignore')
