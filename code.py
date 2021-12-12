import math as m
import random as r
from random import random
import numpy as np


def weighted_choice(
    objects, weights
):  # this function creates a greater probability for the goal node to occur
    weights = np.array(weights, dtype=np.float64)
    sum_of_weights = weights.sum()
    np.multiply(weights, 1 / sum_of_weights, weights)
    weights = weights.cumsum()
    x = random()
    for i in range(len(weights)):
        if x < weights[i]:
            return objects[i]


def collision_check(start, stop, o_x, o_y, o_r):  # collision check+planner
    check = []
    l = []
    a = start[1] - stop[1]
    b = stop[0] - start[0]
    c = (start[0] * stop[1]) - (start[1] * stop[0])
    if a and b is not 0:
        for i in range(len(o_x)):
            x, y, r = o_x[i], o_y[i], o_r[i]
            dist = (abs(a * x + b * y + c)) / m.sqrt(a * a + b * b)
            if dist == r or dist < r:
                check.append(True)
            else:
                check.append(False)

    if check.count(True) > 0:
        return True
    else:
        return False  # col


def sampler():  # this function takes random samples
    l = []
    n = []
    for i in np.around(np.linspace(-0.5, 0.5, 100), 2):
        for j in np.around(np.linspace(-0.5, 0.5, 100), 2):

            o = []
            o.append(float(i))
            o.append(float(j))
            n.append(o)
    weights = []
    for i in range(len(n)):
        if i == n.index([0.5, 0.5]):
            k = (0.2 * len(n)) / len(n)
            weights.append(k)
        else:
            k = 1 / len(n)
            weights.append(k)
    res = [weighted_choice(n, weights) for i in range(len(n))]
    return r.sample(res, 1)[0]


def opt_ctg(a):  # this function  generates the heurestics cost to go
    distance = m.sqrt(pow(0.5 - a[0], 2) + pow(0.5 - a[1], 2))
    return distance


def nearest(sampled_list, a):  # this function generates the nearest node to a  sample
    dist = []
    for i in range(len(sampled_list)):
        if sampled_list[i] is not x_goal:
            o = []
            distance = m.sqrt(
                pow(sampled_list[i][0] - a[0], 2) + pow(sampled_list[i][1] - a[1], 2)
            )
            o.append(distance)
            o.append(sampled_list[i])
            dist.append(o)
    return min(dist)[1]


def edge(a, b):  # this function generates the edge between two nodes
    distance = m.sqrt(pow(b[0] - a[0], 2) + pow(b[1] - a[1], 2))
    return distance


def node_dict(i, sample, d):  # creates a dictionary with the nodes an their index
    d.update(eval("{" + str(i) + ":" + str(sample) + "}"))
    return d


def node_file_creator(index, sample, hctg):  # creates input for node file
    o = []
    o.append(index)
    o.append(sample[0])
    o.append(sample[1])
    o.append(hctg)
    return o


def edge_file_creator(
    start, stop, edge, node_dictionary
):  # creates input for edge file
    o = []
    for key, value in node_dictionary.items():
        if start == value:
            o.append(key)
    for key, value in node_dictionary.items():
        if stop == value:
            o.append(key)
    o.append(edge)
    return o


x_start = [-0.5, -0.5]
x_goal = [0.5, 0.5]
obs_x, obs_y, obs_r = [], [], []
edges, hctg, NODES = [], [], []
node_dictionary = {}
i = 3
tree = [x_start]
obstacle = open("obstacles.csv", "r")  # initializes object
for x in obstacle:
    x = str(x)
    if x[0] is not "#":
        le = x.split(",")
        obs_y.append(float(le[1]))
        obs_x.append(float(le[0]))
        obs_r.append(float(le[2]) / 2)  #  '''  #
x_samp0 = sampler()  # initialzation start
x_near0 = nearest(tree, x_samp0)
if collision_check(x_near0, x_samp0, obs_x, obs_y, obs_r) == False:
    i, j, k = 1, 2, 3
    tree.append(x_samp0)
    node_dictionary = node_dict(i, x_start, node_dictionary)
    node_dictionary = node_dict(j, x_goal, node_dictionary)
    node_dictionary = node_dict(k, x_samp0, node_dictionary)
    n = node_file_creator(k, x_samp0, opt_ctg(x_samp0))
    node_file = open("nodes.csv", "w")
    node_file.write(str(n)[1 : len(str(n)) - 1] + "\n")
    e = edge_file_creator(x_near0, x_samp0, edge(x_near0, x_samp0), node_dictionary)
    edge_file = open("edge.csv", "w")
    edge_file.write(str(e)[1 : len(str(e)) - 1] + "\n")
    print(k)
x_samp = sampler()  # initialization end
indice = 3
while x_samp is not x_goal:  # loop to search
    x_near = nearest(tree, x_samp)
    if collision_check(x_near, x_samp, obs_x, obs_y, obs_r) == False:
        indice += 1
        print(indice)
        tree.append(x_samp)
        node_dictionary = node_dict(indice, x_samp, node_dictionary)
        n = node_file_creator(indice, x_samp, opt_ctg(x_samp))
        print(n)
        node_file = open("nodes.csv", "a")
        node_file.write(str(n)[1 : len(str(n)) - 1] + "\n")
        e = edge_file_creator(x_near, x_samp, edge(x_near, x_samp), node_dictionary)
        print(e)
        edge_file = open("edge.csv", "a")
        edge_file.write(str(e)[1 : len(str(e)) - 1] + "\n")

    x_samp = sampler()
