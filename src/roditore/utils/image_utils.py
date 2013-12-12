import os

def voxel_coord_gen(shape, mask=None):
    for k in xrange(0, shape[2]):
        for j in xrange(0, shape[1]):
            for i in xrange(0, shape[0]):
                if mask == None or mask[i,j,k] == 1:
                    yield(i,j,k)

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
