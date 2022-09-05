"""
Modeling module
Declare operation model logic constraints.

Pengfei Cheng

1. lambda constraint: dispatch only, sum of extreme points is y
2. relationship between y and z0
3. minimum on-hours during start-up
4. z0 and z relationship
5. limitation on start up times

UPDATE:
    06-08-2022: added start-up time limitation constraint
"""

# ------------------------------------------------------------------------------

function add_operation_mode_logic_constraints(model)

    lambda = model[:lambda]
    y = model[:y]
    z = model[:z]
    z0 = model[:z0]

    # 1. LAMBDA CONSTRAINT: DISPATCH ONLY, SUM OF EXTREME POINTS IS Y
    # when y = 0, z = 0, sum of lambda = 0, x_load_D = 0
    # when y = 1, z = 1, start-up: x_load_D[i, dispatch_idx] = 0
    # when y = 1, z = 0, normal dispatch mode: x_load_D[i, dispatch_idx]
    # is a combination of convex points
    @constraint(
        model, eq_lambda[i = set_hour_0],
        sum(lambda[i, k] for k in x_range_extreme_points)
        ==
        y[i] - z[i]
    )

    # --------------------------------------------------------------------------

    # 2. RELATIONSHIP BETWEEN Y AND Z
    @constraint(
        model, eq_transition[i = set_hour],
        z0[i]
        >=
        y[i] - y[i - 1]
    )
    @constraint(
        model, eq_transition_init,
        z0[0]
        ==
        0
    )

    # 3. MINIMUM ON-HOURS DURING START-UP
    @constraint(model, eq_min_on_hours[i = set_hour_0],
        y[i] >= sum(z0[i - k + 1] for k in set_start_up_hour if i - k + 1 >= 0)
    )

    # --------------------------------------------------------------------------

    # 4. Z AND Z2 RELATIONSHIP
    @constraint(
        model, eq_transitioning_states[i = set_hour_0],
        z[i] 
        == 
        sum((z0[i - k + 1]) for k in set_start_up_hour if i - k + 1 >= 0)
    )

    # 5. Limitation on start up times
    if limit_start_up
        @constraint(
            model, eq_limit_startup_times,
            sum(z0[i] for i in set_hour_0)
            <=
            5
        )
    end
end