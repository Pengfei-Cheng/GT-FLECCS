"""
Objective Module
Define the objective function.

Pengfei Cheng
2022

UPDATE:
    12-09-2021: added capital cost of DAC.
    01-19-2022: DAC cost annualized.
    04-01-2022: transformed into NPV:
        Changed expression from cost to profit.
        DAC capital cost: added PV transformation; added depreciation.
        operational profit: added tax and PV transition.
    04-12-2022: 
        updated depreciation terms.
        updated TOC distribution.
        transformed DAC TPC to TOC.
        added FOM and VOM terms.
    07-29-2022: update time index.
"""

function add_objective_function(m)

    x_fuel = m[:x_fuel]
    x_vent_CO2 = m[:x_vent_CO2]
    x_compress_CO2 = m[:x_compress_CO2]
    x_power_out = m[:x_power_out]
    z = m[:z]
    VOM_NGCC = m[:VOM_NGCC]
    VOM_PCC = m[:VOM_PCC]
    VOM_DAC = m[:VOM_DAC]
    VOM_PCC_compressor = m[:VOM_PCC_compressor]
    VOM_DAC_compressor = m[:VOM_DAC_compressor]
    FOM_DAC = m[:FOM_DAC]
    TPC_DAC = m[:TPC_DAC]

    # objective function 
    @expression(m, obj_expr,

        # operational profit/cost
        (
            sum(
                # natural gas cost
                - cost_NG * x_fuel[i]
                # CO2 credit/emission cost
                - CO2_CREDIT * x_vent_CO2[i] 
                # CO2 transportation
                - cost_CO2_transportation * x_compress_CO2[i]
                # power sell
                + power_price[i] * x_power_out[i]
                # start-up cost
                - cost_start_up * z[i]
                # VOM
                - VOM_NGCC[i] - VOM_PCC[i] - VOM_DAC[i] - VOM_PCC_compressor[i] - VOM_DAC_compressor[i]
            for i in set_hour)
            
            # FOM
            - FOM_DAC
        )
        # consider tax
        * (1 - tax_r)
        # expand to 20 year running period, consider interest rate
        * sum(1 / (1 + int_r) ^ j for j in 2:21)
        - 
        # DAC capital cost
        TPC_DAC
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