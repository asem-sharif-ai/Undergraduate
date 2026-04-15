# Multimedia Security Project

A comprehensive, professional-grade desktop application for **Digital Watermarking** and **Multimedia Analysis**. Built with **Python** and **CustomTkinter**, this tool provides a unified interface for embedding and extracting secure watermarks across three primary media types: Images, Audio, and Video.

## Key Features

### Image Security

  * **Advanced Watermarking:** Supports LSB (Least Significant Bit), DCT (Discrete Cosine Transform), and DWT (Discrete Wavelet Transform) methods.
  * **Attack Simulation:** Test watermark robustness against geometric attacks (scaling, rotation) and binarization.
  * **Metadata Analysis:** View detailed image properties and color mode information.

### Audio Security

  * **Signal Embedding:** Securely hide text data within audio signals using bit-plane manipulation.
  * **Real-time Recording:** Integrated audio recording and playback functionality for immediate testing.
  * **Property Inspection:** Analyze sample rates, bit depth, peak amplitudes, and RMS values.

### Video Security

  * **Frequency Domain Watermarking:** Implementation of DCT and DWT algorithms on individual video frames.
  * **Stream Analysis:** Detailed breakdown of video properties, including frame count, FPS, and audio stream verification.
  * **Frame-by-Frame Processing:** Precise control over watermark alpha (intensity) and binarization thresholds.

-----

## Technical Stack

  * **GUI Framework:** [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) (Modern UI library for Tkinter)
  * **Core Processing:** [OpenCV (cv2)](https://opencv.org/), [NumPy](https://numpy.org/)
  * **Signal Analysis:** [PyWavelets (pywt)](https://pywavelets.readthedocs.io/), [SciPy](https://scipy.org/)
  * **Media Handling:** PIL (Pillow), MoviePy, SoundDevice, Wave

## Project Architecture

  * **`App.py` / `Main.py`**: The application's core logic and main window management.
  * **`GUI/`**: Contains modular frame logic (`ImageFrame.py`, `VideoFrame.py`, `AudioFrame.py`) and custom UI components (`Utils.py`).
  * **`Methods/`**: The algorithmic heart of the project containing the mathematical implementations for Image, Audio, and Video watermarking.
