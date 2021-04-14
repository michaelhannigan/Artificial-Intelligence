import math
import matplotlib.pyplot as plt
import numpy

n = set()
x0 = 0
y0 = 0
tup_list = []
blue_set = set()
red_set = set()

for i in range(3, 7):
    coordinates = set()
    n = math.pow(10, i)
    a = 0
    for k in range(int(n)):
        x = numpy.random.random()
        y = numpy.random.random()
        tup = (x, y)
        squared = math.pow(x-x0, 2) + math.pow(y-y0, 2)
        if math.sqrt(squared) < 1:
            a += 1
            if i == 4:
                blue_set.add(tup)
        elif i == 4:
            red_set.add(tup)

    a_div_s = (a/n)*4
    error = abs((math.pi - a_div_s)/math.pi)*100
    new_tuple = (i, a_div_s, error)
    tup_list.append(new_tuple)

for t in tup_list:
    t0 = t[0]
    t1 = t[1]
    t2 = t[2]
    txt = "n = 10 ^ {0} pi = {1:6f} error = {2:4f} %"
    print(txt.format(t[0], t[1], t[2]))

zip_blue = zip(*blue_set)
zip_red = zip(*red_set)

plt.scatter(*zip_blue, 1, marker='.', color='b', label='b-set')
plt.scatter(*zip_red, 1, marker='.',  color='r', label='r-set')

label = "Figure 1: Estimating π using simulation"
plt.xlabel(label)


plt.show()






