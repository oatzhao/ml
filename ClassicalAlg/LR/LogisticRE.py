from numpy import *
import numpy
import matplotlib.pyplot as plt

#download data
def loadDataSet():
    dataMat = []
    labelMat = []
    fr = open('dataSet.csv')
    for line in fr.readlines():
        lineArr = line.strip().split()
        dataMat.append([1.0, float(lineArr[0]), float(lineArr[1])])
        labelMat.append(int(lineArr[2]))
    return dataMat, labelMat

def sigmoid(inx):
    i =  inx
    j =  1.0 / (1 + exp(-inx))
    return 1.0 / (1 + exp(-inx))


def gradAscent(dataMat, labelMat):
    dataMatrix = mat(dataMat)
    classLabels = mat(labelMat).transpose()
    m ,n = shape(dataMatrix)
    alpha = 0.001
    maxCycles = 500
    weights = ones((n, 1))
    for k in range(maxCycles):
        h = sigmoid(dataMatrix * weights)
        error = (classLabels - h)
        weights = weights + alpha * dataMatrix.transpose()*error
    return weights


def randomGradAscent(data, label):
    data = np.array(data)
    n ,m = data.shape
    alpha = 0.01
    weights = np.ones(m)
    for i in range(n):
        h = sigmoid(np.sum(data[i]*weights))
        err = label[i] - h
        weights = weights + data[i] * alpha * err
    return weights


def plot(weights):
    data, label = loadDataSet()
    n = len(data)
    x1 = []
    y1 = []
    x2 = []
    y2 = []
    for i in range(n):
        if label[i] == 1:
            x1.append(data[i][1])
            y1.append(data[i][2])
        else:
            x2.append(data[i][1])
            y2.append(data[i][2])
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(x1, y1, s = 30, c = 'red', marker = 's')
    ax.scatter(x2, y2, s = 30, c = 'green')
    x = numpy.arange(-3.0, 3.0, 0.1)
    y = (-weights[0] - weights[1] * x) / weights[2]
    ax.plot(x, y)
    plt.xlabel('X1')
    plt.ylabel('X2')
    plt.show()

dataMat, labelMax = loadDataSet()
weights = gradAscent(dataMat, labelMax)
plot(weights.getA())





