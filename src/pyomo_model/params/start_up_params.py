"""
Start-Up Parameter Module
Start-up related parameters.

Pengfei Cheng
2023
"""

# load factor range for the normal dispatch mode
x_range = {
    1: 50.0,
    2: 100.0,
}

# extreme points
x_range_extreme_points = [1, 2]

# time for transitioning, hour
start_up_h = 9

# trajectory for GT load
load_trajectory = {
    1: 0,
    2: 0.33,
    3: 9.37,
    4: 9.98,
    5: 14.27,
    6: 27.92,
    7: 50.40,
    8: 59.91,
    9: 84.40
}