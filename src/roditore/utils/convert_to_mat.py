import numpy as np
import scipy.io as sio
import argparse

def convert_to_mat(input, output, varname):
    sio.savemat(output, {varname:np.load(input)})
    
def convert_to_mat_argparser():
    parser = argparse.ArgumentParser(
            description=('Converts a NumPy array into a MATLAB-style .mat '
                'file.'))
    parser.add_argument('-i', '--input', metavar='INPUT', required=True,
            help='Input NumPy array.')
    parser.add_argument('-o', '--output', metavar='OUTPUT', required=True,
            help='MATLAB-style file will be saved in OUTPUT.')
    parser.add_argument('-v', '--variable-name', metavar='VARNAME',
            required=True, help=('The NumPy array will by saved under '
                'variable name VARNAME.'))

def main():
    args = convert_to_mat_argparse().parse_args()
    convert_to_mat(args.input, args.output, args.variable_name)

if __name__ = '__main__':
    main()
