#!/usr/bin/env python

import argparse
import sys

def parse_infomap_output(treefile, output):
    commdict = {}
    with open(treefile, 'r') as t:
        for line in t:
            if not line.startswith('#'):
                split = line.split()
                voxel = (int(split[2].strip('"')), int(split[3]), 
                        int(split[4].strip('"')))
                commdict[voxel] = int(split[0].split(':')[0])
    for voxel in commdict:
        output.write('{0[0]} {0[1]} {0[2]} {1}\n'.format(voxel, 
            commdict[voxel]))

def parse_infomap_output_argparser():
    parser = argparse.ArgumentParser(
            description='Parses the tree output of Infomap')
    parser.add_argument('input', metavar='INPUT',
            help='Input tree file')
    parser.add_argument('-o', '--output', metavar='OUTPUTFILE',
            help='Output file')
    return parser

def main():
    args = parse_infomap_output_argparser().parse_args()

    if args.output is not None:
        output = open(args.output, 'w')
    else:
        output = sys.stdout

    parse_infomap_output(args.input, output)

    if args.output is not None:
        output.close()



if __name__ == '__main__':
    main()
