#-*- coding:utf-8-*-

import numpy as np
import pandas as pd
from numpy.linalg import inv
from numpy import dot

iris = pd.read_csv('iris.csv')

#normal fun
temp = iris.iloc[:, 2:5]
temp['x0'] = 1
print temp
X = temp.iloc[:, [3, 0, 1, 2]]
print X
Y = iris.iloc[:, 1]
print Y
Y = Y.values.reshape(len(iris), 1)
print Y
theta_n = dot(dot(inv(dot(X.T, X)),X.T), Y)
print theta_n


#bgradient
theta_g = np.array([1., 1., 1., 1.])
theta_g = theta_g.reshape(4, 1)
alpha = 0.1
print theta_g
temp = theta_g
print X
X0 = X.iloc[:, 0].values.reshape(150, 1)
X1 = X.iloc[:, 1].values.reshape(150, 1)
X2 = X.iloc[:, 2].values.reshape(150, 1)
X3 = X.iloc[:, 3].values.reshape(150, 1)
# print X0
print X1
# print X2
# print X3
J = pd.Series(np.arange(800, dtype=float))
print J
#theta j := theta j + alpha*(yi - h(xi))*xi
for i in range(800):
    temp[0] = theta_g[0] + alpha * np.sum((Y - dot(X, theta_g)) * X0) / 150.
    temp[1] = theta_g[1] + alpha * np.sum((Y - dot(X, theta_g)) * X1) / 150.
    temp[2] = theta_g[2] + alpha * np.sum((Y - dot(X, theta_g)) * X2) / 150.
    temp[3] = theta_g[3] + alpha * np.sum((Y - dot(X, theta_g)) * X3) / 150.
    J[i] = 0.5 * np.sum((Y - dot(X, theta_g)) ** 2)  # 计算损失函数值
    theta_g = temp  # 更新theta

print theta_g
print J.plot(ylim = [0, 50])
