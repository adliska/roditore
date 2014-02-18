#!/usr/bin/env python

import numpy as np
import h5py
import argparse

def corrmat_to_linklist(corrmatfile, dataset, outputfile, threshold=None):
    f = h5py.File(corrmatfile, 'r')
    corrmat = f[dataset][...]
    f.close()

    with open(outputfile, 'w') as o:
        for i in xrange(0, corrmat.shape[0]):
            for j in xrange(i+1, corrmat.shape[0]):
                if threshold == None or corrmat[i,j] > threshold:
                    o.write('{} {} {}\n'.format(i+1, j+1, corrmat[i,j]))

def corrmat_to_linklist_argparser():
    parser = argparse.ArgumentParser(
            description=('Converts a correlation matrix'
            'to a network in link list format.'))
    parser.add_argument('-i', '--input', metavar='FILE',
            help='Input HDF5 file', required=True)
    parser.add_argument('-d', '--dataset', metavar='DATASET',
            help='Input dataset', required=True)
    parser.add_argument('-o', '--output', metavar='FILE',
            help='Output link list file', required=True)
    parser.add_argument('-t', '--threshold', metavar='NUMBER',
            type=float, help='Threshold')
    return parser

def main():
    args = corrmat_to_linklist_argparser().parse_args()
    corrmat_to_linklist(args.input, args.dataset, args.output, 
            threshold=args.threshold)

if __name__ == '__main__':
    main()
