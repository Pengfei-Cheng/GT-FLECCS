"""
Modeling module
Constraints related to costing.

Pengfei Cheng
2022
"""

function add_OM_costing_constraints(m)

    x_cost_NGCC_VOM = m[:x_cost_NGCC_VOM]
    x_load = m[:x_load]

    # VOM of NGCC
    @constraint(
        m, eq_VOM_NGCC[i = set_hour_0],
        x_cost_NGCC_VOM[i]
        ==
        a_cost_NGCC_VOM * x_load[i]
    )

end