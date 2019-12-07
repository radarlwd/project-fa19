import argparse, os, shutil
from utils import *
from student_utils import *

def select_outputs(pickle_dir):
    pfiles = get_files_with_extension(pickle_dir, 'p')
    dic = {}
    meta_dic = {}
    for pf in pfiles:
        pobj = load_obj(pf)
        for item in pobj:
            # key=<./path/to/input_file>.in, value=(<./path/to/output_file.out>, cost)
            input_file = item[0]
            output_file = item[1]
            cost = item[2][0]
            if input_file in dic:
                dic[input_file].append((output_file, cost))
            else:
                dic[input_file] = [(output_file, cost)]
    if not os.path.isdir('final/outputs'):
        os.mkdir('final')
        os.mkdir('final/outputs')
    for lst in dic.values():
        best_output, best_cost = min(lst, key=lambda x: x[1])
        os.system('cp ' + best_output + ' final/outputs/')
        meta_dic[best_output] = best_cost
    save_obj(meta_dic, 'final/meta.p')
    write_data_to_file('final/meta.txt', meta_dic.items(), '\n')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Parsing arguments')
    parser.add_argument('solver', type=str, help='Name of your solver, e.g. son_solver.py')
    parser.add_argument('algo', type=str, help='Name of your algorithm, e.g. nearest_neighbor_algo')
    parser.add_argument('input', type=str, help='Name of your input folder, e.g. inputs')
    parser.add_argument('mode', type=str, help='The modes: test, test_validate, all, validate, compress, clean, generate')
    args = parser.parse_args()
    full_algo = os.getcwd() + '/' + args.algo
    full_outputs = full_algo + '/outputs'
    outputs = args.algo + '/outputs'
    pickle = 'pickle_output/' + args.algo + '.p'
    log = args.algo + '/log.txt'
    if args.mode == 'test':
        os.system('python3 ' + args.solver + ' --all test_inputs test_outputs')
    elif args.mode == 'test_validate':
        os.system('python3 output_validator.py --all test_inputs test_outputs pickle_output/test.p 2>&1 | tee test_log.txt')
    elif args.mode == 'all':
        if not os.path.isdir(full_algo):
            os.mkdir(full_algo)
        if not os.path.isdir(full_outputs):
            os.mkdir(full_outputs)
        os.system('python3 ' + args.solver + ' --all ' + args.input + ' ' + outputs)
    elif args.mode == 'validate':
        os.system('python3 output_validator.py --all inputs ' + outputs + ' ' + pickle + ' 2>&1 | tee ' + log)
    elif args.mode == 'compress':
        os.system('python3 compress_output.py ' + outputs + '/')
    elif args.mode == 'clean':
        if os.path.isdir('final'):
            shutil.rmtree('final')
        if os.path.isdir('test_outputs'):
            shutil.rmtree('test_outputs')
        if os.path.isfile('outputs.json'):
            os.remove('outputs.json')
        if os.path.isfile('pickle_output/final.p'):
            os.remove('pickle_output/final.p')
        if os.path.isfile('pickle_output/test.p'):
            os.remove('pickle_output/test.p')
    elif args.mode == 'generate':
        select_outputs('pickle_output')

