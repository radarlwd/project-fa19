import os
import sys
sys.path.append('..')
sys.path.append('../..')
import argparse
import utils
from student_utils import *

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
    nodes = homes_idx + [start_idx]
    graph, msg = adjacency_matrix_to_graph(adjacency_matrix)
    newgraph = graph.subgraph(nodes)
    if not nx.is_connected(newgraph):
        newgraph = connect_homes(graph, nodes)
    mst = nx.minimum_spanning_tree(newgraph, 'weight')
    dfs = list(nx.dfs_edges(mst, start_idx))
    path = [start_idx]
    drop_offs = {}
    if start_idx in homes_idx:
        drop_offs[start_idx] = [start_idx]
    current_idx = -1
    while dfs:
        edge = dfs.pop(0)
        current_idx = edge[1]
        if current_idx not in path:
            path.append(current_idx)
            drop_offs[current_idx] = [current_idx]
    final_path = [path[0]]
    for i in range(len(path)-1):
        if graph.has_edge(path[i], path[i+1]):
            final_path.append(path[i+1])
        else:
            final_path.pop()
            final_path.extend(nx.shortest_path(graph, path[i], path[i+1], 'weight'))
    last_shortest_path = nx.shortest_path(graph, final_path[-1], start_idx, 'weight')
    final_path.pop()
    final_path.extend(last_shortest_path)
    return final_path, drop_offs

def connect_homes(graph, nodes):
    newgraph = nx.Graph()
    newgraph.add_nodes_from(nodes)
    for i in range(len(nodes)):
        for j in range(i + 1, len(nodes)):
            w = nx.shortest_path_length(graph, nodes[i], nodes[j], 'weight')
            newgraph.add_edge(nodes[i], nodes[j], weight=w)
    return newgraph


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
