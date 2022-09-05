# Integrated Design and Operation Model for NGCC-PCC-DAC Retrofit

This repo contains the optimization model for the NGCC-PCC-DAC retrofit design modeled in `Julia`/`Jump`.

## Main features
- co-optimizes the design and operational decisions
- considers multiple future energy scenarios (varying electricity prices for a year + varying CO2 prices)
- formulates a novel DAC model to account for sorbent dynamics
- contains logic for system start-up/shutdown

For the full model description, please contact [Pengfei Cheng](pengfeicheng@gatech.edu).

## Branches

There are currently 2 branches:
- `main`: the most up-to-date one with all the features 
- `base-NGCC`: contains the optimization model for the operations of B31A (unretrofitted NGCC)

## `main` Branch Layout

```
.
├── FLECCS_env                          # Julia environment configuration
├── src                                 # source files
│   ├── models                          # optimization model files
│       ├── constraints
│       ├── output
│       ├── params
│       ├── model.jl                    # main file
│       ├── obj.jl
│       └── variables.jl
│   ├── post_processing                 # post-processing scripts
│   ├── regression                      # regression scripts for data from simulation
│   └── resources                       # other resource files
├── .gitignore
├── README.md
└── requirements.txt
```

## Installation

### `Julia` Environment
The model code is based on `Julia 1.7.0`. To install packages, run the following commands in a `Julia` REPL:
```Julia
# press "]" to enter Julia's Pkg (package manager) REPL
# cd to the project directory
(@1.7) pkg> activate FLECCS_env
(FLECCS_env) pkg> instantiate
```
For more information, see the [instruction](https://pkgdocs.julialang.org/v1/environments/).

### `Python` Environment
`Python` scripts/`Jupyter` notebooks are used for post processing, and only basic packages are needed.
To install these packages, run
```shell
pip install -r requirements.text
```

### Optimization solver
To use a certain MILP solver, please install it separately.
Please make sure that the solver has accessible API to `Julia`/`Jump`.

## Usage

To run the model in the `Julia` REPL (in terminal):
```Julia
# make sure the environment has been configured
include("src/models/model.jl")
# remember to set the output directory for the first-time usage in src/models/output/output.jl
```

## Data Sources

|Location|File name|Function|Source|
|---|---|---|---|
|`src/regression/`|`coefs.csv`|coefficients from simulation (only considers 50% and 100% load), currently in use|linear regression|
|`src/resources/`|`NGCC_performance.xlsx`|system performance coefficients|Howard Hendrix|
|`src/resources/`|`overall-price-signals.csv`|all sets of electricity price series|Princeton team and NREL team|
|`src/models/params`|`.jl` files|other data|Georgia Tech FLECCS team|

## Credits

The code was initially developed by David Thierry and further developed and
maintained by Pengfei Cheng.
The development was funded by the ARPA-E's [FLECCS program](https://arpa-e.energy.gov/technologies/programs/fleccs)
and supported by the Georgia Tech FLECCS Team (Matthew Realff, Joseph Scott, Fani Boukouvala, Howard Hendrix, 
Christopher Jones, Ryan Lively, Frank Kong, and Trimeric staff).
