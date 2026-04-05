import numpy  as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier

from sklearn.feature_selection import RFE
from sklearn.decomposition import PCA

def set_dtype(input_string): # `dtype:value`
    DTYPES = {
        'float': float,
        'int': int,
        'str': str,
        'bool': bool,
        'complex': complex,
    }

    if input_string.lower() == 'nan':
        return np.nan
    elif input_string.lower() == 'none':
        return None
    else:
        try:
            dtype, value = input_string.split(':', 1)
        except:
            return input_string
        else:
            if dtype in DTYPES:
                try:
                    if dtype.lower() == 'bool':
                        return {'true' : True , '1': True,
                                'false': False, '0': False} [value.lower()]
                    else:
                        return DTYPES[dtype.lower()](value)
                except:
                    return input_string
            else:
                return input_string


def count_na(dataframe, axis):
    return dataframe.isna().any(axis=axis).sum()

def get_na_indices(dataframe, axis):
    return dataframe[dataframe.isna().any(axis=axis)].index.values

def get_na_cols(dataframe):
    return dataframe.columns[dataframe.isna().any()].tolist()

def search(dataframe, key):
    places = []
    for col in dataframe.columns:
        if key is None:
            rows = dataframe.index[dataframe[col].isnull()].tolist()
        elif pd.isna(key):
            rows = dataframe.index[dataframe[col].isna()].tolist()
        else:
            rows = dataframe.index[dataframe[col] == key].tolist()
        for row in rows:
            places.append((col, row))
    if places == []:
        return f'Key `{key}` Was Not Found.'
    else:
        return '\n'.join([f'{str(place[0]).ljust(max(len(str(p[0])) for p in places) + 2)}: {str(place[1]).ljust(max(len(str(p[1])) for p in places) + 2)}' for place in places])


def check_balance(dataframe: pd.DataFrame, _label_column: str):
    class_counts = dataframe[_label_column].value_counts()
    if all(abs(count - class_counts.mean()) <= 0.5 * class_counts.mean() for count in class_counts):
        return (True, None)
    else:
        return (False, class_counts.idxmax())

def plot_classes(dataframe: pd.DataFrame, _label_column: str):
    plt.figure(figsize=(4, 4))
    dataframe[_label_column].value_counts().plot(kind='bar', color='k')
    plt.xticks(rotation=0)
    plt.show()

def features_rank_message(dataframe: pd.DataFrame, _label_column: str, _sub_model: str):
    if _sub_model == 'Decision Tree':
        _sub_model = DecisionTreeClassifier()
    elif _sub_model == 'Random Forest':
        _sub_model = RandomForestClassifier()
    elif _sub_model == 'Support Vector Machine':
        _sub_model = SVC(kernel='linear')
    elif _sub_model == 'Neural Network':
        _sub_model = MLPClassifier()
    elif _sub_model == 'K-Neighbors':
        _sub_model = KNeighborsClassifier()
    elif _sub_model == 'Logistic Regression':
        _sub_model = LogisticRegression(solver='liblinear')

    model = RFE(_sub_model, n_features_to_select=1)
    model.fit(dataframe.drop(columns=[_label_column], axis=1), dataframe[_label_column])

    ranks = sorted([(model.ranking_[i], dataframe.columns[i]) for i in range(len(model.ranking_))], key=lambda x: x[0])
    return_msg = '\n'.join([f'[{rank[0]:02}] {rank[1]}' for rank in ranks])
    return return_msg

def principal_components_message(dataframe: pd.DataFrame, _label_column: str):
    components = dataframe.drop(columns=[_label_column], axis=1)
    model = PCA(n_components=len(components.columns))
    model.fit_transform(components)

    var = model.explained_variance_ratio_
    cs_var = np.cumsum(var)

    weights = pd.DataFrame(data=model.components_.T, columns=[f'PC_{i:02}' for i in range(1, len(components.columns)+1)], index=components.columns)

    return_msg = f'''Explained Variance:
{'\n'.join([f'[PC_{i+1:02}] {round(var[i], 10)}' for i in range(len(var))])}\n
Cumulative Explained Variance:
{'\n'.join([f'[{i+1:02} PCs] {round(cs_var[i], 10)}' for i in range(len(cs_var))])}\n
Weights:
{'\n'.join([f'{col}:\n' + '\n'.join([f'  - [{pc}] {round(weights.loc[col, pc], 10)}' for pc in weights.columns]) + '\n' for col in components.columns])}'''

    plt.figure(figsize=(5, 5))
    plt.bar(range(0, len(var)), var, width=0.75, color='black', label='Individual Explained Variance')
    plt.step(range(0, len(var)), cs_var, color='black', label='Cumulative Explained Variance')
    plt.legend(loc='best')

    return return_msg, plt