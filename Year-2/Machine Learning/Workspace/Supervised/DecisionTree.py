import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from io import StringIO
from typing import Literal

from sklearn.metrics import (confusion_matrix,
                             accuracy_score, 
                             precision_score,
                             recall_score,
                             f1_score,
                             classification_report,
                             mean_absolute_error,
                             mean_absolute_percentage_error,
                             mean_squared_error,
                             root_mean_squared_error,
                             explained_variance_score,
                             r2_score)

from Workspace.PreProcessing.PreProcessing import split

from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor, plot_tree

#! ----- ----- ----- ----- ----- ----- ----- ----- <<<<< Classifier >>>>> ----- ----- ----- ----- ----- ----- ----- -----

class DecisionTree_ClassifierModel(DecisionTreeClassifier):
    def __init__(self, dataframe: pd.DataFrame,
                       label_column: str,
                       splitter: str|Literal['best', 'random'],
                       criterion: str|Literal['gini', 'entropy', 'log_loss'],
                       max_depth: int,
                       min_impurity_decrease: float,
                       random_state: int,
                       split_method: str|Literal['Holdout', 'K- Fold'],
                       test_size: float
                       ):

        super().__init__(splitter=splitter,
                         criterion=criterion,
                         max_depth=max_depth,
                         min_impurity_decrease=min_impurity_decrease,
                         random_state=random_state,
                         )

        self.dataframe = dataframe
        self.label_column = label_column
        self.random_state = random_state
        self.split_method = split_method
        self.test_size = test_size

    def split_data(self):
        self.x_train, self.x_test, self.y_train, self.y_test = split(dataframe=self.dataframe,
                                                                     _label_column=self.label_column,
                                                                     _method=self.split_method,
                                                                     _test_size=self.test_size,
                                                                     _random_state=self.random_state)

        self.train_data = pd.concat(objs=[self.x_train, self.y_train], axis=1)
        train_data_buffer = StringIO()
        self.train_data.info(buf=train_data_buffer)
        self.train_data_info = train_data_buffer.getvalue().replace("<class 'pandas.core.frame.DataFrame'>",
                                                                    "Decision Tree Train Data Information:")

        self.test_data = pd.concat(objs=[self.x_test, self.y_test], axis=1)
        test_data_buffer = StringIO()
        self.test_data.info(buf=test_data_buffer)
        self.test_data_info = test_data_buffer.getvalue().replace("<class 'pandas.core.frame.DataFrame'>",
                                                                  "Decision Tree Test Data Information:")

    def train(self):
        self.fit(self.x_train, self.y_train)

    def test(self):
        self.y_pred    = self.predict(self.x_test)
        self.confusion = confusion_matrix(self.y_test, self.y_pred)
        self.report    = classification_report(self.y_test, self.y_pred)
        self.accuracy  = accuracy_score(self.y_test, self.y_pred)
        self.precision = precision_score(self.y_test, self.y_pred, average='weighted')
        self.recall    = recall_score(self.y_test, self.y_pred, average='weighted')
        self.f1        = f1_score(self.y_test, self.y_pred, average='weighted')

    def plot_tree(self):
        plt.figure('Decision Tree', figsize=(15, 10))
        plot_tree(self, filled=True, rounded=True, feature_names=self.x_train.columns, fontsize=10)
        plt.tight_layout()
        plt.show()

    def plot_confusion_matrix(self):
        plt.figure('Confusion Matrix', figsize=(7, 5))
        sns.heatmap(self.confusion, annot=True, fmt='d', cmap='Blues', linewidths=.5)
        plt.xlabel('Predicted Labels'); plt.ylabel('True Labels')
        plt.title('Decision Tree Confusion Matrix', y=1.025)
        plt.tight_layout()
        plt.show()

#! ----- ----- ----- ----- ----- ----- ----- ----- <<<<< Regressor >>>>> ----- ----- ----- ----- ----- ----- ----- -----

class DecisionTree_RegressorModel(DecisionTreeRegressor):
    def __init__(self, dataframe: pd.DataFrame,
                       label_column: str,
                       splitter: str|Literal['best', 'random'],
                       criterion: str|Literal['gini', 'entropy', 'log_loss'],
                       max_depth: int,
                       min_impurity_decrease: float,
                       random_state: int,
                       split_method: str|Literal['Holdout', 'K- Fold'],
                       test_size: float
                       ):

        super().__init__(splitter=splitter,
                         criterion=criterion,
                         max_depth=max_depth,
                         min_impurity_decrease=min_impurity_decrease,
                         random_state=random_state,
                         )

        self.dataframe = dataframe
        self.label_column = label_column
        self.random_state = random_state
        self.split_method = split_method
        self.test_size = test_size

    def split_data(self):
        self.x_train, self.x_test, self.y_train, self.y_test = split(dataframe=self.dataframe,
                                                                     _label_column=self.label_column,
                                                                     _method=self.split_method,
                                                                     _test_size=self.test_size,
                                                                     _random_state=self.random_state)
        
        self.train_data = pd.concat(objs=[self.x_train, self.y_train], axis=1)
        train_data_buffer = StringIO()
        self.train_data.info(buf=train_data_buffer)
        self.train_data_info = train_data_buffer.getvalue().replace("<class 'pandas.core.frame.DataFrame'>",
                                                                    "Decision Tree Train Data Information:")

        self.test_data = pd.concat(objs=[self.x_test, self.y_test], axis=1)
        test_data_buffer = StringIO()
        self.test_data.info(buf=test_data_buffer)
        self.test_data_info = test_data_buffer.getvalue().replace("<class 'pandas.core.frame.DataFrame'>",
                                                                  "Decision Tree Test Data Information:")

    def train(self):
        self.fit(self.x_train, self.y_train)

    def test(self):
        self.y_pred                   = self.predict(self.x_test)        
        self.explained_variance       = explained_variance_score(self.y_test, self.y_pred) 
        self.mean_absolute_percentage = mean_absolute_percentage_error(self.y_test, self.y_pred)
        self.mean_absolute            = mean_absolute_error(self.y_test, self.y_pred)
        self.mean_squared             = mean_squared_error(self.y_test, self.y_pred)
        self.root_mean_squared        = root_mean_squared_error(self.y_test, self.y_pred)
        self.r2                       = r2_score(self.y_test, self.y_pred)

    def plot_tree(self):
        plt.figure('Decision Tree', figsize=(15, 10))
        plot_tree(self, filled=True, rounded=True, feature_names=self.x_train.columns, fontsize=10)
        plt.tight_layout()
        plt.show()

    def plot_regression(self):
        plt_range = list(range(len(self.y_test)))
        fig, ax = plt.subplots(figsize=(5, 5))
        fig.patch.set_facecolor('#080808')
        ax.set_facecolor('#101010')

        ax.scatter(plt_range, self.y_test, color='red', s=50)
        ax.plot(plt_range, self.y_pred, color='white')

        for i in range(len(self.y_test)):
            ax.plot([plt_range[i], plt_range[i]], [self.y_test.iloc[i, 0], self.y_pred[i]], color='red')

        ax.set_title('Decision Tree Regression', color='white', y=1.025)
        ax.tick_params(axis='both', colors='#D8D8D8')

        for edge in ['bottom', 'top', 'left', 'right']:
            ax.spines[edge].set_color('#D8D8D8')
        ax.grid(color='#D8D8D8')

        plt.tight_layout()
        plt.show()
