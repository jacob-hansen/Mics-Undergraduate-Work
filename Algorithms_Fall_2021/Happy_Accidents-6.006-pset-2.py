def count_happy_accidents(A, a = 0, b = None):
    """
    Divide and Conquer Algorithm to identify conflicts in the ordering of a list.
    Specifically, a "happy_accident" is every pair of values that the right is smaller than the left

    Run-time analysis is O(n) per merge and O(logn) merges
    Total O(nlogn)
    """
    if b is None:
        b = len(A)
    value = 0
    if 1 < b - a:
        c = (a + b + 1) // 2
        value += count_happy_accidents(A, a, c)
        value += count_happy_accidents(A, c, b)
        L, R = A[a:c], A[c:b]
        i, j = 0, 0
        while a < b:
            if (j >= len(R)) or (i < len(L) and L[i] < R[j]): # O(1) check side
                A[a] = L[i]
                i=i+1
            else:
                A[a] = R[j]
                j=j+1
                if(i < len(L)):
                    value += len(L)-i
            a=a+1
    return value
