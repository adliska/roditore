def voxelCoordinateGenerator(shape, mask=None):
    for k in xrange(0, shape[2]):
        for j in xrange(0, shape[1]):
            for i in xrange(0, shape[0]):
                if mask == None or mask[i,j,k] == 1:
                    yield(i,j,k)

def isVoxelInMask(i, j, k, mask):
    if (i >= 0 and i < mask.shape[0]
            and j >= 0 and j < mask.shape[1]
            and k >= 0 and k < mask.shape[2]
            and mask[i,j,k] == 1):
        return True
    else:
        return False
