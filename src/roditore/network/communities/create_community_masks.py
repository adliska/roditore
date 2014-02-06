#!/usr/bin/env python 

import argparse
import nibabel as nib
import numpy as np

def extract_communities(commfile):
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

def create_community_masks(commdict, masterimage, prefix):
    master = nib.load(masterimage)
    for community in commdict:
        data = np.zeros(master.get_shape())
        for voxel in commdict[community]:
            data[voxel] = 1
        nib.save(nib.Nifti1Image(data, master.get_affine()), 
                prefix+community+'.nii.gz')

def create_community_masks_argparser():
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
    args = create_community_masks_argparser().parse_args()

    commdict = extract_communities(args.input)
    if (args.limit == None or 
            (args.limit > 0 and len(commdict) <= args.limit)):
        create_community_masks(commdict, args.master, args.prefix)
    else:
        print ("Number of communities (" + str(len(commdict)) +
                'is above the limit.')

if __name__ == "__main__":
    main();
