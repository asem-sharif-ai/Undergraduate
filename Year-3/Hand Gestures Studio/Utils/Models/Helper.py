import numpy as np
import pandas as pd

import time
import json
import h5py as hdf
from io import StringIO

from tkinter import filedialog

class Helper:
    @staticmethod
    def import_dataset(filename=None) -> tuple[pd.DataFrame, str]: # return (DataFrame, Info)
        if isinstance(filename, pd.DataFrame):
            return filename, Helper.get_info(filename)
        if filename is None:
            filename = filedialog.askopenfilename(
                title='Import Dataset (HDF or CSV File).',
                filetypes=[('HDF or CSV Files', '*.h5;*.csv')]
            )
            if filename:
                try:
                    return Helper.read_csv(filename) if filename.endswith('.csv') else Helper.read_hdf(filename)
                except Exception as error:
                    return (error, None)
            else:
                return (None, None)

    @staticmethod
    def read_csv(filename):
        return (df := pd.read_csv(filename), Helper.get_info(df))

    @staticmethod
    def read_hdf(filename):
        data = []
        with hdf.File(filename, 'r') as root:
            for label in root.keys():
                group = root[label]
                for dataset in group.keys():
                    data.append(
                        {'Label': label, **{f'Pixel {i+1}': pixel for i, pixel in enumerate(group[dataset][:].flatten())}}
                        )
        return (df := pd.DataFrame(data), Helper.get_info(df))

    @staticmethod
    def export_dataset(data: dict, shape: int=None) -> str:
        filename = filedialog.asksaveasfilename(
            title='Export Dataset',
            initialfile=f'Data-[{shape}x{shape}]-[{Helper.time()}]',
            defaultextension='.h5',
            filetypes=[('HDF5 File', '*.h5'), ('CSV File', '*.csv')],
        )

        if filename.endswith('.csv'):
            rows = []
            cols = ['Label'] + [f'Pixel_{i+1}' for i in range(list(data.values())[0][0].size)]

            for label, matrices in data.items():
                for matrix in matrices:
                    rows.append([label] + matrix.flatten().tolist())
            pd.DataFrame(data=rows, columns=cols).to_csv(filename, index=False)

        elif filename and filename.endswith('.h5'):
            with hdf.File(filename, 'w') as root:
                for label, matrices in data.items():
                    group = root.create_group(label)
                    for i, matrix in enumerate(matrices):
                        group.create_dataset(f'Matrix_{i+1}', data=matrix, dtype=int)
        return filename

    @staticmethod
    def get_brief(dataframe: pd.DataFrame, lim_row: int=250, lim_col: int=30) -> pd.DataFrame:
        if len(dataframe) > lim_row:
            dataframe = dataframe.iloc[:lim_row]
        if len(dataframe.columns) > lim_col:
            dataframe = pd.concat([dataframe.iloc[:, :lim_col//2],
                                   pd.DataFrame(['...'] * len(dataframe), columns=['...']),
                                   dataframe.iloc[:, -lim_col//2:]], axis=1)
        return dataframe

    @staticmethod
    def get_info(dataframe: pd.DataFrame):
        buffer = StringIO()
        dataframe.info(buf=buffer)
        info = '\n'.join(buffer.getvalue().splitlines()[1:-1])
        buffer.close()
        return info

    @staticmethod
    def validate_dataset(dataframe: pd.DataFrame, label_column: str, writer: callable) -> bool:
        if dataframe is None:
            writer('The Dataset was not picked yet.')
            return False

        if label_column is None or label_column not in dataframe.columns:
            writer('The Dataset label was not determined or does not exist.')
            return False

        valid = True
        if dataframe.isna().any().any():
            writer('The Dataset contains NaN values.')
            valid = False

        features = dataframe.drop(columns=[label_column])
        label    = dataframe[label_column]

        if not all(features.dtypes.apply(lambda x: np.issubdtype(x, np.number))):
            writer('The Dataset contains non-numeric columns.')
            valid = False

        num_features = len(features.columns)
        if (num_features + 1) == (int(np.sqrt(num_features)) ** 2 + 1):
            shape = f'{(l := int(np.sqrt(num_features)))}x{l}'
        else:
            writer('Number of features does not match 2D square images.')
            valid = False
        
        if valid:
            writer('\n'.join([f'Label `{label_column}`: {count} x [{shape}]' for label_column, count in sorted(label.value_counts().items())]))
        return valid

    @staticmethod
    def import_settings():
        filename = filedialog.askopenfilename(
            title='Import Settings (JSON File).',
            filetypes=[('JSON Files', '*.json')]
        )
        if filename:
            with open(filename, 'r') as file:
                return json.load(file)
        else:
            return None

    @staticmethod
    def export_settings(**dicts):
        filename = filedialog.asksaveasfilename(
            title='Export Settings',
            initialfile=f'Settings-[{Helper.time()}]',
            defaultextension='.json',
            filetypes=[('JSON File', '*.json')],
        )
        if filename:
            with open(filename, 'w') as file:
                json.dump(dicts, file, indent=4)

    @staticmethod
    def export_output(text: str):
        filename = filedialog.asksaveasfilename(
            title='Export Output',
            initialfile=f'Output-[{Helper.time()}]',
            defaultextension='.txt',
            filetypes=[('Text File', '*.txt')],
        )
        if filename:
            with open(filename, 'w') as file:
                file.write(text)

    @staticmethod
    def get_directory(mkdir: bool=True):
        return filedialog.askdirectory(title='Select Model Directory', mustexist=not mkdir)

    @staticmethod
    def get_instance_and_model():
        files = filedialog.askopenfilenames(
            title='Select Instance `.pkl` and Model `.keras` files',
            filetypes=[('Keras and Pickle Files', '*.keras;*.pkl')]
        )

        if len(files) != 2:
            return None, None

        instance, model = None, None
        for file in files:
            if file.endswith('.keras'):
                model = file
            elif file.endswith('.pkl'):
                instance = file

        return (instance, model) if instance and model else (None, None)

    @staticmethod
    def time():
        t = time.localtime()
        return f'{t.tm_hour:02}.{t.tm_min:02}.{t.tm_mday:02}.{t.tm_mon:02}.{t.tm_year}'

# - H5 File:
#   - Group for each label.
#     - Dataset as each matrix in that label.

# - CSV File:
#   Label | Pixel 1 | ... Pixel N