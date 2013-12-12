#!/usr/bin/env python

import argparse
import numpy as np
import sys

def avg_corr_matrix(matfiles, verbose=False):
    if verbose:
        print 'Total number of matrices:', str(len(matfiles))
        print '1..'

    subjmat = np.load(matfiles[0])
    np.fill_diagonal(subjmat, 0)
    avgmat = np.arctanh(subjmat)

    for i in xrange(1, len(matfiles)):
        if verbose:
            print str(i+1)+'..'
        subjmat = np.load(matfiles[i])
        np.fill_diagonal(subjmat, 0)
        avgmat = avgmat + np.arctanh(subjmat)

    avgmat = np.tanh(avgmat / float(len(matfiles)))
    
    return avgmat

def avg_corr_matrix_argparser():
    parser = argparse.ArgumentParser(
            description=('Computes the average correlation matrix from '
                'given correlation matrices. Uses Fisher transformation.'))
    parser.add_argument('-i', '--input', metavar='SUBJMATs', nargs='+',
            help='Input correlation matrices', required=True)
    parser.add_argument('-o', '--output', metavar='AVGMAT', 
            help='The averaged correlation matrix will be written to AVGMAT.',
            required=True)
    parser.add_argument('-v', '--verbose', help='switch on the verbose mode',
            action='store_true', default=False)
    return parser

def main():
    args = avg_corr_matrix_argparser().parse_args()
    np.save(args.output, avg_corr_matrix(args.input, verbose=args.verbose))

if __name__ == "__main__":
    main()
