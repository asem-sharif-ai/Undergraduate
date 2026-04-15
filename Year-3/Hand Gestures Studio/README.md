# Hand Sign Recognition Studio

An end-to-end Deep Learning application designed for creating custom hand sign datasets, training Convolutional Neural Networks (CNNs), and performing real-time inference with live preprocessing.

## Overview
This project provides a comprehensive "Studio" environment for hand sign recognition. Instead of using static datasets, it empowers users to record their own signs, experiment with model architectures, and see live results using Computer Vision.

## Key Features

### 1. Dataset Generation & Management
* **Live Recording:** Capture hand signs directly from your webcam.
* **Labeling System:** Easily add, delete, and manage multiple sign classes.
* **Format Support:** Export and import datasets in **HDF5 (.h5)** for high performance or **CSV** for compatibility.
* **Brief View:** Built-in data table to inspect your samples instantly.

### 2. Custom CNN Training
* **Dynamic Architecture:** Adjust model "Complexity" to scale the number of convolutional and dense layers.
* **Hyperparameter Control:** Fine-tune Learning Rate, Batch Size, Test Size, and Epochs directly from the UI.
* **Live Visualization:** Watch the model learn with real-time Accuracy and Loss plots during the training phase.
* **Advanced Evaluation:** Generate Confusion Matrices, ROC-AUC curves, and detailed Classification Reports.

### 3. Real-Time Inference & Vision
* **Hand Tracking:** Powered by **MediaPipe** for precise 21-landmark detection.
* **Region of Interest (ROI):** Automatically isolates and crops the hand, ensuring the model focuses only on relevant features.
* **Live Preprocessing:** Toggle between multiple modes including:
    * Adaptive Thresholding
    * Sobel Edge Detection
    * Gaussian Blurring
* **Model Activation:** Load saved models and test them against your live camera feed with a single click.

## Tech Stack
* **GUI:** [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) (Modern Dark Theme/Glassmorphism)
* **Deep Learning:** TensorFlow / Keras
* **Computer Vision:** OpenCV, MediaPipe
* **Data Science:** Pandas, NumPy, Scikit-learn, Matplotlib, Seaborn
* **Storage:** HDF5 (h5py), Pickle

## Project Structure
* `App.py` / `Main.py`: Entry point and central application logic.
* `CNN.py`: Core Deep Learning logic (model generation, training, and plotting).
* `Detector.py`: Hand detection and image preprocessing engine.
* `DataFrame.py`: Dataset creation and management interface.
* `ModelFrame.py`: Training controls and evaluation metrics.
* `ControlFrame.py`: Camera settings, detector parameters, and inference activation.
* `Helper.py`: Utility functions for file I/O and data validation.
* `Tracker.py`: Custom Keras callbacks for real-time GUI updates.

## Installation

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/asem-sharif-ai-Undergraduate/HandSign-Studio.git](https://github.com/asem-sharif-ai/Undergraduate/HandSign-Studio.git)
   cd handsign-dl-studio
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
   *Note: Requires TensorFlow, MediaPipe, OpenCV, and CustomTkinter.*

3. **Run the application:**
   ```bash
   python App.py
   ```

## Usage Guide
1. **Create Data:** Go to the Data Section, add your labels (e.g., 'A', 'B', 'C'), and click 'Capture' while showing the sign to the camera.
2. **Export:** Save your dataset as an `.h5` file.
3. **Train:** Switch to the Model Section, import your dataset, adjust complexity, and hit 'Train'. Observe the live plots.
4. **Test:** Once trained (or after loading a saved model), click 'Activate Model' in the Control Section to see real-time predictions.
