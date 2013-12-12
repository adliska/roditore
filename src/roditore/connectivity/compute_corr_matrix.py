#!/usr/bin/env python

import argparse
import nibabel as nib
import numpy as np
from roditore.utils.image_utils import voxel_coord_gen

def compute_corr_matrix(imagefile, maskfile, output=None, index=None):
    img = nib.load(imagefile).get_data()
    mask = nib.load(maskfile).get_data()

    voxels = [pos for pos in voxel_coord_gen(mask.shape, mask=mask)]
    corrmat = np.corrcoef([img[pos] for pos in voxels])

    if output != None:
        np.save(output, corrmat)
    if index != None:
        with open(index, 'w') as f:
            for voxel in voxels:
                f.write('{0[0]} {0[1]} {0[2]}\n'.format(voxel))

    return corrmat

def compute_corr_matrix_argparse():
    parser = argparse.ArgumentParser(description=('Computes correlation '
        'matrix for the given image file.'))
    parser.add_argument('-i', '--input', metavar='INPUT',
            required=True, help='Input image')
    parser.add_argument('-o', '--output', metavar='OUTPUT',
            required=True, 
            help='Correlation matrix will be written to OUTPUT')
    parser.add_argument('-x', '--index', metavar='INDEXFILE',
            help='The index file will be output to INDEXFILE.')
    parser.add_argument('-m', '--mask', metavar='MASK',
            required=True, help='Mask')
    return parser

def main():
    args = compute_corr_matrix_argparse().parse_args()
    compute_corr_matrix(args.input, args.mask, output=args.output, 
            index=args.index)

if __name__ == "__main__":
    main()
