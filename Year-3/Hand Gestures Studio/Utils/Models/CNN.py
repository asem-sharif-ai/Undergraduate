import math
import cv2 as cv
import numpy as np
import pandas as pd

import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
from matplotlib.patches import Rectangle
from matplotlib.cm import ScalarMappable

import os, sys, io
import pickle

import tensorflow
Models = tensorflow.keras.models
Layers = tensorflow.keras.layers
Optimizer = tensorflow.keras.optimizers.Adam
Generator = tensorflow.keras.preprocessing.image.ImageDataGenerator
OneHotEncoder = tensorflow.keras.utils.to_categorical

from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    precision_score, recall_score, f1_score,
    classification_report, confusion_matrix,
    roc_curve, auc
    )

class CNN:
    def __init__(self, complexity: int, dataset: pd.DataFrame, label: str, min_max_dim: tuple=(28, 56), writer: callable=print):
        self.dataset = dataset
        self.label = label
        self.write = writer

        self.complexity = complexity
        self.shape = (int(math.sqrt(len(dataset.columns) - 1)),) * 2
        self.classes = sorted(self.dataset[self.label].unique().tolist())

        self._validate_dataset(min_dimension=min_max_dim[0], max_dimension=min_max_dim[1])

        self.model = CNN._generate_model(complexity, self.shape, len(self.classes))
        self.stats = {
            'Training Loss'      : [],
            'Validation Loss'    : [],
            'Training Accuracy'  : [],
            'Validation Accuracy': []
        }

    def preprocess(self, data: np.ndarray):
      return data.astype('float32').reshape(-1, *self.shape, 1) / 255.

    def load_data(self, test_size: float, batch_size: int, use_generator: bool):
        self.test_size = test_size
        self.batch_size = batch_size
        self.use_generator = use_generator
        
        self.encode_map = {val: idx for idx, val in enumerate(self.classes)}
        self.decode_map = {idx: val for val, idx in self.encode_map.items()}

        x, y = self.dataset.drop(columns=[self.label]), self.dataset[self.label]

        X = self.preprocess(x.values)                    # Normalize & Reshape Features
        Y = OneHotEncoder(y.map(self.encode_map),        # Encode Labels (Label Encoder)
                          num_classes=len(self.classes)) # Encode Labels (OneHotEncoder)

        self.x_train, x_val_test, self.y_train, y_val_test = train_test_split(
            X, Y, test_size=test_size*2, random_state=1024, stratify=Y.argmax(axis=1)
        )
        self.x_val, self.x_test, self.y_val, self.y_test = train_test_split(
            x_val_test, y_val_test, test_size=0.5, random_state=1024, stratify=y_val_test.argmax(axis=1)
        )

        if use_generator:
            generator = Generator(
                rotation_range=15,
                width_shift_range=0.15,
                height_shift_range=0.15,
                shear_range=0.15,
                zoom_range=0.15,
                horizontal_flip=True,
                fill_mode='nearest'
            )

            augmented_images, augmented_labels = [], []
            for (image_batch, label_batch) in generator.flow(self.x_train, self.y_train, batch_size=batch_size, shuffle=True):
                augmented_images.append(image_batch)
                augmented_labels.append(label_batch)
                if len(augmented_images) * batch_size >= len(self.x_train):
                    break
            self.x_train = np.vstack(augmented_images)
            self.y_train = np.vstack(augmented_labels)

    def compile(self, learning_rate: float):
        self.learning_rate = learning_rate
        self.model.compile(
            optimizer=Optimizer(learning_rate=learning_rate),
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )

    def train(self, epochs: int, verbose: int=0, callbacks: list=[]):
        self.epochs = epochs
        process = self.model.fit(
            self.x_train, self.y_train,
            validation_data=(self.x_val, self.y_val),
            epochs=epochs,
            batch_size=self.batch_size,
            callbacks=callbacks,
            verbose=verbose,
        )
        if callbacks in [[], None]:
          self._catch_stats({
            'Training Loss'      : process.history['loss'],
            'Validation Loss'    : process.history['val_loss'],
            'Training Accuracy'  : process.history['accuracy'],
            'Validation Accuracy': process.history['val_accuracy']
        })

    def _catch_stats(self, stats: dict):
        self.stats = stats

    def evaluate(self, verbose: int=0, callbacks: list=[]):
        self.loss, self.accuracy = self.model.evaluate(self.x_test, self.y_test, verbose=verbose, callbacks=callbacks)
        y_pred = np.argmax(self.model.predict(self.x_test, verbose=0), axis=1)
        y_true = np.argmax(self.y_test, axis=1)
        self.confusion = confusion_matrix(y_true, y_pred)
        self.accuracy = self.accuracy * 100
        self.precision = precision_score(y_true, y_pred, zero_division=1.0, average='weighted')
        self.recall = recall_score(y_true, y_pred, zero_division=1.0, average='weighted')
        self.f1 = f1_score(y_true, y_pred, zero_division=1.0, average='weighted')
        self.report = classification_report(y_true, y_pred, target_names=[str(c) for c in self.classes])

        if len(self.classes) == 2:
            y_prob = self.model.predict(self.x_test)[:, 1]
            fpr, tpr, _ = roc_curve(self.y_test[:, 1], y_prob)
            self.roc_auc = {'roc': [fpr, tpr], 'auc': auc(fpr, tpr)}
            self.is_binary = True
        else:
            self.roc_auc = {}
            for i, class_name in enumerate(self.classes):
                fpr, tpr, _ = roc_curve(self.y_test[:, i], self.model.predict(self.x_test)[:, i])
                self.roc_auc[class_name] = {'roc': [fpr, tpr], 'auc': auc(fpr, tpr)}

    def predict(self, matrix: np.ndarray, return_confidence: bool=False, return_decoded: bool=False):
        x_matrix = self.preprocess(matrix)
        y_output = self.model.predict(x_matrix)
        pred = self._decode(key=np.argmax(y_output, axis=1)[0], apply=return_decoded)
        conf = np.round(np.max(y_output)* 100 , 2)
        return (pred, conf) if return_confidence else pred

    def _decode(self, key: int, apply: bool):
        return self.decode_map.get(key, None) if apply else key

    def summary(self):
        stream = io.StringIO()
        sys.stdout = stream
        self.model.summary()
        sys.stdout = sys.__stdout__
        self.write(stream.getvalue())

    def overview(self):
        self.write(f'Accuracy : {self.accuracy:.2f}%')
        self.write(f'Precision: {self.precision:.2f}')
        self.write(f'Recall   : {self.recall:.2f}')
        self.write(f'F1 Score : {self.f1:.2f}')
        self.write(f'Classification Report: \n{self.report}\n')

    def plot_confusion_matrix(self):
        plt.style.use('dark_background')
        plt.figure('Confusion Matrix', figsize=(8, 6))
        sns.heatmap(self.confusion,
                    cmap='magma', annot=False,
                    xticklabels=self.classes,
                    yticklabels=self.classes,
                    linewidths=0.5, linecolor='gray'
            ).add_patch(Rectangle((0, 0), self.confusion.shape[1], self.confusion.shape[0], fill=False, linewidth=3))
        plt.gca().invert_yaxis()
        for _ in [plt.title, plt.xlabel, plt.ylabel]:
            _(' ')
        plt.show()

    def plot_loss_and_accuracy(self):
        def plot(x, y, cmap, segments=100, *args, **kwargs):
            for i in range(len(x) - 1):
                x_interpolation = np.linspace(x[i], x[i + 1], segments)
                y_interpolation = np.linspace(y[i], y[i + 1], segments)
                for j in range(segments - 1):
                    if i + j != 0 and 'label' in kwargs.keys():
                        kwargs.pop('label')
                    plt.plot(
                        x_interpolation[j:j + 2], y_interpolation[j:j + 2],
                        color=cmap.to_rgba((y_interpolation[j] + y_interpolation[j + 1]) / 2),
                        linewidth=1, *args, **kwargs
                    )

        epochs = range(1, len(self.stats['Validation Accuracy']) + 1)
        a_min = min(min(self.stats['Training Accuracy']), min(self.stats['Validation Accuracy'])) * 100
        l_max = max(max(self.stats['Training Loss']), max(self.stats['Validation Loss']))

        plt.style.use('dark_background')
        plt.figure('Model Accuracy and Loss', figsize=(11, 5))

        ta_cmap = ScalarMappable(norm=Normalize(vmin=0, vmax=100), cmap='Blues')
        va_cmap = ScalarMappable(norm=Normalize(vmin=0, vmax=100), cmap='Purples')
        tl_cmap = ScalarMappable(norm=Normalize(vmin=0, vmax=max(1, l_max)), cmap='Reds')
        vl_cmap = ScalarMappable(norm=Normalize(vmin=0, vmax=max(1, l_max)), cmap='Oranges')

        plt.subplot(1, 2, 1)
        plot(epochs, np.array(self.stats['Training Accuracy']) * 100, ta_cmap, label='Training')
        plot(epochs, np.array(self.stats['Validation Accuracy']) * 100, va_cmap, label='Validation')
        plt.xlabel('Epochs', color='white')
        plt.ylabel('Accuracy', color='white')
        plt.grid(alpha=0.3, color='gray')
        plt.title('Accuracy', color='white')
        plt.ylim(0, 100)
        plt.xlim(1, len(epochs))
        plt.legend()

        plt.subplot(1, 2, 2)
        plot(epochs, self.stats['Training Loss'], tl_cmap, label='Training')
        plot(epochs, self.stats['Validation Loss'], vl_cmap, label='Validation')
        plt.xlabel('Epochs', color='white')
        plt.ylabel('Loss', color='white')
        plt.grid(alpha=0.3, color='gray')
        plt.title('Loss', color='white')
        plt.ylim(0, max(1, l_max))
        plt.xlim(1, len(epochs))
        plt.legend()

        plt.tight_layout()
        plt.show()

    def plot_roc_auc(self):
        plt.figure('Receiver Operating Characteristic', figsize=(7, 6), facecolor='black')
        ax = plt.gca()
        ax.set_facecolor('black')
        for axis in ['x', 'y']:
            ax.tick_params(axis=axis, colors='white')
        for edge in [ax.spines[e] for e in ['top', 'bottom', 'left', 'right']]:
            edge.set_color('white')

        colors = [f'#{r:02x}0000' for r in np.linspace(250, 55, len(self.roc_auc)).astype(int)]
        plt.plot([0, 1], [0, 1], '--', label='Chance Level', linewidth=1, color='white')
        if getattr(self, 'is_binary', False):
            plt.plot(self.roc_auc['roc'][0], self.roc_auc['roc'][1],
                     label=f'(AUC = {self.roc_auc["auc"]:.2f})',
                     color=colors[0])
        else:
            for i, (label, roc_auc) in enumerate(self.roc_auc.items()):
                plt.plot(roc_auc['roc'][0], roc_auc['roc'][1],
                         label=f'Class `{label}`: {roc_auc["auc"]:.2f}',
                         color=colors[i % len(colors)]
                         )

        plt.title(' ')
        plt.xlabel('False Positive Rate', color='white')
        plt.ylabel('True Positive Rate', color='white')
        # plt.legend(loc='lower right', facecolor='black', edgecolor='white', fontsize='medium')
        plt.grid(alpha=0.3, color='gray')
        plt.show()

    def save(self, directory, name):
        if not os.path.exists(directory):
            os.makedirs(directory)
        directory = os.path.join(directory, name)
        if not os.path.exists(directory):
            os.makedirs(directory)

        self.model.save(os.path.join(directory, 'Model.keras'))

        write = self.write
        model = self.model

        self.model = None
        self.write = print

        with open(os.path.join(directory, 'Instance.pkl'), 'wb') as file:
            pickle.dump(self, file)

        self.write = write
        self.model = model
        
        self.write(f'Model has been saved at `{directory}`.')

    def _validate_dataset(self, min_dimension: int=28, max_dimension: int=56):
        if (d := self.shape[0]) < min_dimension:
            self.write(f'Dataset dimension [{d}x{d}] is too small, upsampling to [{min_dimension}x{min_dimension}].')
            self.__upsample(min_dimension=min_dimension)
        elif (d := self.shape[0]) > max_dimension:
            self.write(f'Dataset dimension [{d}x{d}] is too large, downsampling to [{max_dimension}x{max_dimension}].')
            self.__downsample(max_dimension=max_dimension)
            
    def __upsample(self, min_dimension: int = 28):
        self.dataset = pd.concat([self.dataset[[self.label]], pd.DataFrame(
            self.dataset.drop(columns=[self.label]).apply(
            lambda row: cv.resize(
                src=row.values.reshape(self.shape),
                dsize=(min_dimension, min_dimension),
                interpolation=cv.INTER_LINEAR
            ).flatten(),
            axis=1
        ).tolist(),
            columns=[f'Pixel_{i}' for i in range(1, min_dimension**2 + 1)]
        )], axis=1)
        self.shape = (min_dimension, min_dimension)

    def __downsample(self, max_dimension: int = 56):
        self.dataset = pd.concat([self.dataset[[self.label]], pd.DataFrame(
            self.dataset.drop(columns=[self.label]).apply(
            lambda row: cv.resize(
                src=np.nan_to_num(row.values.reshape(self.shape)),
                dsize=(max_dimension, max_dimension),
                interpolation=cv.INTER_AREA
            ).flatten(),
            axis=1
        ).tolist(),
            columns=[f'Pixel_{i}' for i in range(1, max_dimension**2 + 1)]
        )], axis=1)
        self.shape = (max_dimension, max_dimension)

    @staticmethod
    def _generate_model(complexity: int, input_shape: tuple, classes_count: int):
        try:
            layers = [Layers.Input(shape=(*input_shape, 1))]
            for _ in range(complexity):
                layers += [
                    Layers.Conv2D(complexity * 8, (3, 3), padding='same', activation='relu'),
                    Layers.MaxPooling2D(pool_size=(2, 2), padding='same'),
                ]
            layers += [
                Layers.Flatten(),
                Layers.Dense(complexity * 8 * ((input_shape[0] // (complexity ** 2)) ** 2), activation='relu'),
                Layers.Dropout(0.25),
                Layers.Dense(classes_count, activation='softmax')
            ]
            return Models.Sequential(layers)
        except tensorflow.errors.ResourceExhaustedError:
            print(f'Memory allocation failed for the network with a linear size of `{complexity * 8 * ((input_shape[0] // (complexity ** 2)) ** 2)}`.')
            sys.exit()

    @staticmethod
    def load(instance_path, model_path):
        if model_path is None or instance_path is None:
            raise ValueError('Required files (`.pkl`, `.keras`) were not found.')
        with open(instance_path, 'rb') as pickle_path:
            instance = pickle.load(pickle_path)
        instance.model = Models.load_model(model_path)
        return instance