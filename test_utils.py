from utils import *


def test_perm(n, r):
    print("%d-permutations of" % r, [i for i in range(n)])
    for perm in permutations(n, r):
        print(perm)


def test_comb(n, r):
    print("%d-combinations of" % r, [i for i in range(n)])
    for comb in combinations(n, r):
        print(comb)


def test_perm_list(numbers, r):
    print("%d-permutations of" % r, numbers)
    for perm in permutations_list(numbers, r):
        print(perm)


def test_comb_list(numbers, r):
    print("%d-combinations of" % r, numbers)
    for comb in combinations_list(numbers, r):
        print(comb)


def test_perm_exclude(n, r, exclude=None):
    print("%d-permutations of" % r, [i for i in range(n)], "excluding", exclude)
    for perm in permutations_exclude(n, r, exclude):
        print(perm)


test_perm(2, 1)
test_perm(3, 2)
test_perm_list([3, 2, 1, 4, 0], 3)
test_comb(2, 1)
test_comb(3, 2)
test_comb_list([3, 2, 1, 4, 0], 3)
test_perm_exclude(2, 1)
test_perm_exclude(3, 2)
test_perm_exclude(5, 3, [False, False, True, True, False])
