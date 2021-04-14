import random
import numpy as np
import matplotlib.pyplot as plt
import math as m

num_city = 100
num_air = 3
num_center = 5
sigma = 0.1
alpha = .001
cities = set()
ap1 = set()
ap2 = set()
ap3 = set()
airports = []
obj_list = []

a_list = [ap1, ap2, ap3]

obj_set = set()

for i in range(num_center):
    x = random.random()
    y = random.random()
    xc = np.random.normal(x, sigma, num_city//num_center)
    yc = np.random.normal(y, sigma, num_city//num_center)
    cities = cities.union(zip(xc, yc))
    print(cities)

for i in range(num_air):
    x = random.random()
    y = random.random()
    airports.append([x, y])


def closest_airport():
    ap1.clear()
    ap2.clear()
    ap3.clear()

    for c in cities:
        smallest = m.inf
        designated_airport = 0
        for a in range(num_air):
            curr = m.pow(c[0]-airports[a][0], 2) + m.pow(airports[a][1]-c[1], 2)
            if curr <= smallest:
                smallest = curr
                designated_airport = a

        if designated_airport == 0:
            ap1.add(c)
        elif designated_airport == 1:
            ap2.add(c)
        else:
            ap3.add(c)

        # print(smallest)


closest_airport()


def partial_div(string):
    total = 0
    if string == "x1":
        index = 0
        coord = 0
    elif string == "y1":
        index = 0
        coord = 1
    elif string == "x2":
        index = 1
        coord = 0
    elif string == "y2":
        index = 1
        coord = 1
    elif string == "x3":
        index = 2
        coord = 0
    else:
        index = 2
        coord = 1

    for city in a_list[index]:
        total += (airports[index][coord] - city[coord])

    return 2 * total


def move_airports():
    x1 = partial_div("x1")
    y1 = partial_div("y1")
    x2 = partial_div("x2")
    y2 = partial_div("y2")
    x3 = partial_div("x3")
    y3 = partial_div("y3")

    airports[0][0] = airports[0][0] - alpha * x1
    airports[0][1] = airports[0][1] - alpha * y1
    airports[1][0] = airports[1][0] - alpha * x2
    airports[1][1] = airports[1][1] - alpha * y2
    airports[2][0] = airports[2][0] - alpha * x3
    airports[2][1] = airports[2][1] - alpha * y3


def get_obj_func():
    total = 0
    index = 0

    for ap in a_list:
        for c in ap:
            total += m.pow(airports[index][0] - c[0], 2) + m.pow(airports[index][1] - c[1], 2)

        index += 1
    return total


def is_exit(num):
    if num in obj_set:
        return True
    else:
        return False


zip_cities = zip(*cities)
plt.scatter(*zip_cities, marker='+',color='b', label='Cities')
zip_airs = zip(*airports)
plt.scatter(*zip_airs, marker='*', color='r', s=100, label='Airports')
plt.legend()
plt.show()

initial_obj = get_obj_func()

obj_list.append(initial_obj)

print(initial_obj)


def solver():
    lowest = m.inf
    count = 0
    previous = get_obj_func()
    for x in range(1000):
        count += 1
        closest_airport()
        move_airports()
        obj = get_obj_func()
        obj_list.append(obj)

        if obj < lowest:
            lowest = obj
            low1 = airports[0]
            low2 = airports[1]
            low3 = airports[2]

        if abs(obj - previous) < 0.0001:
            airports[0] = low1
            airports[1] = low2
            airports[2] = low3
            return airports
        previous = obj


solver()

zip_cities = zip(*cities)
plt.scatter(*zip_cities, marker='+', color='b', label='Cities')
zip_airs = zip(*airports)
plt.scatter(*zip_airs, marker='*', color='r', s=100, label='Airports')
plt.legend()
plt.show()

plt.plot(obj_list, 'o')
plt.scatter
plt.show()
