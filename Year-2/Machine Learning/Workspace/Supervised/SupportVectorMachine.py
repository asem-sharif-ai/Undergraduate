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

from copy import deepcopy
from sklearn.svm import SVC, SVR

#! ----- ----- ----- ----- ----- ----- ----- ----- <<<<< Classifier >>>>> ----- ----- ----- ----- ----- ----- ----- -----

class SVCModel(SVC):
    def __init__(self, dataframe: pd.DataFrame,
                       label_column: str,
                       C: float,
                       kernel: str|Literal['gini', 'entropy', 'log_loss'],
                       max_iter: int,
                       tol: float,
                       random_state: int,
                       test_size: float,
                       split_method: str|Literal['Holdout', 'K-Fold']
                       ):

        super().__init__(C=C,
                         kernel=kernel,
                         max_iter=max_iter,
                         tol=tol,
                         random_state=random_state
                         )

        self.dataframe = dataframe
        self.label_column = label_column
        self.random_state = random_state
        self.split_method = split_method
        self.test_size = test_size
        self.copy = deepcopy(self)

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
                                                                    "Support Vector Machine Train Data Information:")

        self.test_data = pd.concat(objs=[self.x_test, self.y_test], axis=1)
        test_data_buffer = StringIO()
        self.test_data.info(buf=test_data_buffer)        
        self.test_data_info = test_data_buffer.getvalue().replace("<class 'pandas.core.frame.DataFrame'>",
                                                                  "Support Vector Machine Test Data Information:")

    def train(self):
        self.fit(self.x_train, self.y_train)

    def test(self):
        self.y_pred = self.predict(self.x_test)
        self.confusion = confusion_matrix(self.y_test, self.y_pred)
        self.report    = classification_report(self.y_test, self.y_pred)
        self.accuracy  = accuracy_score(self.y_test, self.y_pred)
        self.precision = precision_score(self.y_test, self.y_pred, average='weighted')
        self.recall    = recall_score(self.y_test, self.y_pred, average='weighted')
        self.f1        = f1_score(self.y_test, self.y_pred, average='weighted')

    def plot_confusion_matrix(self):
        plt.figure('Confusion Matrix', figsize=(7, 5))
        sns.heatmap(self.confusion, annot=True, fmt='d', cmap='Blues', linewidths=.5)
        plt.xlabel('Predicted Labels'); plt.ylabel('True Labels')
        plt.title('Support Vector Machine Confusion Matrix', y=1.025)
        plt.tight_layout()
        plt.show()

    def plot_machine(self, x_ax, y_ax):
        X = self.dataframe[[x_ax, y_ax]].values
        y = self.dataframe[self.label_column].values

        self.copy.fit(X, y)
        fig = plt.figure(figsize=(12, 6))

        ax1 = fig.add_subplot(121)
        ax1.scatter(X[:, 0], X[:, 1], c=y, cmap='viridis', edgecolors='k', marker='o')
        ax1.grid(True)
        xlim = ax1.get_xlim()
        ylim = ax1.get_ylim()
        xx = np.linspace(xlim[0], xlim[1], 30)
        yy = np.linspace(ylim[0], ylim[1], 30)
        YY, XX = np.meshgrid(yy, xx)
        xy = np.vstack([XX.ravel(), YY.ravel()]).T
        Z = self.copy.predict(xy).reshape(XX.shape)
        ax1.contourf(XX, YY, Z, alpha=0.5, cmap='viridis')
        ax1.set_xlabel(x_ax, fontsize=10)
        ax1.set_ylabel(y_ax, fontsize=10)

        ax2 = fig.add_subplot(122, projection='3d')
        ax2.scatter(X[:, 0], X[:, 1], y, c=y, cmap='viridis', edgecolors='k', marker='o')
        ax2.grid(True)
        for i in range(len(np.unique(y))):
            ax2.contour(XX, YY, Z == i, zdir='z', offset=i, cmap='viridis', alpha=0.5)

        ax2.set_xlabel(x_ax, fontsize=10)
        ax2.set_ylabel(y_ax, fontsize=10)
        ax2.set_zlabel('Label', fontsize=10)
        ax2.set_zticks(np.unique(y))
        ax2.view_init(elev=30, azim=145)

        plt.tight_layout()
        plt.show()

#! ----- ----- ----- ----- ----- ----- ----- ----- <<<<< Regressor >>>>> ----- ----- ----- ----- ----- ----- ----- -----

class SVRModel(SVR):
    def __init__(self, dataframe: pd.DataFrame,
                       label_column: str,
                       C: float,
                       kernel: str|Literal['gini', 'entropy', 'log_loss'],
                       max_iter: int,
                       tol: float,
                       random_state: int,
                       test_size: float,
                       split_method: str|Literal['Holdout', 'K-Fold']
                       ):

        super().__init__(C=C,
                         kernel=kernel,
                         max_iter=max_iter,
                         tol=tol
                         )

        self.dataframe = dataframe
        self.label_column = label_column
        self.random_state = random_state
        self.split_method = split_method
        self.test_size = test_size
        self.copy = deepcopy(self)

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
                                                                    "Support Vector Machine Train Data Information:")

        self.test_data = pd.concat(objs=[self.x_test, self.y_test], axis=1)
        test_data_buffer = StringIO()
        self.test_data.info(buf=test_data_buffer)
        self.test_data_info = test_data_buffer.getvalue().replace("<class 'pandas.core.frame.DataFrame'>",
                                                                  "Support Vector Machine Test Data Information:")

    def train(self):
        self.fit(self.x_train, self.y_train)

    def test(self):
        self.y_pred = self.predict(self.x_test)
        self.explained_variance = explained_variance_score(self.y_test, self.y_pred) 
        self.mean_absolute_percentage = mean_absolute_percentage_error(self.y_test, self.y_pred)
        self.mean_absolute = mean_absolute_error(self.y_test, self.y_pred)
        self.mean_squared  = mean_squared_error(self.y_test, self.y_pred)
        self.root_mean_squared  = root_mean_squared_error(self.y_test, self.y_pred)
        self.r2 = r2_score(self.y_test, self.y_pred)

    def plot_machine(self, x_ax, y_ax):
        X = self.dataframe[[x_ax, y_ax]].values
        y = self.dataframe[self.label_column].values

        self.copy.fit(X, y)
        self.copy.predict(X)

        fig = plt.figure(figsize=(10, 7))
        ax = fig.add_subplot(111, projection='3d')

        ax.scatter(X[:, 0], X[:, 1], y, color='black', label='Data')

        x0_range = np.linspace(X[:, 0].min(), X[:, 0].max(), 100)
        x1_range = np.linspace(X[:, 1].min(), X[:, 1].max(), 100)
        x0_mesh, x1_mesh = np.meshgrid(x0_range, x1_range)
        X_mesh = np.c_[x0_mesh.ravel(), x1_mesh.ravel()]
        y_pred_mesh = self.copy.predict(X_mesh)
        y_pred_mesh = y_pred_mesh.reshape(x0_mesh.shape)

        ax.plot_surface(x0_mesh, x1_mesh, y_pred_mesh, cmap='viridis', alpha=0.5)

        ax.set_xlabel(x_ax)
        ax.set_ylabel(y_ax)
        ax.set_zlabel(self.label_column)

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