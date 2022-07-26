import numpy as np
import random
from tempfile import TemporaryFile
from regex import B
from scipy import rand
from numpy import savetxt
import copy


class NeuralNetwork:
    def __init__(self, layer_sizes):
        self.layersize = layer_sizes
        self.mutation_rate = 0.01
        weight_shapes = [(a, b)
                         for a, b in zip(layer_sizes[1:], layer_sizes[:-1])]

        self.weights = [np.random.standard_normal(
            s) for s in weight_shapes]

        self.biases = [np.zeros((s, 1)) for s in layer_sizes[1:]]

    def predict(self, a):
        for w, b in zip(self.weights, self.biases):
            a = self.activation(np.matmul(w, a) + b)
        return a

    def mutation(self, val):
        prob = [0.25, 0.25, 0.5]
        n = copy.deepcopy(self)
        for i in range(len(n.biases)):
            for j in range(n.biases[i].shape[0]):
                x = np.random.choice(np.arange(0, 3), p=prob)
                if (x == 2):
                    pass
                elif (x == 1):
                    n.biases[i][j] = n.biases[i][j]+(self.mutation_rate*val)
                elif (not(x)):
                    n.biases[i][j] = n.biases[i][j]-(self.mutation_rate*val)

        for i in range(len(n.weights)):
            for j in range(n.weights[i].shape[0]):
                for k in range(n.weights[i][j].shape[0]):
                    x = np.random.choice(np.arange(0, 3), p=prob)
                    if (x == 2):
                        pass
                    elif (x == 1):
                        n.weights[i][j][k] = n.weights[i][j][k] + \
                            (self.mutation_rate*val)
                    elif (not(x)):
                        n.weights[i][j][k] = n.weights[i][j][k] - \
                            (self.mutation_rate*val)

        return n

    def evolve(self, sorted):
        n = copy.deepcopy(sorted[0])
        prob = [0.2, 0.2, 0.2, 0.1, 0.1,0.1,0.1]

        for i in range(len(n.biases)):
            for j in range(n.biases[i].shape[0]):
                x = np.random.choice(np.arange(0, 7), p=prob)
                if (x == 6):
                    n.biases[i][j] = sorted[6].biases[i][j]
                if (x == 5):
                    n.biases[i][j] = sorted[5].biases[i][j]
                if (x == 4):
                    n.biases[i][j] = sorted[4].biases[i][j]
                if (x == 3):
                    n.biases[i][j] = sorted[3].biases[i][j]
                if (x == 2):
                    n.biases[i][j] = sorted[2].biases[i][j]
                elif (x == 1):
                    n.biases[i][j] = sorted[1].biases[i][j]
                elif (not(x)):
                    n.biases[i][j] = sorted[0].biases[i][j]

        for i in range(len(n.weights)):
            for j in range(n.weights[i].shape[0]):
                for k in range(n.weights[i][j].shape[0]):
                    x = np.random.choice(np.arange(0, 7), p=prob)
                    if (x == 6):
                        n.weights[i][j][k] = sorted[6].weights[i][j][k]
                    if (x == 5):
                        n.weights[i][j][k] = sorted[5].weights[i][j][k]
                    if (x == 4):
                        n.weights[i][j][k] = sorted[4].weights[i][j][k]
                    if (x == 3):
                        n.weights[i][j][k] = sorted[3].weights[i][j][k]
                    if (x == 2):
                        n.weights[i][j][k] = sorted[2].weights[i][j][k]
                    elif (x == 1):
                        n.weights[i][j][k] = sorted[1].weights[i][j][k]
                    elif (not(x)):
                        n.weights[i][j][k] = sorted[0].weights[i][j][k]

        return n

    def keep(self, name):
        layer = ""
        biases = ""
        weights = ""

        with open(name+".txt", "w") as f:
            for i in self.layersize:
                layer = layer+" " + str(i)
            f.write(layer.strip()+"\n")

            for i in range(len(self.biases)):
                biases = ""
                for j in range(self.biases[i].shape[0]):
                    biases = biases+" "+str(self.biases[i][j][0])
                f.write(biases.strip()+"\n")

            for i in range(len(self.weights)):
                for j in range(self.weights[i].shape[0]):
                    weights = ""
                    for k in range(self.weights[i][j].shape[0]):
                        weights = weights+" "+str(self.weights[i][j][k])
                    f.write(weights.strip()+"\n")

    def read(self, name):
        with open(name+".txt", "r") as f:
            string = f.read()
            lst = string.split("\n")

            layer = (int(lst[0].split(" ")[0]), int(
                lst[0].split(" ")[1]), int(lst[0].split(" ")[2]))
            net = NeuralNetwork(layer)
            lineno = 1

            for i in range(len(net.biases)):
                bias = lst[lineno]
                lineno = lineno+1
                for j in range(net.biases[i].shape[0]):
                    net.biases[i][j][0] = bias.split(" ")[j]

            for i in range(len(net.weights)):
                for j in range(net.weights[i].shape[0]):
                    weight = lst[lineno]
                    lineno = lineno+1
                    for k in range(net.weights[i][j].shape[0]):
                        net.weights[i][j][k] = weight.split(" ")[k]
        return net

    @staticmethod
    def activation(x):
        return 1/(1+np.exp(-x))
