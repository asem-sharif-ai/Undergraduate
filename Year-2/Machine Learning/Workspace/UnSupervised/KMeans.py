import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from io import StringIO
from typing import Literal

from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score, calinski_harabasz_score, davies_bouldin_score

from sklearn.model_selection import GridSearchCV
from yellowbrick.cluster import KElbowVisualizer

class KMeans_Model(KMeans):
    def __init__(self, dataframe: pd.DataFrame,
                       label_column: str,
                       n_clusters: int,
                       algorithm: str|Literal['lloyd', 'elkan'],
                       init: str|Literal['k-means++', 'random'],
                       n_init: int|Literal['auto'],
                       max_iter: int,
                       tol: float,
                       random_state: int,
                       ):

        super().__init__(n_clusters=n_clusters,
                         algorithm=algorithm,
                         init=init,
                         n_init=n_init,
                         max_iter=max_iter,
                         tol=tol,
                         random_state=random_state
                        )

        self.dataframe = dataframe
        self.label_column = label_column
        self.random_state = random_state


        dataframe_buffer = StringIO()
        self.dataframe.info(buf=dataframe_buffer)
        self.dataframe_info = dataframe_buffer.getvalue().replace("<class 'pandas.core.frame.DataFrame'>",
                                                                    "K-Means Clustering Data Information:")

    def cluster(self):
        self.fit(self.dataframe)

        self.centers = self.cluster_centers_
        self.inertia = self.inertia_
        self.silhouette = silhouette_score(self.dataframe, self.labels_)
        self.davies_bouldin = davies_bouldin_score(self.dataframe, self.labels_)
        self.calinski_harabasz = calinski_harabasz_score(self.dataframe, self.labels_)

    def assign_clusters(self):
        self.dataframe[self.label_column] = self.predict(self.dataframe)
    
    def plot_clusters(self, x_ax, y_ax, z_ax=None):
        X = self.dataframe[[x_ax]].values
        Y = self.dataframe[[y_ax]].values
        if z_ax is None:
            fig, ax = plt.subplots()
            fig.patch.set_facecolor('#080808')
            ax.set_facecolor('#101010')
            ax.scatter(X[:, 0], Y[:, 0], c=self.labels_, cmap='viridis', edgecolors='white', s=50, linewidths=1)
            ax.scatter(self.cluster_centers_[:, 0], self.cluster_centers_[:, 1], marker='x', s=100, c='white')
        else:
            Z = self.dataframe[[z_ax]].values
            fig = plt.figure()
            fig.patch.set_facecolor('#080808')
            ax = fig.add_subplot(111, projection='3d')
            ax.set_facecolor('#080808')

            ax.scatter(X[:, 0], Y[:, 0], Z[:, 0], c=self.labels_, cmap='viridis', edgecolors='white', s=50, linewidths=1)
            ax.scatter(self.cluster_centers_[:, 0], self.cluster_centers_[:, 1], self.cluster_centers_[:, 2], marker='x', s=100, c='white')
            ax.set_zlabel(z_ax, color='#D8D8D8')
        ax.set_xlabel(x_ax, color='#D8D8D8')
        ax.set_ylabel(y_ax, color='#D8D8D8')

        ax.tick_params(axis='both', colors='#D8D8D8')
        for edge in ['bottom', 'top', 'left', 'right']:
            ax.spines[edge].set_color('#D8D8D8')
        ax.grid(color='#D8D8D8')

        plt.tight_layout()
        plt.show()

    def grid_search(self):
        self.params = {'n_clusters'  : list(range(2, 21)),
                       'algorithm'   : ['lloyd', 'elkan'],
                       'init'        : ['k-means++', 'random']
                       }

        self.tuner_grid = GridSearchCV(self, self.params, cv=5).fit(self.dataframe)
        self.visualizer = KElbowVisualizer(self.tuner_grid.best_estimator_, k=(2, 21)).fit(self.dataframe)

        self.visualizer.ax.tick_params(axis='both', which='major', labelsize=10)
        self.visualizer.show()