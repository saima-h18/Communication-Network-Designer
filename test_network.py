def prodofList(arr):
    # multiplies values in an array - useful for reliability
    prod = 1
    for x in arr:
        prod *= x
    return prod

rel_ring = [0.94, 0.97, 0.96, 0.9919, 0.9919, 0.93]
RelofLoop =prodofList(rel_ring)
# add probabilities where one and only one edge fails
for indx, r in enumerate(rel_ring):
    copy = rel_ring.copy()
    failure = 1 - r
    copy.pop(indx)
    tmp = prodofList(copy)
    product = failure * tmp
    RelofLoop += product

print(RelofLoop)