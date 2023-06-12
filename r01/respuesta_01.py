import numpy as np
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split

# Cargar el dataset Iris
iris = load_iris()
X = iris.data
y = iris.target

# Dividir el dataset en conjuntos de entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
# Función de activación sigmoide
def sigmoid(x):
    return 1 / (1 + np.exp(-x))

# Derivada de la función de activación sigmoide
def sigmoid_derivative(x):
    return sigmoid(x) * (1 - sigmoid(x))

# Función de error de entropía cruzada
def cross_entropy_loss(y_true, y_pred):
    epsilon = 1e-7
    y_pred = np.clip(y_pred, epsilon, 1 - epsilon)
    return -np.mean(y_true * np.log(y_pred) + (1 - y_true) * np.log(1 - y_pred))

# Clase para representar una red neuronal
class NeuralNetwork:
    def __init__(self, input_size, hidden_size, output_size):
        # Inicializar los pesos de las conexiones con valores aleatorios
        self.weights1 = np.random.rand(input_size, hidden_size)
        self.weights2 = np.random.rand(hidden_size, hidden_size)
        self.weights3 = np.random.rand(hidden_size, output_size)

        # Inicializar los sesgos con valores aleatorios
        self.biases1 = np.random.rand(hidden_size)
        self.biases2 = np.random.rand(hidden_size)
        self.biases3 = np.random.rand(output_size)

    def feedforward(self, X):
        # Calcular la salida de la red neuronal
        hidden_layer1 = sigmoid(np.dot(X, self.weights1) + self.biases1)
        hidden_layer2 = sigmoid(np.dot(hidden_layer1, self.weights2) + self.biases2)
        output_layer = sigmoid(np.dot(hidden_layer2, self.weights3) + self.biases3)
        return output_layer

    def train(self, X, y, epochs, learning_rate):
        for epoch in range(epochs):
            # Feedforward
            hidden_layer1 = sigmoid(np.dot(X, self.weights1) + self.biases1)
            hidden_layer2 = sigmoid(np.dot(hidden_layer1, self.weights2) + self.biases2)
            output_layer = sigmoid(np.dot(hidden_layer2, self.weights3) + self.biases3)

            # Backpropagation
            output_error = y - output_layer
            output_delta = output_error * sigmoid_derivative(output_layer)

            hidden_error2 = output_delta.dot(self.weights3.T)
            hidden_delta2 = hidden_error2 * sigmoid_derivative(hidden_layer2)

            hidden_error1 = hidden_delta2.dot(self.weights2.T)
            hidden_delta1 = hidden_error1 * sigmoid_derivative(hidden_layer1)

            # Actualizar pesos y sesgos
            self.weights3 += hidden_layer2.T.dot(output_delta) * learning_rate
            self.biases3 += np.sum(output_delta, axis=0) * learning_rate

            self.weights2 += hidden_layer1.T.dot(hidden_delta2) * learning_rate
            self.biases2 += np.sum(hidden_delta2, axis=0) * learning_rate

            self.weights1 += X.T.dot(hidden_delta1) * learning_rate
            self.biases1 += np.sum(hidden_delta1, axis=0) * learning_rate

            # Calcular la pérdida en cada iteración
            loss = cross_entropy_loss(y, output_layer)
            print(f"Epoca {epoch + 1}/{epochs}, perdida: {loss}")

# Configuración de la red neuronal
input_size = X.shape[1]
hidden_size = 10
output_size = len(np.unique(y))
epochs = 1000
learning_rate = 0.1

# Crear una instancia de la red neuronal
network = NeuralNetwork(input_size, hidden_size, output_size)

# Entrenar la red neuronal
network.train(X_train, np.eye(output_size)[y_train], epochs, learning_rate)

# Evaluar la red neuronal en el conjunto de prueba
predictions = np.argmax(network.feedforward(X_test), axis=1)
accuracy = np.mean(predictions == y_test)
print("Accuracy:", accuracy)
