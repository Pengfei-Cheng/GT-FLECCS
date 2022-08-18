"""
Modeling module
Constraints related to costing.

Pengfei Cheng
2022
"""

function add_OM_costing_constraints(m)
    FOM_DAC = m[:FOM_DAC]
    TPC_DAC = m[:TPC_DAC]
    VOM_NGCC = m[:VOM_NGCC]
    x_load_factor = m[:x_load_factor]
    VOM_PCC = m[:VOM_PCC]
    VOM_DAC = m[:VOM_DAC]
    x_CO2_DAC_cap = m[:x_CO2_DAC_cap]
    VOM_PCC_compressor = m[:VOM_PCC_compressor]
    VOM_DAC_compressor = m[:VOM_DAC_compressor]

    # FOM of DAC
    @constraint(
        m, eq_FOM_DAC,
        FOM_DAC
        ==
        TPC_DAC * 0.05 + 2 * 110000
    )

    # VOM of NGCC
    @constraint(
        m, eq_VOM_NGCC[i = set_hour_0],
        VOM_NGCC[i]
        ==
        a_VOM_NGCC * x_load_factor[i]
    )

    # VOM of PCC
    @constraint(
        m, eq_VOM_PCC[i = set_hour_0],
        VOM_PCC[i]
        ==
        a_VOM_PCC * x_load_factor[i]
    )

    # VOM of DAC
    @constraint(
        m, eq_VOM_DAC[i = set_hour_0],
        VOM_DAC[i]
        ==
        a_VOM_DAC * sum(x_CO2_DAC_cap[i, j] for j in set_quarter)
    )

    # VOM of PCC compressor
    @constraint(
        m, eq_VOM_PCC_compressor[i = set_hour_0],
        VOM_PCC_compressor[i]
        ==
        a_VOM_PCC_compressor * x_load_factor[i]
    )

    # VOM of DAC compressor
    @constraint(
        m, eq_VOM_DAC_compressor[i = set_hour_0],
        VOM_DAC_compressor[i]
        ==
        a_VOM_DAC_compressor * sum(x_CO2_DAC_cap[i, j] for j in set_quarter)
    )
end