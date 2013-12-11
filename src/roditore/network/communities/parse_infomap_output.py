#!/usr/bin/env python

import argparse

def parseInfomapOutput(treefile, outputfile):
    commdict = {}
    with open(treefile, 'r') as t:
        for line in t:
            if not line.startswith('#'):
                split = line.split()
                voxel = (int(split[2].strip('"')), int(split[3]), 
                        int(split[4].strip('"')))
                commdict[voxel] = int(split[0].split(':')[0])
    with open(outputfile, 'w') as o:
        for voxel in commdict:
            o.write('{0[0]} {0[1]} {0[2]} {1}\n'.format(voxel, 
                commdict[voxel]))

def parseInfomapOutputArgparser():
    parser = argparse.ArgumentParser(
            description='Parses the tree output of Infomap')
    parser.add_argument('-i', '--input', metavar='FILE',
            help='Input tree file', required=True)
    parser.add_argument('-o', '--output', metavar='OUTPUTFILE',
            help='Output file', required=True)
    return parser

def main():
    args = parseInfomapOutputArgparser().parse_args()
    parseInfomapOutput(args.input, args.output)

if __name__ == '__main__':
    main()
