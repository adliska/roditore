#!/usr/bin/env python

import argparse
import nibabel as nib
import h5py
import numpy as np
import roditore.utils.image_utils as imutils

def correlation_matrix(image, voxelindex):
    return np.corrcoef([image[pos] for pos in voxelindex])

def correlation_matrix_argparse():
    parser = argparse.ArgumentParser(description=('Computes correlation '
        'matrix for the given image file.'))
    parser.add_argument('input', metavar='INPUT', help='Input image')
    parser.add_argument('-o', '--output', metavar='OUTPUT', required=True,
            help='Correlation matrix will be written to OUTPUT')
    parser.add_argument('-d', '--dataset', metavar='DATASET',
            required=True, help='Name of the HDF5 dataset.')
    parser.add_argument('-x', '--index', metavar='INDEX', required=True,
            help='The voxel index file.')
    return parser

def main():
    args = correlation_matrix_argparse().parse_args()

    image = nib.load(args.input).get_data()
    voxelindex = imutils.voxel_index(args.index)

    corrmat = correlation_matrix(image, voxelindex)

    f = h5py.File(args.output, 'w-')
    f.create_dataset(args.dataset, data=corrmat)
    f.close()

if __name__ == "__main__":
    main()
