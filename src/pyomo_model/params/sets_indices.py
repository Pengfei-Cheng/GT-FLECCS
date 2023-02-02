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

# SP version scenarios: different CO2 prices
set_scenario = [1, 2, 3]

# probability of each scenario
scenario_prob = {
    1: 1 / 3,
    2: 1 / 3,
    3: 1 / 3,
}