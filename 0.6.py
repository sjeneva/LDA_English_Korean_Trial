import numpy as np
import matplotlib.pyplot as plt

# Generate example data (same as before)
np.random.seed(0)
data = np.random.randn(100, 2)

# Parameters
num_neurons = 4  # Number of neurons in the output layer
learning_rate = 0.1
epochs = 100

# Initialize neurons (weights)
neurons = np.random.randn(num_neurons, data.shape[1])

# Training process
for epoch in range(epochs):
    for i in range(data.shape[0]):
        # Compute distances to each neuron
        distances = np.linalg.norm(data[i] - neurons, axis=1)
        # Find the winning neuron
        winner_index = np.argmin(distances)
        # Update the weights of the winning neuron
        neurons[winner_index] += learning_rate * (data[i] - neurons[winner_index])

# Plot the data points and neurons
plt.scatter(data[:, 0], data[:, 1], c='blue', label='Data Points')
plt.scatter(neurons[:, 0], neurons[:, 1], c='red', s=200, label='Neurons')
plt.xlabel('Feature 1')
plt.ylabel('Feature 2')
plt.title('Competitive Neural Network')
plt.legend()
plt.show()
