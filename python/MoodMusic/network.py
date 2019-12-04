import random
import numpy as np


class Network(object):

    def __init__(self, sizes, weights=None, biases=None):
        """The list ``sizes`` contains the number of neurons in each layers of the network.
        For example, if the list was [2, 3, 1] then it would be a three-layer network, with
        the first (input) layer containing 2 neurons, the second (1st hidden) layer 3 neurons,
        and the third (output) layer 1 neuron. The biases and weights for the network are
        initialized randomly, using a Gaussian distribution with mean 0, and variance 1.
        No biases are imposed on the first layer."""
        print("Sizes:", sizes[0])
        self.num_layers = len(sizes)
        self.sizes = sizes
        self.biases = self.random_biases() if biases is None else biases
        self.weights = self.random_weights() if weights is None else weights

    def random_biases(self):
        return np.array([np.random.randn(y, 1) for y in self.sizes[1:]])

    def random_weights(self):
        return np.array([np.random.randn(y, x)
                         for x, y in zip(self.sizes[:-1], self.sizes[1:])])

    def output(self, a):
        """Return the output of the network if ``a`` is input.  Output is returned as a column
        vector of all outputs. A separate function is needed to determine which is/are used."""
        for b, w in zip(self.biases, self.weights):
            a = sigmoid(np.dot(w, a)+b)
        return a

    def get_output_index(self, inputs):
        a = self.output(inputs)[-1]
        index = 0
        max = a[0]
        for i in range(len(a)):
            if a[i] > max:
                max = a[i]
                index = i
        return index

    def SGD(self, training_data, iterations, mini_batch_size, rate,
            inputs=None):
        """Train the neural network using mini-batch stochastic gradient descent.  The
        ``training_data`` is a list of tuples ``(x, y)`` representing the training inputs and the
        desired outputs (x being inputs and y being outputs).  The other non-optional parameters
        are self-explanatory.  If ``inputs`` is provided then the network will be evaluated against
        the input data after each iteration, and partial progress printed out.  This is useful for
        tracking progress, but slows things down substantially."""
        """Example y is [0, 0, 1, 0, 0, 0] where 1 is correct output"""
        print("\nBegin Training")
        training_data = list(training_data)
        n = len(training_data)

        if inputs:
            inputs = list(inputs)
            n_input = len(inputs)
        else:
            n_input = None
        for j in range(iterations):
            random.shuffle(training_data)
            mini_batches = [
                training_data[k:k+mini_batch_size]
                for k in range(0, n, mini_batch_size)]
            for mini_batch in mini_batches:
                self.update_mini_batch(mini_batch, rate)
            if inputs:
                print("Iteration {} : {} / {}".format(j, self.evaluate(inputs), n_input))
            else:
                print("Iteration {} complete".format(j))
        print("End Training \n")

    def update_mini_batch(self, mini_batch, rate):
        """Update the network's weights and biases by applying
        gradient descent using backpropagation to a single mini batch.
        The ``mini_batch`` is a list of tuples ``(x, y)``, and ``rate``
        is the learning rate."""
        """nabla is the Greek letter used to denominate gradient"""
        nabla_b = [np.zeros(b.shape) for b in self.biases]
        nabla_w = [np.zeros(w.shape) for w in self.weights]
        for x, y in mini_batch:
            delta_nabla_b, delta_nabla_w = self.backprop(x, y)
            nabla_b = [nb+dnb for nb, dnb in zip(nabla_b, delta_nabla_b)]
            nabla_w = [nw+dnw for nw, dnw in zip(nabla_w, delta_nabla_w)]
        self.weights = [w-(rate/len(mini_batch))*nw
                        for w, nw in zip(self.weights, nabla_w)]
        self.biases = [b-(rate/len(mini_batch))*nb
                       for b, nb in zip(self.biases, nabla_b)]

    def backprop(self, x, y):
        """Return a tuple ``(nabla_b, nabla_w)`` representing the
        gradient for the cost function C_x.  ``nabla_b`` and
        ``nabla_w`` are layer-by-layer lists of numpy arrays, similar
        to ``self.biases`` and ``self.weights``."""
        nabla_b = [np.zeros(b.shape) for b in self.biases]
        nabla_w = [np.zeros(w.shape) for w in self.weights]
        # output
        activation = x
        activations = [x] # list to store all the activations, layer by layer
        zs = [] # list to store all the z vectors, layer by layer
        for b, w in zip(self.biases, self.weights):
            z = np.dot(w, activation)+b
            zs.append(z)
            activation = sigmoid(z)
            activations.append(activation)
        # backward pass
        delta = self.cost_derivative(activations[-1], y) * \
            sigmoid_prime(zs[-1])
        nabla_b[-1] = delta
        nabla_w[-1] = np.dot(delta, activations[-2].transpose())
        for l in range(2, self.num_layers):
            z = zs[-l]
            sp = sigmoid_prime(z)
            delta = np.dot(self.weights[-l+1].transpose(), delta) * sp
            nabla_b[-l] = delta
            nabla_w[-l] = np.dot(delta, activations[-l-1].transpose())
        return nabla_b, nabla_w

    def evaluate(self, inputs):
        """Return the number of input inputs for which the neural
        network outputs the correct result. Note that the neural
        network's output is assumed to be the index of whichever
        neuron in the final layer has the highest activation."""
        input_results = [(np.argmax(self.output(x)), y)
                        for (x, y) in inputs]
        return sum(int(x == y) for (x, y) in input_results)

    def cost_derivative(self, output_activations, y):
        """Return the vector of partial derivatives partial C_x /
        partial a for the output activations."""
        return output_activations - y


def sigmoid(z):
    """The sigmoid function."""
    return 1.0/(1.0+np.exp(-z))


def sigmoid_prime(z):
    """Derivative of the sigmoid function."""
    return sigmoid(z)*(1-sigmoid(z))
