import os
import sys
sys.path.append('..')
sys.path.append('../..')
import argparse
import utils
from student_utils import *
from queue import PriorityQueue

"""
======================================================================
  Complete the following function.
======================================================================
"""

def solve(list_of_locations, list_of_homes, starting_car_location, adjacency_matrix, params=[]):
    """
    Write your algorithm here.
    Input:
        list_of_locations: A list of locations such that node i of the graph corresponds to name at index i of the list
        list_of_homes: A list of homes
        starting_car_location: The name of the starting location for the car
        adjacency_matrix: The adjacency matrix from the input file
    Output:
        A list of locations representing the car path
        A dictionary mapping drop-off location to a list of homes of TAs that got off at that particular location
        NOTE: both outputs should be in terms of indices not the names of the locations themselves
    """

    start_idx = list_of_locations.index(starting_car_location)
    homes_idx = [list_of_locations.index(h) for h in list_of_homes]
    graph1, msg1 = adjacency_matrix_to_graph(adjacency_matrix)
    start_shortest_paths = nx.shortest_path(graph1, start_idx, target=None, weight='weight')
    minimum = float('inf')
    final_path = []
    final_dropoffs = {}
    for h in homes_idx:
        path = []
        path.extend(start_shortest_paths[h])
        path.pop()
        drop_offs = {}
        if start_idx in homes_idx:
            drop_offs[start_idx] = [start_idx]
            homes_idx.remove(start_idx)
        homes_copy = homes_idx.copy()
        current_idx = h
        while homes_copy:
            lst_dist = []
            shortest_path_length = nx.shortest_path_length(graph1, current_idx, target=None, weight='weight')
            for h in homes_copy:
                lst_dist.append((h, shortest_path_length[h]))
            idx, _ = min(lst_dist, key=lambda x: x[1])
            shortest_path = nx.shortest_path(graph1, current_idx, idx, 'weight')
            shortest_path.pop()
            path.extend(shortest_path)
            drop_offs[idx] = [idx]
            current_idx = idx
            homes_copy.remove(idx)
        last_shortest_path = nx.shortest_path(graph1, current_idx, start_idx, 'weight')
        path.extend(last_shortest_path)
        cost = cost_of_solution_no_print(graph1, path, drop_offs)
        if cost < minimum:
            final_path = path
            final_dropoffs = drop_offs
    return final_path, final_dropoffs


"""
======================================================================
   No need to change any code below this line
======================================================================
"""

"""
Convert solution with path and dropoff_mapping in terms of indices
and write solution output in terms of names to path_to_file + file_number + '.out'
"""
def convertToFile(path, dropoff_mapping, path_to_file, list_locs):
    string = ''
    for node in path:
        string += list_locs[node] + ' '
    string = string.strip()
    string += '\n'

    dropoffNumber = len(dropoff_mapping.keys())
    string += str(dropoffNumber) + '\n'
    for dropoff in dropoff_mapping.keys():
        strDrop = list_locs[dropoff] + ' '
        for node in dropoff_mapping[dropoff]:
            strDrop += list_locs[node] + ' '
        strDrop = strDrop.strip()
        strDrop += '\n'
        string += strDrop
    utils.write_to_file(path_to_file, string)

def solve_from_file(input_file, output_directory, params=[]):
    print('Processing', input_file)

    input_data = utils.read_file(input_file)
    num_of_locations, num_houses, list_locations, list_houses, starting_car_location, adjacency_matrix = data_parser(input_data)
    car_path, drop_offs = solve(list_locations, list_houses, starting_car_location, adjacency_matrix, params=params)

    basename, filename = os.path.split(input_file)
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    output_file = utils.input_to_output(input_file, output_directory)

    convertToFile(car_path, drop_offs, output_file, list_locations)


def solve_all(input_directory, output_directory, params=[]):
    input_files = utils.get_files_with_extension(input_directory, 'in')

    for input_file in input_files:
        solve_from_file(input_file, output_directory, params=params)


if __name__=="__main__":
    parser = argparse.ArgumentParser(description='Parsing arguments')
    parser.add_argument('--all', action='store_true', help='If specified, the solver is run on all files in the input directory. Else, it is run on just the given input file')
    parser.add_argument('input', type=str, help='The path to the input file or directory')
    parser.add_argument('output_directory', type=str, nargs='?', default='.', help='The path to the directory where the output should be written')
    parser.add_argument('params', nargs=argparse.REMAINDER, help='Extra arguments passed in')
    args = parser.parse_args()
    output_directory = args.output_directory
    if args.all:
        input_directory = args.input
        solve_all(input_directory, output_directory, params=args.params)
    else:
        input_file = args.input
        solve_from_file(input_file, output_directory, params=args.params)
