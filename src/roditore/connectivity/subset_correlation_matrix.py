#!/usr/bin/env python

import numpy as np
import h5py
import argparse
import roditore.utils.image_utils as imutils

def subset_correlation_matrix(corrmat, index, subset):
    indices = [index.index(pos) for pos in subset]
    return corrmat[np.ix_(indices, indices)]

def subset_correlation_matrix_argparser():
    parser = argparse.ArgumentParser(
            description=('Subsets a correlation matrix.'))
    parser.add_argument('input', metavar='INPUT', help='Input HDF5 file')
    parser.add_argument('subset', metavar='subset', help='List of voxels of '
            'interest.')
    parser.add_argument('-d', '--dataset', metavar='dataset',
            help='Dataset with the correlation matrix (for both input '
            'and output.', required=True)
    parser.add_argument('-x', '--index', metavar='index',
            help='The voxel index file', required=True)
    parser.add_argument('-o', '--output', metavar='OUTPUT',
            help='Output HDF5 file', required=True)
    
    return parser

def main():
    args = subset_correlation_matrix_argparser().parse_args()

    print 'Reading input dataset.'
    f = h5py.File(args.input, 'r')
    corrmat = f[args.dataset][...]
    f.close()
    print 'Total number of voxels:', str(corrmat.shape[0])

    print 'Reading voxel index.'
    index = imutils.voxel_index(args.index)

    print 'Reading the voxels subset.'
    subset = imutils.voxel_index(args.subset)
    print 'Total number of voxels in the subset:', str(len(subset))

    print 'Subsetting the correlation matrix.'
    output = subset_correlation_matrix(corrmat, index, subset)

    print 'Writing output.'
    f = h5py.File(args.output, 'w-')
    f.create_dataset(args.dataset, data=output)
    f.close()

if __name__ == '__main__':
    main()
