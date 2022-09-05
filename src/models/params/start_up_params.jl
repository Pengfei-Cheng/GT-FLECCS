"""
Start-Up Parameter Module
Start-up related parameters.

Pengfei Cheng
2022
"""

# load factor range for the normal dispatch mode
global x_range = [50.0, 100.0]

# extreme points
global x_range_extreme_points = [1, 2]

# time for transitioning, hour
global start_up_h = 9

# trajectory for GT load
global load_trajectory = Dict(
    1 => 0,
    2 => 0.33,
    3 => 9.38,
    4 => 9.99,
    5 => 14.28,
    6 => 27.93,
    7 => 50.42,
    8 => 59.92,
    9 => 84.42
)