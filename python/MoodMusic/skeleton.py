from network import *
import json

"""Use this as a general framework to use the Network class.
To change the number of layers in a new network, change the layers list in line 24
Training data needs to be in a tuple format (x, y) with the inputs as x and the
outputs as y. Both need to be lists, such as [0.25 0.3 -0.47 0.5] and [0 0 1 0]
for a network with 4 inputs and 4 outputs.
The input data can be just a list such as [0.25 0.3 -0.47 0.5] for a network with 4
inputs. All inputs and outputs have to range from -1 to 1."""

"""Things still left to implement:
getting input data (unless importing data from .txt file
inputs are currently not being taken)"""


def getNetwork():
    """Checks to see if enough data is available to load a previously
    generated network. If not, defines the amount of layers and nodes
     in a new network and calls the function to create the network."""
    try:
        return loadNetwork()
    except:
        print("\nNetwork failed to load/No usable Network in directory \n")
        return newNetwork()


def loadNetwork():
    """Opens the three text files that contain the data of the network. Using the
    data, creates a new network and overwrites the weights and biases with the
    previously saved data (since the new network is randomly generated, this changes
    the new network into the one that was previously used). """

    n = getData('network_info.txt')
    print("Loaded Network Info Successfully")
    w = getData('weights.txt')
    print("Loaded Weights Successfully")
    b = getData('biases.txt')
    print("Loaded Biases Successfully")
    net = Network(n)
    net.biases = b
    net.weights = w
    return net

def getData(filename):
    file = open(filename, 'r')
    contents = file.read()
    replaced = ', '.join(contents.replace('[ ', '[').split())
    return np.array(json.loads(replaced))


def newNetwork(layers=np.array([6, 6])):
    """Creates and returns a new network based on the number of layers specified
    in the list. Also creates three files that contain the data of the network.
    The files are used to reload the network when the program is ran again."""
    net = Network(layers)
    print("New Network Created")
    saveNetwork(net)
    return net


def trainNetwork(net, training='training_data.txt', inputs=None, iterations=5, rate=1):
    """Requires a file (even a blank file) for training data. As many networks are given
    very large data sets for training, a mini-batch stochastic gradient descent method is
    used to train the network. The number of iterations is how many times the training
    data is used to initially train the network. While this can train the network faster,
    it can also over specialize the network to the data set. The mini batch size is the
    number of the training data items are used. Instead of training with all of the training
    data, only a number of items are used in each iteration. These are also chosen randomly
    from the training data. By default this is set based on the number of iterations. If
    the number of iterations is 5, the 20% of the data is used each iteration. If the number
    of iterations is 8, 12.5% of the data is used. The more data is used in each iteraion, the
    longer the training will take. The rate is how aggressive the changes to the weights and
    biases is. A smaller rate can help fine tune a network, but more iterations will be required."""
    try:
        with open(training, 'r') as training_data:
            train_data = []
            for line in training_data:
                train_data.append(line)
            mini_batch_size = len(train_data) / iterations
            net.SGD(train_data, iterations, mini_batch_size, rate, inputs)
    except:
        print("Input proper Training Data")
    saveNetwork(net)


def saveNetwork(net):
    """Saves the data of the network necessary to recreate the network.
    All previous data on the network is removed, so there is no history
    of the network saved."""
    try:
        writeData('network_info.txt', net.sizes)
        writeData('weights.txt', net.weights)
        writeData('biases.txt', net.biases)
        print("Network Saved Successfully")
    except:
        print("Error Saving Network")



def writeData(filename, data):
    # Assumes data is an array of numpy arrays
    with open(filename, 'w') as f:
        f.write(np.array_str(data))


def fixer(feeling, outputs):
    out = np.array([0]*len(outputs))
    feeling = feeling.lower()
    for i in range(len(outputs)):
        if feeling == outputs[i]:
            feeling = i
    out[feeling] = 1
    return out


def superlearn(net, inputs, output):
    net.SGD([(inputs, output)], 1, 1, 0.5)
    saveNetwork(net)

def main():
    net = getNetwork()
    outputs = ['angry', 'excited', 'focused', 'happy',  'relaxed', 'sad']
    """training = 'training_data.txt'"""
    inputs = np.array([0.25, 0.73, 0.11, 0.55, 0.96, 0.75])

    while True:
        '''insert lines to get input data'''


        """"# iterations =
        # rate =
        trainNetwork(net, training, inputs)"""

        output_node_index = net.get_output_index(inputs)
        output = outputs[output_node_index]
        print("\nI believe you are feeling " + output)

        feeling = input("\nHow are you feeling? (Choose one):\nAngry\nExcited\nFocused" +
                        "\nHappy\nRelaxed\nSad\n")
        correctout = fixer(feeling, outputs)
        superlearn(net, inputs, correctout)


if __name__ == '__main__':
    main()
