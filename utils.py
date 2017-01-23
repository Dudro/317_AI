def permutations(n, r):
    if n < r or n < 1 or r < 0:
        raise Exception("Must have: 0 <= r, 1 <= n, r <= n permutations.")
    else:
        return _permutations_helper(range(1, n+1), r)

def _permutations_helper(numbers, r):
    if r == 0:
        yield []
    else:
        for num in numbers:
            numbers_copy = [i for i in numbers if i != num]
            for comb in _permutations_helper(numbers_copy, r-1):
                ret = [num]
                ret.extend(comb)
                yield ret

def combinations(n, r):
    if n < r or n < 1 or r < 0:
        raise Exception("Must have: 0 <= r, 1 <= n, r <= n combinations.")
    else:
        return _combinations_helper(range(1, n+1), r)

def _combinations_helper(numbers, r):
    if r == 0:
        yield []
    else:
        for num in numbers:
            index = numbers.index(num)
            numbers_copy = [i for i in numbers if numbers.index(i) > index]
            for comb in _combinations_helper(numbers_copy, r-1):
                ret = [num]
                ret.extend(comb)
                yield ret
print "Perms"
for perm in permutations(3,2):
   print perm
print "Combs"
for comb in combinations(3,2):
   print comb
print "More"
for comb in _combinations_helper([3,4,5], 2):
    print comb
