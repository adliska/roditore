#/usr/bin/env python

import numpy as np
import argparse

def corrmatToLinkList(corrmatfile, threshold, outputfile):
    corrmat = np.load(corrmatfile)
    with open(outputfile, 'w') as o:
        for i in xrange(0, corrmat.shape[0]):
            for j in xrange(i+1, corrmat.shape[0]):
                if corrmat[i,j] >= threshold:
                    o.write('{} {} {}\n'.format(i+1, j+1, corrmat[i,j]))

def corrmatToLinkListArgparser():
    parser = argparse.ArgumentParser(
            description=('Converts a correlation matrix'
            'to a network in link list format.'))
    parser.add_argument('-i', '--input', metavar='FILE',
            help='Input matrix', required=True)
    parser.add_argument('-o', '--output', metavar='FILE',
            help='Output link list file', required=True)
    parser.add_argument('-t', '--threshold', metavar='NUMBER',
            type=float, help='Threshold')
    return parser

def main():
    args = corrmatToLinkListArgparser().parse_args()
    corrmatToLinkList(args.input, args.threshold, args.output)

if __name__ == '__main__':
    main()
