import os
import math
import numpy as np

def voxel_coord_gen(shape, mask=None):
    for k in xrange(0, shape[2]):
        for j in xrange(0, shape[1]):
            for i in xrange(0, shape[0]):
                if mask == None or mask[i,j,k] == 1:
                    yield(i,j,k)

def mask_voxels(mask):
    return zip(*np.where(mask == 1))

def print_voxels(voxels, output):
    for voxel in voxels:
        output.write('{0[0]} {0[1]} {0[2]}\n'.format(voxel))

def is_in_mask(i, j, k, mask):
    if (i >= 0 and i < mask.shape[0]
            and j >= 0 and j < mask.shape[1]
            and k >= 0 and k < mask.shape[2]
            and mask[i,j,k] == 1):
        return True
    else:
        return False

def imagename(path):
    name = os.path.splitext(os.path.basename(path))[0]
    if name.endswith('.nii'):
        name = os.path.splitext(name)[0]

    return name

def voxel_distance(voxel1, voxel2, resolution):
    return math.sqrt(((voxel1[0]-voxel2[0])*resolution[0])**2 +
            ((voxel1[1]-voxel2[1])*resolution[1])**2 +
            ((voxel1[2]-voxel2[2])*resolution[2])**2)

def voxel_index(indexfile):
    with open(indexfile, 'r') as f:
        index = [tuple([int(y) for y in x]) for x in [line.split() for line in f]]
    return index

def voxel_map(index):
    return {v:k for k, v in enumerate(index)}

def voxel_neighbourhood(radius, dimensions):
    rad0 = int(radius/dimensions[0])
    rad1 = int(radius/dimensions[1])
    rad2 = int(radius/dimensions[2])

    neighbours = []
    for i in xrange(0, rad0+1):
        for j in xrange(0, rad1+1):
            for k in xrange(0, rad2+1):
                distance = voxel_distance([0,0,0], [i,j,k], dimensions)
                if ((i>0 or j>0 or k>0) and distance <= radius):
                    neighbours.extend({(i, j, k), 
                                       (i, j, -k),
                                       (i, -j, k),
                                       (i, -j, -k),
                                       (-i, j, k),
                                       (-i, j, -k),
                                       (-i, -j, k),
                                       (-i, -j, -k)})
    return neighbours
