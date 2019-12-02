import argparse, os

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Parsing arguments')
    parser.add_argument('solver', type=str, help='Name of your solver, e.g. son_solver.py')
    parser.add_argument('algo', type=str, help='Name of your algorithm, e.g. nearest_neighbor_algo')
    parser.add_argument('mode', type=str, help='The modes: test, test_validate, all, validate, compress')
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
        os.system('python3 ' + args.solver + ' --all inputs ' + outputs)
    elif args.mode == 'validate':
        os.system('python3 output_validator.py --all inputs ' + outputs + ' ' + pickle + ' 2>&1 | tee ' + log)
    elif args.mode == 'compress':
        os.system('python3 compress_output.py ' + outputs + '/')



