# CS 170 Fall 2019 Project

## Approaches

- We used different algorithms to generate outputs for all inputs, and we
  store them in separated directories.
    + Each directory such as `nearest_neighbor_algo` contains: an
    outputs directory with all the output files, and a log.txt file with
    all the messages.
- Then we wrote a script to pick the best output for each input based on
  the cost of it.

## How to produce the final outputs?

- Run `jupyter notebook` and open the solvers.ipynb
    + The file contains code for multiple solvers
    + Copy the content of the `<something>_solver` function to the `solve()`
    function in the `solver.py`
    + Copy all the helpers functions in the cell above the solver
    function
    + Import all the needed libraries for each solver
- Open a terminal at the current directory where this `README.md` located
- Run the following command in any shell to generate outputs for each
  solver:
    + `python3 terminator.py solver.py <name_of_solver> <input_directory> all`
    + `python3 terminator.py solver.py nearest_neighbor_solver inputs all`
    + The output files will be placed in the directory: `nearest_neighbor_solver/outputs/`
    + Repeat the same process for all other solvers
- Run the following command to generate the final outputs:
    + `python3 terminator.py solver.py final inputs generate`
- Run the following command to generate the json file:
    + `python3 terminator.py solver.py final outputs compress`


