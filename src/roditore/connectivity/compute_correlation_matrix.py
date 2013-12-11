#!/usr/bin/env python

import argparse
import nibabel as nib
import numpy as np
from roditore.utils.image_utils import voxelCoordinateGenerator

def computeCorrelationMatrix(imagefile, maskfile, output=None, index=None):
    img = nib.load(imagefile).get_data()
    mask = nib.load(maskfile).get_data()

    voxelpositions = [pos for pos in voxelCoordinateGenerator(mask.shape,
        mask=mask)]
    '''for pos in voxelCoordinateGenerator(mask.shape, mask=mask):
        voxelpositions.append(pos)'''
    
    corrmat = np.corrcoef([img[pos] for pos in voxelpositions])

    if output != None:
        np.save(output, corrmat)
    if index != None:
        with open(index, 'w') as f:
            for pos in voxelpositions:
                f.write('{0[0]} {0[1]} {0[2]}\n'.format(pos))

    return corrmat

def computeCorrelationMatrixArgparse():
    parser = argparse.ArgumentParser(description=('Computes correlation '
        'matrix for the given image file.'))
    parser.add_argument('-i', '--input', metavar='dset',
            required=True, help='Input dataset')
    parser.add_argument('-o', '--output', metavar='FILE',
            required=True, help='Output correlation matrix')
    parser.add_argument('-x', '--index', metavar='INDEXFILE',
            help='Output index file')
    parser.add_argument('-m', '--mask', metavar='FILE',
            required=True, help='Mask')
    return parser

def main():
    args = computeCorrelationMatrixArgparse().parse_args()
    computeCorrelationMatrix(args.input, args.mask, output=args.output, 
            index=args.index)

if __name__ == "__main__":
    main()
