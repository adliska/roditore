#!/usr/bin/env python

import numpy as np
import h5py
import argparse
import roditore.utils.image_utils as imutils

def remove_voxels(corrmat, index, remove):
    indices = [i for i,j in enumerate(index) if j in remove]

    corrmat = np.delete(corrmat, indices, 0) ;
    corrmat = np.delete(corrmat, indices, 1) ;

    return corrmat
    

def remove_voxels_argparser():
    parser = argparse.ArgumentParser(
            description=('Removes voxels specified by dimensions.'))
    parser.add_argument('input', metavar='INPUT', help='Input HDF5 file')
    parser.add_argument('-d', '--dataset', metavar='DATASET',
            help='Dataset with the correlation matrix (for both input '
            'and output.', required=True)
    parser.add_argument('-x', '--index', metavar='INDEX',
            help='The voxel index file', required=True)
    parser.add_argument('-r', '--remove', metavar='REMOVE',required=True,
            help='List of voxels to remove')
    parser.add_argument('-o', '--output', metavar='OUTPUT',
            help='Output HDF5 file', required=True)
    
    return parser

def main():
    args = remove_voxels_argparser().parse_args()

    print 'Reading input dataset.'
    f = h5py.File(args.input, 'r')
    corrmat = f[args.dataset][...]
    f.close()
    
    print 'Total number of voxels:', str(corrmat.shape[0])

    print 'Reading voxel index.'
    index = imutils.voxel_index(args.index)

    print 'Reading voxels to remove.'
    remove = imutils.voxel_index(args.remove)

    print 'Removing voxels.'
    output = remove_voxels(corrmat, index, remove)

    print 'Writing output.'
    f = h5py.File(args.output, 'w-')
    f.create_dataset(args.dataset, data=output)
    f.close()

if __name__ == '__main__':
    main()
