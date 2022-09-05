global set_mode = 0:1  # 0: start-up, 1: normal dispatch
global set_start_up_hour = 1:start_up_h

# index for modes
global start_up_idx = 0
global dispatch_idx = 1

# horizon length
global n_hour = 24 * 364

# define sets
global set_hour_0 = 0:n_hour
global set_hour = 1:n_hour
