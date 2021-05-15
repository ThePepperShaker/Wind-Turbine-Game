import numpy as np 
import matplotlib.pyplot as plt 
import random
import time 

# Constants 
# Generate a list of 1:20 numbers 
WS = []
for i in range(21):
    WS.append(i)

# Create a function generating draws from a Weibull distribution 
def Weibull(x, lamb, k): 
    return (k/lamb)*((x/lamb)**(k-1)) * np.exp(-((x/lamb)**k))


def Wind_speed(int_list, lamb, k):
    weibull_dist = []
    # Generate probabilities from the Weibull distribution
    for i in range(21): 
        freq = Weibull(i, lamb, k)
        weibull_dist.append(freq)
    wind_speed = random.choices(int_list, weibull_dist)
    return wind_speed[0]

'''
# Checking if draws are coming from the Weibull distribution correctly
wind_speed_counter = {}
for i in range(2000):
    wind_speed = Wind_speed(WS, 6,2)
    print(wind_speed)
    if wind_speed in wind_speed_counter: 
        wind_speed_counter[wind_speed] += 1
    else:
        wind_speed_counter[wind_speed] = 1

# Plot the relationship
x = list(wind_speed_counter.keys())
y = list(wind_speed_counter.values())
plt.scatter(x,y)
'''

# Define a super basic power function 
# Use power curve of wind turbine as reference point and recreate later 
def Power_output(wind_speed): 
    power = 0 
    if wind_speed < 2: 
        power = 0 
    elif (2 < wind_speed <=5): 
        power = 50 
    elif (5 < wind_speed <= 8): 
        power = 100
    elif (8 < wind_speed <= 10):
        power = 150 
    elif (10 < wind_speed <= 13): 
        power = 300 
    elif (13 < wind_speed <= 15): 
        power = 400
    else: 
        power = 500 
    return power / 2

