#!/usr/bin/env python 

import numpy as np
import argparse

def create_cooccurrence_network(filenames):
    commassignments = np.loadtxt(filenames[0], dtype=int)[:,3]
    communities = np.unique(commassignments)
    numvoxels = commassignments.shape[0]
    result = np.zeros((numvoxels,numvoxels))
    for community in communities:
        idx = np.nonzero(commassignments == community)[0]
        result[np.ix_(idx,idx)] += 1
    
    for i in xrange(1,len(filenames)):
        print i
        commassignments = np.loadtxt(filenames[i], dtype=int)[:,3]
        communities = np.unique(commassignments)
        for community in communities:
            idx = np.nonzero(commassignments == community)[0]
            result[np.ix_(idx,idx)] += 1

    result = result / len(filenames)
    return result
    
def create_cooccurrence_network_argparser():
    parser = argparse.ArgumentParser(
            description=('Cretes a weighted network for a set of community '
            'assignment files. Nodes in the network are voxels. Edge weights '
            'represent the ratio of networks in which the two connected '
            'voxels appeared in the same community.'))
    parser.add_argument('-i', '--input', metavar='INPUTs', required=True,
            nargs='+',help='Input network assignments.')
    parser.add_argument('-o', '--output', metavar='OUTPUT', required=True,
            help='Name of the output file. Network represented by an '
            'adjacency matrix.')
    return parser

def main():
    args = create_cooccurrence_network_argparser().parse_args()
    np.save(args.output, create_cooccurrence_network(args.input))

if __name__ == '__main__':
    main()
