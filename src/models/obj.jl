"""
Objective Module
Define the objective function.

Pengfei Cheng
2022
"""

function add_objective_function(m)

    x_fuel = m[:x_fuel]
    x_CO2_cap_total = m[:x_CO2_cap_total]
    x_CO2_compress = m[:x_CO2_compress]
    x_power_net = m[:x_power_net]
    z0 = m[:z0]
    x_cost_NGCC_VOM = m[:x_cost_NGCC_VOM]
    x_cost_PCC_VOM = m[:x_cost_PCC_VOM]
    x_cost_DAC_VOM = m[:x_cost_DAC_VOM]
    x_cost_PCC_compr_VOM = m[:x_cost_PCC_compr_VOM]
    x_cost_DAC_compr_VOM = m[:x_cost_DAC_compr_VOM]
    x_cost_DAC_FOM = m[:x_cost_DAC_FOM]
    x_cost_DAC_TPC = m[:x_cost_DAC_TPC]

    # objective function 
    @expression(m, obj_expr,

        # operational profit/cost
        (
            sum(
                # natural gas cost
                - cost_NG * x_fuel[i]
                # CO2 credit/emission cost
                + CO2_CREDIT * x_CO2_cap_total[i] 
                # CO2 transportation
                - a_cost_CO2_TS * x_CO2_compress[i]
                # power sell
                + power_price[i] * x_power_net[i]
                # start-up cost
                - cost_start_up * z0[i]
                # VOM
                - x_cost_NGCC_VOM[i] - x_cost_PCC_VOM[i] - x_cost_DAC_VOM[i] - x_cost_PCC_compr_VOM[i] - x_cost_DAC_compr_VOM[i]
            for i in set_hour)
            
            # FOM
            - x_cost_DAC_FOM
        )
        # consider tax
        * (1 - tax_r)
        # expand to 20 year running period, consider interest rate
        * sum(1 / (1 + int_r) ^ j for j in 2:21)
        - 
        # DAC capital cost
        x_cost_DAC_TPC
        # TPC to TOC
        * (1 + 0.0311 + 0.0066 + 0.1779)
        * (
            # distribution of TOC (30/70)
            0.3 + 0.7 / (1 + int_r)
            # impact of depreciation on PV: tax_r * D (depreciation) * (1 + int_r) ^ j
            - sum(tax_r * depreciate_r * ((1 - depreciate_r) ^ j) * ((1 + int_r) ^ (- j - 2)) for j in 0:19)
        )
    )

    @objective(m, Max, obj_expr)
end