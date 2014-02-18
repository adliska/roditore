#/usr/bin/env python

import numpy as np
import h5py
import argparse
import roditore.utils.image_utils as imutils

def corrmat_to_pajek(corrmat, output, threshold=None, index=None):
    if index is None:
        index = range(1, corrmat.shape[0]+1)

    output.write('*Vertices {}\n'.format(corrmat.shape[0]))
    for i in xrange(0, corrmat.shape[0]):
        output.write('{0} "{1[0]} {1[1]} {1[2]}"\n'.format(i+1, index[i]))
    
    output.write('*Edges\n')
    for i in xrange(0, corrmat.shape[0]):
        for j in xrange(i+1, corrmat.shape[0]):
            if threshold is None or corrmat[i,j] >= threshold:
                output.write('{} {} {}\n'.format(i+1, j+1, corrmat[i,j]))

def corrmat_to_pajek_argparser():
    parser = argparse.ArgumentParser(
            description=('Converts a correlation matrix' 
                'to a network in Pajek format'))
    parser.add_argument('input', metavar='INPUT', help='Input HDF5 file.')
    parser.add_argument('-d', '--dataset', metavar='DATASET',
            help='Dataset with the correlation matrix.', required=True)
    parser.add_argument('-x', '--index', metavar='INDEXFILE',
            help='Voxel index file')
    parser.add_argument('-o', '--output', metavar='OUTPUT',
            help='Output network in Pajek format')
    parser.add_argument('-t', '--threshold', metavar='THRESHOLD',
            type=float, help='Threshold')
    return parser

def main():
    args = corrmat_to_pajek_argparser().parse_args()

    print 'Reading input dataset.'
    f = h5py.File(args.input, 'r')
    corrmat = f[args.dataset][...]
    f.close()

    if args.index is not None:
        print 'Reading voxel index.'
        index = imutils.voxel_index(args.index)
    else:
        index = None

    if args.output is not None:
        print 'Opening output file.'
        output = open(args.output, 'w')
    else:
        output = sys.stdout

    print 'Converting the matrix.'
    corrmat_to_pajek(corrmat, output, threshold=args.threshold, index=index)

    if args.output is not None:
        print 'Closing file.'
        output.close()

if __name__ == '__main__':
    main()
