# import statements
from sklearn.datasets import make_blobs
import numpy as np
import matplotlib.pyplot as plt
# import KMeans
from sklearn.cluster import KMeans

# create np array for data points
points = [[1,1,1],[2,2,2],[3,3,3],[1,1,1],[2,2,2],[2,2,2],[5,3,5]]
# create kmeans object
kmeans = KMeans(n_clusters=3)
# fit kmeans object to data
kmeans.fit(points)
# print location of clusters learned by kmeans object
print(kmeans.cluster_centers_)
# save new clusters for chart
y_km = kmeans.fit_predict(points)

# create scatter plot
plt.scatter(points, points, c=points, cmap='viridis')
plt.xlim(-15,15)
plt.ylim(-15,15)

plt.show()