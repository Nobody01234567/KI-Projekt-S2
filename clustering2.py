import pandas as pd 
import numpy as np
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from IPython.display import clear_output

# weather data for Sacramento
weatherdf = pd.read_csv('USW00023271_2021.csv')

features = ['prcp', 'tmax', 'tmin']

weatherdf = weatherdf.dropna(subset=features)

data = weatherdf[features].copy()

data = data.astype(int)
data = ((data - data.min()) / (data.max() - data.min())) * 9 + 1

def randomCentroids(data, k):
    centroids = []
    for i in range(k):
        centroid = data.apply(lambda x: float(x.sample()))
        centroids.append(centroid)
    return pd.concat(centroids, axis=1)

centroids = randomCentroids(data, 3)

def getLabels(data, centroids):
    distances = centroids.apply(lambda x: np.sqrt(((data - x) ** 2).sum(axis=1)))
    return distances.idxmin(axis=1)    

labels = getLabels(data, centroids)

def newCentroids(data, labels, k):
    return data.groupby(labels).apply(lambda x: np.exp(np.log(x).mean())).T


def update_plot(frame):
    global centroids, labels
    
    old_centroids = centroids.copy()

    labels = getLabels(data, centroids)

    centroids = newCentroids(data, labels, k)

    plotClusters(data, labels, centroids, frame+1)

    return centroids.equals(old_centroids)


def init_plot():
    fig, ax = plt.subplots()
    ax.set_title('Clustering Animation')
    ax.scatter([], [], c=[], cmap='viridis')
    return fig, ax


def plotClusters(data, labels, centroids, iteration):
    pca = PCA(n_components=2)
    data_2d = pca.fit_transform(data)
    centroids_2d = pca.fit_transform(centroids.T)
    ax.clear()
    ax.set_title(f'Iteration {iteration}')
    ax.scatter(x=data_2d[:, 0], y=data_2d[:, 1], c=labels)
    ax.scatter(x=centroids_2d[:, 0], y=centroids_2d[:, 1], c='red')


max_iterations = 100 
k = 2

centroids = randomCentroids(data, k)
labels = getLabels(data, centroids)

fig, ax = init_plot()
animation = FuncAnimation(fig, update_plot, frames=max_iterations-1, interval=500, repeat=False)

plt.show()

