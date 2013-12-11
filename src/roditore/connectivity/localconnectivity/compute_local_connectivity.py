import numpy as np
import nibabel as nib
import math
import argparse
from roditore.utils.image_utils import (isVoxelInMask, 
        voxelCoordinateGenerator)

def computeLocalConnectivity(imagefile, radius, maskfile, prefix=None):
    img = nib.load(imagefile)
    mask = nib.load(maskfile).get_data()

    shape = img.get_shape()
    zooms = img.get_header().get_zooms()
    data = img.get_data()
    
    neighbourhood = getNeighbourhood(radius, zooms)
    
    localConnectivity = np.zeros(data.shape[0:3])
    for i,j,k in voxelCoordinateGenerator(data.shape, mask=mask):
        connections = 0
        for ii, jj, kk in neighbourhood:
            ni = i +ii
            nj = j+jj
            nk = k+kk
            if (isVoxelInMask(ni, nj, nk, mask) and
                np.corrcoef(data[i,j,k], data[ni,nj,nk])[0,1] >= 0.25):
                connections = connections+1
        localConnectivity[i,j,k] = connections
    if prefix != None:
        nib.save(nib.Nifti1Image(localConnectivity, img.get_affine()),\
                prefix)

def voxelCoordGenerator(shape):
    for k in xrange(0, shape[2]):
        for j in xrange(0, shape[1]):
            for i in xrange(0, shape[0]):
                yield(i,j,k)

def getNeighbourhood(radius, zooms):
    rad0 = int(radius/zooms[0])
    rad1 = int(radius/zooms[1])
    rad2 = int(radius/zooms[2])

    neighbours = []
    for i in xrange(0, rad0+1):
        for j in xrange(0, rad1+1):
            for k in xrange(0, rad2+1):
                if ((i>0 or j>0 or k>0) and
                    math.sqrt((i*zooms[0])**2 +
                        (j*zooms[1])**2 + (k*zooms[2])**2) <= radius):
                    neighbours.extend({(i, j, k),
                                       (i, j, -k),
                                       (i, -j, k),
                                       (i, -j, -k),
                                       (-i, j, k),
                                       (-i, j, -k),
                                       (-i, -j, k),
                                       (-i, -j, -k)})
    return neighbours

def computeLocalConnectivityArgparser():
    parser = argparse.ArgumentParser(
            description=('Computers local connectivity for each voxel within'
                'the given radius and outputs it as a NIFTI image.'))
    parser.add_argument('-i', '--input', metavar='CORRMAT',
            help='Input correlation matrix', required=True)
    parser.add_argument('-p', '--prefix', metavar='PREFIX',
            help='Prefix of the output file', required=True)
    parser.add_argument('-r', '--radius', metavar='RADIUS', type=float,
            help='Radius of local neighbourhood', required=True)
    parser.add_argument('-m', '--mask', metavar='MASK', 
            help='Mask image', required=True)
    return parser

def main():
    args = computeLocalConnectivityArgparser().parse_args()
    computeLocalConnectivity(args.input, args.radius, args.mask, 
            prefix=args.prefix)

if __name__ == '__main__':
    main()
