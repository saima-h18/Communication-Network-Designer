def prodofList(arr):
    # multiplies values in an array - useful for reliability
    prod = 1
    for x in arr:
        prod *= x
    return prod

rel_ring = [1-pow(1-0.97,2), 1-pow(1-0.96,3),1-pow(1-0.94,3), 1-pow(1-0.91,3), 1-pow(1-0.93,3), 1-pow(1-0.91,3)]
# rel_ring = [0.99,0.93,0.96,0.96,0.94]
RelofLoop =prodofList(rel_ring)
# add probabilities where one and only one edge fails
for indx, r in enumerate(rel_ring):
    copy = rel_ring.copy()
    failure = 1 - r
    copy.pop(indx)
    tmp = prodofList(copy)
    product = failure * tmp
    RelofLoop += product

# print(RelofLoop*0.9984)
print(RelofLoop)
# 0.9999965812408375

#0.9983958167067905
#0.945275118336
#0.9982508265745879