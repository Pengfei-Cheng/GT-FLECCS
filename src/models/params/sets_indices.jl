# slices per hour, for DAC-state variables
global n_slice = 4

# index for modes
global start_up_idx = 0
global dispatch_idx = 1

# define sets
global set_quarter_0 = 0:n_slice
global set_quarter = 0:n_slice-1
global set_mode = start_up_idx:dispatch_idx  # 0: start-up, 1: normal dispatch
global set_start_up_hour = 1:start_up_h

# total hours
global n_hour = 24 * 364
# set of hours
global set_hour_0 = 0:n_hour  # start from 0
global set_hour = 1:n_hour  # start from 1