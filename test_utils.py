from utils import *

def test_perm(n, r):
    print "Permutations of", range(0, n), "P", r
    for perm in permutations(n, r):
        print perm

def test_comb(n, r):
    print "Combinations of", range(0, n), "C", r
    for comb in combinations(n, r):
        print comb

def test_perm_list(numbers, r):
    print "Permutations of", numbers, "P", r
    for perm in permutations_list(numbers, r):
        print perm

def test_comb_list(numbers, r):
    print "Combinations of", numbers, "C", r
    for comb in combinations_list(numbers, r):
        print comb

test_perm(2, 1)
test_perm(3, 2)
test_perm_list([3, 2, 1, 4, 0], 3)
test_comb(2, 1)
test_comb(3, 2)
test_comb_list([3, 2, 1, 4, 0], 3)

