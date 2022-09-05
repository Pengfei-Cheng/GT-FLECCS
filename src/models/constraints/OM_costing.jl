"""
Modeling module
Constraints related to costing.

Pengfei Cheng
2022
"""

function add_OM_costing_constraints(m)
    x_cost_DAC_FOM = m[:x_cost_DAC_FOM]
    x_cost_DAC_TPC = m[:x_cost_DAC_TPC]
    x_cost_NGCC_VOM = m[:x_cost_NGCC_VOM]
    x_load = m[:x_load]
    x_cost_PCC_VOM = m[:x_cost_PCC_VOM]
    x_cost_DAC_VOM = m[:x_cost_DAC_VOM]
    x_CO2_DAC = m[:x_CO2_DAC]
    x_cost_PCC_compr_VOM = m[:x_cost_PCC_compr_VOM]
    x_cost_DAC_compr_VOM = m[:x_cost_DAC_compr_VOM]

    # FOM of DAC
    @constraint(
        m, eq_FOM_DAC,
        x_cost_DAC_FOM
        ==
        x_cost_DAC_TPC * 0.05 + 2 * 110000
    )

    # VOM of NGCC
    @constraint(
        m, eq_VOM_NGCC[i = set_hour_0],
        x_cost_NGCC_VOM[i]
        ==
        a_cost_NGCC_VOM * x_load[i]
    )

    # VOM of PCC
    @constraint(
        m, eq_cost_PCC_VOM[i = set_hour_0],
        x_cost_PCC_VOM[i]
        ==
        a_VOM_PCC * x_load[i]
    )

    # VOM of DAC
    @constraint(
        m, eq_cost_DAC_VOM[i = set_hour_0],
        x_cost_DAC_VOM[i]
        ==
        a_cost_DAC_VOM * sum(x_CO2_DAC[i, j] for j in set_quarter)
    )

    # VOM of PCC compressor
    @constraint(
        m, eq_cost_PCC_compr_VOM[i = set_hour_0],
        x_cost_PCC_compr_VOM[i]
        ==
        a_cost_PCC_compr_VOM * x_load[i]
    )

    # VOM of DAC compressor
    @constraint(
        m, eq_VOM_DAC_compressor[i = set_hour_0],
        x_cost_DAC_compr_VOM[i]
        ==
        a_cost_DAC_compr_VOM * sum(x_CO2_DAC[i, j] for j in set_quarter)
    )
end