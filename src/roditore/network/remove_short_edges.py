#!/usr/bin/env python

import numpy as np
import h5py
import argparse
import roditore.utils.image_utils as imutils

def remove_short_edges(corrmat, index, dimensions, radius):
    neighbourhood = imutils.voxel_neighbourhood(radius, dimensions)
    voxelmap = imutils.voxel_map(index)
    
    for i in xrange(0, len(index)):
        if i % 2000 == 0:
            print i
        for move in neighbourhood:
            neighbour = tuple(x+y for x,y in zip(index[i], move))
            if neighbour in voxelmap:
                corrmat[i, voxelmap[neighbour]] = 0
                corrmat[voxelmap[neighbour], i] = 0

        '''
        for j in xrange(i, len(index)):
            if i*len(index)+j % 10000 == 0:
                print str(i*len(index)+j)
            print str(i), str(j)
            if imutils.voxel_distance(index[i], index[j], 
                    resolution) < radius:
                corrmat[i,j] = 0
                corrmat[j,i] = 0'''
    return corrmat

def remove_short_edges_argparser():
    parser = argparse.ArgumentParser(
            description=('Modifies network by removing short distance '
            'relationships. See Power et al. 2011 (Neuron). '))
    parser.add_argument('input', metavar='INPUT', help='Input HDF5 file')
    parser.add_argument('-d', '--dataset', metavar='DATASET',
            help='Dataset with the correlation matrix (for both input '
            'and output.', required=True)
    parser.add_argument('-x', '--index', metavar='VOXELINDEX',
            help='The voxel index file', required=True)
    parser.add_argument('-r', '--radius', metavar='RADIUS',required=True,
            type=float, help='Radius')
    parser.add_argument('-o', '--output', metavar='OUTPUT',
            help='Output HDF5 file', required=True)

    
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-n', '--dimen', metavar='DIM', nargs=3, type=float,
            help='Dimensions of the dataset.')
    group.add_argument('-m', '--master', metavar='MASTER', 
            help='Master image. Either dimensions or a master image '
            'must be given.')
    
    return parser

def main():
    args = remove_short_edges_argparser().parse_args()

    print 'Reading input dataset.'
    f = h5py.File(args.input, 'r')
    corrmat = f[args.dataset][...]
    f.close()
    
    print ('Total number of edges:', 
            str(corrmat.shape[0]*corrmat.shape[1]/2))

    print 'Reading voxel index.'
    index = imutils.voxel_index(args.index)

    if args.dimen != None:
        dimensions=args.dimen

    print 'Modifying the network.'
    output = remove_short_edges(corrmat, index, dimensions, args.radius)

    print 'Writing output.'
    f = h5py.File(args.output, 'w-')
    f.create_dataset(args.dataset, data=output)
    f.close()

if __name__ == '__main__':
    main()
