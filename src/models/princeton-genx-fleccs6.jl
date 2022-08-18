"""
GenX: An Configurable Capacity Expansion Model
Copyright (C) 2021,  Massachusetts Institute of Technology
This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
A complete copy of the GNU General Public License v2 (GPLv2) is available
in LICENSE.txt.  Users uncompressing this from an archive may not have
received this license file.  If not, see <http://www.gnu.org/licenses/>.
"""

@doc raw
"""
fleccs6(EP::Model, inputs::Dict, UCommit::Int, Reserves::Int)

The FLECCS6 module creates decision variables, expressions, and constraints
related to NGCC-CCS coupled with DAC solvent storage systems. In this module, we
will write up all the constraints formulations associated with the power plant.

# Pengfei 5-8-2022: Please update the docstring if necessary.
This module uses the following 'helper' functions in separate files:
FLECCS2_commit() for FLECCS subcompoents subject to unit commitment decisions
and constraints (if any) and FLECCS2_no_commit() for FLECCS subcompoents not
subject to unit commitment (if any).
"""

function fleccs6(EP::Model, inputs::Dict, FLECCS::Int, UCommit::Int, Reserves::Int)

	println("FLECCS6, NGCC CCS + DAC (GaTech)")

	T = inputs["T"]     # Number of time steps (hours)
    Z = inputs["Z"]     # Number of zones
    G_F = inputs["G_F"] # Number of FLECCS generator
	FLECCS_ALL = inputs["FLECCS_ALL"] # set of FLECCS generator
	dfGen_ccs = inputs["dfGen_ccs"] # FLECCS general data

	# get number of flexible subcompoents
	N_F = inputs["N_F"]
	n = length(N_F)
 


	NEW_CAP_ccs = inputs["NEW_CAP_FLECCS"] #allow for new capcity build
	RET_CAP_ccs = inputs["RET_CAP_FLECCS"] #allow for retirement

	START_SUBPERIODS = inputs["START_SUBPERIODS"] #start
    INTERIOR_SUBPERIODS = inputs["INTERIOR_SUBPERIODS"] #interiors

    hours_per_subperiod = inputs["hours_per_subperiod"]

	fuel_type = collect(skipmissing(dfGen_ccs[!,:Fuel]))

	fuel_CO2 = inputs["fuel_CO2"]
	fuel_costs = inputs["fuel_costs"]



	STARTS = 1:inputs["H"]:T
    # Then we record all time periods that do not begin a sub period
    # (these will be subject to normal time couping constraints, looking back one period)
    INTERIORS = setdiff(1:T,STARTS)


	# variales related to power generation/consumption
    @variables(EP, begin
        # Continuous decision variables
        vP_gt[y in FLECCS_ALL, 1:T]  >= 0 # generation from combustion TURBINE (gas TURBINE)
    end)

	# variales related to CO2 and solvent
	@variables(EP, begin
	    vCAPTURE_pcc[y in FLECCS_ALL,1:T] >= 0 # captured CO2 from PCC
        vCAPTURE_dac[y in FLECCS_ALL,1:T] >= 0 # captured CO2 from DAC
        vREGEN_dac[y in FLECCS_ALL,1:T] >= 0 # regenerated CO2
        vSORBENT_fresh[y in FLECCS_ALL,1:T] >= 0 # fresh sorbent
        vSORBENT_saturated[y in FLECCS_ALL,1:T] >= 0 # saturated sorbent
	end)

	# the order of those variables must follow the order of subcomponents in the "FLECCS_data.csv"
	# 1. gas turbine
	# 2. steam turbine 
	# 3. PCC
	# 4. compressor
	# 5. DAC1
	# 6. DAC2
	# 7. DAC3
	# 8. BOP

	# get the ID of each subcompoents 
	# gas turbine 
	NGCT_id = inputs["NGCT_id"]
	# steam turbine
	NGST_id = inputs["NGST_id"]
	# pcc 
	PCC_id = inputs["PCC_id"]
	# compressor
	Comp_id = inputs["Comp_id"]
	# DAC1, absorb
	DAC1_id = inputs["DAC1_id"]
	# dac2, desorb
	DAC2_id = inputs["DAC2_id"]
	# dac3, sorbent
	DAC3_id = inputs["DAC3_id"]
	#BOP 
	BOP_id = inputs["BOP_id"]

	# Specific constraints for FLECCS system
    # Thermal Energy input of combustion TURBINE (or oxyfuel power cycle) at hour "t" [MMBTU]
	# eq1. 
    @expression(EP, 
		eFuel[y in FLECCS_ALL,t=1:T], 
		dfGen_ccs[!, :P1][1+n*(y-1)] * vP_gt[y, t]
	)
   
	# power output from steam turbine is a function vP_gt and vREGEN_dac and vCAPTURE_pcc
	# eq2. 
	@expression(EP, 
		ePower_st[y in FLECCS_ALL,t=1:T], 
		dfGen_ccs[!, :P2_1][1+n*(y-1)] * vP_gt[y, t] + dfGen_ccs[!, :P2_2][1+n*(y-1)] * vREGEN_dac[y, t] + dfGen_ccs[!, :P2_3][1+n*(y-1)] * vCAPTURE_pcc[y, t]
	)

	# lower bound of power output from steam turbine
	# Eq 2.1
	@constraint(EP, [y in FLECCS_ALL,t=1:T], 
		ePower_st[y, t] >= vP_gt[y, t] * dfGen_ccs[!, :P2_0][1+n*(y-1)]
	)
    
	# CO2 generated from flue gas is a function eFuel
	# eq 3
	@expression(EP, 
		eCO2_flue[y in FLECCS_ALL,t=1:T],
		dfGen_ccs[!,:P3][1+n*(y-1)] * eFuel[y,t]
	)

	#eq 4 
	@constraint(EP, [y in FLECCS_ALL,t=1:T], 
		vCAPTURE_pcc[y,t] <= dfGen_ccs[!,:P4][1+n*(y-1)] * eCO2_flue[y,t]
	)

	# eq 5
	@expression(EP, 
		eCO2_vent_pcc[y in FLECCS_ALL,t=1:T],
		eCO2_flue[y,t] - vCAPTURE_pcc[y,t]
	)

	# eq 6
	@expression(EP,
		ePower_use_pcc[y in FLECCS_ALL,t=1:T],
		dfGen_ccs[!,:P6][1+n*(y-1)] * vCAPTURE_pcc[y,t]
	)


	#sorbent storage mass balance
	#eq 7 
	# dynamic of saturated sorbent storage system, normal [tonne solvent/sorbent]
	@constraint(EP, [y in FLECCS_ALL, t in INTERIOR_SUBPERIODS],vSORBENT_saturated[y, t] == vSORBENT_saturated[y, t-1] - vREGEN_dac[y,t]/dfGen_ccs[!,:pSorbentCapacity][1+n*(y-1)] + vCAPTURE_dac[y,t]/dfGen_ccs[!,:pSorbentCapacity][1+n*(y-1)])
	# dynamic of saturated sorbent, wrapping [tonne solvent/sorbent]
	#@constraint(EP, [y in FLECCS_ALL, t in START_SUBPERIODS],vSORBENT_saturated[y, t] == vSORBENT_saturated[y,t+hours_per_subperiod-1] - vREGEN_dac[y,t]/dfGen_ccs[!,:pSorbentCapacity][1+n*(y-1)] + vCAPTURE_dac[y,t]/dfGen_ccs[!,:pSorbentCapacity][1+n*(y-1)])
	
	#eq 8 
	# dynamic of fresh sorbent storage system, normal [tonne solvent/sorbent]
	@constraint(EP, [y in FLECCS_ALL, t in INTERIOR_SUBPERIODS],vSORBENT_fresh[y, t] == vSORBENT_fresh[y, t-1] + vREGEN_dac[y,t]/dfGen_ccs[!,:pSorbentCapacity][1+n*(y-1)] - vCAPTURE_dac[y,t]/dfGen_ccs[!,:pSorbentCapacity][1+n*(y-1)])
	# dynamic of fresh sorbent, wrapping [tonne solvent/sorbent]
	#@constraint(EP, [y in FLECCS_ALL, t in START_SUBPERIODS],vSORBENT_fresh[y, t] == vSORBENT_fresh[y,t+hours_per_subperiod-1] + vREGEN_dac[y,t]/dfGen_ccs[!,:pSorbentCapacity][1+n*(y-1)] - vCAPTURE_dac[y,t]/dfGen_ccs[!,:pSorbentCapacity][1+n*(y-1)])
	
	# eq 9, already satisfied when creating the variables..
    # eq 10 
	@constraint(EP, [y in FLECCS_ALL, t=1:T], vCAPTURE_dac[y, t]/dfGen_ccs[!,:pSorbentCapacity][1+n*(y-1)] <= EP[:eTotalCapFLECCS][y, DAC3_id]  )

    # eq 11
    @constraint(EP, [y in FLECCS_ALL, t=1:T], vREGEN_dac[y, t]/dfGen_ccs[!,:pSorbentCapacity][1+n*(y-1)] <= EP[:eTotalCapFLECCS][y, DAC3_id] )

    # eq 12 and eq 18 combine together

	@constraint(EP, [y in FLECCS_ALL, t in START_SUBPERIODS], vSORBENT_fresh[y, t] == EP[:eTotalCapFLECCS][y, DAC3_id]/dfGen_ccs[!,:pCAPRatio_dac][1+n*(y-1)]  )
    
	# eq 13. 
	@constraint(EP, [y in FLECCS_ALL, t in START_SUBPERIODS], vSORBENT_saturated[y, t] == 0  )


	#eq 14
	@expression(EP, eSteam_dac[y in FLECCS_ALL,t=1:T], dfGen_ccs[!,:P14][1+n*(y-1)] * vREGEN_dac[y,t])

	#eq 16
	@constraint(EP,[y in FLECCS_ALL,t=1:T], eSteam_dac[y,t] <= dfGen_ccs[!,:P14][1+n*(y-1)] * vP_gt[y,t] + dfGen_ccs[!,:P14][1+n*(y-1)] * EP[:eTotalCapFLECCS][y, PCC_id])

	#eq 17
	@expression(EP, ePower_use_dac[y in FLECCS_ALL,t=1:T], dfGen_ccs[!,:P17][1+n*(y-1)] * vCAPTURE_dac[y,t])

	#skip eq 18 for now

	#eq 19
	@expression(EP, eCO2_vent_compress[y in FLECCS_ALL,t=1:T], dfGen_ccs[!,:P19][1+n*(y-1)] * vREGEN_dac[y,t])

	#eq 20 minus vREGEN, eCO2_vent could be negative 
	@expression(EP, eCO2_vent[y in FLECCS_ALL,t=1:T], eCO2_vent_compress[y,t] + eCO2_vent_pcc[y,t] - vREGEN_dac[y,t])

	#eq 21
	@expression(EP, eCO2_compressed[y in FLECCS_ALL,t=1:T], vREGEN_dac[y,t] + vCAPTURE_pcc[y,t] - eCO2_vent_compress[y,t])

	#eq 22
	@expression(EP, ePower_use_comp[y in FLECCS_ALL,t=1:T], dfGen_ccs[!,:P22_1][1+n*(y-1)] * vCAPTURE_pcc[y,t] + dfGen_ccs[!,:P22_2][1+n*(y-1)] *vREGEN_dac[y,t])

	#eq 22
	@expression(EP, ePower_others[y in FLECCS_ALL,t=1:T], dfGen_ccs[!,:P23][1+n*(y-1)] * vP_gt[y,t] )

	#eq 24 net power output 
	@expression(EP, eCCS_net[y in FLECCS_ALL,t=1:T], vP_gt[y,t] + ePower_st[y,t] - ePower_use_dac[y,t]- ePower_use_pcc[y,t] - ePower_others[y,t] - ePower_use_comp[y,t])
    # eq 25
    @constraint(EP,  [y in FLECCS_ALL, t in INTERIOR_SUBPERIODS],eCCS_net[y,t] >= 0 )

	# power balance of fleccs
	@expression(EP, ePowerBalanceFLECCS[t=1:T, z=1:Z], sum(eCCS_net[y,t] for y in unique(dfGen_ccs[(dfGen_ccs[!,:Zone].==z),:R_ID])))

	## Power Balance##
	EP[:ePowerBalance] += ePowerBalanceFLECCS

	# create a container for FLECCS output.
	@constraints(EP, begin
	    [y in FLECCS_ALL, i in NGCT_id, t = 1:T],EP[:vFLECCS_output][y,i,t] == vP_gt[y,t]
		[y in FLECCS_ALL, i in NGST_id,t = 1:T],EP[:vFLECCS_output][y,i,t] == ePower_st[y,t]	
		[y in FLECCS_ALL, i in Comp_id, t =1:T],EP[:vFLECCS_output][y,i,t] == eCO2_compressed[y,t]	
		[y in FLECCS_ALL, i in PCC_id,t = 1:T],EP[:vFLECCS_output][y,i,t] == vCAPTURE_pcc[y,t]

		[y in FLECCS_ALL, i in DAC1_id, t =1:T],EP[:vFLECCS_output][y,i,t] == vCAPTURE_dac[y,t]
		[y in FLECCS_ALL, i in DAC2_id, t =1:T],EP[:vFLECCS_output][y,i,t] == vREGEN_dac[y,t]	

		[y in FLECCS_ALL, i in DAC3_id, t =1:T],EP[:vFLECCS_output][y,i,t] == vSORBENT_fresh[y,t] * dfGen_ccs[!,:pCAPRatio_dac][1+n*(y-1)]

		[y in FLECCS_ALL, i in BOP_id, t =1:T],EP[:vFLECCS_output][y,i,t] == eCCS_net[y,t]			
	end)

	@constraint(EP, [y in FLECCS_ALL], EP[:eTotalCapFLECCS][y, BOP_id] == EP[:eTotalCapFLECCS][y, NGCT_id]+ EP[:eTotalCapFLECCS][y,NGST_id])




	########### variable cost ##################
	#fuel cost
	@expression(EP, eCVar_fuel[y in FLECCS_ALL, t = 1:T],(inputs["omega"][t]*fuel_costs[fuel_type[1]][t]*eFuel[y,t]))

	# CO2 sequestration cost applied to sequestrated CO2
	@expression(EP, eCVar_CO2_sequestration[y in FLECCS_ALL, t = 1:T],(inputs["omega"][t]*eCO2_compressed[y,t]*dfGen_ccs[!,:pCO2_sequestration][1+n*(y-1)]))


	# start variable O&M
	# variable O&M for ngcc
	@expression(EP,eCVar_ngcc[y in FLECCS_ALL, t = 1:T], inputs["omega"][t]*(dfGen_ccs[(dfGen_ccs[!,:FLECCS_NO].==NGCT_id) .& (dfGen_ccs[!,:R_ID].==y),:Var_OM_Cost_per_Unit][1])*vP_gt[y,t] +
	(dfGen_ccs[(dfGen_ccs[!,:FLECCS_NO].==NGST_id) .& (dfGen_ccs[!,:R_ID].==y),:Var_OM_Cost_per_Unit][1])*ePower_st[y,t])
	
	 # variable O&M for compressor
	@expression(EP,eCVar_comp[y in FLECCS_ALL, t = 1:T], inputs["omega"][t]*(dfGen_ccs[(dfGen_ccs[!,:FLECCS_NO].== Comp_id) .& (dfGen_ccs[!,:R_ID].==y),:Var_OM_Cost_per_Unit][1])*(eCO2_compressed[y,t]))

	 # variable O&M for PCC
	 @expression(EP,eCVar_pcc[y in FLECCS_ALL, t = 1:T], inputs["omega"][t]*(dfGen_ccs[(dfGen_ccs[!,:FLECCS_NO].== PCC_id) .& (dfGen_ccs[!,:R_ID].==y),:Var_OM_Cost_per_Unit][1])*(vCAPTURE_pcc[y,t]))

	 # variable O&M for dac
	 @expression(EP,eCVar_dac[y in FLECCS_ALL, t = 1:T], inputs["omega"][t]*(dfGen_ccs[(dfGen_ccs[!,:FLECCS_NO].== DAC2_id) .& (dfGen_ccs[!,:R_ID].==y),:Var_OM_Cost_per_Unit][1])*(vREGEN_dac[y,t]))


	#adding up variable cost

	@expression(EP,eVar_FLECCS[t = 1:T], sum(eCVar_fuel[y,t] + eCVar_CO2_sequestration[y,t] + eCVar_ngcc[y,t] + eCVar_comp[y,t] + eCVar_pcc[y,t]  + eCVar_dac[y,t]  for y in FLECCS_ALL))

	@expression(EP,eTotalCVar_FLECCS, sum(eVar_FLECCS[t] for t in 1:T))


	EP[:eObj] += eTotalCVar_FLECCS

	return EP
end