import numpy as np
import pandas as pd

state_matrix = np.matrix('0.9322 0.0068 0.0610 0.0; 0.49315 0.1620 0.0 0.34485; 0.4391 0.0 0.4700 0.0909;'
                         '0.0 0.15515 0.4091 0.4375')

num_runs = 1000000

dictionary = {0: 0, 1: 0, 2: 0, 3: 0}

current_state = np.random.randint(0, 4)

for i in range(num_runs):
    index = 0
    next_state = np.random.random()
    curr_probability = state_matrix[current_state].item(index)
    if next_state <= curr_probability != 0:
        current_state = index
        dictionary[current_state] += 1
        continue

    index += 1
    curr_probability += state_matrix[current_state].item(index)

    if next_state <= curr_probability:
        current_state = index
        dictionary[current_state] += 1
        continue

    index += 1
    curr_probability += state_matrix[current_state].item(index)

    if next_state <= curr_probability:
        current_state = index
        dictionary[current_state] += 1
        continue

    index += 1
    curr_probability += state_matrix[current_state].item(index)

    if next_state <= curr_probability:
        current_state = index
        dictionary[current_state] += 1
        continue

C = (dictionary[0] + dictionary[1])/num_runs
notC = (dictionary[2] + dictionary[3])/num_runs

print('Part A. the sampling probabilities')
print('(C|-s,r) = <0.8780,0.1220>')
print('(C|-s, -r) = <0.3103,0.6897>')
print('(R|c,-s, w) = <0.9863,0.0137>')
print('(R|-c, -s, w) = <0.8181,0.1818>\n')

print('Part B. The transition probability matrix')
cols = ['S1', 'S2', 'S3', 'S4']
data_matrix = pd.DataFrame(state_matrix, columns=cols, index=cols)
print(data_matrix,"\n")

print('Part C. The The probability for the query')
print('(C|-s,w) = <', C, ",", notC, ">")






