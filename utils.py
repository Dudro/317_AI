def permutations(n, r):
    """
    Returns a generator of all r-permutations of the numbers 0 to n-1.
    """
    return permutations_list(range(0, n), r)

def permutations_list(numbers, r):
    """
    Returns a generator of all r-permutations of the given list of numbers.
    If numbers are not unique, this function will give the wrong result.
    """
    if r == 0:
        yield []
    else:
        for num in numbers:
            remaining_numbers = [i for i in numbers if i != num]
            for perm in permutations_list(remaining_numbers, r-1):
                ret = [num]
                ret.extend(perm)
                yield ret

                
def permutations_exclude(n, r, exclude=[]):
    numbers = list(range(0, n))
    refnumbers = range(0, n)
    for i in range(n):
        if exclude[i]:
            numbers.remove(refnumbers[i])
    return permutations_list(numbers, r)
                
def combinations(n, r):
    """
    Returns a generator of all r-combinations of the numbers 0 to n-1.
    """
    return combinations_list(range(0, n), r)

def combinations_list(numbers, r):
    """
    Returns a generator of all r-combinations of the given list of numbers.
    If numbers are not unique, this function will give the wrong result.
    """
    if r == 0:
        yield []
    else:
        for num in numbers:
            remaining = range(numbers.index(num) + 1, len(numbers))
            remaining_numbers = [numbers[i] for i in remaining]
            for comb in combinations_list(remaining_numbers, r-1):
                ret = [num]
                ret.extend(comb)
                yield ret

