#!/usr/bin/env python

import argparse
import h5py
import numpy as np
import sys

def avg_correlation_matrix(matfiles, verbose=False):
    if verbose:
        print 'Total number of matrices:', str(len(matfiles))
        print '1..'

    f = h5py.File(matfiles[0], 'r')
    subjmat = f['corrmat'][...]
    f.close()
    np.fill_diagonal(subjmat, 0)
    avgmat = np.arctanh(subjmat)

    for i in xrange(1, len(matfiles)):
        if verbose:
            print str(i+1)+'..'
        f = h5py.File(matfiles[i], 'r')
        subjmat = f['corrmat'][...]
        f.close()
        np.fill_diagonal(subjmat, 0)
        avgmat = avgmat + np.arctanh(subjmat)

    avgmat = np.tanh(avgmat / float(len(matfiles)))
    
    return avgmat

def avg_correlation_matrix_argparser():
    parser = argparse.ArgumentParser(
            description=('Computes the average correlation matrix from '
                'given correlation matrices. Uses Fisher transformation.'))
    parser.add_argument('input', metavar='SUBJMAT', nargs='+',
            help='Input correlation matrices')
    parser.add_argument('-o', '--output', metavar='AVGMAT', 
            help='The averaged correlation matrix will be written to AVGMAT.',
            required=True)
    parser.add_argument('-d', '--dataset', metavar='DATASET',
            help='Name of the HDF5 dataset.', required=True)
    parser.add_argument('-v', '--verbose', help='switch on the verbose mode',
            action='store_true', default=False)
    return parser

def main():
    args = avg_correlation_matrix_argparser().parse_args()

    avgcorrmat = avg_correlation_matrix(args.input, verbose=args.verbose)

    f = h5py.File(args.output, 'w-')
    f.create_dataset(args.dataset, data=avgcorrmat)
    f.close()

if __name__ == "__main__":
    main()
