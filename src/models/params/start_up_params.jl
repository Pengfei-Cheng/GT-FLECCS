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
    3 => 9.37,
    4 => 9.98,
    5 => 14.27,
    6 => 27.92,
    7 => 50.40,
    8 => 59.91,
    9 => 84.40
)