from sklearn.cluster import KMeans
import numpy as np
import matplotlib.pyplot as plt

# Generate example data
np.random.seed(0)
data = np.random.randn(100, 2)

# Apply KMeans
kmeans = KMeans(n_clusters=3, random_state=0)
kmeans.fit(data)

# Plot the data points and centroids
plt.scatter(data[:, 0], data[:, 1], c=kmeans.labels_, cmap='viridis')
centroids = kmeans.cluster_centers_
plt.scatter(centroids[:, 0], centroids[:, 1], c='red', s=200, alpha=0.75)
plt.xlabel('Feature 1')
plt.ylabel('Feature 2')
plt.title('K-Means Clustering')
plt.show()
