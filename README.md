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

- Open a terminal at the current directory where this README.md located
- Run the following command in any shell to generate outputs:
    + `python3 terminator.py solver.py final outputs generate`
    + The output files will be placed in the directory: `final/outputs/`
- Run the following command to generate the json file:
    + `python3 terminator.py solver.py final outputs compress`


