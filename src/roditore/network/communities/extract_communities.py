#!/usr/bin/env python 

import argparse
import nibabel as nib
import numpy as np

def extractCommunities(commfile):
    with open(commfile, 'r') as f:
        commdict = {}
        for line in f:
            split = line.split()
            community = split[3]
            voxel = (int(split[0]), int(split[1]), int(split[2]))
            if community in commdict:
                commdict[community].append(voxel)
            else:
                commdict[community] = [voxel]
    return commdict

def createCommunityMasks(commdict, masterimage, prefix):
    master = nib.load(masterimage)
    for community in commdict:
        data = np.zeros(master.get_shape())
        for voxel in commdict[community]:
            data[voxel] = 1
        nib.save(nib.Nifti1Image(data, master.get_affine()), 
                prefix+community+'.nii.gz')

def extractCommunitiesArgparser():
    parser = argparse.ArgumentParser(
            description='Extract community specific maps')
    parser.add_argument('-i', '--input', metavar='INPUTFILE', 
            help='Input file', required=True)
    parser.add_argument('-p', '--prefix', metavar='PREFIX', 
            help='Prefix', required=True)
    parser.add_argument('-m', '--master', metavar='MASTER',
            help='Master image', required=True)
    parser.add_argument('-l', '--limit', metavar='LIMIT',
            help='Maximum number of masks allowed', type=int)
    return parser

def main():
    args = extractCommunitiesArgparser().parse_args()

    commdict = extractCommunities(args.input)
    if (args.limit == None or 
            (args.limit > 0 and len(commdict) <= args.limit)):
        createCommunityMasks(commdict, args.master, args.prefix)
    else:
        print ("Number of communities (" +
                str(len(commdict)) +
                'is above the limit.')

if __name__ == "__main__":
    main();
