#/usr/bin/env python

import numpy as np
import argparse

def corrmatToPajek(corrmatfile, threshold, outputfile, indexfile=None):
    corrmat = np.load(corrmatfile)
    
    vertices = []
    if indexfile != None:
        with open(indexfile, 'r') as i:
            vertices = [x.strip() for x in i.readlines()]
    else:
        vertices = range(1, corrmat.shape[0]+1)

    with open(outputfile, 'w') as o:
        o.write('*Vertices {}\n'.format(corrmat.shape[0]))
        for i in xrange(0, corrmat.shape[0]):
            o.write('{} "{}"\n'.format(i+1, vertices[i]))
        
        o.write('*Edges\n')
        for i in xrange(0, corrmat.shape[0]):
            for j in xrange(i+1, corrmat.shape[0]):
                if corrmat[i,j] >= threshold:
                    o.write('{} {} {}\n'.format(i+1, j+1, corrmat[i,j]))

def corrmatToPajekArgparser():
    parser = argparse.ArgumentParser(
            description=('Converts a correlation matrix' 
                'to a network in Pajek format'))
    parser.add_argument('-i', '--input', metavar='FILE',
            help='Input matrix', required=True)
    parser.add_argument('-x', '--indices', metavar='INDEXFILE',
            help='Index file')
    parser.add_argument('-o', '--output', metavar='FILE',
            help='Output network in Pajek format', required=True)
    parser.add_argument('-t', '--threshold', metavar='NUMBER',
            type=float, help='Threshold')
    return parser

def main():
    args = corrmatToPajekArgparser().parse_args()
    corrmatToPajek(args.input, args.threshold, args.output, 
            indexfile=args.indices)

if __name__ == '__main__':
    main()
