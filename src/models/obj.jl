"""
Objective Module
Define the objective function.

Pengfei Cheng
2022

UPDATE:
    04-14-2022: simplified the objective function.
"""

function add_objective_function(m)

    x_fuel = m[:x_fuel]
    x_CO2_flue = m[:x_CO2_flue]
    x_power_net = m[:x_power_net]
    z0 = m[:z0]
    x_cost_NGCC_VOM = m[:x_cost_NGCC_VOM]

    # objective function 
    @expression(m, obj_expr,

        # operational profit/cost
        (
            sum(
                # natural gas cost
                - cost_NG * x_fuel[i]
                # CO2 credit/emission cost
                - CO2_CREDIT * x_CO2_flue[i]
                # power sell
                + power_price[i] * x_power_net[i]
                # start-up cost
                - cost_start_up * z0[i]
                # VOM
                - x_cost_NGCC_VOM[i]
            for i in set_hour)
        )
    )

    @objective(m, Max, obj_expr)

end