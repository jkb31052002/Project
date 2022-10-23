L = [23, 20, 48, 15, 90]


def SelectionSort(L):
    n = len(L)
    if n < 1:
        return(L)
    for i in range(n):
        # Assume L[:i] is sorted
        mpos = i
        print(mpos)
# mpos: position of minimum in L[i:]
        for j in range(i+1, n):
            if L[j] < L[mpos]:
                mpos = j
            print(L)
# L[mpos] : smallest value in L[i:]
# Exchange L[mpos] and L[i]
        (L[i], L[mpos]) = (L[mpos], L[i])
        print(L)
# Now L[:i+1] is sorted
    return(L)


print(SelectionSort(L))
