# Integrated Design and Operation Model for NGCC-PCC-DAC Retrofit

This repo contains the optimization model for the NGCC-PCC-DAC retrofit design modeled in `Julia/Jump` and `Python/Pyomo`.

## Main features
- co-optimizes the design and operational decisions
- considers multiple future energy scenarios (varying electricity prices for a year + varying CO2 prices)
- formulates a novel DAC model to account for sorbent dynamics
- contains logic for system start-up/shutdown

For the full model description, please contact [Pengfei Cheng](pengfeicheng@gatech.edu).

## Branches

Currently there are 4 branches:
- `main`: the most up-to-date one with all the features
- `base-NGCC`: contains the optimization model for the operations of B31A (unretrofitted NGCC)
- `pyomo-ver`: the identical model formulated in `Python/Pyomo`
- `pyomo-SP`: the stochastic version of the model in in `Python/Pyomo`

## `pyomo-SP` Branch Layout

```
.
├── src                                 # source files
│   ├── post_processing                 # post-processing scripts
│   ├── pyomo_model                     # optimization model files
│       ├── constraints
│       ├── output
│       ├── params
│       ├── model.py                    # main file
│       ├── obj.py
│       └── variables.py
│   ├── regression                      # regression scripts for data from simulation
│   └── resources                       # other resource files
├── README.md
└── requirements.txt
```

## Installation

### `Python` Environment
To install required packages, run
```shell
pip install -r requirements.text
```

### Optimization solver
To use a certain MILP solver, please install it separately.

## Usage (path setting may be necessary)

To directly run the model, simply execute `model.py`.

To run the model in a Jupyter notebook for exploratory programming, run:
```Python
from src.pyomo_model.model import *
```

## Data Sources

|Location|File name|Function|Source|
|---|---|---|---|
|`src/regression/`|`coefs.csv`|coefficients from simulation (only considers 50% and 100% load), currently in use|linear regression|
|`src/resources/`|`NGCC_performance.xlsx`|system performance coefficients|Howard Hendrix|
|`src/resources/`|`overall-price-signals.csv`|all sets of electricity price series|Princeton team and NREL team|
|`src/models/params`|`.py` files|other data|Georgia Tech FLECCS team|

## Credits

The code was initially developed by David Thierry and further developed and
maintained by Pengfei Cheng.
The development was funded by the ARPA-E's [FLECCS program](https://arpa-e.energy.gov/technologies/programs/fleccs)
and supported by the Georgia Tech FLECCS Team (Matthew Realff, Joseph Scott, Fani Boukouvala, Howard Hendrix,
Christopher Jones, Ryan Lively, Frank Kong, and Trimeric staff).
