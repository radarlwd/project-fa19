import os
import sys
sys.path.append('..')
sys.path.append('../..')
import argparse
import utils
from student_utils import *
import student_utils
import random as rd
import math
from queue import PriorityQueue


L_MAX = 120
INIT_TEMP = 24
ITER_NUM = 1000
INIT_PROB = 0.5

"""
======================================================================
  Complete the following function.
======================================================================
"""

def solve(list_of_locations, list_of_homes, starting_car_location, adjacency_matrix, input_file, params=[]):
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

    homes_idx = [list_of_locations.index(h) for h in list_of_homes]
    graph, msg = student_utils.adjacency_matrix_to_graph(adjacency_matrix)

    #nn_output_directory = 'nearest_neighbor_algo/outputs'
    #nn_output_directory = 'local_search/outputs'
    nn_output_directory = 'mst_2_approximation/outputs'
    nn_output_file = utils.input_to_output(input_file, nn_output_directory)
    nn_output_data = utils.read_file(nn_output_file)
    car_cycle = nn_output_data[0]
    car_cycle_idx = student_utils.convert_locations_to_indices(car_cycle, list_of_locations)

    shortest_paths = nx.floyd_warshall(graph, weight='weight')
    new_car_cycle_idx = local_search(car_cycle_idx, shortest_paths)

    #final_path
    final_cycle = []
    for i in range(len(new_car_cycle_idx)-1):
        shortest_path = nx.shortest_path(graph, new_car_cycle_idx[i], new_car_cycle_idx[i+1], weight='weight')
        shortest_path.pop()
        final_cycle.extend(shortest_path)
    final_cycle.append(new_car_cycle_idx[-1])
    dropoffs = get_valid_dropoffs(final_cycle, homes_idx)
    return final_cycle, dropoffs

def get_shortest_cost(car_path, shortest_paths):
    total = 0
    for i in range(len(car_path)-1):
        total += (shortest_paths[car_path[i]][car_path[i+1]] * 2 / 3)
    return total


def inverse(car_path, i, j):
    """swap anything in between i and j, both indices inclusively"""
    return car_path[:i] + car_path[i:j+1][::-1] + car_path[j+1:]

def insert(car_path, i, j):
    p = car_path[:]
    item = p.pop(j)
    p.insert(i, item)
    return p

def swap(car_path, i, j):
    p = car_path[:]
    p[i], p[j] = p[j], p[i]
    return p

def get_valid_dropoffs(car_path, homes_idx):
    drop_off_locations = {}
    for v in car_path:
        if v in homes_idx:
            drop_off_locations[v] = [v]
    return drop_off_locations

def get_local_best_neighbor(car_path, shortest_paths, i ,j):
    """Minimum of three modified paths, original one not included"""
    p1 = inverse(car_path, i, j)
    p2 = insert(car_path, i, j)
    p3 = swap(car_path, i, j)
    cost_dict = {}
#     print(get_shortest_cost(car_path, shortest_paths))
    cost_dict["p1"] = get_shortest_cost(p1, shortest_paths)
    cost_dict["p2"] = get_shortest_cost(p2, shortest_paths)
    cost_dict["p3"] = get_shortest_cost(p3, shortest_paths)

#     print(cost_dict)
    minKey = min(cost_dict, key=cost_dict.get)
    if minKey == "p1":
        return p1, cost_dict["p1"]
    elif minKey == "p2":
        return p2, cost_dict["p2"]
    else:
        return p3, cost_dict["p3"]


def init_temp_list(car_path, shortest_paths, length):
    L = PriorityQueue()
    i = 0
    while i < length:
        neighbor, costy = rand_gen_neighbor(car_path, shortest_paths)
        costx = get_shortest_cost(car_path, shortest_paths)
        if costy < costx:
            car_path = neighbor
        else:
            t = -abs(costy - costx) / math.log(INIT_PROB)
            L.put(-t)
            i = i + 1
    return L

def gen_rand_idx(x, y):
    while True:
        a = rd.randint(x, y)
        b = rd.randint(x, y)
        if abs(a-b) >= 2:
            if a < b:
                return a, b
            else:
                return b, a

def rand_gen_neighbor(car_path, shortest_paths):
    i, j = gen_rand_idx(1, len(car_path)-2)
    return get_local_best_neighbor(car_path, shortest_paths, i, j)

def acceptance_probability(delta, t_max):
    try:
        return math.exp(-delta / t_max)
    except ZeroDivisionError:
        return 0
    except OverflowError:
        return 0

def new_temp(t, delta, r):
    return (t - delta) / math.log(r)

def local_search(car_path, shortest_paths):
    L = init_temp_list(car_path, shortest_paths, L_MAX)
    k = 0
    while k < L_MAX - 1:
        t_max = -L.get(block=False)
        k = k + 1
        t = 0
        c = 0
        m = 0
        while m < ITER_NUM:
            m = m + 1
            neighbor, costy = rand_gen_neighbor(car_path, shortest_paths)
            costx = get_shortest_cost(car_path, shortest_paths)
            if costy < costx:
                car_path = neighbor
            else:
                delta = costy - costx
                p = acceptance_probability(delta, t_max)
                r = rd.random()
                if r < p:
                    t = new_temp(t, delta, r)
                    c = c + 1
        if c != 0:
            L.get(block=False)
            L.put(-t/c)
    return car_path


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
    car_path, drop_offs = solve(list_locations, list_houses, starting_car_location, adjacency_matrix, input_file, params=params)

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
