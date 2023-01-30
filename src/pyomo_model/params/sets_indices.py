"""
Parameter Module
Sets and indices.

Pengfei Cheng
2023
"""

# slices per hour, for DAC-state variables
n_slice = 4

# index for modes
start_up_idx = 0
dispatch_idx = 1

# define sets
set_quarter_0 = list(range(n_slice + 1))
set_quarter = list(range(n_slice))
set_mode = [start_up_idx, dispatch_idx]
start_up_h = 9
set_start_up_hour = list(range(1, start_up_h + 1))

# total hours
n_hour = 24 * 364
# set of hours
set_hour_0 = list(range(n_hour + 1))
set_hour = list(range(1, n_hour + 1))