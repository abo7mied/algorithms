# This is a divide-and-conquer algorithm for closest points in the plane
# implemented by Ahmed Alzahrani in leisure in CMSC451 in Fall 2024.

# Given:
# points: array of distinct 2d points (float 2-tuples)

# Return:
# res: a pair (p1, p2) in points, with shape ((float, float), (float, float)),
# such that dist(p1, p2) <= dist(p, q) for all distinct p and q in points.

# Main Idea:
# 1- In each recursion step, find the 2 closest pairs in the left and right halves along the x-axis.
# 2- A potentially closer pair of 2 points lying in different halves (p1, p2) satisfies the following:
#       i   - the x-coordinate value of p1 is within delta of the boundary value;
#       ii  - the y-coordinate values of p1 and p2 are within 15 positions of each other
#               along the y-axis among points relevant in the current recursion step.

# Time complexity: should be O(n lgn)

import math


# Assume points are distinct
def closest_points(points: [(float, float)]) -> ((float, float), (float, float)):
    n = len(points)
    sx = sorted(points, key= lambda p: p[0])
    return closest_points_rec(sx, 0, n-1)


# Euclidean distance for points in the plane
def dist(pair: ((float, float), (float, float))) -> float:
    return math.sqrt((pair[1][0] - pair[0][0])**2 + (pair[1][1] - pair[0][1])**2)


# sx: array of all points in order of increasing x-coordinate.
# sy: array of points sx[l] to sx[r] inclusive in order of increasing the y-coordinate.
# c: middle index
# mid: boundary (x-coordinate value) separating the left half from the right half
# delta: smallest distance of two points lying in the same half
def closest_points_rec(sx: [(float, float)], l: int, r: int) -> ((float, float), (float, float)):
    if r - l < 16: # somewhat arbitrary criterion for the small case
        return closest_points_small(sx, l, r)

    sy = sorted(sx[l:r+1], key= lambda p: p[1])

    c = (l + r) // 2
    lpair = closest_points_rec(sx, l, c)
    rpair = closest_points_rec(sx, c + 1, r)
    ld = dist(lpair)
    rd = dist(rpair)
    if rd < ld:
        delta = rd
        res = rpair
    else:
        delta = ld
        res = lpair

    # Change the following from linear to binary.
    i = j = c
    mid = (sx[c][0] + sx[c+1][0]) / 2
    while i > l and mid - sx[i-1][0] < delta:
        i -= 1
    while j < r and sx[j+1][0] - mid < delta:
        j += 1

    d_min = delta
    for kx in range(i, j+1):
        p1 = sx[kx]
        ypos = sy.index(p1)
        # The assumption of distinct points is used in the loop below in specific.
        for ky in range(max(0, ypos-15), min(ypos+16, len(sy))):
            p2 = sy[ky]
            d = dist((p1, p2))
            if 0 < d < d_min:
                d_min = d
                res = (p1, p2)

    return res


# Brute force algorithm for small arrays.
def closest_points_small(sx: [(float, float)], l: int, r: int):
    if r - l < 1:
        return None

    res = (sx[l], sx[l+1])
    d_min = dist((sx[l], sx[l+1]))

    for i in range(l, r):
        for j in range(i+1, r+1):
            d = dist((sx[i], sx[j]))
            if d < d_min:
                res = (sx[i], sx[j])

    return res


def test1():
    assert dist(((-1,-1), (2,3))) == 5


def test2():
    points = [(x,5555) for x in range(-10000, 10001, 2)] + [(5555, y) for y in range(-10000, 10001, 2)]
    pair = closest_points(points) # should return ((5556,5555), (5555, 5556)) or an equivalent pair
    d = dist(pair)
    print(d)
    assert d < 2


def test3():
    points = [(5, y) for y in range(-100,101,2)] + [(x, 5) for x in range(-100,101,2)]
    pair = closest_points(points)
    d = dist(pair)
    print(d)
    assert d < 2


def test():
    test1()
    test2()
    test3()


test()