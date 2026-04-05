
import numpy as np
import pandas as pd

from typing import Union, Literal, Optional

from sklearn.impute import SimpleImputer

from sklearn.preprocessing import (LabelEncoder, OneHotEncoder, 
                                   StandardScaler, MinMaxScaler)

from imblearn.over_sampling import SMOTE, SMOTEN, SMOTENC, ADASYN, RandomOverSampler
from imblearn.under_sampling import NearMiss, RandomUnderSampler

from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import (RandomForestClassifier, GradientBoostingClassifier)

from sklearn.decomposition import PCA
from sklearn.feature_selection import RFE

from sklearn.model_selection import KFold, train_test_split

#! ----- ----- ----- ----- ----- ----- ----- ----- <<<<< Drop Rows/Columns/Values >>>>> ----- ----- ----- ----- ----- ----- ----- -----

def drop_column(dataframe: pd.DataFrame, _column_name: str) -> pd.DataFrame:
    return dataframe.drop(columns=[_column_name])

def drop_row(dataframe: pd.DataFrame, _row_index: int|str) -> pd.DataFrame:
    if _row_index.isdigit():
        dataframe = dataframe.drop(index=int(_row_index), axis=0)
    else:
        try:    start = int(_row_index.split(':')[0])
        except: start = 0
        try:    end   = int(_row_index.split(':')[1])
        except: end   = dataframe.index.get_loc(dataframe.index[-1])

        dataframe = dataframe.drop(index=range(start, end+1))
    return dataframe.reset_index(drop=True)

def drop_value(dataframe: pd.DataFrame, _value: any, _axis: int|Literal[0, 1]):
    return (dataframe[dataframe.ne(_value).all(axis=1)] if _axis == 0 else dataframe.loc[:, dataframe.ne(_value).all()])

def replace_value(dataframe, _old, _new):
    return dataframe.replace(_old, _new)

#! ----- ----- ----- ----- ----- ----- ----- ----- <<<<< Handle NaN >>>>> ----- ----- ----- ----- ----- ----- ----- -----

def drop_na(dataframe: pd.DataFrame, _axis: int|Literal[0, 1], _how: str|Literal['Any', 'All']) -> pd.DataFrame:
    dataframe.dropna(inplace=True, axis=_axis, how=_how.lower())
    return dataframe

def fill_na(dataframe: pd.DataFrame,
            _method: Union[Literal['bfill', 'ffill'], None] = None,
            _value: Union[any, None] = None) -> pd.DataFrame:
    if _value is not None:
        dataframe.fillna(value=_value, inplace=True)
    elif _method:
        if _method in ['Mean', 'Median', 'Most Frequent']:
            nan = dataframe.isna()
            dataframe.fillna(value={'Mean': dataframe.where(~nan).mean(),
                                    'Median': dataframe.where(~nan).median(),
                                    'Most Frequent': dataframe.where(~nan).mode().iloc[0]}[_method], inplace=True)
        elif _method == 'bfill':
            dataframe.bfill(inplace=True)
        elif _method == 'ffill':
            dataframe.ffill(inplace=True)
    return dataframe

#! ----- ----- ----- ----- ----- ----- ----- ----- <<<<< Imputer >>>>> ----- ----- ----- ----- ----- ----- ----- -----

def impute(dataframe: pd.DataFrame, _column: str, _strategy: Literal['mean', 'median', 'most_frequent']) -> pd.DataFrame:
    imputer = SimpleImputer(strategy=_strategy)
    dataframe[_column] = imputer.fit_transform(dataframe[[_column]])[:, 0]
    return dataframe

#! ----- ----- ----- ----- ----- ----- ----- ----- <<<<< Encoder >>>>> ----- ----- ----- ----- ----- ----- ----- -----

def encode(dataframe: pd.DataFrame, _column: str, _encoder: str|Literal['Label', 'One Hot']) -> pd.DataFrame:
    if _encoder == 'Label':
        encoder = LabelEncoder()
        dataframe[_column] = encoder.fit_transform(dataframe[_column])
    else:
        columns = dataframe.columns.tolist()
        encoder = OneHotEncoder()
        encoded_columns = encoder.fit_transform(dataframe[[_column]])
        encoded_columns = pd.DataFrame(encoded_columns.toarray(), columns=encoder.get_feature_names_out([_column]))
        dataframe = dataframe.drop(columns=[_column], axis=1)
        for i, col in enumerate(encoded_columns.columns):
            dataframe.insert(columns.index(_column) + i, col, encoded_columns[col].values)

    return dataframe

#! ----- ----- ----- ----- ----- ----- ----- ----- <<<<< Scaler >>>>> ----- ----- ----- ----- ----- ----- ----- -----

def scale(dataframe: pd.DataFrame, _label_column: str, _scaler: str|Literal['Standard', 'Min Max']) -> pd.DataFrame:
    if _scaler == 'Standard':
        scaler = StandardScaler(copy=True, with_mean=True, with_std=True) 
    else:
        scaler = MinMaxScaler()

    x = scaler.fit_transform(dataframe.drop(columns=[_label_column], axis=1).values)
    dataframe[dataframe.columns[dataframe.columns != _label_column]] = x

    return dataframe

#! ----- ----- ----- ----- ----- ----- ----- ----- <<<<< Features Selection >>>>> ----- ----- ----- ----- ----- ----- ----- -----

def select_features(dataframe: pd.DataFrame,
                    _label_column: str,
                    _sub_model: str|Literal['linear', 'poly', 'sigmoid', 'precomputed', 'rbf'],
                    _n_features: int):

    x = dataframe.drop(columns=[_label_column], axis=1)
    y = dataframe[_label_column]

    if _sub_model == 'Support Vector Machine':
        _sub_model = SVC(kernel='linear')
    elif _sub_model == 'Decision Tree':
        _sub_model = DecisionTreeClassifier()
    elif _sub_model == 'Random Forest':
        _sub_model = RandomForestClassifier()
    elif _sub_model == 'Neural Network':
        _sub_model = MLPClassifier()
    elif _sub_model == 'K-Neighbors':
        _sub_model = KNeighborsClassifier()
    elif _sub_model == 'Gradient Boosting':
        _sub_model = GradientBoostingClassifier()
    elif _sub_model == 'Logistic Regression':
        _sub_model = LogisticRegression(solver='liblinear')

    model = RFE(_sub_model, n_features_to_select=_n_features)
    model.fit(x, y)

    dataframe = pd.concat(objs=[pd.DataFrame(data=x[x.columns[model.support_]],
                                             columns=[x.columns[i] for i in range (len(x.columns)) if model.support_[i]]),
                                pd.DataFrame(data=y.reset_index(drop=True),
                                             columns=[_label_column])],
                          axis=1)
    return dataframe

#! ----- ----- ----- ----- ----- ----- ----- ----- <<<<< Principal Components Analysis >>>>> ----- ----- ----- ----- ----- ----- ----- -----

def analyse_principal_components(dataframe: pd.DataFrame, _label_column: str, _n_components: int):
    x = dataframe.drop(columns=[_label_column], axis=1)
    y = dataframe[_label_column]

    model = PCA(n_components=_n_components)
    dataframe = pd.concat(objs=[pd.DataFrame(data=model.fit_transform(x),
                                             columns=[f'PC_{i:02}' for i in range(1, _n_components+1)]),
                                pd.DataFrame(data=y.reset_index(drop=True),
                                             columns=[_label_column])],
                          axis=1)
    return dataframe

#! ----- ----- ----- ----- ----- ----- ----- ----- <<<<< Resolve Imbalance >>>>> ----- ----- ----- ----- ----- ----- ----- -----

def resolve_imbalance(dataframe: pd.DataFrame,
                      _label_column: str,
                      _resolve_method: str|Literal['Oversampling', 'Undersampling']) -> pd.DataFrame:
    x = dataframe.drop(columns=[_label_column], axis=1)
    y = dataframe[_label_column]

    if _resolve_method == 'Oversampling - SMOTE':
        model = SMOTE()
    elif _resolve_method == 'Oversampling - SMOTEN':
        model = SMOTEN()
    elif _resolve_method == 'Oversampling - SMOTENC':
        model = SMOTENC()
    elif _resolve_method == 'Oversampling - ADASYN':
        model = ADASYN()
    elif _resolve_method == 'Oversampling - Random':
        model = RandomOverSampler()
    elif _resolve_method == 'Undersampling - NearMiss':
        model = NearMiss()
    elif _resolve_method == 'Undersampling - Random':
        model = RandomUnderSampler()

    _x, _y = model.fit_resample(x, y)
    dataframe = pd.concat(
        objs=[pd.DataFrame(_x, columns=[i for i in dataframe.columns if i != _label_column]),
              pd.DataFrame(_y, columns=[_label_column])],
        axis=1)

    return dataframe

#! ----- ----- ----- ----- ----- ----- ----- ----- <<<<< Data Split >>>>> ----- ----- ----- ----- ----- ----- ----- -----

def split(dataframe: pd.DataFrame,
          _label_column: str,
          _method: Literal['Holdout', 'K-Fold'],
          _test_size: Optional[float],
          _random_state: Optional[int]) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:

    x = dataframe.drop(columns=[_label_column], axis=1)
    y = dataframe[_label_column]

    if _test_size    == None: _test_size    = 0.25
    if _random_state == None: _random_state = 42

    if _method == 'Holdout':
        x_train, x_test, y_train, y_test = (pd.DataFrame(i) for i in train_test_split(x, y, test_size=_test_size, random_state=_random_state))
    else:
        model = KFold(n_splits=round(1/_test_size), random_state=_random_state, shuffle=True)
        for train_i, test_i in model.split(x):
            x_train, x_test = x.iloc[train_i], x.iloc[test_i]
            y_train, y_test = y.iloc[train_i], y.iloc[test_i]

    return x_train, x_test, y_train, y_test